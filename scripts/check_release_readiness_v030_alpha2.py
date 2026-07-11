#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.2"
REPOSITORY_STATE = "PUBLISHED_PRERELEASE"
RELEASE_COMMIT = "207e24290e0a66bf0dd34e13f9b3525a42a5a6c9"
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
        "implementation_status": "PUBLISHED_PRERELEASE",
        "integration_status": "MERGED_TO_MAIN",
        "release_ready": True,
        "tagged": True,
        "published": True,
        "release_tag": VERSION,
        "release_commit": RELEASE_COMMIT,
    }
    for key, expected in expected_status.items():
        passed = status.get(key) == expected
        checks.append({"check": "status_field", "target": key, "passed": passed})
        if not passed:
            errors.append(f"unexpected status field {key}: {status.get(key)!r}")

    published_at = status.get("published_at")
    published_at_ok = isinstance(published_at, str) and bool(published_at.strip())
    checks.append({"check": "published_at_recorded", "passed": published_at_ok, "value": published_at})
    if not published_at_ok:
        errors.append("published_at must be recorded; UNKNOWN is allowed when the authoritative timestamp is unavailable")

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

    readme_path = ROOT / "README-v0.3.0-alpha.2.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    for phrase in ["Published prerelease status", "release_ready: true", "tagged: true", "published: true", RELEASE_COMMIT]:
        passed = phrase in readme
        checks.append({"check": "release_readme_phrase", "target": phrase, "passed": passed})
        if not passed:
            errors.append(f"alpha.2 README missing published phrase: {phrase}")

    if RELEASE_NOTES.is_file():
        notes = RELEASE_NOTES.read_text(encoding="utf-8")
        for phrase in [VERSION, "Highlights", "Validation", "Known limitations", RELEASE_COMMIT, "Published"]:
            passed = phrase in notes
            checks.append({"check": "release_notes_phrase", "target": phrase, "passed": passed})
            if not passed:
                errors.append(f"release notes missing phrase: {phrase}")

    report = {
        "report_version": "3",
        "protocol_version": VERSION,
        "repository_state": REPOSITORY_STATE if not errors else "PUBLISHED_PRERELEASE_INCONSISTENT",
        "release_ready": not errors,
        "tagged": status.get("tagged"),
        "published": status.get("published"),
        "release_tag": status.get("release_tag"),
        "release_commit": status.get("release_commit"),
        "published_at": published_at,
        "checks": checks,
        "errors": errors,
        "limitations": [
            "This audit verifies repository metadata and release artifacts; it does not independently query the GitHub Releases API.",
            "The publication timestamp may remain UNKNOWN until an authoritative timestamp is recorded.",
            "The internal apply runtime never performs external actions.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
