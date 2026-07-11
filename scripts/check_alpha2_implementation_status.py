#!/usr/bin/env python3
from __future__ import annotations

import json

from madp_validation import ROOT, load_yaml

STATUS = ROOT / "docs" / "planning" / "MADP-v0.3.0-alpha.2-implementation-status.yaml"
EXPECTED_IDS = {f"TODO-CMD-{index:03d}" for index in range(1, 10)}


def main() -> int:
    data = load_yaml(STATUS)
    errors: list[str] = []
    items = data.get("items", [])
    by_id = {item.get("todo_id"): item for item in items}

    if data.get("protocol_version") != "MADP-v0.3.0-alpha.2":
        errors.append("protocol_version mismatch")
    if data.get("implementation_status") != "RELEASE_CANDIDATE_READY":
        errors.append("implementation_status must be RELEASE_CANDIDATE_READY")
    if data.get("integration_status") != "MERGED_TO_MAIN":
        errors.append("integration_status must be MERGED_TO_MAIN")
    if data.get("release_ready") is not True:
        errors.append("release_ready must be true")
    if data.get("tagged") is not False:
        errors.append("tagged must remain false before publication")
    if data.get("published") is not False:
        errors.append("published must remain false before publication")
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
        "release_ready": data.get("release_ready"),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
