#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import io
import sys
import tempfile
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_alpha4_prerelease_package import archive_files, check
from generate_alpha4_prerelease_package import (
    ARCHIVE_FILENAME,
    ARCHIVE_MANIFEST_FILENAME,
    CHECKSUM_FILENAME,
    SIDECAR_MANIFEST_FILENAME,
    deterministic_zip,
    write_package,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def replace_archive(directory: Path, files: dict[str, bytes]) -> None:
    (directory / ARCHIVE_FILENAME).write_bytes(deterministic_zip(files))


def main() -> int:
    parser = argparse.ArgumentParser(description="Test alpha.4 prerelease package generation")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        first = base / "first"
        second = base / "second"
        write_package(first, args.repository, args.source_commit, root=ROOT)
        write_package(second, args.repository, args.source_commit, root=ROOT)

        first_files = {path.name: path.read_bytes() for path in first.iterdir()}
        second_files = {path.name: path.read_bytes() for path in second.iterdir()}
        require(first_files == second_files, "two package generations differ")
        require(not check(first, args.repository, args.source_commit, root=ROOT), "canonical package failed validation")

        archive_bytes = (first / ARCHIVE_FILENAME).read_bytes()
        files, problems = archive_files(archive_bytes)
        require(not problems, f"canonical archive metadata failed: {problems}")

        tampered_manifest_dir = base / "tampered-manifest"
        write_package(tampered_manifest_dir, args.repository, args.source_commit, root=ROOT)
        manifest = yaml.safe_load((tampered_manifest_dir / SIDECAR_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        manifest["publication_authorized"] = True
        (tampered_manifest_dir / SIDECAR_MANIFEST_FILENAME).write_text(
            yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8", newline="\n"
        )
        observed = check(tampered_manifest_dir, args.repository, args.source_commit, root=ROOT)
        require(observed, "publication-authority tampering was accepted")

        tampered_internal_dir = base / "tampered-internal"
        write_package(tampered_internal_dir, args.repository, args.source_commit, root=ROOT)
        internal_files, _ = archive_files((tampered_internal_dir / ARCHIVE_FILENAME).read_bytes())
        embedded_manifest = yaml.safe_load(internal_files[ARCHIVE_MANIFEST_FILENAME].decode("utf-8"))
        embedded_manifest["stable_release_authorized"] = True
        internal_files[ARCHIVE_MANIFEST_FILENAME] = yaml.safe_dump(
            embedded_manifest, sort_keys=False
        ).encode("utf-8")
        replace_archive(tampered_internal_dir, internal_files)
        observed = check(tampered_internal_dir, args.repository, args.source_commit, root=ROOT)
        require(observed, "embedded authority tampering was accepted")

        tampered_checksum_dir = base / "tampered-checksum"
        write_package(tampered_checksum_dir, args.repository, args.source_commit, root=ROOT)
        checksum_files, _ = archive_files((tampered_checksum_dir / ARCHIVE_FILENAME).read_bytes())
        checksum_files[CHECKSUM_FILENAME] = b"0" * 64 + b"  README.md\n"
        replace_archive(tampered_checksum_dir, checksum_files)
        observed = check(tampered_checksum_dir, args.repository, args.source_commit, root=ROOT)
        require(any("SHA256SUMS" in item for item in observed), "checksum tampering was not detected")

        extra_file_dir = base / "extra-file"
        write_package(extra_file_dir, args.repository, args.source_commit, root=ROOT)
        extra_files, _ = archive_files((extra_file_dir / ARCHIVE_FILENAME).read_bytes())
        extra_files["UNDECLARED.txt"] = b"undeclared\n"
        replace_archive(extra_file_dir, extra_files)
        observed = check(extra_file_dir, args.repository, args.source_commit, root=ROOT)
        require(observed, "undeclared archive content was accepted")

    print("alpha.4 prerelease package regression tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
