#!/usr/bin/env python3
from __future__ import annotations

from apply_command_v030_alpha2 import execute, initial_state
from parse_command_v030_alpha2 import normalize


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    repeated = normalize(
        "/madp request-review --review_focus schema --review_focus authority --artifacts command.schema.yaml --artifacts commands.yaml"
    )
    require("command_block" in repeated, f"list-valued arguments failed: {repeated}")
    args = repeated["command_block"]["arguments"]
    require(args["review_focus"] == ["schema", "authority"], "review_focus did not accumulate")
    require(args["artifacts"] == ["command.schema.yaml", "commands.yaml"], "artifacts did not accumulate")

    duplicate_scalar = normalize("/madp todo-add --title one --title two")
    require("command_parse_error" in duplicate_scalar, "scalar duplicate was not rejected")
    require("CMD_REPEATED_OPTION:title" in duplicate_scalar["command_parse_error"]["reason"], "wrong scalar duplicate error")

    state = initial_state()
    no_grant = execute("/madp todo-add --title runtime-test", state=state)
    require(no_grant["state_changed"] is False, "PROPOSE_ONLY command changed state without grant")
    require(no_grant["authority"]["result"] == "USER_CONFIRMATION_REQUIRED", "missing grant not detected")

    grants = [
        {
            "grant_id": "GRANT-INTERNAL-001",
            "issued_by": "USER",
            "action": "apply-internal-command",
            "scope": "internal-state",
            "active": True,
        }
    ]
    added = execute(
        "/madp todo-add --title runtime-test --priority HIGH",
        state=state,
        grants=grants,
        confirmation_ref="GRANT-INTERNAL-001",
    )
    require(added["result"] == "APPLIED", f"TODO add failed: {added}")
    require(added["state"]["todos"][0]["todo_id"] == "TODO-001", "TODO id mismatch")
    require(added["state"]["state_version"] == 1, "state version did not increment")

    started = execute(
        "/madp todo-update --todo_id TODO-001 --status IN_PROGRESS",
        state=added["state"],
        grants=grants,
        confirmation_ref="GRANT-INTERNAL-001",
    )
    require(started["result"] == "APPLIED", f"TODO start failed: {started}")
    require(started["state"]["todos"][0]["status"] == "IN_PROGRESS", "TODO did not enter IN_PROGRESS")

    completed = execute(
        "/madp todo-done --todo_id TODO-001 --completion_basis tested",
        state=started["state"],
        grants=grants,
        confirmation_ref="GRANT-INTERNAL-001",
    )
    require(completed["result"] == "APPLIED", f"TODO done failed: {completed}")
    require(completed["state"]["todos"][0]["status"] == "DONE", "TODO status mismatch")

    invalid_reopen = execute(
        "/madp todo-update --todo_id TODO-001 --status IN_PROGRESS",
        state=completed["state"],
        grants=grants,
        confirmation_ref="GRANT-INTERNAL-001",
    )
    require(invalid_reopen["state_changed"] is False, "invalid DONE transition changed state")
    require(invalid_reopen["message"] == "TODO_INVALID_STATUS_TRANSITION", "invalid transition not reported")

    paused = execute("/madp pause --reason maintenance", state=completed["state"], issued_by="USER")
    require(paused["state"]["workflow_status"] == "PAUSED", "pause failed")
    resumed = execute("/madp resume", state=paused["state"], issued_by="USER")
    require(resumed["state"]["workflow_status"] == "ACTIVE", "resume failed")

    external = execute(
        "/madp external-action --action push --scope repository --confirmation_ref GRANT-INTERNAL-001",
        state=resumed["state"],
        grants=grants,
        confirmation_ref="GRANT-INTERNAL-001",
    )
    require(external["state_changed"] is False, "external action changed state")
    require(external["external_actions_performed"] is False, "external action was reported as performed")
    require(external["authority"]["result"] == "EXTERNAL_EXECUTION_NOT_IMPLEMENTED", "external boundary mismatch")

    status = execute("/madp status", state=resumed["state"])
    require(status["state_changed"] is False, "status command changed state")
    require(status["effect_result"]["workflow_status"] == "ACTIVE", "status output mismatch")

    print("command runtime tests: MADP-v0.3.0-alpha.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
