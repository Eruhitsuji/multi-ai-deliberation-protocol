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
    for script in ("generate_schema_bundles.py", "generate_text_bundles.py"):
        status = run(script, args.check)
        if status != 0:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
