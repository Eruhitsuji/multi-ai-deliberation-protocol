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

REQUIRED_FILES = (
    "docs/planning/DEC-MADP-ALPHA4-001.yaml",
    "docs/planning/MADP-v0.3.0-alpha.4-implementation-status.yaml",
    "README-v0.3.0-alpha.4.md",
    "docs/releases/MADP-v0.3.0-alpha.4.md",
    "scripts/check_alpha4_kickoff.py",
    ".github/workflows/validate-alpha4-kickoff.yml",
)


def load_yaml(relative: str):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    problems: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"missing alpha.4 kickoff file: {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    decision = load_yaml("docs/planning/DEC-MADP-ALPHA4-001.yaml")
    if decision.get("decision_id") != "DEC-MADP-ALPHA4-001":
        problems.append("alpha.4 decision ID mismatch")
    if decision.get("status") != "ACCEPTED":
        problems.append("alpha.4 decision is not accepted")
    if decision.get("parent_decision_ref") != "docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml":
        problems.append("rapid prerelease parent decision mismatch")
    if decision.get("decision", {}).get("target_version") != VERSION:
        problems.append("alpha.4 target version mismatch")
    if decision.get("decision", {}).get("development_model") != "RELEASE_EARLY_FIX_FORWARD":
        problems.append("alpha.4 development model mismatch")
    if decision.get("decision", {}).get("stable_release_authorized") is not False:
        problems.append("stable release must remain unauthorized")
    if decision.get("decision", {}).get("formal_release_evidence") is not False:
        problems.append("formal release evidence must remain false")
    if decision.get("authorization_boundary", {}).get("kickoff_merge_authorized") is not False:
        problems.append("kickoff merge must remain a separate action")
    for key in ("tag_authorized", "github_release_authorized", "pages_publication_authorized"):
        if decision.get("authorization_boundary", {}).get(key) is not False:
            problems.append(f"{key} must remain false")

    increments = decision.get("increments", [])
    increment_ids = [item.get("id") for item in increments if isinstance(item, dict)]
    if increment_ids != ["A4-INC-001", "A4-INC-002", "A4-INC-003"]:
        problems.append(f"alpha.4 increment sequence mismatch: {increment_ids!r}")

    status = load_yaml("docs/planning/MADP-v0.3.0-alpha.4-implementation-status.yaml")
    expected_status = {
        "protocol_version": VERSION,
        "implementation_status": "KICKOFF_BASELINE_READY",
        "integration_status": "IMPLEMENTATION_BRANCH",
        "base_version": "MADP-v0.3.0-alpha.3",
        "base_main_commit": BASE_COMMIT,
        "branch": BRANCH,
        "release_ready": False,
        "tagged": False,
        "published": False,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            problems.append(f"implementation status mismatch for {key}: {status.get(key)!r}")

    compatibility = status.get("compatibility_policy", {})
    for key in (
        "alpha3_command_namespace_preserved_during_kickoff",
        "legacy_fact_records_preserved",
        "alpha3_artifacts_remain_historical_and_unchanged",
    ):
        if compatibility.get(key) is not True:
            problems.append(f"compatibility invariant missing: {key}")
    if compatibility.get("breaking_schema_change_in_kickoff") is not False:
        problems.append("kickoff must not introduce a breaking schema change")

    environment = status.get("development_environment", {})
    if environment.get("github_hosted_workflow_first_class") is not True:
        problems.append("GitHub-hosted development must be first-class")
    if environment.get("local_checkout_required") is not False:
        problems.append("local checkout must remain optional")

    readme = text("README-v0.3.0-alpha.4.md")
    release_notes = text("docs/releases/MADP-v0.3.0-alpha.4.md")
    for marker in (
        "implementation kickoff baseline",
        "Human Final Authority",
        "Agreement among AI systems is not evidence",
        "MADP-v0.3.0-alpha.2",
        "Known limitations",
    ):
        if marker not in readme:
            problems.append(f"alpha.4 README marker missing: {marker}")
    for marker in (
        "DRAFT — implementation kickoff only",
        "Known limitations",
        "Rollback and previous version",
        "MADP-v0.3.0-alpha.2",
        "Formal release evidence remains false",
    ):
        if marker not in release_notes:
            problems.append(f"alpha.4 release-note marker missing: {marker}")

    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])")
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for relative in REQUIRED_FILES:
        body = text(relative)
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
