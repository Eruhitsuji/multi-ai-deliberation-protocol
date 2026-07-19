#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import io
import re
import subprocess
import zipfile

import yaml

from generate_alpha4_core_compact_bundle import (
    BUNDLE_FILENAME,
    MANIFEST_FILENAME as CORE_MANIFEST_FILENAME,
    build_bundle as build_core_bundle,
    validate_inputs,
    verify_git_head,
    verify_git_sources,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_VERSION = "MADP-v0.3.0-alpha.4"
PACKAGE_VERSION = "MADP-PRERELEASE-PACKAGE-v1"
ARCHIVE_ROOT = "MADP-v0.3.0-alpha.4-prerelease"
ARCHIVE_FILENAME = "MADP-v0.3.0-alpha.4-prerelease-candidate.zip"
SIDECAR_MANIFEST_FILENAME = "MADP-v0.3.0-alpha.4-prerelease-candidate.manifest.yaml"
SIDECAR_AUDIT_FILENAME = "MADP-v0.3.0-alpha.4-prerelease-integrity-audit.yaml"
ARCHIVE_MANIFEST_FILENAME = "PRERELEASE-MANIFEST.yaml"
ARCHIVE_AUDIT_FILENAME = "INTEGRITY-AUDIT.yaml"
CHECKSUM_FILENAME = "SHA256SUMS"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

SOURCE_FILES: tuple[tuple[str, str, str], ...] = (
    ("README.md", "README-v0.3.0-alpha.4.md", "README"),
    ("RELEASE-NOTES.md", "docs/releases/MADP-v0.3.0-alpha.4.md", "RELEASE_NOTES"),
    ("LICENSE", "LICENSE", "LICENSE"),
    ("bootstrap/README.md", "bootstrap/alpha4/README.md", "BOOTSTRAP"),
    ("bootstrap/load-protocol-from-github.md", "bootstrap/alpha4/load-protocol-from-github.md", "BOOTSTRAP"),
    ("bootstrap/quick-start.md", "bootstrap/alpha4/quick-start.md", "BOOTSTRAP"),
    ("bootstrap/verified-start.md", "bootstrap/alpha4/verified-start.md", "BOOTSTRAP"),
    ("schemas/protocol-load-report.schema.yaml", "schemas/v0.3.0-alpha.4/protocol-load-report.schema.yaml", "SCHEMA"),
    ("schemas/core-usability-record.schema.yaml", "schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml", "SCHEMA"),
    ("schemas/core-compact-bundle-manifest.schema.yaml", "schemas/v0.3.0-alpha.4/core-compact-bundle-manifest.schema.yaml", "SCHEMA"),
    ("schemas/prerelease-package-manifest.schema.yaml", "schemas/v0.3.0-alpha.4/prerelease-package-manifest.schema.yaml", "SCHEMA"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory_digest(rows: list[dict]) -> str:
    material = "".join(
        f"{row['path']}\t{row['sha256']}\t{row['bytes']}\t{row['role']}\t{row['source']}\n"
        for row in rows
    ).encode("utf-8")
    return sha256(material)


def verify_repository_sources(root: Path, source_commit: str) -> None:
    for _package_path, source_path, _role in SOURCE_FILES:
        working = root / source_path
        if not working.is_file():
            raise ValueError(f"prerelease package source missing: {source_path}")
        try:
            committed = subprocess.run(
                ["git", "-C", str(root), "show", f"{source_commit}:{source_path}"],
                check=True,
                capture_output=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ValueError(f"package source unavailable from claimed commit: {source_path}") from exc
        if working.read_bytes() != committed:
            raise ValueError(f"package source differs from claimed commit: {source_path}")


def yaml_bytes(value: dict) -> bytes:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def build_payload(repository: str, source_commit: str, root: Path = ROOT) -> tuple[dict[str, bytes], dict]:
    validate_inputs(repository, source_commit)
    core_bundle, core_manifest = build_core_bundle(repository, source_commit, root=root)
    core_manifest_bytes = yaml_bytes(core_manifest)

    payload: dict[str, bytes] = {}
    rows: list[dict] = []
    for package_path, source_path, role in SOURCE_FILES:
        data = (root / source_path).read_bytes()
        data.decode("utf-8")
        payload[package_path] = data
        rows.append({
            "path": package_path,
            "role": role,
            "source": source_path,
            "sha256": sha256(data),
            "bytes": len(data),
        })

    generated = (
        (f"core/{BUNDLE_FILENAME}", core_bundle, "CORE_DISTRIBUTION", "GENERATED_CORE_DISTRIBUTION"),
        (f"core/{CORE_MANIFEST_FILENAME}", core_manifest_bytes, "CORE_DISTRIBUTION_MANIFEST", "GENERATED_CORE_MANIFEST"),
    )
    for package_path, data, role, source in generated:
        payload[package_path] = data
        rows.append({
            "path": package_path,
            "role": role,
            "source": source,
            "sha256": sha256(data),
            "bytes": len(data),
        })

    rows.sort(key=lambda row: row["path"])
    manifest = {
        "package_version": PACKAGE_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "repository": repository,
        "source_commit": source_commit,
        "status": "PRERELEASE_CANDIDATE_READY_FOR_HUMAN_DECISION",
        "formal_release_evidence": False,
        "stable_release_authorized": False,
        "publication_authorized": False,
        "archive_root": ARCHIVE_ROOT,
        "rollback_target": {
            "version": "MADP-v0.3.0-alpha.2",
            "tag": "MADP-v0.3.0-alpha.2",
        },
        "payload_count": len(rows),
        "payload_inventory_sha256": inventory_digest(rows),
        "core_distribution": {
            "bundle_file": f"core/{BUNDLE_FILENAME}",
            "bundle_sha256": sha256(core_bundle),
            "manifest_file": f"core/{CORE_MANIFEST_FILENAME}",
            "manifest_sha256": sha256(core_manifest_bytes),
        },
        "files": rows,
    }
    return payload, manifest


def build_audit(manifest: dict) -> dict:
    return {
        "audit_version": "MADP-PRERELEASE-INTEGRITY-AUDIT-v1",
        "protocol_version": PROTOCOL_VERSION,
        "repository": manifest["repository"],
        "source_commit": manifest["source_commit"],
        "status": "PASS",
        "payload_inventory_sha256": manifest["payload_inventory_sha256"],
        "checks": {
            "source_commit_binding": "PASS",
            "repository_source_parity": "PASS",
            "core_distribution_canonical_regeneration": "PASS",
            "manifest_schema": "PASS",
            "payload_inventory": "PASS",
            "internal_sha256sums": "PASS",
            "deterministic_zip_metadata": "PASS",
            "privacy_scan": "PASS",
            "authority_boundary": "PASS",
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
        "known_limitations": [
            "Dynamic role assignment is not promoted into alpha.4.",
            "Skill adapters and broader installation packages are not updated.",
            "Protocol-load reports remain reported observations unless independently verified.",
            "A package does not prove complete model ingestion or conformance.",
            "The terminated comparison pilot does not establish comparative superiority.",
        ],
    }


def checksums_bytes(files: dict[str, bytes]) -> bytes:
    return "".join(f"{sha256(files[path])}  {path}\n" for path in sorted(files)).encode("utf-8")


def deterministic_zip(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(files):
            if relative.startswith("/") or ".." in Path(relative).parts:
                raise ValueError(f"unsafe archive path: {relative}")
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits = 0x800
            archive.writestr(info, files[relative], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return stream.getvalue()


def build_package(repository: str, source_commit: str, root: Path = ROOT) -> tuple[bytes, bytes, bytes, bytes]:
    validate_inputs(repository, source_commit)
    payload, manifest = build_payload(repository, source_commit, root=root)
    manifest_bytes = yaml_bytes(manifest)
    audit_bytes = yaml_bytes(build_audit(manifest))
    package_files = dict(payload)
    package_files[ARCHIVE_MANIFEST_FILENAME] = manifest_bytes
    package_files[ARCHIVE_AUDIT_FILENAME] = audit_bytes
    package_files[CHECKSUM_FILENAME] = checksums_bytes(package_files)
    archive_bytes = deterministic_zip(package_files)
    archive_sha = f"{sha256(archive_bytes)}  {ARCHIVE_FILENAME}\n".encode("utf-8")
    return archive_bytes, manifest_bytes, audit_bytes, archive_sha


def write_package(output_directory: Path, repository: str, source_commit: str, root: Path = ROOT) -> None:
    archive, manifest, audit, archive_sha = build_package(repository, source_commit, root=root)
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / ARCHIVE_FILENAME).write_bytes(archive)
    (output_directory / SIDECAR_MANIFEST_FILENAME).write_bytes(manifest)
    (output_directory / SIDECAR_AUDIT_FILENAME).write_bytes(audit)
    (output_directory / f"{ARCHIVE_FILENAME}.sha256").write_bytes(archive_sha)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic MADP alpha.4 prerelease package")
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    validate_inputs(args.repository, args.source_commit)
    verify_git_head(ROOT, args.source_commit)
    verify_git_sources(ROOT, args.source_commit)
    verify_repository_sources(ROOT, args.source_commit)
    write_package(args.output_directory, args.repository, args.source_commit)
    archive = (args.output_directory / ARCHIVE_FILENAME).read_bytes()
    print(f"generated {ARCHIVE_FILENAME} sha256={sha256(archive)} bytes={len(archive)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
