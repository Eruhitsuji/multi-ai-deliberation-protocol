#!/usr/bin/env python3
from __future__ import annotations
import copy, json
from pathlib import Path
from typing import Any
from parse_command_v030_alpha3 import normalize, command_map

VERSION = "MADP-v0.3.0-alpha.3"
READ_ONLY = {"status", "session-status", "todo-list", "summarize-state", "check-authority", "help-context-create"}
USER_ONLY = {name for name, d in command_map().items() if d["command_class"] == "USER_COMMAND"} | {"approve", "reject", "defer", "prioritize", "pause", "resume", "status"}
EXTERNAL = {"external-action"}
PRESTART_ALLOWED = READ_ONLY | {
    "goal-propose", "goal-confirm", "session-start",
    "participant-add", "participant-update-capability", "participant-set-mode",
    "role-assign", "role-pause", "role-retire",
    "help", "help-exit",
}
HANDLER_STRATEGIES = {name: ("external-deny" if name in EXTERNAL else "read-only" if name in READ_ONLY else "explicit-or-proposal") for name in command_map()}


def initial_state() -> dict[str, Any]:
    return {
        "protocol_version": VERSION,
        "session_id": "SESSION-001",
        "state_version": 1,
        "workflow_status": "PLANNING",
        "phase": "GOAL_GATE",
        "session_started": False,
        "help_stack": [],
        "plans": {"PLAN-001": {"revision": 1, "status": "PENDING"}},
        "decisions": {"DEC-001": {"revision": 1, "status": "PROPOSED"}},
        "todos": {"TODO-001": {"status": "OPEN"}},
        "participants": {},
        "roles": {},
        "ingests": {},
        "normalizations": {},
        "claims": {},
        "minutes": {},
        "imports": {},
        "checkpoints": {},
        "proposals": [],
        "command_history": [],
        "external_actions_performed": False,
    }


def result(code: str, state: dict[str, Any], changed=False, effect=None, message="") -> dict[str, Any]:
    return {
        "result": code,
        "message": message,
        "state": state,
        "state_changed": changed,
        "effect_applied": changed,
        "effect": effect,
        "external_actions_performed": False,
    }


def exact_state(args: dict[str, Any], state: dict[str, Any], key="source_state_version") -> bool:
    return key not in args or args[key] == state["state_version"]


def increment(state: dict[str, Any]) -> None:
    state["state_version"] += 1


def _next(prefix: str, mapping: dict[str, Any]) -> str:
    return f"{prefix}-{len(mapping)+1:03d}"


