#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import importlib.util
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def capabilities(**overrides):
    result = {
        "facilitation": True,
        "generation": True,
        "critique": True,
        "evidence_review": True,
        "recording": True,
        "exact_file_reading": True,
        "web_research": True,
        "code_execution": False,
        "long_context": True,
    }
    result.update(overrides)
    return result


def service(service_id: str, group: str, **overrides):
    row = {
        "service_id": service_id,
        "provider": "Fixture Provider",
        "model_label": "Fixture Model",
        "chat_context_id": f"CHAT-{service_id}",
        "independence_group": group,
        "availability": "AVAILABLE",
        "usage_preference": "NORMAL",
        "cost_mode": "SUBSCRIPTION",
        "capabilities": capabilities(),
        "known_correlations": [],
    }
    row.update(overrides)
    return row


def config(services):
    return {
        "plan_id": "ROLE-PLAN-TEST",
        "task": {
            "task_id": "TASK-TEST",
            "title": "Fixture task",
            "required_roles": ["FACILITATOR", "PROPOSER", "CRITIC", "EVIDENCE_REVIEWER", "RECORDER"],
            "blind_first_round_required": True,
            "blind_initial_response_count": 2,
        },
        "services": services,
    }


def main() -> int:
    generator = load_module(
        "dynamic_role_generator",
        ROOT / "scripts/generate_alpha3_dynamic_role_plan.py",
    )
    import sys
    sys.modules["generate_alpha3_dynamic_role_plan"] = generator
    checker = load_module(
        "dynamic_role_checker",
        ROOT / "scripts/check_alpha3_dynamic_role_plan.py",
    )
    compact_generator = load_module(
        "compact_generator",
        ROOT / "scripts/generate_alpha3_core_compact_bundle.py",
    )
    sys.modules["generate_alpha3_core_compact_bundle"] = compact_generator
    compact_checker = load_module(
        "compact_checker",
        ROOT / "scripts/check_alpha3_core_compact_bundle.py",
    )

    distinct = generator.build_plan(config([service("A", "IG-A"), service("B", "IG-B")]))
    assert distinct["status"] == "READY"
    assert distinct["blind_first_round"]["status"] == "PLAN_VALID"
    assert checker.semantic_errors(distinct) == []

    same_group = generator.build_plan(config([service("A", "IG-SAME"), service("B", "IG-SAME")]))
    assert same_group["status"] == "DEGRADED"
    assert same_group["blind_first_round"]["status"] == "PLAN_DEGRADED"
    assert checker.semantic_errors(same_group) == []

    missing_recorder = config([
        service("A", "IG-A", capabilities=capabilities(recording=False)),
        service("B", "IG-B", capabilities=capabilities(recording=False)),
    ])
    draft = generator.build_plan(missing_recorder)
    assert draft["status"] == "DRAFT"
    assert "RECORDER" in draft["unfilled_roles"]
    assert checker.semantic_errors(draft) == []

    tampered = deepcopy(distinct)
    tampered["approval_authority_granted"] = True
    assert "APPROVAL_AUTHORITY_MUST_REMAIN_FALSE" in checker.semantic_errors(tampered)

    tampered = deepcopy(distinct)
    tampered["blind_first_round"]["eligible_service_ids"] = ["A"]
    assert "BLIND_ELIGIBLE_RECOMPUTE_MISMATCH" in checker.semantic_errors(tampered)

    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        mock_root = temp / "repo"
        for relative, _role in compact_generator.SOURCE_FILES:
            path = mock_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture source: {relative}\n", encoding="utf-8")
        out_a = temp / "a"
        out_b = temp / "b"
        commit = "a" * 40
        compact_generator.write_bundle(out_a, "example/repo", commit, root=mock_root)
        compact_generator.write_bundle(out_b, "example/repo", commit, root=mock_root)
        files_a = {item.name: item.read_bytes() for item in out_a.iterdir()}
        files_b = {item.name: item.read_bytes() for item in out_b.iterdir()}
        assert files_a == files_b
        assert compact_checker.check(out_a, "example/repo", commit, root=mock_root) == []
        bundle = out_a / compact_generator.BUNDLE_FILENAME
        data = bytearray(bundle.read_bytes())
        data[-10] ^= 1
        bundle.write_bytes(data)
        assert "bundle SHA-256 mismatch" in compact_checker.check(
            out_a, "example/repo", commit, root=mock_root
        )

    print("alpha.3 Core distribution and role planning tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
