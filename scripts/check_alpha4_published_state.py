#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGET_COMMIT = "3333c66b8b9873581af3f621615a7e1f7fc20e0a"
TARGET_TAG = "MADP-v0.3.0-alpha.4"
ROLLBACK_TAG = "MADP-v0.3.0-alpha.2"
RELEASE_URL = (
    "https://github.com/Eruhitsuji/multi-ai-deliberation-protocol/"
    "releases/tag/MADP-v0.3.0-alpha.4"
)
ONE_TIME_WORKFLOWS = (
    ROOT / ".github/workflows/publish-alpha4-prerelease-once.yml",
    ROOT / ".github/workflows/resume-alpha4-prerelease.yml",
)


def load_yaml(path: str) -> dict:
    value = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected mapping: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    authorization = load_yaml("docs/planning/DEC-MADP-ALPHA4-007.yaml")
    cleanup = load_yaml("docs/planning/DEC-MADP-ALPHA4-008.yaml")
    implementation = load_yaml(
        "docs/planning/MADP-v0.3.0-alpha.4-implementation-status.yaml"
    )
    publication = load_yaml(
        "docs/planning/MADP-v0.3.0-alpha.4-publication-handoff-status.yaml"
    )
    readme = (ROOT / "README-v0.3.0-alpha.4.md").read_text(encoding="utf-8")
    release_notes = (
        ROOT / "docs/releases/MADP-v0.3.0-alpha.4.md"
    ).read_text(encoding="utf-8")

    require(authorization["status"] == "ACCEPTED", "publication decision not accepted")
    require(authorization["decision"]["exact_target_commit"] == TARGET_COMMIT, "authorization target mismatch")
    require(authorization["decision"]["tag"] == TARGET_TAG, "authorization tag mismatch")
    require(authorization["decision"]["github_release_mode"] == "PRERELEASE", "authorization release mode mismatch")
    require(authorization["decision"]["pages_publication_authorized"] is False, "Pages must remain unauthorized")
    require(authorization["decision"]["stable_release_authorized"] is False, "stable release must remain unauthorized")
    require(authorization["decision"]["formal_release_evidence"] is False, "formal evidence must remain false")

    require(cleanup["status"] == "ACCEPTED", "cleanup decision not accepted")
    require(cleanup["decision"]["publication_status"] == "PUBLISHED_GITHUB_PRERELEASE", "cleanup publication status mismatch")
    require(cleanup["decision"]["exact_tag_target_commit"] == TARGET_COMMIT, "cleanup target mismatch")
    require(cleanup["decision"]["tag"] == TARGET_TAG, "cleanup tag mismatch")
    require(cleanup["decision"]["release_url"] == RELEASE_URL, "cleanup release URL mismatch")
    require(cleanup["rollback_target"]["tag"] == ROLLBACK_TAG, "cleanup rollback mismatch")
    require(len(cleanup["published_assets"]) == 5, "expected five published assets")

    require(implementation["implementation_status"] == "PUBLISHED_PRERELEASE", "implementation status mismatch")
    require(implementation["content_ready"] is True, "content must be ready")
    require(implementation["release_ready"] is True, "release must be ready")
    require(implementation["tagged"] is True, "tagged must be true")
    require(implementation["published"] is True, "published must be true")
    require(implementation["release_mode"] == "PRERELEASE", "implementation release mode mismatch")
    require(implementation["publication"]["exact_tag_target_commit"] == TARGET_COMMIT, "implementation target mismatch")
    require(implementation["publication"]["tag"] == TARGET_TAG, "implementation tag mismatch")
    require(implementation["published_rollback_target"]["tag"] == ROLLBACK_TAG, "implementation rollback mismatch")
    require(implementation["stable_release_authorized"] is False, "stable release must remain false")
    require(implementation["formal_release_evidence"] is False, "formal evidence must remain false")
    require(implementation["pages_published"] is False, "Pages must remain unpublished")

    require(publication["implementation_status"] == "PUBLISHED", "publication status mismatch")
    require(publication["publication"]["exact_tag_target_commit"] == TARGET_COMMIT, "publication target mismatch")
    require(publication["publication"]["target_tag"] == TARGET_TAG, "publication tag mismatch")
    require(publication["publication"]["release_mode"] == "PRERELEASE", "publication mode mismatch")
    require(publication["publication"]["asset_count"] == 5, "publication asset count mismatch")
    require(publication["publication"]["github_asset_digests_verified"] is True, "asset digests must be verified")
    require(publication["handoff"]["rollback_target"] == ROLLBACK_TAG, "handoff rollback mismatch")
    require(publication["boundaries"]["one_time_publication_workflows_retired"] is True, "one-time workflows must be retired")
    require(publication["boundaries"]["automatic_republication_enabled"] is False, "automatic republication must be disabled")
    require(publication["boundaries"]["pages_published"] is False, "Pages boundary mismatch")
    require(publication["boundaries"]["stable_release_authorized"] is False, "stable boundary mismatch")
    require(publication["boundaries"]["formal_release_evidence"] is False, "formal evidence boundary mismatch")

    for workflow in ONE_TIME_WORKFLOWS:
        require(not workflow.exists(), f"one-time publication workflow still exists: {workflow}")

    require((ROOT / ".github/workflows/validate-alpha4-publication-handoff.yml").is_file(), "read-only handoff workflow missing")
    require((ROOT / ".github/workflows/validate-alpha4-published-state.yml").is_file(), "published-state audit workflow missing")

    for document, name in ((readme, "README"), (release_notes, "release notes")):
        require("PUBLISHED GITHUB PRERELEASE" in document, f"{name} publication marker missing")
        require(TARGET_TAG in document, f"{name} tag missing")
        require(TARGET_COMMIT in document, f"{name} target commit missing")
        require(ROLLBACK_TAG in document, f"{name} rollback tag missing")

    print("MADP v0.3.0-alpha.4 published-state records: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
