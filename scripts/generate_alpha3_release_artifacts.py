#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import shutil
import sys
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.3"
SKILLS = ["madp-start", "madp-facilitator", "madp-participant", "madp-recorder", "madp-help"]

LOAD_SET = [
    "README-v0.3.0-alpha.2.md",
    "protocol/MADP-v0.3.0-alpha.2.md",
    "protocol/GLOSSARY-v0.3.0-alpha.2.md",
    "README-v0.3.0-alpha.3.md",
    "protocol/MADP-v0.3.0-alpha.3.md",
    "protocol/GLOSSARY-v0.3.0-alpha.3.md",
    "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "schemas/v0.3.0-alpha.3/command.schema.yaml",
    "schemas/v0.3.0-alpha.3/migration.schema.yaml",
    "schemas/v0.3.0-alpha.3/session-portability.schema.yaml",
    "registries/v0.3.0-alpha.3/commands.yaml",
    "docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md",
    "docs/profiles/MADP_HELP-v0.3.0-alpha.3.md",
    "docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md",
    "docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md",
    "docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md",
    "docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md",
    "docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md",
    "skills/README.md",
    *[f"skills/{name}/SKILL.md" for name in SKILLS],
]

SCHEMAS = [
    "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "schemas/v0.3.0-alpha.3/command.schema.yaml",
    "schemas/v0.3.0-alpha.3/migration.schema.yaml",
    "schemas/v0.3.0-alpha.3/session-portability.schema.yaml",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_deterministic_zip(path: Path, entries: list[tuple[str, bytes]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def generate(out: Path, repository: str, commit: str):
    if len(commit) != 40 or any(c not in "0123456789abcdefABCDEF" for c in commit):
        raise ValueError("source commit must be 40 hexadecimal characters")
    missing = [item for item in LOAD_SET if not (ROOT / item).is_file()]
    if missing:
        raise FileNotFoundError("missing load-set files: " + ", ".join(missing))

    out.mkdir(parents=True, exist_ok=True)
    (out / "schemas").mkdir(exist_ok=True)
    (out / "chatgpt-skills").mkdir(exist_ok=True)
    claude_root = out / "claude-project" / ".claude" / "skills"
    claude_root.mkdir(parents=True, exist_ok=True)

    files = []
    for relative in LOAD_SET:
        path = ROOT / relative
        files.append({"path": relative, "sha256": digest(path), "bytes": path.stat().st_size})

    manifest = {
        "bundle_version": "MADP-ALPHA3-BUNDLE-v2",
        "protocol_version": VERSION,
        "repository": repository,
        "source_commit": commit,
        "files": files,
        "skill_packages": SKILLS,
        "session_portability_format": "MADP-PORTABLE-SESSION-v1",
    }
    (out / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    parts = [
        "BEGIN_MADP_BUNDLE_METADATA",
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True).rstrip(),
        "END_MADP_BUNDLE_METADATA",
    ]
    for relative in LOAD_SET:
        parts += [
            f"BEGIN_FILE path={relative}",
            (ROOT / relative).read_text(encoding="utf-8").rstrip(),
            f"END_FILE path={relative}",
        ]
    (out / "complete-protocol-bundle.txt").write_text("\n\n".join(parts) + "\n", encoding="utf-8")

    owner, repo = repository.split("/", 1)
    rows = []
    for relative in LOAD_SET:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{relative}"
        rows.append(f"- `{relative}`\n  {url}")
    verified = (
        "---\n"
        "bootstrap_version: 0.5\n"
        f"protocol_version: {VERSION}\n"
        "usage_mode: VERIFIED\n"
        f"repository_commit: {commit}\n"
        "---\n\n# Load MADP alpha.3 verified bundle\n\n"
        "Read every file below from the same immutable commit. Report READ, PARTIALLY_READ, or FAILED for each file. Do not infer unread content.\n\n"
        + "\n".join(rows)
        + "\n\nDo not begin substantive deliberation until all required files are read, the deliberation goal is confirmed when required, participant authority is explicit, and schema validation limitations are reported. Default authority is PROPOSE_ONLY.\n"
    )
    (out / "verified-start.md").write_text(verified, encoding="utf-8")

    for source, target in [
        ("bootstrap/alpha3/quick-start.md", "quick-start.md"),
        ("bootstrap/alpha3/invite-limited-participant.md", "invite-limited-participant.md"),
        ("bootstrap/alpha3/help.md", "help.md"),
        ("bootstrap/alpha3/start-with-skills.md", "start-with-skills.md"),
        ("docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md", "session-portability.md"),
        ("skills/README.md", "skills-README.md"),
    ]:
        shutil.copy2(ROOT / source, out / target)

    for relative in SCHEMAS:
        data = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
        refs = []

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == "$ref":
                        refs.append(child)
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(data)
        bad = [ref for ref in refs if not str(ref).startswith("#")]
        if bad:
            raise ValueError(f"non-standalone refs in {relative}: {bad}")
        name = Path(relative).name.replace(".schema.yaml", ".bundle.schema.yaml")
        (out / "schemas" / name).write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    all_entries: list[tuple[str, bytes]] = []
    for skill_name in SKILLS:
        source = ROOT / "skills" / skill_name / "SKILL.md"
        data = source.read_bytes()
        skill_entries = [(f"{skill_name}/SKILL.md", data)]
        write_deterministic_zip(out / "chatgpt-skills" / f"{skill_name}.zip", skill_entries)
        target_dir = claude_root / skill_name
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "SKILL.md").write_bytes(data)
        all_entries.extend(skill_entries)
    all_entries.append(("README.md", (ROOT / "skills/README.md").read_bytes()))
    write_deterministic_zip(out / "chatgpt-skills" / "madp-skill-pack.zip", all_entries)

    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--repository", default="Eruhitsuji/multi-ai-deliberation-protocol")
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        manifest = generate(Path(args.output), args.repository, args.source_commit)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f'alpha.3 release artifacts generated: {len(manifest["files"])} source files')
    print(f'agent skills packaged: {len(manifest["skill_packages"])}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