def execute(raw: str, state: dict[str, Any] | None = None, issued_by: str = "SYSTEM") -> dict[str, Any]:
    source = copy.deepcopy(state or initial_state())
    parsed = normalize(raw, issued_by=issued_by)
    if "command_block" not in parsed:
        return result("COMMAND_REJECTED", source, message=json.dumps(parsed, ensure_ascii=False))
    block = parsed["command_block"]
    command = block["command"]
    args = block["arguments"]

    if command in USER_ONLY and issued_by != "USER":
        return result("CMD_AUTHORITY_DENIED", source, message="USER_COMMAND requires issued_by=USER")
    if command in EXTERNAL:
        return result("EXTERNAL_EXECUTION_NOT_IMPLEMENTED", source, message="Runtime never executes external actions")
    if command in READ_ONLY:
        effect = {
            "workflow_status": source["workflow_status"],
            "phase": source["phase"],
            "state_version": source["state_version"],
            "session_started": source["session_started"],
        }
        return result("REFERENCE_ONLY", source, effect=effect)
    if not exact_state(args, source):
        return result("STATE_REVISION_MISMATCH", source)
    if not source["session_started"] and command not in PRESTART_ALLOWED:
        return result("SESSION_NOT_STARTED", source, message="Confirm the goal and execute session-start before substantive transitions")

    s = copy.deepcopy(source)
    effect = None

    if command == "goal-confirm":
        plan = s["plans"].get(args["plan_id"])
        if not plan or plan["revision"] != args["revision"]:
            return result("GOAL_REVISION_MISMATCH", source)
        plan["status"] = "USER_CONFIRMED"
        plan["confirmed_revision"] = args["revision"]
        s["phase"] = "GOAL_CONFIRMED"
        s["workflow_status"] = "PLANNING"
    elif command == "session-start":
        if args["session_id"] != s["session_id"]:
            return result("SESSION_ID_MISMATCH", source)
        plan_id = str(args["deliberation_plan"])
        plan = s["plans"].get(plan_id)
        if not plan or plan.get("status") != "USER_CONFIRMED" or plan.get("confirmed_revision") != plan.get("revision"):
            return result("PLAN_NOT_CONFIRMED", source)
        if s["session_started"]:
            return result("SESSION_ALREADY_STARTED", source)
        s["session_started"] = True
        s["workflow_status"] = "ACTIVE"
        s["phase"] = "DELIBERATION"
        effect = {"session_id": s["session_id"], "plan_id": plan_id}
    elif command == "pause":
        s["workflow_status"] = "PAUSED"
    elif command == "resume":
        if s["workflow_status"] != "PAUSED":
            return result("WORKFLOW_NOT_PAUSED", source)
        s["workflow_status"] = "ACTIVE"
    elif command == "session-resume":
        if args["session_id"] != s["session_id"] or args["expected_state_version"] != s["state_version"]:
            return result("SESSION_REVISION_MISMATCH", source)
        if not s["session_started"]:
            return result("SESSION_NOT_STARTED", source)
        s["workflow_status"] = "ACTIVE"
    elif command == "session-end":
        if args["session_id"] != s["session_id"] or args["expected_state_version"] != s["state_version"]:
            return result("SESSION_REVISION_MISMATCH", source)
        s["workflow_status"] = "ENDED"
        s["phase"] = "ENDED"
        s["end_reason"] = args["end_reason"]
    elif command == "approve":
        d = s["decisions"].get(args["decision"])
        if not d or d["revision"] != args["revision"]:
            return result("APPROVAL_REVISION_MISMATCH", source)
        d["status"] = "APPROVED"
    elif command == "response-ingest":
        iid = _next("ING", s["ingests"])
        s["ingests"][iid] = {
            "raw_response_ref": args["raw_response_ref"],
            "participant_id": args["participant_id"],
            "source_state_version": args["source_state_version"],
            "status": "INGESTED",
        }
        effect = {"ingest_id": iid}
    elif command == "response-normalize":
        if args["ingest_id"] not in s["ingests"]:
            return result("INGEST_REQUIRED", source)
        nid = str(args["normalization_record"])
        s["normalizations"][nid] = {
            "ingest_id": args["ingest_id"],
            "source_state_version": args["source_state_version"],
            "status": "UNCONFIRMED",
        }
        effect = {"normalization_id": nid}
    elif command == "normalization-confirm":
        n = s["normalizations"].get(args["normalization_id"])
        if not n:
            return result("NORMALIZATION_REQUIRED", source)
        n["status"] = args["status"]
    elif command == "minutes-generate":
        if args["session_id"] != s["session_id"]:
            return result("SESSION_ID_MISMATCH", source)
        mid = _next("MIN", s["minutes"])
        s["minutes"][mid] = {
            "revision": 1,
            "status": "AUTO_GENERATED_DRAFT",
            "detail_level": args["detail_level"],
            "source_state_version": args["source_state_version"],
        }
        effect = {"minutes_id": mid, "source_state_version": args["source_state_version"]}
    elif command == "minutes-review":
        m = s["minutes"].get(args["minutes_id"])
        if not m or m["revision"] != args["revision"]:
            return result("MINUTES_REVISION_MISMATCH", source)
        m["status"] = args["review_status"]
    elif command == "minutes-approve":
        m = s["minutes"].get(args["minutes_id"])
        if not m or m["revision"] != args["revision"]:
            return result("MINUTES_REVISION_MISMATCH", source)
        if m["status"] != "HUMAN_REVIEWED":
            return result("MINUTES_REVIEW_REQUIRED", source)
        m["status"] = "APPROVED_RECORD"
    elif command == "session-import":
        iid = _next("IMPORT", s["imports"])
        s["imports"][iid] = {
            "report_revision": 1,
            "source_file": args["source_file"],
            "status": "REVIEW_REQUIRED",
            "canonical_state_modified": False,
        }
        effect = {"import_id": iid, "report_revision": 1}
    elif command == "session-import-confirm":
        imp = s["imports"].get(args["import_id"])
        if not imp:
            return result("IMPORT_REPORT_REQUIRED", source)
        if imp["report_revision"] != args["report_revision"]:
            return result("IMPORT_REPORT_REVISION_MISMATCH", source)
        imp["status"] = args["selected_action"]
        imp["canonical_state_modified"] = args["selected_action"] in {"CREATE_NEW_SESSION", "RESUME_EXISTING"}
    elif command == "help":
        hid = _next("HELP", {str(i): x for i, x in enumerate(s["help_stack"])})
        s["help_stack"].append({
            "help_request_id": hid,
            "prior_phase": s["phase"],
            "help_state_version": s["state_version"] + 1,
        })
        s["phase"] = "HELP"
        effect = {"help_request_id": hid}
    elif command == "help-exit":
        if not s["help_stack"]:
            return result("HELP_CONTEXT_MISMATCH", source)
        top = s["help_stack"][-1]
        if top["help_request_id"] != args["help_request_id"] or top["help_state_version"] != args["source_state_version"]:
            return result("HELP_CONTEXT_MISMATCH", source)
        prior = s["help_stack"].pop()
        s["phase"] = prior["prior_phase"]
    elif command == "team-approval-record":
        d = s["decisions"].get(args["decision_id"])
        if not d or d["revision"] != args["decision_revision"]:
            return result("APPROVAL_REVISION_MISMATCH", source)
        d.setdefault("approved_by", []).append(args["approver_id"])
        d["status"] = "APPROVED"
    elif command == "session-checkpoint-create":
        cid = _next("CHECKPOINT", s["checkpoints"])
        s["checkpoints"][cid] = {"label": args["label"], "source_state_version": args["source_state_version"]}
        effect = {"checkpoint_id": cid}
    elif command == "participant-add":
        s["participants"][str(args["participant_profile"])] = {"status": "REGISTERED"}
    elif command == "role-assign":
        s["roles"][str(args["role_assignment"])] = {"status": "ACTIVE"}
    elif command == "claim-add":
        s["claims"][str(args["claim"])] = {"verification_status": "UNVERIFIED"}
    else:
        s["proposals"].append({"command": command, "arguments": copy.deepcopy(args), "status": "PROPOSED_NOT_APPROVED"})

    increment(s)
    s["command_history"].append({"command": command, "invoked_name": block["invoked_name"], "state_version": s["state_version"]})
    return result("APPLIED_INTERNAL_STATE" if command != "help" else "HELP_ENTERED", s, True, effect)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("command")
    ap.add_argument("--issued-by", default="SYSTEM")
    ns = ap.parse_args()
    print(json.dumps(execute(ns.command, issued_by=ns.issued_by), ensure_ascii=False, indent=2))
