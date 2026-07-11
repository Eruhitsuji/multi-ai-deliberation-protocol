#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.2"
REPOSITORY_STATE = "RELEASE_CANDIDATE_READY"
STATUS_PATH = ROOT / "docs" / "planning" / "MADP-v0.3.0-alpha.2-implementation-status.yaml"
RELEASE_NOTES = ROOT / "docs" / "releases" / "MADP-v0.3.0-alpha.2.md"

REQUIRED_FILES = [
    "README-v0.3.0-alpha.2.md",
    "docs/planning/MADP-v0.3.0-alpha.2-scope.md",
    "docs/planning/MADP-v0.3.0-alpha.2-implementation-status.yaml",
    "docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md",
    "docs/releases/MADP-v0.3.0-alpha.2.md",
    "protocol/MADP-v0.3.0-alpha.2.md",
    "protocol/GLOSSARY-v0.3.0-alpha.2.md",
    "schemas/v0.3.0-alpha.2/command.schema.yaml",
    "schemas/v0.3.0-alpha.2/command-registry.schema.yaml",
    "schemas/v0.3.0-alpha.2/todo.schema.yaml",
    "schemas/v0.3.0-alpha.2/context-package.schema.yaml",
    "schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml",
    "schemas/v0.3.0-alpha.2/review.schema.yaml",
    "schemas/v0.3.0-alpha.2/relay.schema.yaml",
    "registries/v0.3.0-alpha.2/commands.yaml",
    "tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml",
    "scripts/parse_command_v030_alpha2.py",
    "scripts/apply_command_v030_alpha2.py",
    "scripts/test_command_parser_v030_alpha2.py",
    "scripts/test_command_runtime_v030_alpha2.py",
    "scripts/check_todo_lifecycle_v030_alpha2.py",
    "scripts/check_translation_docs.py",
]

EXPECTED_SCHEMA_IDS = {
    "schemas/v0.3.0-alpha.2/command.schema.yaml": "urn:madp:schema:command:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/command-registry.schema.yaml": "urn:madp:schema:command-registry:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/todo.schema.yaml": "urn:madp:schema:todo:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/context-package.schema.yaml": "urn:madp:schema:context-package:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml": "urn:madp:schema:context-package-receipt:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/review.schema.yaml": "urn:madp:schema:review:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/relay.schema.yaml": "urn:madp:schema:relay:0.3.0-alpha.2",
}

REQUIRED_PROTOCOL_PHRASES = [
    "A TODO is not a decision.",
    "A decision is not approval.",
    "Approval is not execution permission.",
    "Raw command text is never authoritative by itself.",
    "Parse first.",
    "Normalize second.",
    "Validate third.",
    "Authorize fourth.",
    "Apply last.",
]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    for relative in REQUIRED_FILES:
        exists = (ROOT / relative).is_file()
        checks.append({"check": "required_file", "target": relative, "passed": exists})
        if not exists:
            errors.append(f"missing required file: {relative}")

    status = load_yaml(STATUS_PATH) if STATUS_PATH.is_file() else {}
    expected_status = {
        "protocol_version": VERSION,
        "implementation_status": "RELEASE_CANDIDATE_READY",
        "integration_status": "MERGED_TO_MAIN",
        "release_ready": True,
        "tagged": False,
        "published": False,
    }
    for key, expected in expected_status.items():
        passed = status.get(key) == expected
        checks.append({"check": "status_field", "target": key, "passed": passed})
        if not passed:
            errors.append(f"unexpected status field {key}: {status.get(key)!r}")

    for relative, expected_id in EXPECTED_SCHEMA_IDS.items():
        path = ROOT / relative
        if path.is_file():
            actual_id = load_yaml(path).get("$id")
            passed = actual_id == expected_id
            checks.append({"check": "schema_id", "target": relative, "passed": passed})
            if not passed:
                errors.append(f"unexpected schema $id: {relative}: {actual_id!r}")

    protocol_path = ROOT / "protocol" / "MADP-v0.3.0-alpha.2.md"
    if protocol_path.is_file():
        text = protocol_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in REQUIRED_PROTOCOL_PHRASES if phrase not in text]
        checks.append({"check": "protocol_required_phrases", "passed": not missing, "missing": missing})
        if missing:
            errors.append(f"alpha.2 protocol missing required phrases: {missing}")

    readme = (ROOT / "README-v0.3.0-alpha.2.md").read_text(encoding="utf-8") if (ROOT / "README-v0.3.0-alpha.2.md").is_file() else ""
    for phrase in ["Release candidate status", "release_ready: true", "tagged: false", "published: false"]:
        passed = phrase in readme
        checks.append({"check": "release_readme_phrase", "target": phrase, "passed": passed})
        if not passed:
            errors.append(f"alpha.2 README missing release phrase: {phrase}")

    if RELEASE_NOTES.is_file():
        notes = RELEASE_NOTES.read_text(encoding="utf-8")
        for phrase in [VERSION, "Highlights", "Validation", "Known limitations"]:
            passed = phrase in notes
            checks.append({"check": "release_notes_phrase", "target": phrase, "passed": passed})
            if not passed:
                errors.append(f"release notes missing phrase: {phrase}")

    report = {
        "report_version": "2",
        "protocol_version": VERSION,
        "repository_state": REPOSITORY_STATE if not errors else "RELEASE_CANDIDATE_INCONSISTENT",
        "release_ready": not errors,
        "tagged": False,
        "published": False,
        "checks": checks,
        "errors": errors,
        "limitations": [
            "A passing audit verifies repository publication readiness but does not create a tag or GitHub Release.",
            "The exact verified main commit must be used as the release tag target after merge.",
            "The internal apply runtime never performs external actions.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
