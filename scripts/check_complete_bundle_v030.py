#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
from pathlib import Path
import re
from typing import Any

import yaml

SOURCE_START = re.compile(
    r"^BEGIN_MADP_SOURCE path=(.+) encoding=base64 bytes=([0-9]+) sha256=([0-9a-f]{64})$"
)
SOURCE_END = re.compile(r"^END_MADP_SOURCE path=(.+)$")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_bundle(path: Path) -> tuple[dict[str, bytes], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    sources: dict[str, bytes] = {}
    errors: list[str] = []
    index = 0
    while index < len(lines):
        match = SOURCE_START.match(lines[index])
        if not match:
            index += 1
            continue
        source_path, expected_length_text, expected_hash = match.groups()
        expected_length = int(expected_length_text)
        index += 1
        encoded_lines: list[str] = []
        while index < len(lines) and not SOURCE_END.match(lines[index]):
            encoded_lines.append(lines[index].strip())
            index += 1
        if index >= len(lines):
            errors.append(f"unterminated source section: {source_path}")
            break
        end_match = SOURCE_END.match(lines[index])
        if end_match is None or end_match.group(1) != source_path:
            errors.append(f"mismatched source end marker: {source_path}")
        try:
            content = base64.b64decode("".join(encoded_lines), validate=True)
        except (binascii.Error, ValueError) as exc:
            errors.append(f"invalid Base64 source section: {source_path}: {exc}")
            content = b""
        if len(content) != expected_length:
            errors.append(f"source byte length mismatch: {source_path}")
        if sha256(content) != expected_hash:
            errors.append(f"source hash mismatch: {source_path}")
        if source_path in sources:
            errors.append(f"duplicate source section: {source_path}")
        sources[source_path] = content
        index += 1
    return sources, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    manifest: dict[str, Any] = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bundle_bytes = args.bundle.read_bytes()
    errors: list[str] = []
    if manifest.get("source_encoding") != "BASE64_RFC4648":
        errors.append("unexpected or missing source_encoding")
    if manifest.get("bundle_sha256") != sha256(bundle_bytes):
        errors.append("bundle SHA-256 mismatch")
    if manifest.get("bundle_byte_length") != len(bundle_bytes):
        errors.append("bundle byte length mismatch")

    sources, parse_errors = parse_bundle(args.bundle)
    errors.extend(parse_errors)
    expected_sources = manifest.get("sources", []) or []
    if len(sources) != len(expected_sources):
        errors.append("source count mismatch")
    for record in expected_sources:
        path = record.get("path")
        content = sources.get(path)
        if content is None:
            errors.append(f"missing source section: {path}")
            continue
        if record.get("sha256") != sha256(content):
            errors.append(f"manifest source hash mismatch: {path}")
        if record.get("byte_length") != len(content):
            errors.append(f"manifest source byte length mismatch: {path}")

    if errors:
        print("complete bundle: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"complete bundle: PASS sources={len(sources)} "
        f"bytes={len(bundle_bytes)} sha256={sha256(bundle_bytes)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
