#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from madp_validation import ROOT, load_yaml, rel

PROFILE = ROOT / "docs" / "profiles" / "AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md"
BOOTSTRAP = ROOT / "bootstrap" / "use-madp-for-ai-driven-development.md"
CONTEXT_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "context-package.schema.yaml"
REVIEW_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "review.schema.yaml"
COMMAND_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "command.schema.yaml"
VALID_HANDOFF = ROOT / "fixtures" / "v0.3.0-alpha.2" / "ai-development" / "valid" / "coding-task-handoff.context-package.yaml"
VALID_REVIEW = ROOT / "fixtures" / "v0.3.0-alpha.2" / "ai-development" / "valid" / "review-before-commit.review.yaml"
INVALID_COMMAND = ROOT / "fixtures" / "v0.3.0-alpha.2" / "ai-development" / "invalid" / "auto-commit-without-approval.command.yaml"

PROFILE_MARKERS = [
    "MADP-AI-DEV-PROFILE-v0.3.0-alpha.2",
    "A TODO is not a decision.",
    "A decision is not approval.",
    "Approval is not execution permission.",
    "A review is not merge approval.",
    "A patch proposal is not repository modification permission.",
    "AI_DEVELOPMENT_STATUS",
    "external_actions_performed: false",
    "user_approval_claimed: false",
]

BOOTSTRAP_MARKERS = [
    "profile: AI_DRIVEN_DEVELOPMENT",
    "Do not claim user approval.",
    "Do not treat a TODO as approval.",
    "AI_DEVELOPMENT_STATUS",
    "AI_DEVELOPMENT_HANDOFF",
    "external_actions_allowed: false",
    "user_approval_inferred: false",
]


def validate_schema(schema_path: Path, fixture_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    instance = load_yaml(fixture_path)
    return [error.message for error in validator.iter_errors(instance)]


def main() -> int:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    for path in [PROFILE, BOOTSTRAP, VALID_HANDOFF, VALID_REVIEW, INVALID_COMMAND]:
        exists = path.is_file()
        checks.append({"check": "required_file", "target": rel(path), "passed": exists})
        if not exists:
            errors.append(f"missing required file: {rel(path)}")

    if PROFILE.is_file():
        text = PROFILE.read_text(encoding="utf-8")
        missing = [marker for marker in PROFILE_MARKERS if marker not in text]
        checks.append({"check": "profile_markers", "passed": not missing, "missing": missing})
        if missing:
            errors.append(f"profile missing markers: {missing}")

    if BOOTSTRAP.is_file():
        text = BOOTSTRAP.read_text(encoding="utf-8")
        missing = [marker for marker in BOOTSTRAP_MARKERS if marker not in text]
        checks.append({"check": "bootstrap_markers", "passed": not missing, "missing": missing})
        if missing:
            errors.append(f"bootstrap missing markers: {missing}")

    if VALID_HANDOFF.is_file():
        schema_errors = validate_schema(CONTEXT_SCHEMA, VALID_HANDOFF)
        instance = load_yaml(VALID_HANDOFF)["context_package"]
        rules = instance["usage_rules"]
        if rules.get("authority_boundary") != "PROPOSE_ONLY":
            schema_errors.append("handoff authority_boundary must be PROPOSE_ONLY")
        if rules.get("may_execute_external_actions") is not False:
            schema_errors.append("handoff may_execute_external_actions must be false")
        checks.append({"check": "valid_handoff", "passed": not schema_errors, "errors": schema_errors})
        errors.extend(schema_errors)

    if VALID_REVIEW.is_file():
        schema_errors = validate_schema(REVIEW_SCHEMA, VALID_REVIEW)
        instance = load_yaml(VALID_REVIEW)["review_request"]
        if instance.get("authority_boundary") != "PROPOSE_ONLY":
            schema_errors.append("review authority_boundary must be PROPOSE_ONLY")
        if "claim_user_approval" not in instance.get("disallowed_actions", []):
            schema_errors.append("review must disallow claim_user_approval")
        checks.append({"check": "valid_review", "passed": not schema_errors, "errors": schema_errors})
        errors.extend(schema_errors)

    if INVALID_COMMAND.is_file():
        schema_errors = validate_schema(COMMAND_SCHEMA, INVALID_COMMAND)
        block = load_yaml(INVALID_COMMAND)["command_block"]
        arguments = block.get("arguments", {})
        semantic_errors: list[str] = []
        if block.get("command") != "external-action":
            semantic_errors.append("invalid command must use external-action")
        if arguments.get("profile") != "AI_DRIVEN_DEVELOPMENT":
            semantic_errors.append("invalid command must identify AI_DRIVEN_DEVELOPMENT profile")
        if "confirmation_ref" not in arguments:
            semantic_errors.append("AI development external action is missing confirmation_ref")
        if block.get("authority_status") == "USER_CONFIRMED" and "confirmation_ref" not in arguments:
            semantic_errors.append("AI development command must not claim USER_CONFIRMED without confirmation_ref")
        passed = not schema_errors and bool(semantic_errors)
        checks.append(
            {
                "check": "invalid_external_action_fixture",
                "schema_valid": not schema_errors,
                "semantic_errors": semantic_errors,
                "passed": passed,
            }
        )
        if schema_errors:
            errors.extend(schema_errors)
        if not semantic_errors:
            errors.append("invalid external action fixture did not trigger semantic guard")

    report = {
        "suite": "alpha.2 AI-driven development profile",
        "result": "FAIL" if errors else "PASS",
        "checks": checks,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
