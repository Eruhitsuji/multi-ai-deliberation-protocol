#!/usr/bin/env python3
from __future__ import annotations

import json

from madp_validation import ROOT, load_yaml

STATUS = ROOT / "docs" / "planning" / "MADP-v0.3.0-alpha.2-implementation-status.yaml"
EXPECTED_IDS = {f"TODO-CMD-{index:03d}" for index in range(1, 10)}
EXPECTED_RELEASE_COMMIT = "207e24290e0a66bf0dd34e13f9b3525a42a5a6c9"
EXPECTED_RELEASE_TAG = "MADP-v0.3.0-alpha.2"


def main() -> int:
    data = load_yaml(STATUS)
    errors: list[str] = []
    items = data.get("items", [])
    by_id = {item.get("todo_id"): item for item in items}

    expected = {
        "protocol_version": EXPECTED_RELEASE_TAG,
        "implementation_status": "PUBLISHED_PRERELEASE",
        "integration_status": "MERGED_TO_MAIN",
        "release_ready": True,
        "tagged": True,
        "published": True,
        "release_tag": EXPECTED_RELEASE_TAG,
        "release_commit": EXPECTED_RELEASE_COMMIT,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key} mismatch: {data.get(key)!r}")

    if not data.get("published_at"):
        errors.append("published_at is required; use UNKNOWN when the authoritative timestamp is unavailable")
    if not data.get("publication_basis"):
        errors.append("publication_basis is required")
    if set(by_id) != EXPECTED_IDS:
        errors.append(f"TODO set mismatch: {sorted(set(by_id) ^ EXPECTED_IDS)}")

    for todo_id in sorted(EXPECTED_IDS):
        item = by_id.get(todo_id, {})
        if item.get("status") != "DONE":
            errors.append(f"{todo_id}: status must be DONE")
        if not item.get("completion_basis"):
            errors.append(f"{todo_id}: completion_basis is required")

    print(json.dumps({
        "suite": "alpha.2 implementation status",
        "result": "FAIL" if errors else "PASS",
        "completed_items": len(items),
        "implementation_status": data.get("implementation_status"),
        "release_tag": data.get("release_tag"),
        "release_commit": data.get("release_commit"),
        "published_at": data.get("published_at"),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
