#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap"
FIXTURES = ROOT / "tests" / "migration"
VERSION = "MADP-v0.3.0-alpha.1"


def complete_protocol_bundle() -> str:
    sources = [
        "protocol/MADP-v0.3.0-alpha.1.md",
        "protocol/GLOSSARY-v0.3.0-alpha.1.md",
        "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml",
        "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml",
        "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml",
        "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml",
    ]
    lines = [
        "BEGIN_MADP_BUNDLE_METADATA",
        f"protocol_version: {VERSION}",
        "status: GENERATED_DISTRIBUTION_DRAFT_INDEX_ONLY",
        "source_branch: feature/v0.3.0-alpha.1",
        "generator: scripts/generate_text_bundles.py",
        "limitations:",
        "- This committed alpha artifact is a reproducible source index, not yet a self-contained upload bundle.",
        "- It is not released or tagged.",
        "included_sources:",
    ]
    lines.extend(f"- {source}" for source in sources)
    lines.extend(
        [
            "END_MADP_BUNDLE_METADATA",
            "",
            "Regenerate with:",
            "python scripts/generate_text_bundles.py",
            "",
            "Check committed output with:",
            "python scripts/generate_text_bundles.py --check",
            "",
        ]
    )
    return "\n".join(lines)


def migration_fixture_bundle() -> str:
    lines = [
        f"{VERSION} migration fixture index",
        "status: GENERATED_DISTRIBUTION_DRAFT_INDEX_ONLY",
        "generator: scripts/generate_text_bundles.py",
        "",
    ]
    for directory in sorted(path for path in FIXTURES.iterdir() if path.is_dir()):
        manifest = yaml.safe_load((directory / "manifest.yaml").read_text(encoding="utf-8"))
        lines.append(f"{manifest['fixture_id']}: {manifest['purpose']}")
        lines.append(f"  semantic_status: {manifest.get('semantic_status', 'DEFERRED')}")
        lines.append(f"  required_files: {', '.join(manifest.get('required_files', []))}")
    lines.extend(
        [
            "",
            "Validation commands:",
            "python scripts/run_schema_fixture_checks.py all --json",
            "python scripts/check_migration_invariants_v030.py",
            "",
        ]
    )
    return "\n".join(lines)


def outputs() -> dict[Path, str]:
    return {
        BOOTSTRAP / "complete-protocol-bundle.txt": complete_protocol_bundle(),
        BOOTSTRAP / "migration-fixtures-bundle.txt": migration_fixture_bundle(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = False
    for path, generated in outputs().items():
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != generated:
                failed = True
                print(f"DRIFT: {path.relative_to(ROOT)}")
                for line in difflib.unified_diff(
                    current.splitlines(), generated.splitlines(),
                    fromfile="committed", tofile="generated", lineterm="",
                ):
                    print(line)
            else:
                print(f"OK: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generated, encoding="utf-8", newline="")
            print(f"WROTE: {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
