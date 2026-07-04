from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
from typing import Any

from madp_validation import ROOT, load_yaml_text, rel


PROTOCOL_VERSION = "MADP-v0.2.5-rc.1"
BOOTSTRAP_FILES = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
BUNDLE_PATH = "bootstrap/complete-protocol-bundle.txt"
REQUIRED_CANONICAL_PATHS = [
    "README.md",
    "protocol/MADP-v0.2.5-rc.1.md",
    "protocol/GLOSSARY-v0.2.5-rc.1.md",
    "schemas/session-state-v0.2.5-rc.1.schema.yaml",
]
DISALLOWED_CANONICAL_PATHS = [
    "protocol/MADP-v0.2.5-draft.md",
    "protocol/GLOSSARY-v0.2.5-draft.md",
    "schemas/session-state-v0.2.5-draft.schema.yaml",
]
REPOSITORY_PLACEHOLDERS = {
    "{{MADP_GITHUB_OWNER}}",
    "{{MADP_GITHUB_REPOSITORY}}",
    "{{MADP_COMMIT_SHA}}",
}
PRESERVED_PLACEHOLDERS = {
    "{{PARTICIPANT_ID}}",
    "{{SESSION_ID}}",
    "{{TASK}}",
    "{{INITIAL_SESSION_STATE}}",
    "{{ROLE}}",
    "{{ALLOWED_ACTIONS}}",
    "{{EXPECTED_RESPONSE}}",
    "{{RELAY_BLOCK}}",
    "{{FAILED_PATHS}}",
    "{{ACCESS_METHOD}}",
    "{{PARTIAL_CONTENT_LIMITATIONS}}",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
RAW_URL_RE = re.compile(r"https://raw\.githubusercontent\.com/([^/\s)]+)/([^/\s)]+)/([^/\s)]+)/([^\s)]+)")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_file_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _expected_bundle(paths: list[str]) -> str:
    blocks: list[str] = []
    for relative_path in paths:
        text = _source_file_text(relative_path)
        if text.endswith("\n"):
            block = f"BEGIN_FILE: {relative_path}\n{text}END_FILE: {relative_path}"
        else:
            block = f"BEGIN_FILE: {relative_path}\n{text}\nEND_FILE: {relative_path}"
        blocks.append(block)
    return "\n\n".join(blocks) + "\n"


def _display(path: Path) -> str:
    try:
        return rel(path)
    except ValueError:
        return str(path)


def _load_yaml_file(path: Path) -> Any:
    return load_yaml_text(path.read_text(encoding="utf-8"), _display(path))


def _fence_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("```"))


def _manifest(path: Path, problems: list[str]) -> dict[str, Any]:
    if not path.exists():
        problems.append(f"{_display(path)}: missing manifest")
        return {}
    data = _load_yaml_file(path)
    if not isinstance(data, dict) or not isinstance(data.get("generated_bootstrap"), dict):
        problems.append(f"{_display(path)}: expected generated_bootstrap mapping")
        return {}
    manifest = data["generated_bootstrap"]
    if manifest.get("protocol_version") != PROTOCOL_VERSION:
        problems.append(f"{_display(path)}: unexpected protocol_version {manifest.get('protocol_version')!r}")
    source_repository = manifest.get("source_repository")
    source_commit = manifest.get("source_commit")
    if not isinstance(source_repository, str) or not REPO_RE.fullmatch(source_repository):
        problems.append(f"{_display(path)}: invalid source_repository {source_repository!r}")
    if not isinstance(source_commit, str) or not SHA_RE.fullmatch(source_commit):
        problems.append(f"{_display(path)}: source_commit must be a lowercase 40-character SHA")
    files = manifest.get("files")
    if not isinstance(files, list):
        problems.append(f"{_display(path)}: files must be a list")
    return manifest


