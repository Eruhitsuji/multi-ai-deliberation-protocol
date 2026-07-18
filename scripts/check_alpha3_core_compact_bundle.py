#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import re
import sys
import yaml
from jsonschema import Draft202012Validator

from generate_alpha3_core_compact_bundle import (
    BUNDLE_FILENAME,
    BUNDLE_VERSION,
    MANIFEST_FILENAME,
    PROTOCOL_VERSION,
    SOURCE_FILES,
    inventory_digest,
    verify_git_head,
    verify_git_sources,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/v0.3.0-alpha.3/experimental/core-compact-bundle-manifest.schema.yaml"
BEGIN_RE = re.compile(
    rb"<!-- MADP_SOURCE_BEGIN index=(\d+) path=([^ ]+) sha256=([0-9a-f]{64}) bytes=(\d+) role=([A-Z_]+) -->\n"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_bundle_header(bundle: bytes) -> dict:
    if not bundle.startswith(b"---\n"):
        raise ValueError("bundle YAML frontmatter missing")
    end = bundle.find(b"---\n", 4)
    if end < 0:
        raise ValueError("bundle YAML frontmatter terminator missing")
    header = yaml.safe_load(bundle[4:end].decode("utf-8"))
    if not isinstance(header, dict):
        raise ValueError("bundle YAML frontmatter is not a mapping")
    return header


def parse_embedded_sources(bundle: bytes) -> list[dict]:
    rows: list[dict] = []
    position = 0
    while True:
        match = BEGIN_RE.search(bundle, position)
        if not match:
            break
        index = int(match.group(1))
        path = match.group(2).decode("utf-8")
        expected_sha = match.group(3).decode("ascii")
        length = int(match.group(4))
        role = match.group(5).decode("ascii")
        data_start = match.end()
        data_end = data_start + length
        if data_end > len(bundle):
            raise ValueError(f"embedded source exceeds bundle length: {path}")
        data = bundle[data_start:data_end]
        end_marker = f"\n<!-- MADP_SOURCE_END path={path} -->".encode("utf-8")
        if bundle[data_end:data_end + len(end_marker)] != end_marker:
            raise ValueError(f"embedded source end marker mismatch: {path}")
        rows.append({
            "index": index,
            "path": path,
            "role": role,
            "sha256": expected_sha,
            "bytes": length,
            "data": data,
        })
        position = data_end + len(end_marker)
    return rows


def check(directory: Path, expected_repository: str | None, expected_commit: str | None, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    manifest_path = directory / MANIFEST_FILENAME
    bundle_path = directory / BUNDLE_FILENAME
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"]
    if not bundle_path.is_file():
        return [f"missing bundle: {bundle_path}"]

    schema = load_yaml(SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    manifest = load_yaml(manifest_path)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        problems.append(f"manifest schema failure: {errors[0].message}")
        return problems

    if expected_repository and manifest.get("repository") != expected_repository:
        problems.append("repository binding mismatch")
    if expected_commit and manifest.get("source_commit") != expected_commit:
        problems.append("source commit binding mismatch")
    if manifest.get("bundle_version") != BUNDLE_VERSION or manifest.get("protocol_version") != PROTOCOL_VERSION:
        problems.append("bundle version binding mismatch")
    if manifest.get("formal_release_evidence") is not False:
        problems.append("compact bundle must remain non-release evidence")

    bundle = bundle_path.read_bytes()
    try:
        header = parse_bundle_header(bundle)
    except (ValueError, UnicodeDecodeError, yaml.YAMLError) as exc:
        problems.append(str(exc))
        header = {}
    expected_header = {
        "bundle_version": manifest.get("bundle_version"),
        "protocol_version": manifest.get("protocol_version"),
        "repository": manifest.get("repository"),
        "source_commit": manifest.get("source_commit"),
        "profile": manifest.get("profile"),
        "status": manifest.get("status"),
        "formal_release_evidence": manifest.get("formal_release_evidence"),
        "source_count": manifest.get("source_count"),
        "source_inventory_sha256": manifest.get("source_inventory_sha256"),
    }
    if header != expected_header:
        problems.append("bundle YAML frontmatter does not match manifest")
    if manifest.get("bundle_sha256") != sha256(bundle):
        problems.append("bundle SHA-256 mismatch")
    if manifest.get("bundle_bytes") != len(bundle):
        problems.append("bundle byte count mismatch")

    expected_rows: list[dict] = []
    for relative, role in SOURCE_FILES:
        source = root / relative
        if not source.is_file():
            problems.append(f"current source missing: {relative}")
            continue
        data = source.read_bytes()
        expected_rows.append({"path": relative, "role": role, "sha256": sha256(data), "bytes": len(data)})
    manifest_rows = manifest.get("source_files", [])
    if manifest_rows != expected_rows:
        problems.append("manifest source inventory does not match current source bytes")
    if manifest.get("source_count") != len(manifest_rows):
        problems.append("source count mismatch")
    paths = [row.get("path") for row in manifest_rows]
    if len(paths) != len(set(paths)):
        problems.append("duplicate source path")
    if manifest.get("source_inventory_sha256") != inventory_digest(manifest_rows):
        problems.append("source inventory digest mismatch")

    try:
        embedded = parse_embedded_sources(bundle)
    except ValueError as exc:
        problems.append(str(exc))
        embedded = []
    if len(embedded) != len(manifest_rows):
        problems.append("embedded source count mismatch")
    for expected_index, (embedded_row, manifest_row) in enumerate(zip(embedded, manifest_rows), 1):
        if embedded_row["index"] != expected_index:
            problems.append("embedded source index mismatch")
        for key in ("path", "role", "sha256", "bytes"):
            if embedded_row[key] != manifest_row[key]:
                problems.append(f"embedded source metadata mismatch: {manifest_row.get('path')}: {key}")
        if sha256(embedded_row["data"]) != manifest_row["sha256"]:
            problems.append(f"embedded source digest mismatch: {manifest_row.get('path')}")
        current_path = root / manifest_row["path"]
        if current_path.is_file() and embedded_row["data"] != current_path.read_bytes():
            problems.append(f"embedded source bytes differ from repository source: {manifest_row['path']}")

    text = bundle.decode("utf-8")
    for marker in (
        "not a PROTOCOL_LOAD_REPORT",
        "formal FIELD_TRIAL artifact",
        "not a PROTOCOL_LOAD_REPORT, validation receipt",
    ):
        if marker not in text:
            problems.append(f"bundle boundary marker missing: {marker}")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify deterministic alpha.3 Core compact bundle")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--repository")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    if args.source_commit:
        try:
            verify_git_head(ROOT, args.source_commit)
            verify_git_sources(ROOT, args.source_commit)
        except ValueError as exc:
            print(f"FAIL: {exc}", file=sys.stderr)
            return 1
    problems = check(args.directory, args.repository, args.source_commit)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print("alpha.3 Core compact bundle: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
