#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, check: bool) -> int:
    args = [sys.executable, str(ROOT / "scripts" / script)]
    if check:
        args.append("--check")
    return subprocess.call(args, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated artifacts differ")
    args = parser.parse_args()
    status = run("generate_schema_bundles.py", args.check)
    if status != 0:
        return status
    # Text bundles are currently curated generated-distribution drafts.
    # A future generator may make them byte-regenerated as well.
    required = [
        ROOT / "bootstrap" / "complete-protocol-bundle.txt",
        ROOT / "bootstrap" / "migration-fixtures-bundle.txt",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        print("missing generated text bundle(s):")
        for item in missing:
            print(f"  {item}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
