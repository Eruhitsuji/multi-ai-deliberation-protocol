#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.2"
REPOSITORY_STATE = "DRAFT_PRERELEASE_PLANNING"

REQUIRED_FILES = [
    "README-v0.3.0-alpha.2.md",
    "docs/planning/MADP-v0.3.0-alpha.2-scope.md",
    "protocol/MADP-v0.3.0-alpha.2.md",
    "protocol/GLOSSARY-v0.3.0-alpha.2.md",
    "schemas/v0.3.0-alpha.2/command.schema.yaml",
    "schemas/v0.3.0-alpha.2/todo.schema.yaml",
    "schemas/v0.3.0-alpha.2/context-package.schema.yaml",
    "fixtures/v0.3.0-alpha.2/command/valid/todo-add.command.yaml",
    "fixtures/v0.3.0-alpha.2/command/valid/approve.command.yaml",
    "fixtures/v0.3.0-alpha.2/command/valid/parse-error.command.yaml",
    "fixtures/v0.3.0-alpha.2/command/invalid/unknown-command.command.yaml",
    "fixtures/v0.3.0-alpha.2/command/invalid/parse-error-applied.command.yaml",
    "fixtures/v0.3.0-alpha.2/todo/valid/initial.todo-list.yaml",
    "fixtures/v0.3.0-alpha.2/todo/invalid/bad-status.todo-list.yaml",
    "fixtures/v0.3.0-alpha.2/context-package/valid/share-context.context-package.yaml",
    "fixtures/v0.3.0-alpha.2/context-package/invalid/external-execution.context-package.yaml",
    "bootstrap/use-madp-commands.md",
    "bootstrap/share-context-with-ai.md",
    "bootstrap/request-review.md",
    "tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml",
    "scripts/validate_alpha2_command_context_todo_fixtures.py",
    "scripts/check_traceability_v030_alpha2.py",
]

EXPECTED_SCHEMA_IDS = {
    "schemas/v0.3.0-alpha.2/command.schema.yaml": "urn:madp:schema:command:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/todo.schema.yaml": "urn:madp:schema:todo:0.3.0-alpha.2",
    "schemas/v0.3.0-alpha.2/context-package.schema.yaml": "urn:madp:schema:context-package:0.3.0-alpha.2",
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

REQUIRED_GLOSSARY_TERMS = [
    "Command Block",
    "Context Package",
    "TODO Item",
    "TODO List",
    "User Command",
    "External Action Command",
    "Relay Mode",
]

REQUIRED_README_PHRASES = [
    "Status: draft, not tagged, not published, and not release-ready.",
    "MADP-v0.3.0-alpha.1` remains the current published alpha prerelease",
    "A TODO is not a decision.",
    "A decision is not approval.",
    "Approval is not execution permission.",
    "release_ready: false",
    "draft_ready_for_review: true | false",
]

REQUIRED_BOOTSTRAP_PROMPTS = {
    "bootstrap/use-madp-commands.md": [
        "MADP-v0.3.0-alpha.2",
        "COMMAND_BLOCK",
        "COMMAND_PARSE_ERROR",
        "COMMAND_NEEDS_ARGUMENTS",
        "Parse first.",
        "Do not claim user approval",
    ],
    "bootstrap/share-context-with-ai.md": [
        "MADP-v0.3.0-alpha.2",
        "CONTEXT_PACKAGE",
        "CONTEXT_PACKAGE_RECEIPT",
        "may_execute_external_actions: false",
        "Do not claim user approval",
    ],
    "bootstrap/request-review.md": [
        "MADP-v0.3.0-alpha.2",
        "REVIEW_REQUEST",
        "REVIEW_RESPONSE",
        "PROPOSE_ONLY",
        "external_actions_performed: false",
    ],
}


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

    for relative, expected_id in EXPECTED_SCHEMA_IDS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        actual_id = load_yaml(path).get("$id")
        passed = actual_id == expected_id
        checks.append({"check": "schema_id", "target": relative, "expected": expected_id, "actual": actual_id, "passed": passed})
        if not passed:
            errors.append(f"unexpected schema $id: {relative}: {actual_id!r}")

    protocol_path = ROOT / "protocol" / "MADP-v0.3.0-alpha.2.md"
    if protocol_path.is_file():
        protocol_text = protocol_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in REQUIRED_PROTOCOL_PHRASES if phrase not in protocol_text]
        passed = not missing
        checks.append({"check": "protocol_required_phrases", "passed": passed, "missing": missing})
        if missing:
            errors.append(f"alpha.2 protocol missing required phrases: {missing}")

    glossary_path = ROOT / "protocol" / "GLOSSARY-v0.3.0-alpha.2.md"
    if glossary_path.is_file():
        glossary_text = glossary_path.read_text(encoding="utf-8")
        missing = [term for term in REQUIRED_GLOSSARY_TERMS if f"**{term}**" not in glossary_text]
        passed = not missing
        checks.append({"check": "glossary_required_terms", "passed": passed, "missing": missing})
        if missing:
            errors.append(f"alpha.2 glossary missing required terms: {missing}")

    readme_path = ROOT / "README-v0.3.0-alpha.2.md"
    if readme_path.is_file():
        readme_text = readme_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in REQUIRED_README_PHRASES if phrase not in readme_text]
        passed = not missing
        checks.append({"check": "readme_required_phrases", "passed": passed, "missing": missing})
        if missing:
            errors.append(f"alpha.2 README missing required phrases: {missing}")

    matrix_path = ROOT / "tests" / "traceability" / "traceability-matrix-v0.3.0-alpha.2.yaml"
    if matrix_path.is_file():
        matrix = load_yaml(matrix_path)
        entries = matrix.get("entries", [])
        passed = matrix.get("protocol_version") == VERSION and len(entries) >= 6
        checks.append({"check": "traceability_matrix_minimum", "entries": len(entries), "passed": passed})
        if not passed:
            errors.append("alpha.2 traceability matrix does not meet minimum draft coverage")

    for relative, phrases in REQUIRED_BOOTSTRAP_PROMPTS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        passed = not missing
        checks.append({"check": "alpha2_bootstrap_prompt", "target": relative, "passed": passed, "missing": missing})
        if missing:
            errors.append(f"alpha.2 bootstrap prompt {relative} missing required phrases: {missing}")

    report = {
        "report_version": "1",
        "protocol_version": VERSION,
        "repository_state": REPOSITORY_STATE if not errors else "DRAFT_INCONSISTENT",
        "release_ready": False,
        "draft_ready_for_review": not errors,
        "checks": checks,
        "errors": errors,
        "limitations": [
            "This audit checks alpha.2 draft readiness only; it does not claim release readiness.",
            "Generated alpha.2 bundle schemas are not required by this draft audit yet.",
            "A passing audit does not authorize merge, tagging, release publication, or external execution.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
