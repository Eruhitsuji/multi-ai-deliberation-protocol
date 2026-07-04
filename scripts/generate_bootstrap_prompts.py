from __future__ import annotations

import argparse
import hashlib
from html import escape
import os
from pathlib import Path
import re
import sys
from typing import Any

import yaml

from madp_validation import ROOT, rel


PROTOCOL_VERSION = "MADP-v0.2.5-rc.1"
BUNDLE_FORMAT = "MADP_COMPLETE_PROTOCOL_BUNDLE_V1"
BOOTSTRAP_DIR = ROOT / "bootstrap"
BOOTSTRAP_FILES = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
CANONICAL_BUNDLE_FILES = [
    "README.md",
    "protocol/MADP-v0.2.5-rc.1.md",
    "protocol/GLOSSARY-v0.2.5-rc.1.md",
    "schemas/session-state-v0.2.5-rc.1.schema.yaml",
]
BUNDLE_OUTPUT_PATH = "bootstrap/complete-protocol-bundle.txt"
BUNDLE_MANIFEST_OUTPUT_PATH = "bootstrap/complete-protocol-bundle.manifest.yaml"
REPOSITORY_PLACEHOLDERS = {
    "{{MADP_GITHUB_OWNER}}",
    "{{MADP_GITHUB_REPOSITORY}}",
    "{{MADP_COMMIT_SHA}}",
}
REPO_PART_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def _fail(message: str) -> None:
    raise SystemExit(message)


def _required_input(name: str, cli_value: str | None, env_value: str | None) -> str:
    if cli_value is not None:
        if not cli_value.strip():
            _fail(f"{name} must not be empty")
        return cli_value.strip()
    if env_value is not None and env_value.strip():
        return env_value.strip()
    _fail(f"{name} is required")


def _optional_input(name: str, cli_value: str | None, env_value: str | None, default: str) -> str:
    if cli_value is not None:
        if not cli_value.strip():
            _fail(f"{name} must not be empty")
        return cli_value.strip()
    if env_value is not None and env_value.strip():
        return env_value.strip()
    return default


def _generated_by(cli_value: str | None, actions_env: str) -> str:
    if cli_value is not None:
        if not cli_value.strip():
            _fail("--generated-by must not be empty")
        return cli_value.strip()
    return "GitHub Actions" if actions_env.strip().lower() == "true" else "LOCAL"


def _parse_repository(value: str) -> tuple[str, str]:
    if not value or "/" not in value:
        _fail("repository must be owner/repository")
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        _fail("repository must contain exactly one owner and one repository")
    owner, repository = parts
    if not REPO_PART_RE.fullmatch(owner) or not REPO_PART_RE.fullmatch(repository):
        _fail("repository contains invalid characters")
    return owner, repository


def _source_sha(value: str) -> str:
    if not value:
        _fail("commit SHA is required")
    if not SHA_RE.fullmatch(value):
        _fail("commit SHA must be a 40-character hexadecimal commit SHA")
    return value.lower()


