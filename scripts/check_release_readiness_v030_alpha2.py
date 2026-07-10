#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.2"
REPOSITORY_STATE = "DRAFT_PRERELEASE_IMPLEMENTED"

REQUIRED_FILES = [
    "README-v0.3.0-alpha.2.md",
    "docs/planning/MADP-v0.3.0-alpha.2-scope.md",
    "docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md",
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
    "fixtures/v0.3.0-alpha.2/command/valid/todo-add.command.yaml",
    "fixtures/v0.3.0-alpha.2/command/semantic-invalid/approve-missing-revision.command.yaml",
    "fixtures/v0.3.0-alpha.2/todo/valid/initial.todo-list.yaml",
    "fixtures/v0.3.0-alpha.2/context-package/valid/share-context.context-package.yaml",
    "fixtures/v0.3.0-alpha.2/context-package-receipt/valid/partial.context-package-receipt.yaml",
    "fixtures/v0.3.0-alpha.2/review/valid/review-response.review.yaml",
    "fixtures/v0.3.0-alpha.2/relay/valid/task-handoff.relay.yaml",
    "fixtures/v0.3.0-alpha.2/relay/invalid/external-action.relay.yaml",
    "fixtures/v0.3.0-alpha.2/ai-development/valid/coding-task-handoff.context-package.yaml",
    "fixtures/v0.3.0-alpha.2/ai-development/invalid/auto-commit-without-approval.command.yaml",
    "tests/todo-lifecycle-v0.3.0-alpha.2/cases.yaml",
    "tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-001/manifest.yaml",
    "tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-002/manifest.yaml",
    "tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml",
    "bootstrap/use-madp-commands.md",
    "bootstrap/share-context-with-ai.md",
    "bootstrap/request-review.md",
    "bootstrap/use-madp-for-ai-driven-development.md",
    "scripts/validate_alpha2_command_context_todo_fixtures.py",
    "scripts/check_command_semantic_invalid_fixtures_v030_alpha2.py",
    "scripts/check_command_registry_v030_alpha2.py",
    "scripts/parse_command_v030_alpha2.py",
    "scripts/test_command_parser_v030_alpha2.py",
    "scripts/check_all_commands_v030_alpha2.py",
    "scripts/check_todo_lifecycle_v030_alpha2.py",
    "scripts/check_ai_development_profile_v030_alpha2.py",
    "scripts/check_migration_v030_alpha2.py",
    "scripts/check_traceability_v030_alpha2.py",
    "scripts/generate_alpha2_bootstrap_prompts.py",
    "scripts/check_generated_alpha2_bootstrap.py",
    "scripts/test_generate_alpha2_bootstrap_prompts.py",
    "scripts/generate_alpha2_schema_bundles.py",
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

REQUIRED_README_PHRASES = [
    "Status: draft, not tagged, not published, and not release-ready.",
    "A TODO is not a decision.",
    "A decision is not approval.",
    "Approval is not execution permission.",
    "release_ready: false",
    "draft_ready_for_review: true | false",
]

REQUIRED_BOOTSTRAP_PROMPTS = {
    "bootstrap/use-madp-commands.md": ["COMMAND_BLOCK", "COMMAND_PARSE_ERROR", "COMMAND_NEEDS_ARGUMENTS"],
    "bootstrap/share-context-with-ai.md": ["CONTEXT_PACKAGE", "CONTEXT_PACKAGE_RECEIPT", "may_execute_external_actions: false"],
    "bootstrap/request-review.md": ["REVIEW_REQUEST", "REVIEW_RESPONSE", "PROPOSE_ONLY"],
    "bootstrap/use-madp-for-ai-driven-development.md": ["AI_DEVELOPMENT_STATUS", "external_actions_allowed: false"],
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
    if readme_path.is_file():
        text = readme_path.read_text(encoding="utf-8")
        missing = [phrase for phrase in REQUIRED_README_PHRASES if phrase not in text]
        checks.append({"check": "readme_required_phrases", "passed": not missing, "missing": missing})
        if missing:
            errors.append(f"alpha.2 README missing required phrases: {missing}")

    matrix_path = ROOT / "tests" / "traceability" / "traceability-matrix-v0.3.0-alpha.2.yaml"
    if matrix_path.is_file():
        entries = load_yaml(matrix_path).get("entries", [])
        passed = len(entries) >= 16
        checks.append({"check": "traceability_matrix_minimum", "entries": len(entries), "passed": passed})
        if not passed:
            errors.append("alpha.2 traceability matrix does not cover completed implementation areas")

    for relative, phrases in REQUIRED_BOOTSTRAP_PROMPTS.items():
        path = ROOT / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            missing = [phrase for phrase in phrases if phrase not in text]
            checks.append({"check": "alpha2_bootstrap_prompt", "target": relative, "passed": not missing, "missing": missing})
            if missing:
                errors.append(f"alpha.2 bootstrap prompt {relative} missing required phrases: {missing}")

    generator_text = (ROOT / "scripts" / "generate_alpha2_schema_bundles.py").read_text(encoding="utf-8")
    bundle_names = ["command", "command-registry", "todo", "context-package", "context-package-receipt", "review", "relay"]
    missing_bundles = [name for name in bundle_names if f'"{name}"' not in generator_text]
    checks.append({"check": "alpha2_schema_bundle_set", "expected_count": 7, "passed": not missing_bundles, "missing": missing_bundles})
    if missing_bundles:
        errors.append(f"alpha.2 schema bundle generator missing schemas: {missing_bundles}")

    report = {
        "report_version": "1",
        "protocol_version": VERSION,
        "repository_state": REPOSITORY_STATE if not errors else "DRAFT_INCONSISTENT",
        "release_ready": False,
        "draft_ready_for_review": not errors,
        "checks": checks,
        "errors": errors,
        "limitations": [
            "This audit checks alpha.2 implementation and draft readiness; it does not claim publication readiness.",
            "A passing audit does not authorize merge, tagging, release publication, or external execution.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
