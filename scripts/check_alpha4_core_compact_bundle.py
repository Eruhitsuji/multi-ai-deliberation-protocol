#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import re
import sys
import yaml
from jsonschema import Draft202012Validator

from generate_alpha4_core_compact_bundle import (
    BUNDLE_FILENAME,
    BUNDLE_VERSION,
    COMPATIBILITY_BASE,
    LOADER_PATH,
    MANIFEST_FILENAME,
    PROTOCOL_VERSION,
    SOURCE_FILES,
    build_bundle,
    inventory_digest,
    loader_metadata,
    parse_frontmatter,
    path_inventory_digest,
    selected_loader_paths,
    verify_git_head,
    verify_git_sources,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = ROOT / "schemas/v0.3.0-alpha.4/core-compact-bundle-manifest.schema.yaml"
BEGIN_RE = re.compile(
    rb"<!-- MADP_SOURCE_BEGIN index=(\d+) path=([^ ]+) sha256=([0-9a-f]{64}) bytes=(\d+) role=([A-Z0-9_]+) -->\n"
)
PUBLIC_ALPHA4_ARTIFACTS = (
    "README-v0.3.0-alpha.4.md",
    "protocol/MADP-v0.3.0-alpha.4-core-usability.md",
    "docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md",
    "docs/profiles/COMPACT_CORE_BUNDLE-v0.3.0-alpha.4.md",
    "registries/v0.3.0-alpha.4/workflow-macros.yaml",
    "schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml",
    "schemas/v0.3.0-alpha.4/protocol-load-report.schema.yaml",
    "schemas/v0.3.0-alpha.4/core-compact-bundle-manifest.schema.yaml",
    "bootstrap/alpha4/README.md",
    "bootstrap/alpha4/load-protocol-from-github.md",
    "bootstrap/alpha4/quick-start.md",
    "bootstrap/alpha4/verified-start.md",
    "docs/planning/DEC-MADP-ALPHA4-003.yaml",
    "docs/planning/MADP-v0.3.0-alpha.4-distribution-status.yaml",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_loader(root: Path = ROOT) -> dict:
    return parse_frontmatter((root / LOADER_PATH).read_bytes())


def parse_bundle_header(bundle: bytes) -> dict:
    return parse_frontmatter(bundle)


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
        rows.append(
            {
                "index": index,
                "path": path,
                "role": role,
                "sha256": expected_sha,
                "bytes": length,
                "data": data,
            }
        )
        position = data_end + len(end_marker)
    return rows


def load_report_problems(report: dict, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    schema = load_yaml(root / "schemas/v0.3.0-alpha.4/protocol-load-report.schema.yaml")
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda e: list(e.path))
    if errors:
        return [f"load report schema failure: {errors[0].message}"]

    loader = load_loader(root)
    profile = report["load_profile"]
    paths = selected_loader_paths(loader, profile)
    recorded_digest = loader["source_inventory_digests"][profile]
    expected_digest = path_inventory_digest(paths)
    if recorded_digest != expected_digest:
        problems.append("loader recorded inventory digest mismatch")
    if report["source_inventory_digest"] != expected_digest:
        problems.append("load report inventory digest mismatch")

    report_paths = [row["path"] for row in report["files"]]
    if report_paths != paths:
        problems.append("load report file inventory or order mismatch")
    if len(report_paths) != len(set(report_paths)):
        problems.append("load report contains duplicate source paths")

    profile_paths = [row["path"] for row in report["authorized_start_profiles"]]
    expected_profiles = loader["load_profiles"][profile]["authorized_start_profiles"]
    if profile_paths != expected_profiles:
        problems.append("authorized start profile inventory mismatch")

    for row in report["authorized_start_profiles"]:
        if row["repository"] != report["repository"]:
            problems.append("authorized profile repository mismatch")
        if row["repository_commit"] != report["repository_commit"]:
            problems.append("authorized profile commit mismatch")

    provenance_rank = {"SELF_ATTESTED": 0, "SOURCE_REFERENCED": 1, "HASH_VERIFIED": 2}
    minimum = loader["load_profiles"][profile]["minimum_provenance"]
    if provenance_rank[report["provenance_level"]] < provenance_rank[minimum]:
        problems.append("load report provenance below profile minimum")

    complete = report["status"] == "COMPLETE"
    if complete:
        if not report["active"]:
            problems.append("complete load report must be active")
        if report["supersedes"] is not None and report["supersedes"] >= report["revision"]:
            problems.append("superseded revision must be older")
        if not report["all_required_files_read"]:
            problems.append("complete load report must mark all required files read")
        if any(row["status"] != "READ" for row in report["files"]):
            problems.append("complete load report contains unread source")
        if report["next_action"]["command"] != "APPLY_START_PROFILE":
            problems.append("complete load report must apply a start profile")
    elif report["next_action"]["command"] != "RECOVER_PROTOCOL_SOURCE":
        problems.append("incomplete load report must recover sources")

    if profile == "QUICK":
        if report["schema_validation_executed"] and report["schema_validation_capability"] != "EXECUTED":
            problems.append("executed QUICK validation must report EXECUTED capability")
    else:
        if report["schema_validation_capability"] != "EXECUTED":
            problems.append("VERIFIED requires executed schema validation")
        if report["schema_validation_executed"] is not True:
            problems.append("VERIFIED requires schema_validation_executed")
        if report["provenance_level"] != "HASH_VERIFIED":
            problems.append("VERIFIED requires HASH_VERIFIED provenance")
        if any(row["content_sha256"] is None for row in report["files"]):
            problems.append("VERIFIED requires every source hash")
        if any(row["content_sha256"] is None for row in report["authorized_start_profiles"]):
            problems.append("VERIFIED requires every profile hash")

    binding = report.get("bundle_binding")
    if binding is not None:
        if binding["repository"] != report["repository"]:
            problems.append("bundle binding repository mismatch")
        if binding["source_commit"] != report["repository_commit"]:
            problems.append("bundle binding commit mismatch")
        if not all(row["access_method"] == "COMPLETE_BUNDLE" for row in report["files"]):
            problems.append("bundle-bound report must use COMPLETE_BUNDLE for all files")

    return sorted(set(problems))


def check(directory: Path, expected_repository: str | None, expected_commit: str | None, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    manifest_path = directory / MANIFEST_FILENAME
    bundle_path = directory / BUNDLE_FILENAME
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path}"]
    if not bundle_path.is_file():
        return [f"missing bundle: {bundle_path}"]

    schema = load_yaml(MANIFEST_SCHEMA)
    Draft202012Validator.check_schema(schema)
    manifest = load_yaml(manifest_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
    if errors:
        return [f"manifest schema failure: {errors[0].message}"]

    if expected_repository and manifest["repository"] != expected_repository:
        problems.append("repository binding mismatch")
    if expected_commit and manifest["source_commit"] != expected_commit:
        problems.append("source commit binding mismatch")
    if manifest["bundle_version"] != BUNDLE_VERSION:
        problems.append("bundle version mismatch")
    if manifest["protocol_version"] != PROTOCOL_VERSION:
        problems.append("protocol version mismatch")
    if manifest["compatibility_base"] != COMPATIBILITY_BASE:
        problems.append("compatibility base mismatch")
    for key in ("formal_release_evidence", "proves_model_ingestion", "external_action_authorization"):
        if manifest[key] is not False:
            problems.append(f"distribution boundary must remain false: {key}")

    decision = load_yaml(root / "docs/planning/DEC-MADP-ALPHA4-003.yaml")
    if decision.get("decision_id") != "DEC-MADP-ALPHA4-003":
        problems.append("distribution decision ID mismatch")
    if decision.get("status") != "ACCEPTED":
        problems.append("distribution decision is not accepted")
    if decision.get("parent_decision_ref") != "docs/planning/DEC-MADP-ALPHA4-002.yaml":
        problems.append("distribution parent decision mismatch")
    decision_body = decision.get("decision", {})
    expected_decision = {
        "target_version": PROTOCOL_VERSION,
        "implementation_slice": "CORE_DISTRIBUTION_SLICE",
        "implementation_authorized": True,
        "prerelease_publication_authorized": False,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }
    for key, expected in expected_decision.items():
        if decision_body.get(key) != expected:
            problems.append(f"distribution decision mismatch: {key}")
    boundary = decision.get("authorization_boundary", {})
    for key in ("merge_authorized", "tag_authorized", "github_release_authorized", "pages_publication_authorized", "stable_release_authorized"):
        if boundary.get(key) is not False:
            problems.append(f"distribution authorization boundary must remain false: {key}")

    status = load_yaml(root / "docs/planning/MADP-v0.3.0-alpha.4-distribution-status.yaml")
    expected_status = {
        "protocol_version": PROTOCOL_VERSION,
        "implementation_slice": "CORE_DISTRIBUTION_SLICE",
        "implementation_status": "DISTRIBUTION_CANDIDATE_IMPLEMENTED_IN_BRANCH",
        "integration_status": "IMPLEMENTATION_BRANCH",
        "base_main_commit": "058f6e10adb601fe3c22f3d476653c8f0f2cb0bf",
        "branch": "feature/v0.3.0-alpha.4-distribution-slice",
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            problems.append(f"distribution status mismatch: {key}")
    for key in ("content_ready", "release_ready", "tagged", "published", "stable_release_authorized", "formal_release_evidence", "tag_authorized", "github_release_authorized", "pages_publication_authorized"):
        if status.get("release_boundary", {}).get(key) is not False:
            problems.append(f"distribution release boundary must remain false: {key}")

    bundle = bundle_path.read_bytes()
    try:
        header = parse_bundle_header(bundle)
    except (ValueError, UnicodeDecodeError, yaml.YAMLError) as exc:
        problems.append(str(exc))
        header = {}
    expected_header = {
        "bundle_version": manifest["bundle_version"],
        "protocol_version": manifest["protocol_version"],
        "compatibility_base": manifest["compatibility_base"],
        "repository": manifest["repository"],
        "source_commit": manifest["source_commit"],
        "status": manifest["status"],
        "formal_release_evidence": manifest["formal_release_evidence"],
        "proves_model_ingestion": manifest["proves_model_ingestion"],
        "external_action_authorization": manifest["external_action_authorization"],
        "supported_load_profiles": manifest["supported_load_profiles"],
        "source_count": manifest["source_count"],
        "source_inventory_sha256": manifest["source_inventory_sha256"],
    }
    if header != expected_header:
        problems.append("bundle YAML frontmatter does not match manifest")
    if manifest["bundle_sha256"] != sha256(bundle):
        problems.append("bundle SHA-256 mismatch")
    if manifest["bundle_bytes"] != len(bundle):
        problems.append("bundle byte count mismatch")

    expected_rows: list[dict] = []
    for relative, role in SOURCE_FILES:
        source = root / relative
        if not source.is_file():
            problems.append(f"current source missing: {relative}")
            continue
        data = source.read_bytes()
        expected_rows.append({"path": relative, "role": role, "sha256": sha256(data), "bytes": len(data)})
    rows = manifest["source_files"]
    if rows != expected_rows:
        problems.append("manifest inventory does not match current source bytes")
    if manifest["source_count"] != len(rows):
        problems.append("source count mismatch")
    if len({row["path"] for row in rows}) != len(rows):
        problems.append("duplicate source path")
    if manifest["source_inventory_sha256"] != inventory_digest(rows):
        problems.append("source inventory digest mismatch")

    loader_sha, loader_digests = loader_metadata(root)
    if manifest["loader_sha256"] != loader_sha:
        problems.append("loader SHA-256 mismatch")
    if manifest["loader_inventory_digests"] != loader_digests:
        problems.append("loader inventory digests mismatch")

    try:
        embedded = parse_embedded_sources(bundle)
    except ValueError as exc:
        problems.append(str(exc))
        embedded = []
    if len(embedded) != len(rows):
        problems.append("embedded source count mismatch")
    for expected_index, (embedded_row, row) in enumerate(zip(embedded, rows), 1):
        if embedded_row["index"] != expected_index:
            problems.append("embedded source index mismatch")
        for key in ("path", "role", "sha256", "bytes"):
            if embedded_row[key] != row[key]:
                problems.append(f"embedded source metadata mismatch: {row['path']}: {key}")
        if sha256(embedded_row["data"]) != row["sha256"]:
            problems.append(f"embedded source digest mismatch: {row['path']}")
        source_path = root / row["path"]
        if source_path.is_file() and embedded_row["data"] != source_path.read_bytes():
            problems.append(f"embedded source differs from repository source: {row['path']}")

    try:
        canonical_bundle, canonical_manifest = build_bundle(manifest["repository"], manifest["source_commit"], root=root)
    except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as exc:
        problems.append(f"canonical regeneration failed: {exc}")
    else:
        if bundle != canonical_bundle:
            problems.append("bundle does not match canonical deterministic output")
        if manifest != canonical_manifest:
            problems.append("manifest does not match canonical deterministic output")

    try:
        text = bundle.decode("utf-8")
    except UnicodeDecodeError:
        problems.append("bundle is not UTF-8")
        text = ""
    for marker in ("not a PROTOCOL_LOAD_REPORT", "does not prove model ingestion", "not formal FIELD_TRIAL or release evidence", "grants no external-action authority"):
        if marker not in text:
            problems.append(f"bundle boundary marker missing: {marker}")

    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])")
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for relative in PUBLIC_ALPHA4_ARTIFACTS:
        path = root / relative
        if not path.is_file():
            problems.append(f"public alpha.4 artifact missing: {relative}")
            continue
        body = path.read_text(encoding="utf-8")
        if exact_private.search(body):
            problems.append(f"private identifier found in {relative}")
        if email.search(body):
            problems.append(f"email address found in {relative}")
        if "human-final-authority-input-raw.md" in body:
            problems.append(f"removed private raw path referenced in {relative}")
        if re.search(r"(?i)publish_identifier_mapping\s*:\s*true", body):
            problems.append(f"identifier mapping publication enabled in {relative}")

    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify deterministic MADP alpha.4 Core distribution bundle")
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
    print("MADP v0.3.0-alpha.4 Core distribution: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
