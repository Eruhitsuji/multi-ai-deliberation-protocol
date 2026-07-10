#!/usr/bin/env python3
from __future__ import annotations

from apply_command_v030_alpha2 import execute, initial_state
from parse_command_v030_alpha2 import normalize
from todo_transitions_v030_alpha2 import ALLOWED_TRANSITIONS, transition_allowed


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def grant(grant_id: str, action: str = "apply-internal-command", scope: str = "internal-state", **extra):
    value = {
        "grant_id": grant_id,
        "issued_by": "USER",
        "action": action,
        "scope": scope,
        "active": True,
        "assurance_level": "USER_CONFIRMED",
        "assurance_origin": "USER_ACTION",
    }
    value.update(extra)
    return value


def main() -> int:
    repeated = normalize("/madp request-review --review_focus schema --review_focus authority --artifacts command.schema.yaml --artifacts commands.yaml")
    require(repeated["command_block"]["arguments"]["review_focus"] == ["schema", "authority"], "LIST argument accumulation failed")
    require("command_parse_error" in normalize("/madp todo-add --title one --title two"), "SCALAR duplicate accepted")

    # Issuer provenance is mandatory at execution and USER_COMMAND cannot be grant-escalated.
    missing_issuer = execute("/madp approve --decision DEC-003 --revision 2")
    require(missing_issuer["result"] == "AUTHORITY_INPUT_REQUIRED", "missing issuer was accepted")
    participant_approve = execute("/madp approve --decision DEC-003 --revision 2", issued_by="PARTICIPANT")
    require(participant_approve["result"] == "NOT_APPLIED", "participant approve applied")
    require(participant_approve["authority"]["result"] == "CMD_AUTHORITY_DENIED", "participant approve wrong denial")
    require(participant_approve["state_changed"] is False, "denied command changed state")
    require(participant_approve["history_appended"] is False, "denied command entered history")
    require(participant_approve["state"]["state_version"] == 1, "denied command incremented state version")
    require(participant_approve["state"]["command_history"] == [], "denied command mutated history")

    state = initial_state()
    no_grant = execute("/madp todo-add --title runtime-test", state=state, issued_by="SYSTEM")
    require(no_grant["effect_applied"] is False, "PROPOSE_ONLY command applied without grant")
    require(no_grant["authority"]["result"] == "USER_CONFIRMATION_REQUIRED", "missing grant not detected")
    require(no_grant["state_changed"] is False, "unconfirmed command changed state")
    require(no_grant["state"]["state_version"] == state["state_version"], "unconfirmed command incremented version")
    require(no_grant["state"]["command_history"] == state["command_history"], "unconfirmed command appended history")

    untrusted = grant("BAD", assurance_level="UNVERIFIED_ASSERTION")
    denied = execute("/madp todo-add --title denied", state=state, grants=[untrusted], confirmation_ref="BAD", issued_by="SYSTEM")
    require(denied["effect_applied"] is False, "untrusted grant accepted")
    require(denied["state_changed"] is False, "untrusted grant attempt changed state")

    grants = [grant("G-ADD"), grant("G-START"), grant("G-DONE"), grant("G-REOPEN"), grant("G-TERMINAL")]
    added = execute("/madp todo-add --title runtime-test --priority HIGH", state=state, grants=grants, confirmation_ref="G-ADD", issued_by="SYSTEM")
    require(added["result"] == "APPLIED", f"TODO add failed: {added}")
    require(added["state"]["todos"][0]["todo_id"] == "TODO-001", "TODO id mismatch")

    replay = execute("/madp todo-add --title replay", state=added["state"], grants=grants, confirmation_ref="G-ADD", issued_by="SYSTEM")
    require(replay["effect_applied"] is False, "single-use grant replay accepted")
    require(replay["state_changed"] is False, "grant replay changed state")

    started = execute("/madp todo-update --todo_id TODO-001 --status IN_PROGRESS", state=added["state"], grants=grants, confirmation_ref="G-START", issued_by="SYSTEM")
    require(started["state"]["todos"][0]["status"] == "IN_PROGRESS", "TODO did not enter IN_PROGRESS")
    completed = execute("/madp todo-done --todo_id TODO-001 --completion_basis tested", state=started["state"], grants=grants, confirmation_ref="G-DONE", issued_by="SYSTEM")
    require(completed["state"]["todos"][0]["status"] == "DONE", "TODO status mismatch")
    second_done = execute("/madp todo-done --todo_id TODO-001 --completion_basis rewritten", state=completed["state"], grants=grants, confirmation_ref="G-REOPEN", issued_by="SYSTEM")
    require(second_done["effect_applied"] is False, "DONE self-transition accepted")
    require(second_done["state"]["todos"][0]["completion_basis"] == "tested", "completion basis was rewritten")

    terminal_edit = execute(
        "/madp todo-update --todo_id TODO-001 --title HACKED --priority LOW",
        state=completed["state"],
        grants=grants,
        confirmation_ref="G-TERMINAL",
        issued_by="SYSTEM",
    )
    require(terminal_edit["effect_applied"] is False, "terminal TODO metadata edit applied")
    require(terminal_edit["message"] == "TODO_ITEM_TERMINAL", "terminal TODO edit returned wrong error")
    require(terminal_edit["state"]["todos"][0]["title"] == "runtime-test", "terminal TODO title changed")
    require(terminal_edit["state"]["todos"][0]["priority"] == "HIGH", "terminal TODO priority changed")

    # Shared transition source must match runtime for every pair.
    for source in ALLOWED_TRANSITIONS:
        for target in ALLOWED_TRANSITIONS:
            require(transition_allowed(source, target) == (target in ALLOWED_TRANSITIONS[source]), f"transition mismatch {source}->{target}")

    # Approval revision must move forward and retain history.
    approved2 = execute("/madp approve --decision DEC-1 --revision 2", state=completed["state"], issued_by="USER")
    require(approved2["effect_applied"] is True, "valid approval failed")
    downgraded = execute("/madp approve --decision DEC-1 --revision 1", state=approved2["state"], issued_by="USER")
    require(downgraded["effect_applied"] is False, "approval revision downgrade accepted")
    require(downgraded["state"]["decisions"]["DEC-1"]["revision"] == 2, "approval revision overwritten")

    # Unique TODO ids are derived from maximum suffix, not list length.
    seeded = initial_state()
    seeded["todos"] = [{"todo_id": "TODO-002", "title": "seed", "status": "OPEN"}]
    unique = execute("/madp todo-add --title unique", state=seeded, grants=[grant("G-UNIQUE")], confirmation_ref="G-UNIQUE", issued_by="SYSTEM")
    require(unique["state"]["todos"][-1]["todo_id"] == "TODO-003", "TODO id collision")

    paused = execute("/madp pause --reason maintenance", state=approved2["state"], issued_by="USER")
    resumed = execute("/madp resume", state=paused["state"], issued_by="USER")
    require(resumed["state"]["workflow_status"] == "ACTIVE", "pause/resume failed")

    external = execute("/madp external-action --action push --scope repository", state=resumed["state"], issued_by="USER")
    require(external["external_actions_performed"] is False, "external action was performed")
    require(external["authority"]["result"] == "EXTERNAL_EXECUTION_NOT_IMPLEMENTED", "external boundary mismatch")
    require(external["state_changed"] is False, "denied external action changed state")

    status = execute("/madp status", state=resumed["state"], issued_by="USER")
    require(status["effect_result"]["workflow_status"] == "ACTIVE", "status output mismatch")
    require(status["state"]["state_version"] == resumed["state"]["state_version"] + 1, "accepted read-only history did not increment state version")
    require(status["state"]["command_history"][-1]["issued_by"] == "USER", "history issuer missing")
    require(status["state_changed"] is True and status["history_appended"] is True, "accepted read-only command not recorded")
    require(status["effect_applied"] is False, "read-only command reported effect application")

    bad_state = execute("/madp status", state={"unexpected": True}, issued_by="USER")
    require(bad_state["result"] == "STATE_DOCUMENT_INVALID", "malformed state not structured")
    bad_grants = execute("/madp status", state=initial_state(), grants={"grant_id": "G"}, issued_by="USER")
    require(bad_grants["result"] == "GRANTS_DOCUMENT_INVALID", "malformed grants not structured")

    print("command runtime tests: MADP-v0.3.0-alpha.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
