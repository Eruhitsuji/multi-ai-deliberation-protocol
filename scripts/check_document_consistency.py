from __future__ import annotations

import re
import sys
from typing import Any

from madp_validation import GLOSSARY_PATH, PROTOCOL_PATH, load_schema


def _schema_enum(schema: dict[str, Any], path: list[str]) -> list[str]:
    node: Any = schema
    for part in path:
        node = node[part]
    return list(node["enum"])


def _backtick_values(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    next_heading = text.find("\n## ", start + 1)
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def _list_after(text: str, marker: str) -> list[str]:
    start = text.find(marker)
    if start == -1:
        return []
    lines = text[start + len(marker) :].splitlines()
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if values:
                break
            continue
        if stripped.startswith("- "):
            values.extend(_backtick_values(stripped))
        elif values:
            break
    return values


def _values_from_sentence(text: str, marker: str) -> list[str]:
    start = text.find(marker)
    if start == -1:
        return []
    sentence = text[start : text.find(".", start) + 1]
    return _backtick_values(sentence)


def _glossary_values(glossary: str, heading: str, label: str = "Canonical values") -> list[str]:
    sec = _section(glossary, heading)
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", sec)
    if not match:
        return []
    return _backtick_values(match.group(1))


def main() -> int:
    schema = load_schema()
    protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
    glossary = GLOSSARY_PATH.read_text(encoding="utf-8")

    checks = {
        "condition.applicability": (
            _schema_enum(schema, ["$defs", "condition", "properties", "applicability"]),
            _list_after(protocol, "Applicability:"),
            _glossary_values(glossary, "## Applicability"),
        ),
        "condition.satisfaction": (
            _schema_enum(schema, ["$defs", "condition", "properties", "satisfaction"]),
            _list_after(protocol, "Satisfaction:"),
            _glossary_values(glossary, "## Satisfaction"),
        ),
        "decision.deliberation_outcome": (
            _schema_enum(schema, ["$defs", "decision", "properties", "deliberation_outcome"]),
            _list_after(protocol, "`decision.deliberation_outcome` values are:"),
            _glossary_values(glossary, "## Deliberation Outcome"),
        ),
        "decision.approval_status": (
            _schema_enum(schema, ["$defs", "decision", "properties", "approval_status"]),
            _list_after(protocol, "`approval_status` values:"),
            _glossary_values(glossary, "## Approval Status"),
        ),
        "approval.assurance_level": (
            _schema_enum(schema, ["$defs", "approvalRecord", "properties", "assurance_level"]),
            _list_after(protocol, "`assurance_level` values:"),
            _glossary_values(glossary, "## Approval Assurance"),
        ),
        "approval.assurance_origin": (
            _schema_enum(schema, ["$defs", "approvalRecord", "properties", "assurance_origin"]),
            _list_after(protocol, "`assurance_origin` values:"),
            _glossary_values(glossary, "## Assurance Origin"),
        ),
        "permission_request.status": (
            _schema_enum(schema, ["$defs", "permissionRequest", "properties", "status"]),
            _values_from_sentence(protocol, "Request status values are"),
            _glossary_values(glossary, "## Permission Request", "Canonical status values"),
        ),
        "permission_grant.action": (
            _schema_enum(schema, ["$defs", "permissionGrant", "properties", "action"]),
            _list_after(protocol, "Only core actions recognized by the identified protocol version are grantable by default:"),
            _glossary_values(glossary, "## Permission Grant", "Canonical action values"),
        ),
        "permission_grant.duration": (
            _schema_enum(schema, ["$defs", "permissionGrant", "properties", "duration"]),
            _values_from_sentence(protocol, "Grant duration is"),
            _glossary_values(glossary, "## Permission Grant", "Canonical duration values"),
        ),
        "participant.status": (
            _schema_enum(schema, ["$defs", "participant", "properties", "status"]),
            _section_values(protocol, "Compact participant statuses:", "Detailed statuses MAY additionally include:"),
            _glossary_values(glossary, "## Participant", "Canonical status values"),
        ),
        "current_issue.status": (
            _schema_enum(schema, ["$defs", "currentIssue", "properties", "status"]),
            _list_after(protocol, "`current_issue.status` values are:"),
            _glossary_values(glossary, "## Current Issue Status"),
        ),
        "usage_budget.status": (
            _schema_enum(schema, ["$defs", "usageBudget", "properties", "status"]),
            _values_from_sentence(protocol, "- `status`:"),
            _glossary_values(glossary, "## Usage Budget", "Canonical status values"),
        ),
        "next_step.user.prompt_action": (
            _schema_enum(schema, ["$defs", "userStep", "properties", "prompt_action"]),
            _list_after(protocol, "Valid `PROMPT_ACTION` values:"),
            _glossary_values(glossary, "## Prompt Action"),
        ),
    }

    failures: list[str] = []
    for name, (schema_values, protocol_values, glossary_values) in checks.items():
        missing_protocol = [value for value in schema_values if value not in protocol_values]
        missing_glossary = [value for value in schema_values if value not in glossary_values]
        if missing_protocol:
            failures.append(f"{name}: protocol missing {missing_protocol!r}")
        if missing_glossary:
            failures.append(f"{name}: glossary missing {missing_glossary!r}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    for name in checks:
        print(f"enum consistency: {name} PASS")
    return 0


def _section_values(protocol: str, compact_marker: str, detailed_marker: str) -> list[str]:
    compact = _list_after(protocol, compact_marker)
    detailed = _list_after(protocol, detailed_marker)
    return detailed + compact if detailed and detailed[0] not in compact else compact + [v for v in detailed if v not in compact]


if __name__ == "__main__":
    raise SystemExit(main())
