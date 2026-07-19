#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_VERSION = "MADP-v0.3.0-alpha.4"
COMPATIBILITY_BASE = "MADP-v0.3.0-alpha.3"
BUNDLE_VERSION = "MADP-CORE-DISTRIBUTION-BUNDLE-v1"
BUNDLE_FILENAME = "MADP-v0.3.0-alpha.4-core-distribution.md"
MANIFEST_FILENAME = "MADP-v0.3.0-alpha.4-core-distribution.manifest.yaml"
LOADER_PATH = "bootstrap/alpha4/load-protocol-from-github.md"

SOURCE_FILES: tuple[tuple[str, str], ...] = (
    ("README-v0.3.0-alpha.4.md", "ALPHA4_README"),
    ("protocol/MADP-v0.3.0-alpha.3.md", "BASE_PROTOCOL"),
    ("protocol/GLOSSARY-v0.3.0-alpha.3.md", "BASE_GLOSSARY"),
    ("registries/v0.3.0-alpha.3/commands.yaml", "COMMAND_REGISTRY"),
    ("schemas/v0.3.0-alpha.3/deliberation.schema.yaml", "BASE_DELIBERATION_SCHEMA"),
    ("protocol/MADP-v0.3.0-alpha.4-core-usability.md", "ALPHA4_EXTENSION"),
    ("docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md", "WORKFLOW_MACRO_PROFILE"),
    ("registries/v0.3.0-alpha.4/workflow-macros.yaml", "WORKFLOW_MACRO_REGISTRY"),
    ("schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml", "CORE_USABILITY_SCHEMA"),
    ("schemas/v0.3.0-alpha.4/protocol-load-report.schema.yaml", "PROTOCOL_LOAD_REPORT_SCHEMA"),
    (LOADER_PATH, "PROTOCOL_LOADER"),
    ("bootstrap/alpha4/quick-start.md", "QUICK_START"),
    ("bootstrap/alpha4/verified-start.md", "VERIFIED_START"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory_digest(rows: list[dict]) -> str:
    material = "".join(
        f"{row['path']}\t{row['sha256']}\t{row['bytes']}\t{row['role']}\n"
        for row in rows
    ).encode("utf-8")
    return sha256(material)


def path_inventory_digest(paths: list[str]) -> str:
    return sha256("".join(f"{path}\n" for path in paths).encode("utf-8"))


def parse_frontmatter(data: bytes) -> dict:
    if not data.startswith(b"---\n"):
        raise ValueError("YAML frontmatter missing")
    end = data.find(b"\n---\n", 4)
    if end < 0:
        raise ValueError("YAML frontmatter terminator missing")
    value = yaml.safe_load(data[4:end].decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("YAML frontmatter is not a mapping")
    return value


def selected_loader_paths(loader: dict, profile: str) -> list[str]:
    profiles = loader.get("load_profiles", {})
    source_sets = loader.get("source_sets", {})
    definition = profiles.get(profile)
    if not isinstance(definition, dict):
        raise ValueError(f"loader profile missing: {profile}")
    result: list[str] = []
    for set_name in definition.get("required_sets", []):
        paths = source_sets.get(set_name)
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            raise ValueError(f"loader source set invalid: {set_name}")
        result.extend(paths)
    if len(result) != len(set(result)):
        raise ValueError(f"loader profile contains duplicate paths: {profile}")
    return result


def loader_metadata(root: Path = ROOT) -> tuple[str, dict[str, str]]:
    path = root / LOADER_PATH
    if not path.is_file():
        raise FileNotFoundError(f"loader missing: {LOADER_PATH}")
    data = path.read_bytes()
    loader = parse_frontmatter(data)
    if loader.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("loader protocol version mismatch")
    if loader.get("report_version") != "MADP-PROTOCOL-LOAD-REPORT-v3":
        raise ValueError("loader report version mismatch")
    if loader.get("inventory_digest_algorithm") != "sha256-newline-paths-v1":
        raise ValueError("loader inventory digest algorithm mismatch")
    digests: dict[str, str] = {}
    for profile in ("QUICK", "VERIFIED"):
        paths = selected_loader_paths(loader, profile)
        observed = path_inventory_digest(paths)
        recorded = loader.get("source_inventory_digests", {}).get(profile)
        if recorded != observed:
            raise ValueError(f"loader inventory digest mismatch: {profile}")
        digests[profile] = observed
    quick = set(selected_loader_paths(loader, "QUICK"))
    verified = set(selected_loader_paths(loader, "VERIFIED"))
    if not quick < verified:
        raise ValueError("VERIFIED loader inventory must strictly include QUICK")
    bundled = {path for path, _role in SOURCE_FILES}
    if not verified.issubset(bundled):
        missing = sorted(verified - bundled)
        raise ValueError(f"bundle omits VERIFIED loader sources: {missing}")
    return sha256(data), digests


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


def verify_git_sources(root: Path, source_commit: str) -> None:
    for relative, _role in SOURCE_FILES:
        working_path = root / relative
        if not working_path.is_file():
            raise ValueError(f"commit-bound source missing from working tree: {relative}")
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "show", f"{source_commit}:{relative}"],
                check=True,
                capture_output=True,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ValueError(f"source unavailable from claimed commit: {relative}") from exc
        if working_path.read_bytes() != result.stdout:
            raise ValueError(f"working-tree source differs from claimed commit: {relative}")


def build_bundle(
    repository: str,
    source_commit: str,
    root: Path = ROOT,
) -> tuple[bytes, dict]:
    validate_inputs(repository, source_commit)
    loader_sha, loader_digests = loader_metadata(root)
    rows: list[dict] = []
    source_blobs: list[tuple[dict, bytes]] = []
    for relative, role in SOURCE_FILES:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"distribution source missing: {relative}")
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"distribution source is not UTF-8: {relative}") from exc
        row = {
            "path": relative,
            "role": role,
            "sha256": sha256(data),
            "bytes": len(data),
        }
        rows.append(row)
        source_blobs.append((row, data))

    source_inventory = inventory_digest(rows)
    header = {
        "bundle_version": BUNDLE_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "compatibility_base": COMPATIBILITY_BASE,
        "repository": repository,
        "source_commit": source_commit,
        "status": "PRERELEASE_DISTRIBUTION_CANDIDATE",
        "formal_release_evidence": False,
        "proves_model_ingestion": False,
        "external_action_authorization": False,
        "supported_load_profiles": ["QUICK", "VERIFIED"],
        "source_count": len(rows),
        "source_inventory_sha256": source_inventory,
    }

    parts: list[bytes] = [
        b"---\n",
        yaml.safe_dump(header, sort_keys=False, allow_unicode=True).encode("utf-8"),
        b"---\n\n",
        b"# MADP v0.3.0-alpha.4 Core Distribution Bundle\n\n",
        (
            b"This deterministic single-file artifact packages the alpha.3 compatibility "
            b"baseline and the alpha.4 Core Usability extension. It is not a "
            b"PROTOCOL_LOAD_REPORT, does not prove model ingestion, is not formal "
            b"FIELD_TRIAL or release evidence, and grants no external-action authority.\n\n"
        ),
        (
            b"Use bootstrap/alpha4/load-protocol-from-github.md and produce an active "
            b"MADP-PROTOCOL-LOAD-REPORT-v3 before applying a start profile.\n\n"
        ),
    ]
    for index, (row, data) in enumerate(source_blobs, 1):
        marker = (
            f"<!-- MADP_SOURCE_BEGIN index={index} path={row['path']} "
            f"sha256={row['sha256']} bytes={row['bytes']} role={row['role']} -->\n"
        ).encode("utf-8")
        end_marker = f"\n<!-- MADP_SOURCE_END path={row['path']} -->\n\n".encode("utf-8")
        parts.extend(
            [
                f"## Embedded source {index}: `{row['path']}`\n\n".encode("utf-8"),
                marker,
                data,
                end_marker,
            ]
        )
    bundle = b"".join(parts)
    manifest = {
        "bundle_version": BUNDLE_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "compatibility_base": COMPATIBILITY_BASE,
        "repository": repository,
        "source_commit": source_commit,
        "status": "PRERELEASE_DISTRIBUTION_CANDIDATE",
        "formal_release_evidence": False,
        "proves_model_ingestion": False,
        "external_action_authorization": False,
        "content_format": "MADP-COMPACT-BUNDLE-MD-v2",
        "bundle_file": BUNDLE_FILENAME,
        "bundle_sha256": sha256(bundle),
        "bundle_bytes": len(bundle),
        "supported_load_profiles": ["QUICK", "VERIFIED"],
        "loader_path": LOADER_PATH,
        "loader_sha256": loader_sha,
        "loader_inventory_digests": loader_digests,
        "source_count": len(rows),
        "source_inventory_sha256": source_inventory,
        "source_files": rows,
    }
    return bundle, manifest


def write_bundle(
    output_directory: Path,
    repository: str,
    source_commit: str,
    root: Path = ROOT,
) -> dict:
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
    parser = argparse.ArgumentParser(
        description="Generate deterministic MADP alpha.4 Core distribution bundle"
    )
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    validate_inputs(args.repository, args.source_commit)
    verify_git_head(ROOT, args.source_commit)
    verify_git_sources(ROOT, args.source_commit)
    manifest = write_bundle(args.output_directory, args.repository, args.source_commit)
    print(
        f"generated {manifest['bundle_file']} "
        f"sha256={manifest['bundle_sha256']} sources={manifest['source_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
