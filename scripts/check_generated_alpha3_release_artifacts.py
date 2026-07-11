#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys
import zipfile
import yaml

SKILLS = ["madp-start", "madp-facilitator", "madp-participant", "madp-recorder", "madp-help"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    directory = Path(args.directory)
    problems = []

    required = [
        "manifest.yaml",
        "complete-protocol-bundle.txt",
        "quick-start.md",
        "verified-start.md",
        "invite-limited-participant.md",
        "help.md",
        "start-with-skills.md",
        "session-portability.md",
        "skills-README.md",
        "schemas/deliberation.bundle.schema.yaml",
        "schemas/command.bundle.schema.yaml",
        "schemas/migration.bundle.schema.yaml",
        "schemas/session-portability.bundle.schema.yaml",
        "chatgpt-skills/madp-skill-pack.zip",
    ]
    required += [f"chatgpt-skills/{name}.zip" for name in SKILLS]
    required += [f"claude-project/.claude/skills/{name}/SKILL.md" for name in SKILLS]

    for relative in required:
        if not (directory / relative).is_file():
            problems.append(f"missing generated artifact: {relative}")

    if (directory / "manifest.yaml").is_file():
        manifest = yaml.safe_load((directory / "manifest.yaml").read_text(encoding="utf-8"))
        if manifest.get("bundle_version") != "MADP-ALPHA3-BUNDLE-v2":
            problems.append("manifest bundle version mismatch")
        if manifest.get("protocol_version") != "MADP-v0.3.0-alpha.3":
            problems.append("manifest protocol version mismatch")
        if manifest.get("source_commit") != args.source_commit:
            problems.append("manifest source commit mismatch")
        if len(manifest.get("files", [])) < 24:
            problems.append("manifest load set incomplete")
        if manifest.get("skill_packages") != SKILLS:
            problems.append("manifest skill package list mismatch")
        if manifest.get("session_portability_format") != "MADP-PORTABLE-SESSION-v1":
            problems.append("manifest portability format mismatch")

        bundle = (directory / "complete-protocol-bundle.txt").read_text(encoding="utf-8") if (directory / "complete-protocol-bundle.txt").is_file() else ""
        for item in manifest.get("files", []):
            if f'BEGIN_FILE path={item["path"]}' not in bundle or f'END_FILE path={item["path"]}' not in bundle:
                problems.append(f'bundle boundary missing: {item["path"]}')

        verified = (directory / "verified-start.md").read_text(encoding="utf-8") if (directory / "verified-start.md").is_file() else ""
        if args.source_commit not in verified or "MADP-v0.3.0-alpha.3" not in verified:
            problems.append("verified prompt is not commit pinned")

    for name in ["deliberation", "command", "migration", "session-portability"]:
        path = directory / f"schemas/{name}.bundle.schema.yaml"
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))

            def walk(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key == "$ref" and not str(child).startswith("#"):
                            problems.append(f"external ref in {path}: {child}")
                        walk(child)
                elif isinstance(value, list):
                    for child in value:
                        walk(child)

            walk(data)

    for skill_name in SKILLS:
        zip_path = directory / "chatgpt-skills" / f"{skill_name}.zip"
        claude_path = directory / "claude-project" / ".claude" / "skills" / skill_name / "SKILL.md"
        if zip_path.is_file():
            with zipfile.ZipFile(zip_path) as archive:
                expected = f"{skill_name}/SKILL.md"
                if archive.namelist() != [expected]:
                    problems.append(f"unexpected skill archive entries: {skill_name}")
                elif claude_path.is_file() and archive.read(expected) != claude_path.read_bytes():
                    problems.append(f"ChatGPT and Claude skill content drift: {skill_name}")

    pack = directory / "chatgpt-skills/madp-skill-pack.zip"
    if pack.is_file():
        with zipfile.ZipFile(pack) as archive:
            expected = {"README.md"} | {f"{name}/SKILL.md" for name in SKILLS}
            if set(archive.namelist()) != expected:
                problems.append("combined skill pack entries mismatch")

    if problems:
        for problem in problems:
            print("FAIL:", problem, file=sys.stderr)
        return 1
    print("generated alpha.3 release artifacts: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
