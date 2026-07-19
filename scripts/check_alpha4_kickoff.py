#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.4"
TARGET_COMMIT = "3333c66b8b9873581af3f621615a7e1f7fc20e0a"
TARGET_TAG = "MADP-v0.3.0-alpha.4"

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
            problems.append(f"missing alpha.4 baseline file: {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    decision = load_yaml(ARTIFACTS[0])
    status = load_yaml(ARTIFACTS[1])

    for key, expected in {
        "decision_id": "DEC-MADP-ALPHA4-001",
        "status": "ACCEPTED",
        "parent_decision_ref": "docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml",
    }.items():
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

    increment_ids = [
        item.get("id")
        for item in decision.get("increments", [])
        if isinstance(item, dict)
    ]
    if increment_ids != ["A4-INC-001", "A4-INC-002", "A4-INC-003"]:
        problems.append(f"increment sequence mismatch: {increment_ids!r}")

    if status.get("protocol_version") != VERSION:
        problems.append("protocol version mismatch")
    if status.get("base_version") != "MADP-v0.3.0-alpha.3":
        problems.append("base version mismatch")
    if status.get("implementation_status") not in {
        "CORE_USABILITY_SLICE_1_READY",
        "DISTRIBUTION_SLICE_READY",
        "PRERELEASE_CANDIDATE_READY",
        "PUBLISHED_PRERELEASE",
    }:
        problems.append(f"unsupported implementation lifecycle state: {status.get('implementation_status')!r}")
    if status.get("stable_release_authorized") is not False:
        problems.append("stable release must remain unauthorized")
    if status.get("formal_release_evidence") is not False:
        problems.append("formal release evidence must remain false")

    published = status.get("published") is True
    if published:
        for key in ("content_ready", "release_ready", "tagged"):
            if status.get(key) is not True:
                problems.append(f"published state requires {key}=true")
        if status.get("release_mode") != "PRERELEASE":
            problems.append("published alpha.4 must remain a prerelease")
        publication = status.get("publication", {})
        if publication.get("tag") != TARGET_TAG:
            problems.append("published tag mismatch")
        if publication.get("exact_tag_target_commit") != TARGET_COMMIT:
            problems.append("published target commit mismatch")
        if status.get("pages_published") is not False:
            problems.append("Pages must remain unpublished")

    compatibility = status.get("compatibility_policy", {})
    for key, expected in {
        "alpha3_command_namespace_preserved": True,
        "breaking_alpha3_schema_change": False,
        "legacy_fact_records_preserved": True,
        "alpha3_artifacts_remain_historical_and_unchanged": True,
        "additive_alpha4_records_only": True,
    }.items():
        if compatibility.get(key) is not expected:
            problems.append(f"compatibility policy mismatch: {key}")

    environment = status.get("development_environment", {})
    if environment.get("github_hosted_workflow_first_class") is not True:
        problems.append("GitHub-hosted workflow must be first-class")
    if environment.get("local_checkout_required") is not False:
        problems.append("local checkout must remain optional")

    work_packages = status.get("work_packages", {})
    kickoff = work_packages.get("kickoff_baseline", {})
    if kickoff.get("status") != "MERGED_TO_MAIN" or kickoff.get("pull_request") != 18:
        problems.append("kickoff baseline record mismatch")
    core = work_packages.get("core_usability_integration", {})
    if published and core.get("status") != "MERGED_TO_MAIN":
        problems.append("published state requires merged Core Usability integration")

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

    print("MADP v0.3.0-alpha.4 lifecycle baseline: PASS")
    print(f"implementation_status={status.get('implementation_status')}")
    print(f"published={str(status.get('published')).lower()}")
    print("local_checkout_required=false")
    print("stable_release_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