def _replace_repository_placeholders(text: str, owner: str, repository: str, sha: str) -> str:
    replacements = {
        "{{MADP_GITHUB_OWNER}}": owner,
        "{{MADP_GITHUB_REPOSITORY}}": repository,
        "{{MADP_COMMIT_SHA}}": sha,
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    remaining = sorted(placeholder for placeholder in REPOSITORY_PLACEHOLDERS if placeholder in text)
    if remaining:
        _fail(f"repository-specific placeholders remain after generation: {', '.join(remaining)}")
    return text


def _with_generated_metadata(text: str, source_path: str, source_repository: str, source_commit: str) -> str:
    comment = (
        f"<!-- Generated from {source_repository} at {source_commit}; "
        f"source template: {source_path}. -->"
    )
    frontmatter = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    if frontmatter:
        insert_at = frontmatter.end()
        return text[:insert_at] + "\n" + comment + "\n\n" + text[insert_at:]
    return comment + "\n\n" + text


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_file_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        _fail(f"missing canonical bundle source file: {relative_path}")
    if not path.is_file():
        _fail(f"canonical bundle source is not a file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _complete_protocol_bundle(paths: list[str], source_repository: str, source_commit: str) -> str:
    metadata = "\n".join(
        [
            "BEGIN_MADP_BUNDLE_METADATA",
            f"bundle_format: {BUNDLE_FORMAT}",
            f"protocol_version: {PROTOCOL_VERSION}",
            f"source_repository: {source_repository}",
            f"source_commit: {source_commit}",
            f"canonical_file_count: {len(paths)}",
            "END_MADP_BUNDLE_METADATA",
        ]
    )
    blocks: list[str] = []
    for relative_path in paths:
        text = _source_file_text(relative_path)
        if text.endswith("\n"):
            block = f"BEGIN_FILE: {relative_path}\n{text}END_FILE: {relative_path}"
        else:
            block = f"BEGIN_FILE: {relative_path}\n{text}\nEND_FILE: {relative_path}"
        blocks.append(block)
    return metadata + "\n\n" + "\n\n".join(blocks) + "\n"


def _complete_protocol_bundle_manifest(
    source_repository: str,
    source_commit: str,
    bundle: str,
    paths: list[str],
) -> str:
    data = {
        "complete_protocol_bundle": {
            "bundle_format": BUNDLE_FORMAT,
            "protocol_version": PROTOCOL_VERSION,
            "source_repository": source_repository,
            "source_commit": source_commit,
            "bundle_path": BUNDLE_OUTPUT_PATH,
            "bundle_sha256": _sha256(bundle),
            "files": [
                {
                    "path": relative_path,
                    "sha256": _sha256(_source_file_text(relative_path)),
                }
                for relative_path in paths
            ],
        }
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _manifest(
    source_repository: str,
    source_commit: str,
    generated_by: str,
    workflow_run_id: str,
    files: list[dict[str, Any]],
) -> str:
    data = {
        "generated_bootstrap": {
            "protocol_version": PROTOCOL_VERSION,
            "source_repository": source_repository,
            "source_commit": source_commit,
            "generated_by": generated_by,
            "workflow_run_id": workflow_run_id,
            "files": files,
        }
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)


def _index_html(owner: str, repository: str, source_commit: str) -> str:
    source_repository = f"{owner}/{repository}"
    repo_url = f"https://github.com/{owner}/{repository}"
    commit_url = f"{repo_url}/commit/{source_commit}"
    links = [
        ("Bootstrap overview", "bootstrap/README.md"),
        ("Load protocol", "bootstrap/load-protocol-from-github.md"),
        ("Start facilitator", "bootstrap/start-facilitator.md"),
        ("Join participant", "bootstrap/join-as-participant.md"),
        ("Recover from failure", "bootstrap/recover-from-load-failure.md"),
        ("Complete protocol bundle (manual paste fallback)", "bootstrap/complete-protocol-bundle.txt"),
        ("Complete protocol bundle manifest", "bootstrap/complete-protocol-bundle.manifest.yaml"),
        ("Manifest", "bootstrap/manifest.yaml"),
        ("Source repository", repo_url),
        ("Source commit", commit_url),
    ]
    items = "\n".join(
        f'      <li><a href="{escape(href, quote=True)}">{escape(label)}</a></li>'
        for label, href in links
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MADP Bootstrap Prompts</title>
  </head>
  <body>
    <main>
      <h1>MADP Bootstrap Prompts</h1>
      <p>Generated from {escape(source_repository)} at commit <code>{escape(source_commit)}</code>.</p>
      <p>The Pages URL may move, but the generated prompt content pins canonical Raw URLs to this source commit.</p>
      <ul>
{items}
      </ul>
    </main>
  </body>
</html>
"""


def generate(output_dir: Path, source_repository: str, source_sha: str, workflow_run_id: str, generated_by: str) -> None:
    owner, repository = _parse_repository(source_repository)
    source_commit = _source_sha(source_sha)
    source_repository = f"{owner}/{repository}"

    bootstrap_output = output_dir / "bootstrap"
    generated_files: list[dict[str, Any]] = []
    for name in BOOTSTRAP_FILES:
        source = BOOTSTRAP_DIR / name
        if not source.exists():
            _fail(f"missing bootstrap template: {rel(source)}")
        source_rel = rel(source)
        text = source.read_text(encoding="utf-8")
        generated = _replace_repository_placeholders(text, owner, repository, source_commit)
        generated = _with_generated_metadata(generated, source_rel, source_repository, source_commit)
        output_path = bootstrap_output / name
        _write_text(output_path, generated)
        generated_files.append(
            {
                "path": f"bootstrap/{name}",
                "source_template": source_rel,
                "source_commit": source_commit,
                "sha256": _sha256(generated),
            }
        )

    bundle = _complete_protocol_bundle(CANONICAL_BUNDLE_FILES, source_repository, source_commit)
    _write_text(bootstrap_output / "complete-protocol-bundle.txt", bundle)
    bundle_manifest = _complete_protocol_bundle_manifest(
        source_repository,
        source_commit,
        bundle,
        CANONICAL_BUNDLE_FILES,
    )
    _write_text(bootstrap_output / "complete-protocol-bundle.manifest.yaml", bundle_manifest)
    generated_files.append(
        {
            "path": BUNDLE_OUTPUT_PATH,
            "source_files": CANONICAL_BUNDLE_FILES,
            "source_commit": source_commit,
            "sha256": _sha256(bundle),
        }
    )
    generated_files.append(
        {
            "path": BUNDLE_MANIFEST_OUTPUT_PATH,
            "source_files": CANONICAL_BUNDLE_FILES,
            "source_commit": source_commit,
            "sha256": _sha256(bundle_manifest),
        }
    )

    manifest = _manifest(
        source_repository,
        source_commit,
        generated_by,
        workflow_run_id,
        generated_files,
    )
    _write_text(bootstrap_output / "manifest.yaml", manifest)
    _write_text(output_dir / "index.html", _index_html(owner, repository, source_commit))

    print(f"generated bootstrap prompts: {output_dir}")
    print(f"source_repository: {source_repository}")
    print(f"source_commit: {source_commit}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate repository-resolved MADP bootstrap prompts.")
    parser.add_argument("output_dir", help="Directory to receive generated Pages files.")
    parser.add_argument("--repository", help="Source repository in owner/repository form.")
    parser.add_argument("--commit-sha", help="Source commit SHA to pin generated Raw URLs to.")
    parser.add_argument("--workflow-run-id", help="Workflow run identifier to record in manifest.")
    parser.add_argument("--generated-by", help="Generator identity to record in manifest.")
    args = parser.parse_args()

    source_repository = _required_input("--repository", args.repository, os.environ.get("GITHUB_REPOSITORY"))
    source_sha = _required_input("--commit-sha", args.commit_sha, os.environ.get("GITHUB_SHA"))
    workflow_run_id = _optional_input("--workflow-run-id", args.workflow_run_id, os.environ.get("GITHUB_RUN_ID"), "LOCAL")
    generated_by = _generated_by(args.generated_by, os.environ.get("GITHUB_ACTIONS", ""))

    generate(
        Path(args.output_dir),
        source_repository,
        source_sha,
        workflow_run_id,
        generated_by,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
