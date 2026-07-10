#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

import yaml

from parse_command_v030_alpha2 import normalize, strict_yaml_load
from todo_transitions_v030_alpha2 import transition_allowed

VERSION = "MADP-v0.3.0-alpha.2"
READ_ONLY_COMMANDS = {"status", "todo-list", "summarize-state", "check-authority"}
USER_COMMANDS = {"approve", "reject", "defer", "prioritize", "pause", "resume", "status"}
TODO_ID_RE = re.compile(r"^TODO-(\d+)$")


def initial_state() -> dict[str, Any]:
    return {
        "protocol_version": VERSION,
        "state_version": 1,
        "workflow_status": "ACTIVE",
        "todos": [],
        "decisions": {},
        "priorities": {},
        "deferrals": {},
        "rejections": {},
        "proposals": [],
        "command_history": [],
        "used_grants": [],
    }


def document_error(code: str, detail: str, state: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "result": code,
        "message": detail,
        "state": copy.deepcopy(state) if isinstance(state, dict) else initial_state(),
        "state_changed": False,
        "external_actions_performed": False,
    }


def validate_state(state: Any) -> list[str]:
    if not isinstance(state, dict):
        return ["state root must be a mapping"]
    required_types = {
        "protocol_version": str,
        "state_version": int,
        "workflow_status": str,
        "todos": list,
        "decisions": dict,
        "priorities": dict,
        "deferrals": dict,
        "rejections": dict,
        "proposals": list,
        "command_history": list,
    }
    errors = [f"missing state field: {key}" for key in required_types if key not in state]
    for key, expected in required_types.items():
        if key in state and (isinstance(state[key], bool) or not isinstance(state[key], expected)):
            errors.append(f"invalid state field type: {key}")
    if state.get("protocol_version") != VERSION:
        errors.append("state protocol_version mismatch")
    if isinstance(state.get("state_version"), int) and state["state_version"] < 1:
        errors.append("state_version must be at least 1")
    if "used_grants" in state and not isinstance(state["used_grants"], list):
        errors.append("used_grants must be a list")
    return errors


def validate_grants(grants: Any) -> list[str]:
    if not isinstance(grants, list):
        return ["grants root must be a list"]
    errors: list[str] = []
    for index, grant in enumerate(grants):
        if not isinstance(grant, dict):
            errors.append(f"grant {index} must be a mapping")
            continue
        for field in ("grant_id", "issued_by", "action", "scope", "active", "assurance_level", "assurance_origin"):
            if field not in grant:
                errors.append(f"grant {index} missing {field}")
    return errors


def trusted_assurance(grant: dict[str, Any]) -> bool:
    level = grant.get("assurance_level")
    origin = grant.get("assurance_origin")
    if level == "USER_CONFIRMED" and origin == "USER_ACTION":
        return True
    if level == "EXTERNALLY_VERIFIED" and origin == "EXTERNAL_VALIDATION":
        return isinstance(grant.get("reference"), str) and bool(grant["reference"].strip())
    return False


def find_grant(
    grants: list[dict[str, Any]],
    confirmation_ref: str | None,
    command: str,
    state: dict[str, Any],
) -> dict[str, Any] | None:
    if not confirmation_ref or confirmation_ref in state.get("used_grants", []):
        return None
    for grant in grants:
        if grant.get("grant_id") != confirmation_ref or grant.get("active") is not True:
            continue
        if grant.get("issued_by") != "USER" or not trusted_assurance(grant):
            continue
        if grant.get("action") not in {"apply-internal-command", command}:
            continue
        if grant.get("scope") not in {"*", command, "internal-state"}:
            continue
        return grant
    return None


def authorize(
    block: dict[str, Any],
    grants: list[dict[str, Any]],
    confirmation_ref: str | None,
    state: dict[str, Any],
) -> dict[str, Any]:
    command = block["command"]
    boundary = block["authority_boundary"]
    issued_by = block["issued_by"]

    if block["command_class"] == "EXTERNAL_ACTION_COMMAND":
        return {
            "result": "EXTERNAL_EXECUTION_NOT_IMPLEMENTED",
            "authorized": False,
            "may_apply_internal_state": False,
            "reason": "alpha.2 runtime records external-action requests but does not execute them",
        }
    if command in USER_COMMANDS and issued_by != "USER":
        return {
            "result": "CMD_AUTHORITY_DENIED",
            "authorized": False,
            "may_apply_internal_state": False,
            "reason": "USER_COMMAND requires trusted invoking-environment provenance issued_by=USER",
        }
    if command in READ_ONLY_COMMANDS or boundary == "REFERENCE_ONLY":
        return {"result": "REFERENCE_ONLY", "authorized": True, "may_apply_internal_state": False}
    if boundary == "USER_CONFIRMED" and issued_by == "USER":
        return {"result": "USER_COMMAND_ACCEPTED", "authorized": True, "may_apply_internal_state": True}

    grant = find_grant(grants, confirmation_ref, command, state)
    if grant:
        return {
            "result": "TRUSTED_GRANT_ACCEPTED",
            "authorized": True,
            "may_apply_internal_state": True,
            "grant_id": grant["grant_id"],
            "single_use": grant.get("single_use", True),
        }
    return {
        "result": "USER_CONFIRMATION_REQUIRED",
        "authorized": False,
        "may_apply_internal_state": False,
        "reason": f"{boundary} command requires a trusted, unused user grant before state application",
    }


