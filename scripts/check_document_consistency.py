from __future__ import annotations

import re
import sys
from typing import Any

from madp_validation import (
    GLOSSARY_PATH,
    PROTOCOL_PATH,
    README_PATH,
    ROOT,
    PROTOCOL_VERSION,
    SCHEMA_VERSION,
    load_schema,
    load_yaml,
    rel,
)


RC_PROTOCOL_PATH = "protocol/MADP-v0.2.5-rc.2.md"
RC_GLOSSARY_PATH = "protocol/GLOSSARY-v0.2.5-rc.2.md"
RC_SCHEMA_PATH = "schemas/session-state-v0.2.5-rc.2.schema.yaml"
HISTORICAL_RC1_CANONICAL_PATHS = [
    "protocol/MADP-v0.2.5-rc.1.md",
    "protocol/GLOSSARY-v0.2.5-rc.1.md",
    "schemas/session-state-v0.2.5-rc.1.schema.yaml",
]
DRAFT_CANONICAL_PATHS = [
    "protocol/MADP-v0.2.5-draft.md",
    "protocol/GLOSSARY-v0.2.5-draft.md",
    "schemas/session-state-v0.2.5-draft.schema.yaml",
]


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
    readme = README_PATH.read_text(encoding="utf-8")

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
    failures.extend(_version_consistency_failures(schema, protocol, glossary, readme))
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
    print("version consistency: current rc.2 references PASS")
    print("normalized rc.1/rc.2 compare: protocol, glossary, schema PASS")
    print("operational records: historical rc.1 and rc.2 readiness PASS")
    for name in checks:
        print(f"enum consistency: {name} PASS")
    return 0


def _version_consistency_failures(schema: dict[str, Any], protocol: str, glossary: str, readme: str) -> list[str]:
    failures: list[str] = []
    if PROTOCOL_VERSION != "MADP-v0.2.5-rc.2":
        failures.append(f"current protocol target is {PROTOCOL_VERSION!r}, expected 'MADP-v0.2.5-rc.2'")
    if SCHEMA_VERSION != "0.2.5-rc.2":
        failures.append(f"current schema target is {SCHEMA_VERSION!r}, expected '0.2.5-rc.2'")
    meta = schema["$defs"]["meta"]["properties"]
    if meta["protocol_version"].get("const") != SCHEMA_VERSION:
        failures.append("schema meta.protocol_version const does not match current schema version")
    if meta["schema_version"].get("const") != SCHEMA_VERSION:
        failures.append("schema meta.schema_version const does not match current schema version")
    if schema.get("$id") != "urn:madp:schema:session-state:0.2.5-rc.2":
        failures.append("schema $id does not match RC version")
    if "Multi-AI Deliberation Protocol v0.2.5-rc.2" not in protocol:
        failures.append("protocol title does not identify RC version")
    if "GLOSSARY-v0.2.5-rc.2.md" not in protocol:
        failures.append("protocol does not reference RC glossary")
    if "GLOSSARY-v0.2.5-draft.md" in _section(protocol, "## 3. Normative terms"):
        failures.append("protocol normative terms section still references draft glossary")
    if "MADP v0.2.5-rc.2" not in glossary:
        failures.append("glossary does not identify RC version")

    status_section = _section(readme, "## Status and canonical files")
    current_section, _, _historical = status_section.partition("Previous draft documents are retained for history:")
    for required in [RC_PROTOCOL_PATH, RC_GLOSSARY_PATH, RC_SCHEMA_PATH]:
        if required not in current_section:
            failures.append(f"README current canonical list missing {required}")
    for draft_path in DRAFT_CANONICAL_PATHS:
        if draft_path in current_section:
            failures.append(f"README current canonical list mixes draft path {draft_path}")
    if 'current_release_candidate: "MADP-v0.2.5-rc.2"' not in readme:
        failures.append("README missing current_release_candidate RC marker")
    if 'previous_release_candidate: "MADP-v0.2.5-rc.1"' not in readme:
        failures.append("README missing previous_release_candidate RC marker")
    if 'previous_draft: "MADP-v0.2.5-draft"' not in readme:
        failures.append("README missing previous_draft marker")
    for historical_path in HISTORICAL_RC1_CANONICAL_PATHS:
        if not (ROOT / historical_path).exists():
            failures.append(f"historical rc.1 canonical file missing: {historical_path}")
    failures.extend(_normalized_version_compare_failures())
    failures.extend(_operational_record_failures())
    return failures


def _normalized_version_compare_failures() -> list[str]:
    pairs = [
        ("protocol", "protocol/MADP-v0.2.5-rc.1.md", "protocol/MADP-v0.2.5-rc.2.md"),
        ("glossary", "protocol/GLOSSARY-v0.2.5-rc.1.md", "protocol/GLOSSARY-v0.2.5-rc.2.md"),
        (
            "schema",
            "schemas/session-state-v0.2.5-rc.1.schema.yaml",
            "schemas/session-state-v0.2.5-rc.2.schema.yaml",
        ),
    ]
    failures: list[str] = []
    for label, left_path, right_path in pairs:
        left = (ROOT / left_path).read_text(encoding="utf-8")
        right = (ROOT / right_path).read_text(encoding="utf-8")
        if _normalize_rc_version_refs(left) != _normalize_rc_version_refs(right):
            failures.append(f"{label}: rc.1 and rc.2 differ beyond normalized version identifiers and paths")
    return failures