def _check_expected_fixture(expect_path: Path | None, manifest: dict[str, Any], problems: list[str]) -> None:
    if expect_path is None:
        return
    expected = _load_yaml_file(expect_path)
    if not isinstance(expected, dict):
        problems.append(f"{_display(expect_path)}: expected mapping")
        return
    comparisons = {
        "github_repository": "source_repository",
        "github_sha": "source_commit",
        "github_run_id": "workflow_run_id",
        "generated_by": "generated_by",
    }
    for expected_key, manifest_key in comparisons.items():
        if expected_key in expected and expected[expected_key] != manifest.get(manifest_key):
            problems.append(
                f"{_display(expect_path)}: expected {manifest_key}={expected[expected_key]!r}, "
                f"got {manifest.get(manifest_key)!r}"
            )


def _check_markdown_files(site_dir: Path, manifest: dict[str, Any], problems: list[str]) -> dict[str, str]:
    bootstrap_dir = site_dir / "bootstrap"
    source_repository = manifest.get("source_repository")
    source_commit = manifest.get("source_commit")
    texts: dict[str, str] = {}
    for name in BOOTSTRAP_FILES:
        generated_path = bootstrap_dir / name
        source_path = ROOT / "bootstrap" / name
        if not generated_path.exists():
            problems.append(f"{_display(generated_path)}: missing generated bootstrap file")
            continue
        text = generated_path.read_text(encoding="utf-8")
        texts[name] = text
        if PROTOCOL_VERSION not in text:
            problems.append(f"{_display(generated_path)}: missing {PROTOCOL_VERSION}")
        if "MADP-v0.2.5-draft" in text or "0.2.5-draft" in text:
            problems.append(f"{_display(generated_path)}: draft version text remains")
        if any(placeholder in text for placeholder in REPOSITORY_PLACEHOLDERS):
            problems.append(f"{_display(generated_path)}: repository-specific placeholder remains")
        if source_repository and source_commit:
            marker = f"Generated from {source_repository} at {source_commit}"
            if marker not in text:
                problems.append(f"{_display(generated_path)}: missing source commit metadata")
        if source_path.exists() and _fence_count(text) != _fence_count(source_path.read_text(encoding="utf-8")):
            problems.append(f"{_display(generated_path)}: Markdown code fence count changed")
        if _fence_count(text) % 2:
            problems.append(f"{_display(generated_path)}: unbalanced Markdown code fences")

    combined = "\n".join(texts.values())
    for placeholder in sorted(PRESERVED_PLACEHOLDERS):
        if placeholder not in combined:
            problems.append(f"generated bootstrap: preserved placeholder missing: {placeholder}")

    if "PROTOCOL_LOAD_REPORT" not in texts.get("load-protocol-from-github.md", ""):
        problems.append("generated load-protocol-from-github.md: missing PROTOCOL_LOAD_REPORT")
    if "PARTICIPANT_RESPONSE" not in texts.get("join-as-participant.md", ""):
        problems.append("generated join-as-participant.md: missing PARTICIPANT_RESPONSE")
    return texts


def _check_raw_urls(texts: dict[str, str], manifest: dict[str, Any], problems: list[str]) -> None:
    source_repository = manifest.get("source_repository")
    source_commit = manifest.get("source_commit")
    if not isinstance(source_repository, str) or "/" not in source_repository:
        return
    owner, repository = source_repository.split("/", 1)
    load_text = texts.get("load-protocol-from-github.md", "")
    urls = RAW_URL_RE.findall(load_text)
    if len(urls) < len(REQUIRED_CANONICAL_PATHS):
        problems.append("generated load-protocol-from-github.md: missing canonical Raw URLs")
    for raw_owner, raw_repo, revision, path in urls:
        if raw_owner != owner or raw_repo != repository:
            problems.append(f"generated Raw URL repository mismatch: {raw_owner}/{raw_repo}")
        if revision != source_commit:
            problems.append(f"generated Raw URL revision mismatch for {path}: {revision}")
        if revision in {"main", "master"}:
            problems.append(f"generated Raw URL uses movable branch: {path}")
    raw_text = "\n".join(
        f"https://raw.githubusercontent.com/{raw_owner}/{raw_repo}/{revision}/{path}"
        for raw_owner, raw_repo, revision, path in urls
    )
    for canonical_path in REQUIRED_CANONICAL_PATHS:
        expected = f"https://raw.githubusercontent.com/{owner}/{repository}/{source_commit}/{canonical_path}"
        if expected not in raw_text:
            problems.append(f"generated load-protocol-from-github.md: missing canonical URL {expected}")
    for disallowed_path in DISALLOWED_CANONICAL_PATHS:
        if disallowed_path in raw_text:
            problems.append(f"generated load-protocol-from-github.md: draft canonical URL remains for {disallowed_path}")


