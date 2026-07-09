#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "schemas" / "v0.3.0-alpha.2"
DEFAULT_OUTPUT_DIR = ROOT / "tmp" / "generated-alpha2-schemas"
PROTOCOL_VERSION = "MADP-v0.3.0-alpha.2"

SCHEMAS = {
    "command": "command.schema.yaml",
    "command-registry": "command-registry.schema.yaml",
    "todo": "todo.schema.yaml",
    "context-package": "context-package.schema.yaml",
    "context-package-receipt": "context-package-receipt.schema.yaml",
    "review": "review.schema.yaml",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"schema root must be an object: {path}")
    return data


def render_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def build_bundle(name: str, source_file: str) -> tuple[str, dict[str, Any]]:
    source_path = SOURCE_DIR / source_file
    source = load_yaml(source_path)
    Draft202012Validator.check_schema(source)
    source_id = source.get("$id")
    if not isinstance(source_id, str) or not source_id:
        raise SystemExit(f"source schema has no $id: {source_path}")

    bundle = dict(source)
    bundle["$id"] = f"urn:madp:schema:bundle:{name}:0.3.0-alpha.2"
    bundle["x-madp-generated-from"] = [source_id]
    bundle["x-madp-protocol-version"] = PROTOCOL_VERSION
    bundle["x-madp-source-path"] = f"schemas/v0.3.0-alpha.2/{source_file}"
    Draft202012Validator.check_schema(bundle)
    return render_json(bundle), bundle


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_files: list[dict[str, Any]] = []

    for name, source_file in SCHEMAS.items():
        rendered, bundle = build_bundle(name, source_file)
        filename = f"{name}-v0.3.0-alpha.2.bundle.schema.json"
        path = output_dir / filename
        path.write_text(rendered, encoding="utf-8", newline="\n")
        manifest_files.append(
            {
                "name": name,
                "path": filename,
                "bundle_id": bundle["$id"],
                "source_id": bundle["x-madp-generated-from"][0],
                "sha256": sha256(rendered),
            }
        )
        print(f"WROTE: {path}")

    manifest = {
        "generated_alpha2_schema_bundles": {
            "protocol_version": PROTOCOL_VERSION,
            "status": "draft generated distribution",
            "file_count": len(manifest_files),
            "files": manifest_files,
        }
    }
    manifest_text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False)
    (output_dir / "manifest.yaml").write_text(manifest_text, encoding="utf-8", newline="\n")
    print(f"WROTE: {output_dir / 'manifest.yaml'}")
    return manifest


def check(output_dir: Path) -> int:
    expected_dir = output_dir.parent / f".{output_dir.name}.expected"
    if expected_dir.exists():
        for path in expected_dir.iterdir():
            if path.is_file():
                path.unlink()
    generate(expected_dir)

    failed = False
    expected_names = {path.name for path in expected_dir.iterdir() if path.is_file()}
    actual_names = {path.name for path in output_dir.iterdir() if path.is_file()} if output_dir.exists() else set()
    if actual_names != expected_names:
        failed = True
        print(f"DRIFT: file set actual={sorted(actual_names)} expected={sorted(expected_names)}")

    for name in sorted(expected_names & actual_names):
        actual = (output_dir / name).read_bytes()
        expected = (expected_dir / name).read_bytes()
        if actual != expected:
            failed = True
            print(f"DRIFT: {output_dir / name}")
        else:
            print(f"OK: {output_dir / name}")

    for path in expected_dir.iterdir():
        if path.is_file():
            path.unlink()
    expected_dir.rmdir()
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate standalone MADP alpha.2 schema bundles.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check(args.output_dir)
    generate(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
