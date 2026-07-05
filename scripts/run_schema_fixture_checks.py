#!/usr/bin/env python3
"""Schema-layer fixture discovery for MADP v0.3.0-alpha.1.

This runner does not perform migration transformation, semantic validation,
quarantine execution, execution gating, or digest recomputation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "migration"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    dirs = sorted(p for p in FIXTURES.iterdir() if p.is_dir())
    if args.target != "all":
        dirs = [p for p in dirs if p.name == args.target]
    results = []
    for directory in dirs:
        manifest = directory / "manifest.yaml"
        if not manifest.exists():
            results.append({"fixture": directory.name, "status": "ERROR", "message": "manifest missing"})
            continue
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        results.append({"fixture": data.get("fixture_id", directory.name), "status": "DISCOVERED", "schema_layer": data.get("expected"), "semantic": "DEFERRED"})
    failed = any(r["status"] == "ERROR" for r in results)
    report = {"report_version": "1", "suite_result": "ERROR" if failed else "PASS", "fixtures": results, "limitations": ["Schema document execution is added after fixture payload files are completed.", "No semantic migration claims are made."]}
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['fixture']}] {item['status']} schema={item.get('schema_layer')} semantic={item.get('semantic')}")
        print(f"suite: {report['suite_result']}")
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