def todo_by_id(state: dict[str, Any], todo_id: str) -> dict[str, Any] | None:
    return next((item for item in state["todos"] if item.get("todo_id") == todo_id), None)


def next_numeric_id(items: list[dict[str, Any]], key: str, prefix: str) -> str:
    maximum = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for item in items:
        value = item.get(key)
        if isinstance(value, str) and (match := pattern.fullmatch(value)):
            maximum = max(maximum, int(match.group(1)))
    return f"{prefix}-{maximum + 1:03d}"


def apply_effect(state: dict[str, Any], block: dict[str, Any]) -> tuple[bool, str, Any]:
    command = block["command"]
    args = block["arguments"]

    if command == "pause":
        state["workflow_status"] = "PAUSED"
        return True, "workflow paused", None
    if command == "resume":
        state["workflow_status"] = "ACTIVE"
        return True, "workflow resumed", None
    if command == "prioritize":
        state["priorities"][str(args["target"])] = args["priority"]
        return True, "priority updated", None
    if command == "defer":
        state["deferrals"][str(args["target"])] = {"until": args.get("until"), "reason": args.get("reason")}
        return True, "target deferred", None
    if command == "reject":
        state["rejections"][str(args["target"])] = args.get("reason")
        return True, "target rejected", None
    if command == "approve":
        decision_id = args["decision"]
        revision = args["revision"]
        previous = state["decisions"].get(decision_id)
        if previous and revision <= previous.get("revision", 0):
            return False, "APPROVAL_REVISION_NOT_NEWER", None
        history = list(previous.get("approval_history", [])) if isinstance(previous, dict) else []
        if previous:
            history.append({key: previous.get(key) for key in ("revision", "status", "scope", "conditions")})
        state["decisions"][decision_id] = {
            "revision": revision,
            "status": "APPROVED",
            "scope": args.get("scope"),
            "conditions": args.get("conditions"),
            "approval_history": history,
        }
        return True, "decision revision approved without external execution", None
    if command == "todo-add":
        todo_id = next_numeric_id(state["todos"], "todo_id", "TODO")
        item = {
            "todo_id": todo_id,
            "title": args["title"],
            "type": args.get("type", "IMPLEMENTATION"),
            "status": "OPEN",
            "priority": args.get("priority", "MEDIUM"),
            "owner": args.get("owner", "UNSPECIFIED"),
            "related_issue": args.get("related_issue"),
            "related_decision": args.get("related_decision"),
            "blocking_reason": None,
            "completion_basis": None,
        }
        state["todos"].append(item)
        return True, "TODO added", item
    if command in {"todo-update", "todo-done", "todo-defer", "todo-promote"}:
        item = todo_by_id(state, str(args["todo_id"]))
        if item is None:
            return False, "TODO_UNKNOWN_ID", None
        if command == "todo-update":
            requested = args.get("status", item["status"])
            if requested == "DONE":
                return False, "TODO_DONE_REQUIRES_TODO_DONE_COMMAND", None
            if requested != item["status"] and not transition_allowed(item["status"], requested):
                return False, "TODO_INVALID_STATUS_TRANSITION", None
            for key in ("title", "priority", "owner", "blocking_reason"):
                if key in args:
                    item[key] = args[key]
            item["status"] = requested
            return True, "TODO updated", item
        if command == "todo-done":
            if not transition_allowed(item["status"], "DONE"):
                return False, "TODO_INVALID_STATUS_TRANSITION", None
            item["status"] = "DONE"
            item["completion_basis"] = args["completion_basis"]
            return True, "TODO completed", item
        if command == "todo-defer":
            if not transition_allowed(item["status"], "DEFERRED"):
                return False, "TODO_INVALID_STATUS_TRANSITION", None
            item["status"] = "DEFERRED"
            item["defer_until"] = args.get("until")
            item["defer_reason"] = args.get("reason")
            return True, "TODO deferred", item
        proposal = {
            "proposal_id": next_numeric_id(state["proposals"], "proposal_id", "PROPOSAL"),
            "source_todo": item["todo_id"],
            "target_type": args["target_type"],
            "rationale": args.get("rationale"),
            "status": "PROPOSED_NOT_APPROVED",
        }
        state["proposals"].append(proposal)
        return True, "TODO promoted to an unapproved proposal", proposal
    return False, "NO_INTERNAL_APPLY_HANDLER", None


