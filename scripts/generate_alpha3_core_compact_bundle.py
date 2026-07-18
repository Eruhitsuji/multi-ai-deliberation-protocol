#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_VERSION = "MADP-v0.3.0-alpha.3"
BUNDLE_VERSION = "MADP-CORE-COMPACT-BUNDLE-v1"
BUNDLE_FILENAME = "MADP-v0.3.0-alpha.3-core-compact.md"
MANIFEST_FILENAME = "MADP-v0.3.0-alpha.3-core-compact.manifest.yaml"

SOURCE_FILES: tuple[tuple[str, str], ...] = (
    ("protocol/MADP-v0.3.0-alpha.3.md", "PROTOCOL"),
    ("registries/v0.3.0-alpha.3/commands.yaml", "COMMAND_REGISTRY"),
    ("registries/v0.3.0-alpha.3/workflow-macros.yaml", "WORKFLOW_MACRO_REGISTRY"),
    ("docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md", "CORE_PROFILE"),
    ("docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md", "MACRO_PROFILE"),
    ("docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md", "BLIND_PROFILE"),
    ("bootstrap/alpha3/quick-start.md", "BOOTSTRAP"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory_digest(rows: list[dict]) -> str:
    material = "".join(
        f"{row['path']}\t{row['sha256']}\t{row['bytes']}\t{row['role']}\n"
        for row in rows
    ).encode("utf-8")
    return sha256(material)


def validate_inputs(repository: str, source_commit: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("repository must be owner/name")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source commit must be 40 lowercase hexadecimal characters")


def verify_git_head(root: Path, source_commit: str) -> None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("repository Git HEAD is unavailable for commit binding") from exc
    head = result.stdout.strip().lower()
    if head != source_commit:
        raise ValueError(f"source commit does not match checked-out Git HEAD: {head}")


def build_bundle(repository: str, source_commit: str, root: Path = ROOT) -> tuple[bytes, dict]:
    validate_inputs(repository, source_commit)
    rows: list[dict] = []
    source_blobs: list[tuple[dict, bytes]] = []
    for relative, role in SOURCE_FILES:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"compact bundle source missing: {relative}")
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"compact bundle source is not UTF-8: {relative}") from exc
        row = {
            "path": relative,
            "role": role,
            "sha256": sha256(data),
            "bytes": len(data),
        }
        rows.append(row)
        source_blobs.append((row, data))

    inv_digest = inventory_digest(rows)
    header = {
        "bundle_version": BUNDLE_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "repository": repository,
        "source_commit": source_commit,
        "profile": "MADP_CORE_CANDIDATE",
        "status": "EXPERIMENTAL_COMPACT_BUNDLE",
        "formal_release_evidence": False,
        "source_count": len(rows),
        "source_inventory_sha256": inv_digest,
    }
    parts: list[bytes] = []
    parts.append(b"---\n")
    parts.append(yaml.safe_dump(header, sort_keys=False, allow_unicode=True).encode("utf-8"))
    parts.append(b"---\n\n")
    parts.append(b"# MADP v0.3.0-alpha.3 Core Compact Bundle\n\n")
    parts.append(
        b"This single-file bundle is an experimental distribution artifact for the "
        b"MADP Core Candidate. It is not a PROTOCOL_LOAD_REPORT, validation receipt, "
        b"formal FIELD_TRIAL artifact, release authorization, or execution authorization.\n\n"
    )
    parts.append(
        b"The embedded source bytes remain bound to the repository commit and per-file "
        b"SHA-256 values recorded in the companion manifest.\n\n"
    )
    for index, (row, data) in enumerate(source_blobs, 1):
        marker = (
            f"<!-- MADP_SOURCE_BEGIN index={index} path={row['path']} "
            f"sha256={row['sha256']} bytes={row['bytes']} role={row['role']} -->\n"
        ).encode("utf-8")
        end_marker = f"\n<!-- MADP_SOURCE_END path={row['path']} -->\n\n".encode("utf-8")
        parts.extend([
            f"## Embedded source {index}: `{row['path']}`\n\n".encode("utf-8"),
            marker,
            data,
            end_marker,
        ])
    bundle = b"".join(parts)
    manifest = {
        "bundle_version": BUNDLE_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "repository": repository,
        "source_commit": source_commit,
        "profile": "MADP_CORE_CANDIDATE",
        "status": "EXPERIMENTAL_COMPACT_BUNDLE",
        "formal_release_evidence": False,
        "content_format": "MADP-COMPACT-BUNDLE-MD-v1",
        "bundle_file": BUNDLE_FILENAME,
        "bundle_sha256": sha256(bundle),
        "bundle_bytes": len(bundle),
        "source_count": len(rows),
        "source_inventory_sha256": inv_digest,
        "source_files": rows,
    }
    return bundle, manifest


def write_bundle(output_directory: Path, repository: str, source_commit: str, root: Path = ROOT) -> dict:
    bundle, manifest = build_bundle(repository, source_commit, root=root)
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / BUNDLE_FILENAME).write_bytes(bundle)
    (output_directory / MANIFEST_FILENAME).write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic alpha.3 Core compact bundle")
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    validate_inputs(args.repository, args.source_commit)
    verify_git_head(ROOT, args.source_commit)
    manifest = write_bundle(args.output_directory, args.repository, args.source_commit)
    print(
        f"generated {manifest['bundle_file']} "
        f"sha256={manifest['bundle_sha256']} sources={manifest['source_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
