from __future__ import annotations

import argparse
import hashlib
from html import escape
import os
from pathlib import Path
import re
from typing import Any

import yaml

from madp_validation import ROOT, rel


PROTOCOL_VERSION = "MADP-v0.3.0-alpha.1"
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
    "README-v0.3.0-alpha.1.md",
    "protocol/MADP-v0.3.0-alpha.1.md",
    "protocol/GLOSSARY-v0.3.0-alpha.1.md",
    "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml",
    "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml",
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
    value = cli_value if cli_value is not None else env_value
    if value is None or not value.strip():
        _fail(f"{name} is required")
    return value.strip()


def _optional_input(name: str, cli_value: str | None, env_value: str | None, default: str) -> str:
    value = cli_value if cli_value is not None else env_value
    if value is None:
        return default
    if not value.strip():
        _fail(f"{name} must not be empty")
    return value.strip()


def _generated_by(cli_value: str | None, actions_env: str) -> str:
    if cli_value is not None:
        if not cli_value.strip():
            _fail("--generated-by must not be empty")
        return cli_value.strip()
    return "GitHub Actions" if actions_env.strip().lower() == "true" else "LOCAL"


def _parse_repository(value: str) -> tuple[str, str]:
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        _fail("repository must be owner/repository")
    owner, repository = parts
    if not REPO_PART_RE.fullmatch(owner) or not REPO_PART_RE.fullmatch(repository):
        _fail("repository contains invalid characters")
    return owner, repository


def _source_sha(value: str) -> str:
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
    remaining = sorted(p for p in REPOSITORY_PLACEHOLDERS if p in text)
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
    if not path.is_file():
        _fail(f"missing canonical bundle source file: {relative_path}")
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
        suffix = "" if text.endswith("\n") else "\n"
        blocks.append(
            f"BEGIN_FILE: {relative_path}\n{text}{suffix}END_FILE: {relative_path}"
        )
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
                {"path": path, "sha256": _sha256(_source_file_text(path))}
                for path in paths
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
    return yaml.safe_dump(
        {
            "generated_bootstrap": {
                "protocol_version": PROTOCOL_VERSION,
                "source_repository": source_repository,
                "source_commit": source_commit,
                "generated_by": generated_by,
                "workflow_run_id": workflow_run_id,
                "files": files,
            }
        },
        sort_keys=False,
        allow_unicode=False,
    )


def _index_html(owner: str, repository: str, source_commit: str) -> str:
    source_repository = f"{owner}/{repository}"
    repo_url = f"https://github.com/{owner}/{repository}"
    links = [
        ("Bootstrap overview", "bootstrap/README.md"),
        ("Load protocol", "bootstrap/load-protocol-from-github.md"),
        ("Start facilitator", "bootstrap/start-facilitator.md"),
        ("Join participant", "bootstrap/join-as-participant.md"),
        ("Recover from failure", "bootstrap/recover-from-load-failure.md"),
        ("Complete protocol bundle", "bootstrap/complete-protocol-bundle.txt"),
        ("Complete protocol bundle manifest", "bootstrap/complete-protocol-bundle.manifest.yaml"),
        ("Manifest", "bootstrap/manifest.yaml"),
        ("Source repository", repo_url),
        ("Source commit", f"{repo_url}/commit/{source_commit}"),
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
    <title>MADP v0.3.0-alpha.1 Bootstrap Prompts</title>
  </head>
  <body>
    <main>
      <h1>MADP v0.3.0-alpha.1 Bootstrap Prompts</h1>
      <p>Generated from {escape(source_repository)} at commit <code>{escape(source_commit)}</code>.</p>
      <p>The Pages URL may move, but generated prompt content pins canonical Raw URLs to this source commit.</p>
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
        generated = _replace_repository_placeholders(
            source.read_text(encoding="utf-8"), owner, repository, source_commit
        )
        generated = _with_generated_metadata(generated, source_rel, source_repository, source_commit)
        _write_text(bootstrap_output / name, generated)
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
        source_repository, source_commit, bundle, CANONICAL_BUNDLE_FILES
    )
    _write_text(bootstrap_output / "complete-protocol-bundle.manifest.yaml", bundle_manifest)
    generated_files.extend(
        [
            {
                "path": BUNDLE_OUTPUT_PATH,
                "source_files": CANONICAL_BUNDLE_FILES,
                "source_commit": source_commit,
                "sha256": _sha256(bundle),
            },
            {
                "path": BUNDLE_MANIFEST_OUTPUT_PATH,
                "source_files": CANONICAL_BUNDLE_FILES,
                "source_commit": source_commit,
                "sha256": _sha256(bundle_manifest),
            },
        ]
    )

    _write_text(
        bootstrap_output / "manifest.yaml",
        _manifest(source_repository, source_commit, generated_by, workflow_run_id, generated_files),
    )
    _write_text(output_dir / "index.html", _index_html(owner, repository, source_commit))

    print(f"generated bootstrap prompts: {output_dir}")
    print(f"protocol_version: {PROTOCOL_VERSION}")
    print(f"canonical_file_count: {len(CANONICAL_BUNDLE_FILES)}")
    print(f"source_repository: {source_repository}")
    print(f"source_commit: {source_commit}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate repository-resolved MADP bootstrap prompts.")
    parser.add_argument("output_dir")
    parser.add_argument("--repository")
    parser.add_argument("--commit-sha")
    parser.add_argument("--workflow-run-id")
    parser.add_argument("--generated-by")
    args = parser.parse_args()

    generate(
        Path(args.output_dir),
        _required_input("--repository", args.repository, os.environ.get("GITHUB_REPOSITORY")),
        _required_input("--commit-sha", args.commit_sha, os.environ.get("GITHUB_SHA")),
        _optional_input("--workflow-run-id", args.workflow_run_id, os.environ.get("GITHUB_RUN_ID"), "LOCAL"),
        _generated_by(args.generated_by, os.environ.get("GITHUB_ACTIONS", "")),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