def read_only_effect(state: dict[str, Any], block: dict[str, Any], grants: list[dict[str, Any]]) -> Any:
    command = block["command"]
    args = block["arguments"]
    if command == "todo-list":
        return state["todos"]
    if command == "status":
        return {"workflow_status": state["workflow_status"], "state_version": state["state_version"]}
    if command == "summarize-state":
        return {"workflow_status": state["workflow_status"], "todo_count": len(state["todos"]), "decision_count": len(state["decisions"])}
    if command == "check-authority":
        action = str(args["action"])
        matching = [g.get("grant_id") for g in grants if isinstance(g, dict) and g.get("active") is True and g.get("action") in {action, "apply-internal-command"} and trusted_assurance(g)]
        return {"action": action, "classification": "GRANTED" if matching else "REQUIRES_USER_CONFIRMATION", "matching_grants": matching}
    return None


def execute(
    raw: str,
    state: dict[str, Any] | None = None,
    grants: list[dict[str, Any]] | None = None,
    confirmation_ref: str | None = None,
    issued_by: str | None = None,
) -> dict[str, Any]:
    if issued_by not in {"USER", "FACILITATOR", "PARTICIPANT", "SYSTEM"}:
        return document_error("AUTHORITY_INPUT_REQUIRED", "issued_by must be explicitly provided")
    source_state = state if state is not None else initial_state()
    state_errors = validate_state(source_state)
    if state_errors:
        return document_error("STATE_DOCUMENT_INVALID", "; ".join(state_errors), source_state if isinstance(source_state, dict) else None)
    grant_list: Any = grants if grants is not None else []
    grant_errors = validate_grants(grant_list)
    if grant_errors:
        return document_error("GRANTS_DOCUMENT_INVALID", "; ".join(grant_errors), source_state)

    working = copy.deepcopy(source_state)
    working.setdefault("used_grants", [])
    normalized = normalize(raw, issued_by=issued_by)
    if "command_block" not in normalized:
        return {"result": "PARSE_OR_VALIDATION_FAILED", "artifact": normalized, "state": working, "state_changed": False, "external_actions_performed": False}

    block = normalized["command_block"]
    auth = authorize(block, grant_list, confirmation_ref, working)
    effect_changed = False
    effect_result: Any = None
    message = auth["result"]

    if auth["authorized"] and auth["may_apply_internal_state"]:
        effect_changed, message, effect_result = apply_effect(working, block)
        if effect_changed and auth.get("grant_id") and auth.get("single_use", True):
            working["used_grants"].append(auth["grant_id"])
    elif auth["authorized"] and block["command"] in READ_ONLY_COMMANDS:
        message = "read-only command accepted"
        effect_result = read_only_effect(working, block, grant_list)

    history_entry = {
        "command_id": block["command_id"],
        "command": block["command"],
        "issued_by": block["issued_by"],
        "issued_at": block["issued_at"],
        "raw_input": block["raw_input"],
        "authority_result": auth["result"],
        "grant_id": auth.get("grant_id"),
        "effect_applied": effect_changed,
        "message": message,
    }
    working["command_history"].append(history_entry)
    working["state_version"] += 1
    return {
        "result": "APPLIED" if effect_changed else "NOT_APPLIED",
        "message": message,
        "authority": auth,
        "command_block": block,
        "effect_result": effect_result,
        "state": working,
        "state_changed": True,
        "effect_applied": effect_changed,
        "external_actions_performed": False,
    }


def load_document(path: Path | None, default: Any) -> Any:
    if path is None:
        return default
    try:
        return strict_yaml_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return {"__load_error__": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Authorize and apply an internal MADP alpha.2 command.")
    parser.add_argument("command", help="CLI or YAML command text")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--grants", type=Path)
    parser.add_argument("--confirmation-ref")
    parser.add_argument("--issued-by", required=True, choices=["USER", "FACILITATOR", "PARTICIPANT", "SYSTEM"])
    args = parser.parse_args()
    state = load_document(args.state, initial_state())
    grants = load_document(args.grants, [])
    if isinstance(state, dict) and "__load_error__" in state:
        result = document_error("STATE_DOCUMENT_INVALID", state["__load_error__"])
    elif isinstance(grants, dict) and "__load_error__" in grants:
        result = document_error("GRANTS_DOCUMENT_INVALID", grants["__load_error__"], state)
    else:
        result = execute(args.command, state=state, grants=grants, confirmation_ref=args.confirmation_ref, issued_by=args.issued_by)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] in {"APPLIED", "NOT_APPLIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
