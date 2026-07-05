#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "migration"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def state(doc):
    return doc.get("session_state", {}) if isinstance(doc, dict) else {}


def target(directory: Path):
    for name in ("expected-target.yaml", "proposed-invalid-target.yaml", "proposed-downcast-target.yaml"):
        path = directory / name
        if path.exists():
            return load(path)
    return {}


def errors_for(directory: Path, fixture_id: str):
    source = load(directory / "source.yaml") if (directory / "source.yaml").exists() else {}
    result = target(directory)
    evidence = load(directory / "evidence.yaml") if (directory / "evidence.yaml").exists() else {}
    errors = []

    if fixture_id == "MIG-FIX-002":
        unknown = {item.get("item_id") for item in evidence.get("entries", []) if item.get("provenance_status") == "UNKNOWN"}
        grants = state(result).get("permission_grants", [])
        if any(item.get("id") in unknown and item.get("assurance_origin") == "USER_ACTION" for item in grants):
            errors.append("MIG_FABRICATED_PROVENANCE")

    if fixture_id == "MIG-FIX-005":
        def active(doc):
            return [p for p in state(doc).get("participants", []) if p.get("type") == "FACILITATOR" and p.get("status") == "ACTIVE"]
        if len(active(source)) > 1 and len(active(result)) == 1:
            errors.append("MIG_AUTOMATIC_FACILITATOR_RESOLUTION")

    if fixture_id == "MIG-FIX-008":
        relay = result.get("relay_block", {})
        digest = relay.get("snapshot_digest", {})
        if relay.get("integrity_claim") == "PRE_INGRESS_TRANSPORT_VERIFIED" and digest.get("provenance") == "POST_INGRESS_BASELINE":
            errors.append("MIG_FALSE_DIGEST_PROVENANCE")

    if fixture_id == "MIG-FIX-009" and state(result).get("meta", {}).get("protocol_version") != "0.3.0-alpha.1":
        errors.append("MIG_VERSION_NOT_UPDATED")

    if fixture_id == "MIG-FIX-010":
        if state(source).get("meta", {}).get("protocol_version") == "0.3.0-alpha.1" and state(result).get("meta", {}).get("protocol_version") == "0.2.5-rc.2":
            errors.append("MIG_UNSAFE_OFFICIAL_DOWNCAST")

    return sorted(errors)


def main():
    rows = []
    failed = False
    for directory in sorted(p for p in FIXTURES.iterdir() if p.is_dir()):
        manifest = load(directory / "manifest.yaml")
        expected = sorted(manifest.get("expected_semantic_errors", []) or [])
        actual = errors_for(directory, manifest.get("fixture_id"))
        matched = expected == actual
        failed = failed or not matched
        rows.append({"fixture_id": manifest.get("fixture_id"), "expected": expected, "actual": actual, "matched": matched})
    print(json.dumps({"suite_result": "FAIL" if failed else "PASS", "results": rows}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
