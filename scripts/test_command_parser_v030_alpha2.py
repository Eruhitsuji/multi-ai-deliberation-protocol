#!/usr/bin/env python3
from __future__ import annotations

from parse_command_v030_alpha2 import normalize


def require_block(raw: str, command: str, expected_arguments: dict) -> None:
    result = normalize(raw)
    if "command_block" not in result:
        raise AssertionError(f"expected command_block for {raw!r}: {result}")
    block = result["command_block"]
    if block["command"] != command or block["arguments"] != expected_arguments:
        raise AssertionError(f"normalization mismatch for {raw!r}: {block}")
    if block["validation_status"] != "SCHEMA_VALID":
        raise AssertionError(f"schema validation failed for {raw!r}: {block}")


def require_error(raw: str, root: str, marker: str) -> None:
    result = normalize(raw)
    if root not in result or marker not in str(result[root]):
        raise AssertionError(f"expected {root}/{marker} for {raw!r}: {result}")


def main() -> int:
    require_block("/madp status", "status", {})
    require_block('/madp todo-add --title "Write parser tests" --priority=HIGH', "todo-add", {"title": "Write parser tests", "priority": "HIGH"})
    require_block('/madp approve --decision DEC-003 --revision 2', "approve", {"decision": "DEC-003", "revision": 2})
    require_block(
        "MADP_COMMAND:\n  command: check-authority\n  arguments:\n    action: commit\n    scope: repository\n",
        "check-authority",
        {"action": "commit", "scope": "repository"},
    )

    require_error('/madp todo-add --title "unterminated', "command_parse_error", "CMD_PARSE_ERROR")
    require_error("/madp unknown-command", "command_parse_error", "CMD_UNKNOWN_COMMAND")
    require_error("/madp todo-add --title one --title two", "command_parse_error", "CMD_REPEATED_OPTION:title")
    require_error("/madp todo-add --title one --teleport true", "command_parse_error", "CMD_UNKNOWN_OPTION:teleport")
    require_error("/madp todo-add unbound", "command_parse_error", "CMD_PARSE_AMBIGUITY:unbound_token:unbound")
    require_error("/madp approve --decision DEC-003", "command_needs_arguments", "revision")

    # Claude review regressions.
    require_error("/madp approve --decision DEC-003 --revision", "command_needs_arguments", "revision")
    require_error("/madp approve --decision --revision 2", "command_needs_arguments", "decision")
    for invalid in ("true", "false", "0", "-1", "two"):
        require_error(f"/madp approve --decision DEC-003 --revision {invalid}", "command_parse_error", "CMD_APPROVAL_REVISION_INVALID")
    require_error("/madp todo-add --title ''", "command_needs_arguments", "title")
    require_error("/madp todo-add --title x --priority BANANA", "command_parse_error", "CMD_ARGUMENT_VALUE_INVALID:priority")
    require_error(
        "MADP_COMMAND:\n  command: status\n  command: approve\n  arguments:\n    decision: DEC-9\n    revision: 1\n",
        "command_parse_error",
        "duplicate key",
    )
    require_error(
        "MADP_COMMAND:\n  command: todo-add\n  arguments: &args\n    title: x\n  copy: *args\n",
        "command_parse_error",
        "anchors, aliases",
    )
    require_error("MADP_COMMAND:\n  command: todo-add\n  arguments:\n    title: null\n", "command_needs_arguments", "title")

    print("command parser tests: MADP-v0.3.0-alpha.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
