#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "migration"


def load(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    directories = sorted(path for path in FIXTURES.iterdir() if path.is_dir())
    if args.target != "all":
        directories = [path for path in directories if path.name == args.target]
    results = []
    for directory in directories:
        manifest = load(directory / "manifest.yaml")
        results.append({"fixture_id": manifest.get("fixture_id"), "expected": manifest.get("expected_semantic_errors", []), "actual": [], "matched": not manifest.get("expected_semantic_errors")})
    failures = sum(1 for item in results if not item["matched"])
    report = {"report_version": "1", "suite_result": "FAIL" if failures else "PASS", "results": results, "limitations": ["Fixture-oriented alpha checks only."]}
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['fixture_id']}] {'PASS' if item['matched'] else 'FAIL'}")
        print(f"suite: {report['suite_result']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
