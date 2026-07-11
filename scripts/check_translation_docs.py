#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "docs" / "en"
JA_DIR = ROOT / "docs" / "ja"
PAIRS = ["README.md", "getting-started.md", "concepts.md", "authority-model.md", "commands.md"]
REQUIRED_JA = {
    "language": "ja",
    "translation_status": None,
    "normative": "false",
    "translation_of": None,
    "source_commit": None,
}
REQUIRED_EN = {
    "language": "en",
    "translation_status": None,
    "normative": "false",
    "source_commit": None,
}


def front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML-style front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated front matter")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid front matter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def check_required(path: Path, required: dict[str, str | None]) -> list[str]:
    errors: list[str] = []
    try:
        data = front_matter(path)
    except (OSError, ValueError) as exc:
        return [f"{path.relative_to(ROOT)}: {exc}"]
    for key, expected in required.items():
        if not data.get(key):
            errors.append(f"{path.relative_to(ROOT)}: missing {key}")
        elif expected is not None and data[key].lower() != expected.lower():
            errors.append(f"{path.relative_to(ROOT)}: {key} must be {expected}")
    commit = data.get("source_commit", "")
    if commit and not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append(f"{path.relative_to(ROOT)}: source_commit must be a 40-character lowercase SHA")
    return errors


def main() -> int:
    errors: list[str] = []
    for name in PAIRS:
        en = EN_DIR / name
        ja = JA_DIR / name
        if not en.exists():
            errors.append(f"missing docs/en/{name}")
        if not ja.exists():
            errors.append(f"missing docs/ja/{name}")
        if en.exists():
            errors.extend(check_required(en, REQUIRED_EN))
        if ja.exists():
            errors.extend(check_required(ja, REQUIRED_JA))
            try:
                translation_of = front_matter(ja).get("translation_of")
                if translation_of != f"docs/en/{name}":
                    errors.append(f"docs/ja/{name}: translation_of must be docs/en/{name}")
            except (OSError, ValueError):
                pass

    policy = ROOT / "docs" / "TRANSLATION_POLICY.md"
    if not policy.exists():
        errors.append("missing docs/TRANSLATION_POLICY.md")
    japanese_readme = ROOT / "README.ja.md"
    if not japanese_readme.exists():
        errors.append("missing README.ja.md")

    if errors:
        print("translation documentation check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"translation documentation check: PASS ({len(PAIRS)} language pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
