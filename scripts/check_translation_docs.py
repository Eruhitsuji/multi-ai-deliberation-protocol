#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "translations.yaml"
POLICY_PATH = ROOT / "docs" / "TRANSLATION_POLICY.md"
JA_ROOT_README = ROOT / "README.ja.md"
ALLOWED_TRANSLATION_STATUS = {"CURRENT", "STALE", "REVIEW_NEEDED"}
SHA_RE = re.compile(r"[0-9a-f]{40}")


def front_matter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML-style front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated front matter")
    raw = text[4:end]
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("front matter must be a mapping")
    normalized = {str(key): str(value).lower() if isinstance(value, bool) else str(value) for key, value in data.items()}
    return normalized, text[end + 5 :]


def load_manifest() -> tuple[dict[str, Any], list[str]]:
    if not MANIFEST_PATH.exists():
        return {}, ["missing docs/translations.yaml"]
    try:
        data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"docs/translations.yaml: {exc}"]
    if not isinstance(data, dict):
        return {}, ["docs/translations.yaml: root must be a mapping"]
    return data, []


def check_front_matter(
    path: Path,
    language: str,
    source_commit: str,
    translation_of: str | None,
) -> tuple[list[str], str]:
    errors: list[str] = []
    try:
        data, body = front_matter(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"{path.relative_to(ROOT)}: {exc}"], ""

    relative = path.relative_to(ROOT)
    required = {
        "language": language,
        "source_commit": source_commit,
        "normative": "false",
    }
    for key, expected in required.items():
        actual = data.get(key)
        if actual != expected:
            errors.append(f"{relative}: {key} must be {expected}, got {actual!r}")

    status = data.get("translation_status")
    if status not in ALLOWED_TRANSLATION_STATUS:
        errors.append(f"{relative}: translation_status must be one of {sorted(ALLOWED_TRANSLATION_STATUS)}")

    commit = data.get("source_commit", "")
    if not SHA_RE.fullmatch(commit):
        errors.append(f"{relative}: source_commit must be a 40-character lowercase SHA")

    if translation_of is None:
        if "translation_of" in data:
            errors.append(f"{relative}: English source must not declare translation_of")
    elif data.get("translation_of") != translation_of:
        errors.append(f"{relative}: translation_of must be {translation_of}")

    return errors, body


def markdown_names(directory: Path) -> set[str]:
    return {path.name for path in directory.glob("*.md") if path.is_file()}


def main() -> int:
    errors: list[str] = []
    manifest, manifest_errors = load_manifest()
    errors.extend(manifest_errors)
    if errors:
        print("translation documentation check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    source_commit = manifest.get("source_commit")
    if not isinstance(source_commit, str) or not SHA_RE.fullmatch(source_commit):
        errors.append("docs/translations.yaml: source_commit must be a 40-character lowercase SHA")
        source_commit = ""

    if manifest.get("source_language") != "en":
        errors.append("docs/translations.yaml: source_language must be en")
    if manifest.get("normative_language") != "en":
        errors.append("docs/translations.yaml: normative_language must be en")
    if manifest.get("managed_translation_languages") != ["ja"]:
        errors.append("docs/translations.yaml: managed_translation_languages must be [ja]")

    pairs = manifest.get("pairs")
    if not isinstance(pairs, list) or not pairs:
        errors.append("docs/translations.yaml: pairs must be a non-empty list")
        pairs = []

    declared_en: set[str] = set()
    declared_ja: set[str] = set()
    for index, pair in enumerate(pairs):
        if not isinstance(pair, dict) or set(pair) != {"en", "ja"}:
            errors.append(f"docs/translations.yaml: pair {index} must contain exactly en and ja")
            continue
        en_rel = pair["en"]
        ja_rel = pair["ja"]
        if not isinstance(en_rel, str) or not isinstance(ja_rel, str):
            errors.append(f"docs/translations.yaml: pair {index} paths must be strings")
            continue
        if en_rel in declared_en or ja_rel in declared_ja:
            errors.append(f"docs/translations.yaml: duplicate pair path at index {index}")
        declared_en.add(en_rel)
        declared_ja.add(ja_rel)

        en = ROOT / en_rel
        ja = ROOT / ja_rel
        if not en.exists():
            errors.append(f"missing {en_rel}")
            continue
        if not ja.exists():
            errors.append(f"missing {ja_rel}")
            continue

        en_errors, en_body = check_front_matter(en, "en", source_commit, None)
        ja_errors, ja_body = check_front_matter(ja, "ja", source_commit, en_rel)
        errors.extend(en_errors)
        errors.extend(ja_errors)

        en_to_ja = f"../ja/{Path(ja_rel).name}"
        ja_to_en = f"../en/{Path(en_rel).name}"
        if en_to_ja not in en_body:
            errors.append(f"{en_rel}: missing reciprocal Japanese link {en_to_ja}")
        if ja_to_en not in ja_body:
            errors.append(f"{ja_rel}: missing reciprocal English link {ja_to_en}")

    actual_en = {f"docs/en/{name}" for name in markdown_names(ROOT / "docs" / "en")}
    actual_ja = {f"docs/ja/{name}" for name in markdown_names(ROOT / "docs" / "ja")}
    if actual_en != declared_en:
        errors.append(f"translation manifest English set mismatch: undeclared={sorted(actual_en - declared_en)}, missing={sorted(declared_en - actual_en)}")
    if actual_ja != declared_ja:
        errors.append(f"translation manifest Japanese set mismatch: undeclared={sorted(actual_ja - declared_ja)}, missing={sorted(declared_ja - actual_ja)}")

    for required in (POLICY_PATH, JA_ROOT_README):
        if not required.exists():
            errors.append(f"missing {required.relative_to(ROOT)}")

    if JA_ROOT_README.exists():
        readme = JA_ROOT_README.read_text(encoding="utf-8")
        for pair in pairs:
            if isinstance(pair, dict) and isinstance(pair.get("ja"), str) and pair["ja"] != "docs/ja/README.md":
                expected = f"({pair['ja']})"
                if expected not in readme:
                    errors.append(f"README.ja.md: missing guide link {pair['ja']}")

    if errors:
        print("translation documentation check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"translation documentation check: PASS ({len(pairs)} managed language pairs, source {source_commit})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
