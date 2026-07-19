#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.4"
BASE_COMMIT = "f7fc84675321c0f55619301642f4d52f601f30d3"
BRANCH = "feature/v0.3.0-alpha.4-kickoff"

ARTIFACTS = (
    "docs/planning/DEC-MADP-ALPHA4-001.yaml",
    "docs/planning/MADP-v0.3.0-alpha.4-implementation-status.yaml",
    "README-v0.3.0-alpha.4.md",
    "docs/releases/MADP-v0.3.0-alpha.4.md",
)
SUPPORT_FILES = (
    "scripts/check_alpha4_kickoff.py",
    ".github/workflows/validate-alpha4-kickoff.yml",
)


def load_yaml(relative: str):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    problems: list[str] = []

    for relative in ARTIFACTS + SUPPORT_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"missing alpha.4 kickoff file: {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    decision = load_yaml(ARTIFACTS[0])
    status = load_yaml(ARTIFACTS[1])

    expected_decision = {
        "decision_id": "DEC-MADP-ALPHA4-001",
        "status": "ACCEPTED",
        "parent_decision_ref": "docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml",
    }
    for key, expected in expected_decision.items():
        if decision.get(key) != expected:
            problems.append(f"decision mismatch for {key}: {decision.get(key)!r}")

    decision_body = decision.get("decision", {})
    for key, expected in {
        "target_version": VERSION,
        "development_model": "RELEASE_EARLY_FIX_FORWARD",
        "implementation_authorized": True,
        "prerelease_authorized": True,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }.items():
        if decision_body.get(key) != expected:
            problems.append(f"decision body mismatch for {key}: {decision_body.get(key)!r}")

    boundary = decision.get("authorization_boundary", {})
    for key in (
        "kickoff_merge_authorized",
        "tag_authorized",
        "github_release_authorized",
        "pages_publication_authorized",
        "stable_release_authorized",
    ):
        if boundary.get(key) is not False:
            problems.append(f"authorization boundary must remain false: {key}")

    increment_ids = [
        item.get("id")
        for item in decision.get("increments", [])
        if isinstance(item, dict)
    ]
    if increment_ids != ["A4-INC-001", "A4-INC-002", "A4-INC-003"]:
        problems.append(f"increment sequence mismatch: {increment_ids!r}")

    expected_status = {
        "protocol_version": VERSION,
        "implementation_status": "KICKOFF_BASELINE_READY",
        "integration_status": "IMPLEMENTATION_BRANCH",
        "base_version": "MADP-v0.3.0-alpha.3",
        "base_main_commit": BASE_COMMIT,
        "branch": BRANCH,
        "content_ready": False,
        "release_ready": False,
        "tagged": False,
        "published": False,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            problems.append(f"status mismatch for {key}: {status.get(key)!r}")

    compatibility = status.get("compatibility_policy", {})
    if compatibility != {
        "alpha3_command_namespace_preserved_during_kickoff": True,
        "breaking_schema_change_in_kickoff": False,
        "legacy_fact_records_preserved": True,
        "alpha3_artifacts_remain_historical_and_unchanged": True,
    }:
        problems.append("kickoff compatibility policy mismatch")

    environment = status.get("development_environment", {})
    if environment.get("github_hosted_workflow_first_class") is not True:
        problems.append("GitHub-hosted workflow must be first-class")
    if environment.get("local_checkout_required") is not False:
        problems.append("local checkout must remain optional")

    readme = read(ARTIFACTS[2])
    release_notes = read(ARTIFACTS[3])
    if "## Known limitations" not in readme:
        problems.append("alpha.4 README lacks known limitations")
    if "Agreement among AI systems is not evidence" not in readme:
        problems.append("alpha.4 README lacks the evidence boundary")
    if "## Known limitations" not in release_notes:
        problems.append("alpha.4 release notes lack known limitations")
    if "## Rollback and previous version" not in release_notes:
        problems.append("alpha.4 release notes lack rollback information")
    if "MADP-v0.3.0-alpha.2" not in readme or "MADP-v0.3.0-alpha.2" not in release_notes:
        problems.append("published rollback version is not documented")

    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(
        rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])"
    )
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for relative in ARTIFACTS:
        body = read(relative)
        if exact_private.search(body):
            problems.append(f"private identifier found in {relative}")
        if email.search(body):
            problems.append(f"email address found in {relative}")
        if "human-final-authority-input-raw.md" in body:
            problems.append(f"removed private raw path referenced in {relative}")
        if re.search(r"(?i)publish_identifier_mapping\s*:\s*true", body):
            problems.append(f"identifier mapping publication enabled in {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("MADP v0.3.0-alpha.4 kickoff baseline: PASS")
    print(f"base_main_commit={BASE_COMMIT}")
    print("local_checkout_required=false")
    print("stable_release_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