def _check_recovery_prompt(texts: dict[str, str], manifest: dict[str, Any], problems: list[str]) -> None:
    source_repository = manifest.get("source_repository")
    if not isinstance(source_repository, str) or "/" not in source_repository:
        return
    owner, repository = source_repository.split("/", 1)
    expected_url = f"https://{owner}.github.io/{repository}/bootstrap/complete-protocol-bundle.txt"
    recovery_text = texts.get("recover-from-load-failure.md", "")
    if expected_url not in recovery_text:
        problems.append("generated recover-from-load-failure.md: missing resolved complete bundle Pages URL")
    if any(placeholder in recovery_text for placeholder in REPOSITORY_PLACEHOLDERS):
        problems.append("generated recover-from-load-failure.md: repository-specific placeholder remains")
    if "PASTED_TEXT" not in recovery_text:
        problems.append("generated recover-from-load-failure.md: missing PASTED_TEXT recovery instruction")
    required_markers = [
        "Do not begin normal MADP deliberation until all four required files have been completely read.",
        "If only part of the bundle is pasted, keep `all_required_files_read: false`.",
        "Do not fill missing content from general knowledge or inference.",
    ]
    for marker in required_markers:
        if marker not in recovery_text:
            problems.append(f"generated recover-from-load-failure.md: missing fail-closed marker {marker!r}")


def _check_complete_bundle(site_dir: Path, manifest: dict[str, Any], problems: list[str]) -> None:
    bundle_path = site_dir / BUNDLE_PATH
    if not bundle_path.exists():
        problems.append(f"{_display(bundle_path)}: missing complete protocol bundle")
        return
    bundle = bundle_path.read_text(encoding="utf-8")
    if not bundle.endswith("\n"):
        problems.append(f"{_display(bundle_path)}: bundle must end with newline")

    positions: list[int] = []
    for canonical_path in REQUIRED_CANONICAL_PATHS:
        begin = f"BEGIN_FILE: {canonical_path}"
        end = f"END_FILE: {canonical_path}"
        begin_count = sum(1 for line in bundle.splitlines() if line == begin)
        end_count = sum(1 for line in bundle.splitlines() if line == end)
        if begin_count != 1:
            problems.append(f"{_display(bundle_path)}: expected one {begin!r}, got {begin_count}")
        if end_count != 1:
            problems.append(f"{_display(bundle_path)}: expected one {end!r}, got {end_count}")
        begin_pos = bundle.find(begin + "\n")
        end_pos = bundle.find("\n" + end)
        if begin_pos == -1 or end_pos == -1:
            continue
        if begin_pos > end_pos:
            problems.append(f"{_display(bundle_path)}: {begin!r} appears after its END marker")
        positions.append(begin_pos)

    if positions != sorted(positions):
        problems.append(f"{_display(bundle_path)}: bundle file order does not match canonical order")
    for disallowed_path in DISALLOWED_CANONICAL_PATHS:
        if f"BEGIN_FILE: {disallowed_path}" in bundle or f"END_FILE: {disallowed_path}" in bundle:
            problems.append(f"{_display(bundle_path)}: draft file boundary included for {disallowed_path}")

    expected = _expected_bundle(REQUIRED_CANONICAL_PATHS)
    if bundle != expected:
        problems.append(f"{_display(bundle_path)}: bundle content differs from canonical source files")

    bundle_entries = [
        entry
        for entry in manifest.get("files", [])
        if isinstance(entry, dict) and entry.get("path") == BUNDLE_PATH
    ]
    if len(bundle_entries) != 1:
        problems.append(f"manifest files: expected one bundle entry, got {len(bundle_entries)}")
        return
    entry = bundle_entries[0]
    if entry.get("source_files") != REQUIRED_CANONICAL_PATHS:
        problems.append("manifest files: bundle source_files do not match canonical list")
    if entry.get("sha256") != _sha256(bundle):
        problems.append("manifest files: bundle sha256 does not match generated bundle")


