#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from madp_validation import ROOT, load_yaml, rel

COMMAND_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "command.schema.yaml"
FIXTURE_DIR = ROOT / "fixtures" / "v0.3.0-alpha.2" / "command" / "semantic-invalid"

EXPECTED_ERRORS = {
    "approve-missing-revision.command.yaml": ["CMD_MISSING_REQUIRED_ARGUMENT:revision"],
    "repeated-option.command.yaml": ["CMD_REPEATED_OPTION:title"],
    "unknown-option.command.yaml": ["CMD_UNKNOWN_OPTION:teleport"],
    "external-action-unconfirmed.command.yaml": ["CMD_EXTERNAL_ACTION_REQUIRES_CONFIRMATION"],
    "silent-approval-repair.command.yaml": ["CMD_AI_SILENT_APPROVAL_REPAIR_FORBIDDEN"],
}


def iter_fixtures() -> list[Path]:
    return sorted(path for path in FIXTURE_DIR.glob("*.y*ml") if path.is_file())


def semantic_errors(instance: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    block = instance.get("command_block", {})
    command = block.get("command")
    command_class = block.get("command_class")
    issued_by = block.get("issued_by")
    authority_status = block.get("authority_status")
    authority_boundary = block.get("authority_boundary")
    arguments = block.get("arguments", {}) or {}

    if command == "approve":
        for required in ("decision", "revision"):
            if required not in arguments:
                errors.append(f"CMD_MISSING_REQUIRED_ARGUMENT:{required}")
        if issued_by != "USER" and authority_status == "USER_CONFIRMED":
            errors.append("CMD_AI_SILENT_APPROVAL_REPAIR_FORBIDDEN")
        if arguments.get("repaired_by_ai") is True:
            errors.append("CMD_AI_SILENT_APPROVAL_REPAIR_FORBIDDEN")

    for option in arguments.get("repeated_options", []) or []:
        errors.append(f"CMD_REPEATED_OPTION:{option}")

    for option in arguments.get("unknown_options", []) or []:
        errors.append(f"CMD_UNKNOWN_OPTION:{option}")

    if command == "external-action":
        has_confirmation_ref = "confirmation_ref" in arguments
        if authority_status == "USER_CONFIRMED" or authority_boundary == "USER_CONFIRMED":
            if not has_confirmation_ref:
                errors.append("CMD_EXTERNAL_ACTION_REQUIRES_CONFIRMATION")
        if command_class != "EXTERNAL_ACTION_COMMAND":
            errors.append("CMD_EXTERNAL_ACTION_CLASS_MISMATCH")

    return sorted(set(errors))


def main() -> int:
    schema = load_yaml(COMMAND_SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    fixtures = iter_fixtures()
    if not fixtures:
        raise SystemExit(f"no semantic-invalid fixtures found in {rel(FIXTURE_DIR)}")

    results = []
    failed = False

    seen = {path.name for path in fixtures}
    missing = sorted(set(EXPECTED_ERRORS) - seen)
    extra = sorted(seen - set(EXPECTED_ERRORS))
    if missing or extra:
        failed = True
        results.append({"fixture": "<fixture set>", "result": "FAIL", "missing": missing, "extra": extra})

    for path in fixtures:
        instance = load_yaml(path)
        schema_errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        actual = semantic_errors(instance)
        expected = sorted(EXPECTED_ERRORS.get(path.name, []))
        matched = not schema_errors and actual == expected
        failed = failed or not matched
        results.append(
            {
                "fixture": rel(path),
                "schema_valid": not schema_errors,
                "expected_semantic_errors": expected,
                "actual_semantic_errors": actual,
                "result": "PASS" if matched else "FAIL",
            }
        )

    print(json.dumps({"suite": "alpha.2 semantic-invalid command fixtures", "result": "FAIL" if failed else "PASS", "fixtures": results}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
