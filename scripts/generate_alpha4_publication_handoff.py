#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse

import yaml

from generate_alpha4_prerelease_package import (
    ARCHIVE_FILENAME,
    SIDECAR_AUDIT_FILENAME,
    SIDECAR_MANIFEST_FILENAME,
    sha256,
    verify_git_head,
    verify_git_sources,
    verify_repository_sources,
)
from generate_alpha4_release_candidate import RECEIPT_FILENAME, build_receipt

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_FILENAME = "MADP-v0.3.0-alpha.4-publication-handoff.yaml"
CHECKLIST_FILENAME = "MADP-v0.3.0-alpha.4-publication-checklist.md"
RELEASE_NOTES_RELATIVE = "docs/releases/MADP-v0.3.0-alpha.4.md"
TARGET_TAG = "MADP-v0.3.0-alpha.4"


def build_handoff(
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
    target_tag: str,
    root: Path = ROOT,
) -> tuple[dict[str, bytes], bytes]:
    if target_tag != TARGET_TAG:
        raise ValueError(f"target tag must be {TARGET_TAG}")
    archive, manifest, audit, archive_sha, receipt = build_receipt(
        repository,
        source_commit,
        source_ref_kind,
        branch_name,
        root=root,
    )
    release_notes = (root / RELEASE_NOTES_RELATIVE).read_bytes()
    handoff = {
        "handoff_version": "MADP-PRERELEASE-PUBLICATION-HANDOFF-v1",
        "protocol_version": "MADP-v0.3.0-alpha.4",
        "repository": repository,
        "source_commit": source_commit,
        "source_ref_kind": source_ref_kind,
        "branch_name": branch_name,
        "target_tag": target_tag,
        "release_mode": "PRERELEASE",
        "candidate": {
            "archive_file": ARCHIVE_FILENAME,
            "archive_sha256": sha256(archive),
            "manifest_file": SIDECAR_MANIFEST_FILENAME,
            "manifest_sha256": sha256(manifest),
            "audit_file": SIDECAR_AUDIT_FILENAME,
            "audit_sha256": sha256(audit),
            "receipt_file": RECEIPT_FILENAME,
            "receipt_sha256": sha256(receipt),
            "release_notes_file": RELEASE_NOTES_RELATIVE,
            "release_notes_sha256": sha256(release_notes),
        },
        "rollback_target": {
            "version": "MADP-v0.3.0-alpha.2",
            "tag": "MADP-v0.3.0-alpha.2",
        },
        "required_human_actions": {
            "authorize_tag": False,
            "authorize_github_release": False,
            "confirm_prerelease": False,
            "inspect_known_limitations": False,
        },
        "boundaries": {
            "tag_created": False,
            "github_release_created": False,
            "pages_published": False,
            "stable_release_authorized": False,
            "formal_release_evidence": False,
            "proves_model_ingestion": False,
        },
    }
    handoff_bytes = yaml.safe_dump(
        handoff, sort_keys=False, allow_unicode=True
    ).encode("utf-8")
    checklist = f"""# MADP v0.3.0-alpha.4 publication checklist

This is a read-only handoff. It does not authorize or perform publication.

- [ ] Confirm source commit: `{source_commit}`
- [ ] Confirm source classification: `{source_ref_kind}` on `{branch_name}`
- [ ] Confirm target tag: `{target_tag}`
- [ ] Inspect `{RELEASE_NOTES_RELATIVE}` and all known limitations
- [ ] Verify `{ARCHIVE_FILENAME}` SHA-256: `{sha256(archive)}`
- [ ] Verify release-candidate receipt and integrity audit
- [ ] Confirm rollback target: `MADP-v0.3.0-alpha.2`
- [ ] Explicitly authorize tag creation
- [ ] Explicitly authorize GitHub Prerelease creation
- [ ] Keep Pages publication, stable release, and formal release evidence separate
""".encode("utf-8")
    files = {
        ARCHIVE_FILENAME: archive,
        SIDECAR_MANIFEST_FILENAME: manifest,
        SIDECAR_AUDIT_FILENAME: audit,
        f"{ARCHIVE_FILENAME}.sha256": archive_sha,
        RECEIPT_FILENAME: receipt,
        HANDOFF_FILENAME: handoff_bytes,
        CHECKLIST_FILENAME: checklist,
    }
    return files, handoff_bytes


def write_handoff(
    output_directory: Path,
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
    target_tag: str,
    root: Path = ROOT,
) -> None:
    files, _handoff = build_handoff(
        repository,
        source_commit,
        source_ref_kind,
        branch_name,
        target_tag,
        root=root,
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (output_directory / name).write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a read-only MADP alpha.4 publication handoff"
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
    parser.add_argument("--target-tag", default=TARGET_TAG)
    args = parser.parse_args()
    verify_git_head(ROOT, args.source_commit)
    verify_git_sources(ROOT, args.source_commit)
    verify_repository_sources(ROOT, args.source_commit)
    write_handoff(
        args.output_directory,
        args.repository,
        args.source_commit,
        args.source_ref_kind,
        args.branch_name,
        args.target_tag,
    )
    handoff = yaml.safe_load(
        (args.output_directory / HANDOFF_FILENAME).read_text(encoding="utf-8")
    )
    print(
        f"generated {HANDOFF_FILENAME} target={handoff['target_tag']} "
        f"source={handoff['source_commit']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
