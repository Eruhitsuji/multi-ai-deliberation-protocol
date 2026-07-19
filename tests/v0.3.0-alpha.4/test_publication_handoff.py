#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_alpha4_publication_handoff import check
from generate_alpha4_publication_handoff import (
    HANDOFF_FILENAME,
    TARGET_TAG,
    write_handoff,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def problems_for(
    directory: Path,
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
) -> list[str]:
    return check(
        directory,
        repository,
        source_commit,
        source_ref_kind,
        branch_name,
        TARGET_TAG,
        root=ROOT,
    )


def verify_status_bridge() -> None:
    workflow_path = ROOT / ".github/workflows/validate-alpha4-publication-handoff.yml"
    workflow = workflow_path.read_text(encoding="utf-8")
    required_markers = (
        "contents: read",
        "statuses: write",
        "Publish exact-main handoff commit status",
        "if: always() && github.event_name == 'push' && github.ref_name == 'main'",
        "context='madp/alpha4-publication-handoff'",
        '"repos/$GITHUB_REPOSITORY/statuses/$GITHUB_SHA"',
        'target_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"',
    )
    for marker in required_markers:
        require(marker in workflow, f"publication handoff status bridge missing: {marker}")
    forbidden_markers = (
        "contents: write",
        "releases: write",
        "pages: write",
        "deployments: write",
        "git tag",
        "gh release create",
    )
    for marker in forbidden_markers:
        require(marker not in workflow, f"publication handoff workflow grants forbidden capability: {marker}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--branch-name", required=True)
    args = parser.parse_args()

    verify_status_bridge()

    # PR-head fixtures must never use the protected main branch name. When this
    # regression suite runs from a push to main, use a deterministic synthetic
    # branch for PR-head-only cases while preserving an explicit MERGED_MAIN/main
    # case below.
    pr_branch = (
        args.branch_name
        if args.branch_name != "main"
        else "feature/test-publication-handoff"
    )

    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        valid = base / "valid"
        write_handoff(
            valid,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            pr_branch,
            TARGET_TAG,
            root=ROOT,
        )
        require(
            problems_for(
                valid,
                args.repository,
                args.source_commit,
                "PULL_REQUEST_HEAD",
                pr_branch,
            ) == [],
            "valid publication handoff must pass",
        )

        second = base / "second"
        write_handoff(
            second,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            pr_branch,
            TARGET_TAG,
            root=ROOT,
        )
        first_files = sorted(path.name for path in valid.iterdir())
        second_files = sorted(path.name for path in second.iterdir())
        require(first_files == second_files, "handoff file inventories must match")
        for name in first_files:
            require(
                (valid / name).read_bytes() == (second / name).read_bytes(),
                f"handoff output must be deterministic: {name}",
            )

        changed_authority = base / "changed-authority"
        write_handoff(
            changed_authority,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            pr_branch,
            TARGET_TAG,
            root=ROOT,
        )
        handoff_path = changed_authority / HANDOFF_FILENAME
        handoff = yaml.safe_load(handoff_path.read_text(encoding="utf-8"))
        handoff["required_human_actions"]["authorize_tag"] = True
        handoff_path.write_text(
            yaml.safe_dump(handoff, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        require(
            any(
                "canonical output" in problem
                or "human action must remain unconfirmed" in problem
                or "handoff schema failure" in problem
                for problem in problems_for(
                    changed_authority,
                    args.repository,
                    args.source_commit,
                    "PULL_REQUEST_HEAD",
                    pr_branch,
                )
            ),
            "confirmed authority must be rejected",
        )

        wrong_tag = base / "wrong-tag"
        try:
            write_handoff(
                wrong_tag,
                args.repository,
                args.source_commit,
                "PULL_REQUEST_HEAD",
                pr_branch,
                "MADP-v0.3.0-alpha.4-other",
                root=ROOT,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("unexpected target tag must fail closed")

        merged = base / "merged-main"
        write_handoff(
            merged,
            args.repository,
            args.source_commit,
            "MERGED_MAIN",
            "main",
            TARGET_TAG,
            root=ROOT,
        )
        require(
            problems_for(
                merged,
                args.repository,
                args.source_commit,
                "MERGED_MAIN",
                "main",
            ) == [],
            "merged-main publication handoff must pass",
        )

    print("MADP v0.3.0-alpha.4 publication handoff tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
