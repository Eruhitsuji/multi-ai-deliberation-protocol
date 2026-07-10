#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import yaml

from madp_validation import ROOT
from parse_command_v030_alpha2 import normalize

VERSION = "MADP-v0.3.0-alpha.2"
EXTERNAL_COMMANDS = {"external-action"}
READ_ONLY_COMMANDS = {"status", "todo-list", "summarize-state", "check-authority"}


def initial_state() -> dict[str, Any]:
    return {
        "protocol_version": VERSION,
        "state_version": 0,
        "workflow_status": "ACTIVE",
        "todos": [],
        "decisions": {},
        "priorities": {},
        "deferrals": {},
        "rejections": {},
        "proposals": [],
        "command_history": [],
    }


def find_grant(grants: list[dict[str, Any]], confirmation_ref: str | None, command: str) -> dict[str, Any] | None:
    if not confirmation_ref:
        return None
    for grant in grants:
        if grant.get("grant_id") != confirmation_ref or grant.get("active") is not True:
            continue
        if grant.get("issued_by") != "USER":
            continue
        if grant.get("action") not in {"apply-internal-command", command}:
            continue
        if grant.get("scope") not in {"*", command, "internal-state"}:
            continue
        return grant
    return None


def authorize(block: dict[str, Any], grants: list[dict[str, Any]], confirmation_ref: str | None) -> dict[str, Any]:
    command = block["command"]
    boundary = block["authority_boundary"]
    issued_by = block["issued_by"]

    if command in EXTERNAL_COMMANDS:
        return {
            "result": "EXTERNAL_EXECUTION_NOT_IMPLEMENTED",
            "authorized": False,
            "may_apply_internal_state": False,
            "reason": "alpha.2 runtime records external-action requests but does not execute them",
        }
    if command in READ_ONLY_COMMANDS or boundary == "REFERENCE_ONLY":
        return {"result": "REFERENCE_ONLY", "authorized": True, "may_apply_internal_state": False}
    if boundary == "USER_CONFIRMED" and issued_by == "USER":
        return {"result": "USER_COMMAND_ACCEPTED", "authorized": True, "may_apply_internal_state": True}

    grant = find_grant(grants, confirmation_ref, command)
    if grant:
        return {
            "result": "TRUSTED_GRANT_ACCEPTED",
            "authorized": True,
            "may_apply_internal_state": True,
            "grant_id": grant["grant_id"],
        }
    return {
        "result": "USER_CONFIRMATION_REQUIRED",
        "authorized": False,
        "may_apply_internal_state": False,
        "reason": f"{boundary} command requires a trusted user grant before state application",
    }


def todo_by_id(state: dict[str, Any], todo_id: str) -> dict[str, Any] | None:
    return next((item for item in state["todos"] if item.get("todo_id") == todo_id), None)


def transition_allowed(old: str, new: str) -> bool:
    allowed = {
        "OPEN": {"IN_PROGRESS", "DEFERRED", "CANCELLED"},
        "IN_PROGRESS": {"BLOCKED", "DONE", "DEFERRED", "CANCELLED"},
        "BLOCKED": {"IN_PROGRESS", "DEFERRED", "CANCELLED"},
        "DEFERRED": {"OPEN", "IN_PROGRESS", "CANCELLED"},
        "DONE": set(),
        "CANCELLED": set(),
    }
    return new == old or new in allowed.get(old, set())


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
        state["decisions"][str(args["decision"])] = {
            "revision": args["revision"],
            "status": "APPROVED",
            "scope": args.get("scope"),
            "conditions": args.get("conditions"),
        }
        return True, "decision revision approved without external execution", None
    if command == "todo-add":
        todo_id = f"TODO-{len(state['todos']) + 1:03d}"
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
            if not transition_allowed(item["status"], requested):
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
            "proposal_id": f"PROPOSAL-{len(state['proposals']) + 1:03d}",
            "source_todo": item["todo_id"],
            "target_type": args["target_type"],
            "rationale": args.get("rationale"),
            "status": "PROPOSED_NOT_APPROVED",
        }
        state["proposals"].append(proposal)
        return True, "TODO promoted to an unapproved proposal", proposal
    return False, "NO_INTERNAL_APPLY_HANDLER", None


def execute(
    raw: str,
    state: dict[str, Any] | None = None,
    grants: list[dict[str, Any]] | None = None,
    confirmation_ref: str | None = None,
    issued_by: str = "USER",
) -> dict[str, Any]:
    working = copy.deepcopy(state if state is not None else initial_state())
    normalized = normalize(raw, issued_by=issued_by)
    if "command_block" not in normalized:
        return {"result": "PARSE_OR_VALIDATION_FAILED", "artifact": normalized, "state": working, "state_changed": False}

    block = normalized["command_block"]
    auth = authorize(block, grants or [], confirmation_ref)
    changed = False
    effect_result: Any = None
    message = auth["result"]

    if auth["authorized"] and auth["may_apply_internal_state"]:
        changed, message, effect_result = apply_effect(working, block)
    elif auth["authorized"] and block["command"] in READ_ONLY_COMMANDS:
        message = "read-only command accepted"
        if block["command"] == "todo-list":
            effect_result = working["todos"]
        elif block["command"] == "status":
            effect_result = {"workflow_status": working["workflow_status"], "state_version": working["state_version"]}

    if changed:
        working["state_version"] += 1
    working["command_history"].append(
        {
            "command_id": block["command_id"],
            "command": block["command"],
            "authority_result": auth["result"],
            "state_changed": changed,
            "message": message,
        }
    )
    return {
        "result": "APPLIED" if changed else "NOT_APPLIED",
        "message": message,
        "authority": auth,
        "command_block": block,
        "effect_result": effect_result,
        "state": working,
        "state_changed": changed,
        "external_actions_performed": False,
    }


def load_document(path: Path | None, default: Any) -> Any:
    if path is None:
        return default
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Authorize and apply an internal MADP alpha.2 command.")
    parser.add_argument("command", help="CLI or YAML command text")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--grants", type=Path)
    parser.add_argument("--confirmation-ref")
    parser.add_argument("--issued-by", default="USER")
    args = parser.parse_args()
    result = execute(
        args.command,
        state=load_document(args.state, initial_state()),
        grants=load_document(args.grants, []),
        confirmation_ref=args.confirmation_ref,
        issued_by=args.issued_by,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] in {"APPLIED", "NOT_APPLIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
