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


PROTOCOL_VERSION = "MADP-v0.2.5-draft"
BOOTSTRAP_DIR = ROOT / "bootstrap"
BOOTSTRAP_FILES = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
REPOSITORY_PLACEHOLDERS = {
    "{{MADP_GITHUB_OWNER}}",
    "{{MADP_GITHUB_REPOSITORY}}",
    "{{MADP_COMMIT_SHA}}",
}
REPO_PART_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def _fail(message: str) -> None:
    raise SystemExit(message)


def _parse_repository(value: str) -> tuple[str, str]:
    if not value or "/" not in value:
        _fail("GITHUB_REPOSITORY must be owner/repository")
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        _fail("GITHUB_REPOSITORY must contain exactly one owner and one repository")
    owner, repository = parts
    if not REPO_PART_RE.fullmatch(owner) or not REPO_PART_RE.fullmatch(repository):
        _fail("GITHUB_REPOSITORY contains invalid characters")
    return owner, repository


def _source_sha(value: str) -> str:
    if not value:
        _fail("GITHUB_SHA is required")
    if not SHA_RE.fullmatch(value):
        _fail("GITHUB_SHA must be a 40-character hexadecimal commit SHA")
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


def generate(output_dir: Path, repository_env: str, sha_env: str, run_id_env: str, actions_env: str) -> None:
    owner, repository = _parse_repository(repository_env.strip())
    source_commit = _source_sha(sha_env.strip())
    source_repository = f"{owner}/{repository}"
    workflow_run_id = run_id_env.strip() or "LOCAL"
    generated_by = "GitHub Actions" if actions_env.strip().lower() == "true" else "LOCAL"

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
    args = parser.parse_args()

    generate(
        Path(args.output_dir),
        os.environ.get("GITHUB_REPOSITORY", ""),
        os.environ.get("GITHUB_SHA", ""),
        os.environ.get("GITHUB_RUN_ID", "LOCAL"),
        os.environ.get("GITHUB_ACTIONS", ""),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