def _normalize_rc_version_refs(text: str) -> str:
    replacements = {
        "MADP-v0.2.5-rc.1": "MADP-v0.2.5-rc.X",
        "MADP-v0.2.5-rc.2": "MADP-v0.2.5-rc.X",
        "v0.2.5-rc.1": "v0.2.5-rc.X",
        "v0.2.5-rc.2": "v0.2.5-rc.X",
        "0.2.5-rc.1": "0.2.5-rc.X",
        "0.2.5-rc.2": "0.2.5-rc.X",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _operational_record_failures() -> list[str]:
    failures: list[str] = []
    expected = {
        "tests/operational/chatgpt-bootstrap-normal-001.yaml": (
            "CHATGPT-BOOTSTRAP-NORMAL-001",
            "MADP-v0.2.5-draft",
        ),
        "tests/operational/chatgpt-relay-mismatch-001.yaml": (
            "CHATGPT-RELAY-MISMATCH-001",
            "MADP-v0.2.5-draft",
        ),
        "tests/operational/gemini-manual-paste-load-001.yaml": (
            "GEMINI-MANUAL-PASTE-LOAD-001",
            "MADP-v0.2.5-rc.1",
        ),
        "tests/operational/gemini-uploaded-bundle-smoke-001.yaml": (
            "GEMINI-UPLOADED-BUNDLE-SMOKE-001",
            "MADP-v0.2.5-rc.1",
        ),
    }
    for relative, (expected_id, expected_version) in expected.items():
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing operational record {relative}")
            continue
        data = load_yaml(path)
        record = data.get("operational_test") if isinstance(data, dict) else None
        if not isinstance(record, dict):
            failures.append(f"{rel(path)}: missing operational_test mapping")
            continue
        if record.get("id") != expected_id:
            failures.append(f"{rel(path)}: unexpected operational test id")
        if record.get("tested_protocol_version") != expected_version:
            failures.append(f"{rel(path)}: unexpected tested protocol version")
        if expected_version == "MADP-v0.2.5-draft":
            if record.get("rc_context") != "MADP-v0.2.5-rc.1":
                failures.append(f"{rel(path)}: operational record missing RC context")
            if record.get("record_type") != "draft evidence for RC promotion":
                failures.append(f"{rel(path)}: operational record does not distinguish draft evidence")
        if expected_id == "GEMINI-MANUAL-PASTE-LOAD-001":
            if record.get("recovery", {}).get("method") != "PASTED_TEXT":
                failures.append(f"{rel(path)}: Gemini recovery method should be PASTED_TEXT")
            if record.get("initial_access", {}).get("all_required_files_read") is not False:
                failures.append(f"{rel(path)}: Gemini record should start with all_required_files_read false")
            if record.get("observed", {}).get("all_required_files_read") is not True:
                failures.append(f"{rel(path)}: Gemini record should end with all_required_files_read true")
        if expected_id == "GEMINI-UPLOADED-BUNDLE-SMOKE-001":
            if record.get("delivery_method") != "UPLOADED_FILE":
                failures.append(f"{rel(path)}: Gemini uploaded bundle record should use UPLOADED_FILE")
            if record.get("deviation", {}).get("code") != "BUNDLE_SOURCE_COMMIT_MISIDENTIFIED":
                failures.append(f"{rel(path)}: Gemini uploaded bundle record missing provenance deviation")
    readiness_path = ROOT / "tests/operational/rc2-release-readiness.yaml"
    if not readiness_path.exists():
        failures.append("missing operational record tests/operational/rc2-release-readiness.yaml")
    else:
        data = load_yaml(readiness_path)
        record = data.get("operational_test") if isinstance(data, dict) else None
        if not isinstance(record, dict):
            failures.append(f"{rel(readiness_path)}: missing operational_test mapping")
        else:
            if record.get("id") != "MADP-RC2-RELEASE-READINESS-001":
                failures.append(f"{rel(readiness_path)}: unexpected operational test id")
            if record.get("candidate_version") != PROTOCOL_VERSION:
                failures.append(f"{rel(readiness_path)}: candidate_version does not match current protocol")
            if record.get("status") != "PENDING_RUNTIME_SMOKE_TEST":
                failures.append(f"{rel(readiness_path)}: readiness status should remain pending runtime smoke test")
            if record.get("based_on", {}).get("previous_candidate") != "MADP-v0.2.5-rc.1":
                failures.append(f"{rel(readiness_path)}: missing previous candidate")
    return failures


def _section_values(protocol: str, compact_marker: str, detailed_marker: str) -> list[str]:
    compact = _list_after(protocol, compact_marker)
    detailed = _list_after(protocol, detailed_marker)
    return detailed + compact if detailed and detailed[0] not in compact else compact + [v for v in detailed if v not in compact]


if __name__ == "__main__":
    raise SystemExit(main())
