#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import io
import re
import sys
import zipfile

import yaml
from jsonschema import Draft202012Validator

from generate_alpha4_prerelease_package import (
    ARCHIVE_AUDIT_FILENAME,
    ARCHIVE_FILENAME,
    ARCHIVE_MANIFEST_FILENAME,
    ARCHIVE_ROOT,
    CHECKSUM_FILENAME,
    SIDECAR_AUDIT_FILENAME,
    SIDECAR_MANIFEST_FILENAME,
    ZIP_TIMESTAMP,
    build_package,
    sha256,
    verify_git_head,
    verify_git_sources,
    verify_repository_sources,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/v0.3.0-alpha.4/prerelease-package-manifest.schema.yaml"


def load_yaml_bytes(data: bytes):
    return yaml.safe_load(data.decode("utf-8"))


def archive_files(archive_bytes: bytes) -> tuple[dict[str, bytes], list[str]]:
    files: dict[str, bytes] = {}
    problems: list[str] = []
    with zipfile.ZipFile(io.BytesIO(archive_bytes), "r") as archive:
        for info in archive.infolist():
            prefix = f"{ARCHIVE_ROOT}/"
            if not info.filename.startswith(prefix):
                problems.append(f"archive entry outside root: {info.filename}")
                continue
            relative = info.filename[len(prefix):]
            if not relative or relative.startswith("/") or ".." in Path(relative).parts:
                problems.append(f"unsafe archive entry: {info.filename}")
                continue
            if relative in files:
                problems.append(f"duplicate archive entry: {relative}")
            if info.date_time != ZIP_TIMESTAMP:
                problems.append(f"non-deterministic ZIP timestamp: {relative}")
            if (info.external_attr >> 16) & 0o777 != 0o644:
                problems.append(f"unexpected ZIP permission: {relative}")
            files[relative] = archive.read(info)
    return files, problems


def check(directory: Path, repository: str, source_commit: str, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    archive_path = directory / ARCHIVE_FILENAME
    manifest_path = directory / SIDECAR_MANIFEST_FILENAME
    audit_path = directory / SIDECAR_AUDIT_FILENAME
    archive_sha_path = directory / f"{ARCHIVE_FILENAME}.sha256"
    for path in (archive_path, manifest_path, audit_path, archive_sha_path):
        if not path.is_file():
            problems.append(f"missing generated artifact: {path.name}")
    if problems:
        return problems

    observed_archive = archive_path.read_bytes()
    observed_manifest = manifest_path.read_bytes()
    observed_audit = audit_path.read_bytes()
    observed_archive_sha = archive_sha_path.read_bytes()

    try:
        expected_archive, expected_manifest, expected_audit, expected_archive_sha = build_package(
            repository, source_commit, root=root
        )
    except Exception as exc:
        return [f"canonical package regeneration failed: {exc}"]

    if observed_archive != expected_archive:
        problems.append("archive does not match canonical deterministic output")
    if observed_manifest != expected_manifest:
        problems.append("sidecar manifest does not match canonical output")
    if observed_audit != expected_audit:
        problems.append("sidecar integrity audit does not match canonical output")
    if observed_archive_sha != expected_archive_sha:
        problems.append("archive SHA-256 sidecar mismatch")

    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    manifest = load_yaml_bytes(observed_manifest)
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        problems.append(f"manifest schema failure: {errors[0].message}")
        return sorted(set(problems))

    if manifest.get("repository") != repository:
        problems.append("repository binding mismatch")
    if manifest.get("source_commit") != source_commit:
        problems.append("source commit binding mismatch")
    for key in ("formal_release_evidence", "stable_release_authorized", "publication_authorized"):
        if manifest.get(key) is not False:
            problems.append(f"authority boundary must remain false: {key}")

    files, zip_problems = archive_files(observed_archive)
    problems.extend(zip_problems)
    if files.get(ARCHIVE_MANIFEST_FILENAME) != observed_manifest:
        problems.append("embedded manifest differs from sidecar")
    if files.get(ARCHIVE_AUDIT_FILENAME) != observed_audit:
        problems.append("embedded integrity audit differs from sidecar")

    expected_payload = {row["path"]: row for row in manifest.get("files", [])}
    if manifest.get("payload_count") != len(expected_payload):
        problems.append("payload count mismatch")
    for relative, row in expected_payload.items():
        data = files.get(relative)
        if data is None:
            problems.append(f"manifest payload missing from archive: {relative}")
            continue
        if sha256(data) != row.get("sha256"):
            problems.append(f"manifest payload digest mismatch: {relative}")
        if len(data) != row.get("bytes"):
            problems.append(f"manifest payload byte count mismatch: {relative}")

    checksum_data = files.get(CHECKSUM_FILENAME)
    if checksum_data is None:
        problems.append("internal SHA256SUMS missing")
    else:
        lines = checksum_data.decode("utf-8").splitlines()
        recorded: dict[str, str] = {}
        for line in lines:
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                problems.append("invalid SHA256SUMS line")
                continue
            recorded[match.group(2)] = match.group(1)
        expected_checksum_paths = set(files) - {CHECKSUM_FILENAME}
        if set(recorded) != expected_checksum_paths:
            problems.append("SHA256SUMS path inventory mismatch")
        for relative in expected_checksum_paths:
            if recorded.get(relative) != sha256(files[relative]):
                problems.append(f"SHA256SUMS digest mismatch: {relative}")

    audit = load_yaml_bytes(observed_audit)
    if audit.get("status") != "PASS":
        problems.append("integrity audit status is not PASS")
    if audit.get("source_commit") != source_commit or audit.get("repository") != repository:
        problems.append("integrity audit provenance mismatch")
    for key, value in audit.get("boundaries", {}).items():
        if value is not False:
            problems.append(f"integrity audit boundary must remain false: {key}")
    for key, value in audit.get("checks", {}).items():
        if value != "PASS":
            problems.append(f"integrity audit check is not PASS: {key}")

    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])")
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for relative, data in files.items():
        if not relative.endswith((".md", ".yaml", ".txt", "LICENSE")):
            continue
        text = data.decode("utf-8")
        if exact_private.search(text):
            problems.append(f"private identifier found in package: {relative}")
        if email.search(text):
            problems.append(f"email address found in package: {relative}")
        if "human-final-authority-input-raw.md" in text:
            problems.append(f"removed private raw path found in package: {relative}")

    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic MADP alpha.4 prerelease package")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        verify_git_head(ROOT, args.source_commit)
        verify_git_sources(ROOT, args.source_commit)
        verify_repository_sources(ROOT, args.source_commit)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    problems = check(args.directory, args.repository, args.source_commit)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print("MADP v0.3.0-alpha.4 prerelease package: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