def _check_manifest_files(site_dir: Path, manifest: dict[str, Any], problems: list[str]) -> None:
    files = manifest.get("files")
    source_commit = manifest.get("source_commit")
    if not isinstance(files, list):
        return
    expected_paths = {f"bootstrap/{name}" for name in BOOTSTRAP_FILES}
    expected_paths.add(BUNDLE_PATH)
    actual_paths: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict):
            problems.append("manifest files: entry is not a mapping")
            continue
        path = entry.get("path")
        if not isinstance(path, str):
            problems.append(f"manifest files: invalid path {path!r}")
            continue
        actual_paths.add(path)
        if path not in expected_paths:
            problems.append(f"manifest files: unexpected path {path!r}")
            continue
        if entry.get("source_commit") != source_commit:
            problems.append(f"manifest files: source_commit mismatch for {path}")
        if not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64:
            problems.append(f"manifest files: invalid sha256 for {path}")
        if not (site_dir / path).exists():
            problems.append(f"manifest files: missing output file {path}")
        if path == BUNDLE_PATH and entry.get("source_files") != REQUIRED_CANONICAL_PATHS:
            problems.append("manifest files: bundle source_files mismatch")
    missing = expected_paths.difference(actual_paths)
    for path in sorted(missing):
        problems.append(f"manifest files: missing entry for {path}")


def _check_index(site_dir: Path, manifest: dict[str, Any], problems: list[str]) -> None:
    index = site_dir / "index.html"
    if not index.exists():
        problems.append(f"{_display(index)}: missing index.html")
        return
    text = index.read_text(encoding="utf-8")
    required = [
        "bootstrap/README.md",
        "bootstrap/load-protocol-from-github.md",
        "bootstrap/start-facilitator.md",
        "bootstrap/join-as-participant.md",
        "bootstrap/recover-from-load-failure.md",
        "bootstrap/complete-protocol-bundle.txt",
        "bootstrap/manifest.yaml",
    ]
    for target in required:
        if target not in text:
            problems.append(f"{_display(index)}: missing link to {target}")
    source_repository = manifest.get("source_repository")
    source_commit = manifest.get("source_commit")
    if source_repository and f"https://github.com/{source_repository}" not in text:
        problems.append(f"{_display(index)}: missing source repository link")
    if source_repository and source_commit and f"https://github.com/{source_repository}/commit/{source_commit}" not in text:
        problems.append(f"{_display(index)}: missing source commit link")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated MADP bootstrap Pages output.")
    parser.add_argument("site_dir", nargs="?", default="_site", help="Generated Pages output directory.")
    parser.add_argument("--expect", help="Optional local generation fixture with expected manifest values.")
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    problems: list[str] = []
    manifest = _manifest(site_dir / "bootstrap" / "manifest.yaml", problems)
    _check_expected_fixture(Path(args.expect) if args.expect else None, manifest, problems)
    texts = _check_markdown_files(site_dir, manifest, problems)
    _check_raw_urls(texts, manifest, problems)
    _check_recovery_prompt(texts, manifest, problems)
    _check_complete_bundle(site_dir, manifest, problems)
    _check_manifest_files(site_dir, manifest, problems)
    _check_index(site_dir, manifest, problems)

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print(f"generated bootstrap: {site_dir} PASS")
    print(f"source_repository: {manifest['source_repository']}")
    print(f"source_commit: {manifest['source_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
