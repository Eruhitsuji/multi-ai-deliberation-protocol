#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re

import yaml

from generate_alpha4_prerelease_package import (
    ARCHIVE_FILENAME,
    SIDECAR_AUDIT_FILENAME,
    SIDECAR_MANIFEST_FILENAME,
    build_package,
    sha256,
    verify_git_head,
    verify_git_sources,
    verify_repository_sources,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_FILENAME = "MADP-v0.3.0-alpha.4-release-candidate.receipt.yaml"
RELEASE_NOTES_PATH = ROOT / "docs/releases/MADP-v0.3.0-alpha.4.md"


def validate_ref(source_ref_kind: str, branch_name: str) -> None:
    if source_ref_kind not in {"PULL_REQUEST_HEAD", "MERGED_MAIN"}:
        raise ValueError("source_ref_kind must be PULL_REQUEST_HEAD or MERGED_MAIN")
    if not branch_name or not re.fullmatch(r"[A-Za-z0-9._/-]+", branch_name):
        raise ValueError("branch_name is invalid")
    if source_ref_kind == "MERGED_MAIN" and branch_name != "main":
        raise ValueError("MERGED_MAIN requires branch_name main")
    if source_ref_kind == "PULL_REQUEST_HEAD" and branch_name == "main":
        raise ValueError("PULL_REQUEST_HEAD cannot use branch_name main")


def build_receipt(
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
    root: Path = ROOT,
) -> tuple[bytes, bytes, bytes, bytes, bytes]:
    validate_ref(source_ref_kind, branch_name)
    archive, manifest_bytes, audit_bytes, archive_sha_bytes = build_package(
        repository, source_commit, root=root
    )
    audit = yaml.safe_load(audit_bytes.decode("utf-8"))
    limitations = audit.get("known_limitations", [])
    if not isinstance(limitations, list) or not limitations:
        raise ValueError("package audit must contain known limitations")
    release_notes = (root / "docs/releases/MADP-v0.3.0-alpha.4.md").read_bytes()
    main_candidate = source_ref_kind == "MERGED_MAIN"
    receipt = {
        "receipt_version": "MADP-RELEASE-CANDIDATE-RECEIPT-v1",
        "protocol_version": "MADP-v0.3.0-alpha.4",
        "repository": repository,
        "source_commit": source_commit,
        "source_ref_kind": source_ref_kind,
        "branch_name": branch_name,
        "main_branch_candidate": main_candidate,
        "status": (
            "MERGED_MAIN_CANDIDATE_VALIDATED"
            if main_candidate
            else "PR_HEAD_CANDIDATE_VALIDATED"
        ),
        "artifact_name": f"madp-v0.3.0-alpha.4-release-candidate-{source_commit}",
        "package_archive_file": ARCHIVE_FILENAME,
        "package_archive_sha256": sha256(archive),
        "package_manifest_sha256": sha256(manifest_bytes),
        "release_notes_sha256": sha256(release_notes),
        "known_limitation_count": len(limitations),
        "checks": {
            "retained_alpha4_validation": "PASS",
            "package_regression": "PASS",
            "deterministic_generation": "PASS",
            "package_canonical_validation": "PASS",
            "privacy_scan": "PASS",
            "authority_boundary": "PASS",
            "release_notes_known_limitations": "PASS",
        },
        "boundaries": {
            "formal_release_evidence": False,
            "stable_release_authorized": False,
            "publication_authorized": False,
            "tag_authorized": False,
            "github_release_authorized": False,
            "pages_publication_authorized": False,
            "proves_model_ingestion": False,
        },
    }
    receipt_bytes = yaml.safe_dump(
        receipt, sort_keys=False, allow_unicode=True
    ).encode("utf-8")
    return archive, manifest_bytes, audit_bytes, archive_sha_bytes, receipt_bytes


def write_candidate(
    output_directory: Path,
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
    root: Path = ROOT,
) -> None:
    archive, manifest, audit, archive_sha, receipt = build_receipt(
        repository,
        source_commit,
        source_ref_kind,
        branch_name,
        root=root,
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / ARCHIVE_FILENAME).write_bytes(archive)
    (output_directory / SIDECAR_MANIFEST_FILENAME).write_bytes(manifest)
    (output_directory / SIDECAR_AUDIT_FILENAME).write_bytes(audit)
    (output_directory / f"{ARCHIVE_FILENAME}.sha256").write_bytes(archive_sha)
    (output_directory / RECEIPT_FILENAME).write_bytes(receipt)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a commit-bound MADP alpha.4 release candidate and receipt"
    )
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--source-ref-kind",
        required=True,
        choices=("PULL_REQUEST_HEAD", "MERGED_MAIN"),
    )
    parser.add_argument("--branch-name", required=True)
    args = parser.parse_args()
    verify_git_head(ROOT, args.source_commit)
    verify_git_sources(ROOT, args.source_commit)
    verify_repository_sources(ROOT, args.source_commit)
    write_candidate(
        args.output_directory,
        args.repository,
        args.source_commit,
        args.source_ref_kind,
        args.branch_name,
    )
    receipt = yaml.safe_load(
        (args.output_directory / RECEIPT_FILENAME).read_text(encoding="utf-8")
    )
    print(
        f"generated {receipt['artifact_name']} "
        f"status={receipt['status']} sha256={receipt['package_archive_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
