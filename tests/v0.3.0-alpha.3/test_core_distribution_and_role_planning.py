#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import importlib.util
import subprocess
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

    three_service_config = config([
        service("A", "IG-A"),
        service("B", "IG-B"),
        service("C", "IG-A", known_correlations=["A"]),
    ])
    three_service_config["task"]["blind_initial_response_count"] = 3
    partially_independent = generator.build_plan(three_service_config)
    assert partially_independent["status"] == "DEGRADED"
    assert partially_independent["blind_first_round"]["assigned_service_ids"] == ["A", "B", "C"]
    assert partially_independent["blind_first_round"]["eligible_service_ids"] == ["A", "B"]
    assert partially_independent["blind_first_round"]["independence_group_count"] == 2
    assert checker.semantic_errors(partially_independent) == []

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

    tampered = deepcopy(distinct)
    tampered["assignments"][0]["service_id"] = "B"
    assert "NONDETERMINISTIC_OR_TAMPERED_PLAN" in checker.semantic_errors(tampered)

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

        frontmatter_out = temp / "frontmatter"
        compact_generator.write_bundle(frontmatter_out, "example/repo", commit, root=mock_root)
        bundle = frontmatter_out / compact_generator.BUNDLE_FILENAME
        manifest_path = frontmatter_out / compact_generator.MANIFEST_FILENAME
        altered = bundle.read_bytes().replace(
            f"source_commit: {commit}".encode("utf-8"),
            f"source_commit: {'b' + commit[1:]}".encode("utf-8"),
            1,
        )
        bundle.write_bytes(altered)
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["bundle_sha256"] = compact_generator.sha256(altered)
        manifest["bundle_bytes"] = len(altered)
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
            newline="\n",
        )
        assert "bundle YAML frontmatter does not match manifest" in compact_checker.check(
            frontmatter_out, "example/repo", commit, root=mock_root
        )

        bundle = out_a / compact_generator.BUNDLE_FILENAME
        data = bytearray(bundle.read_bytes())
        data[-10] ^= 1
        bundle.write_bytes(data)
        assert "bundle SHA-256 mismatch" in compact_checker.check(
            out_a, "example/repo", commit, root=mock_root
        )

        subprocess.run(["git", "init", "-q"], cwd=mock_root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=mock_root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=mock_root, check=True)
        subprocess.run(["git", "add", "."], cwd=mock_root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=mock_root, check=True)
        actual_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=mock_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        compact_generator.verify_git_head(mock_root, actual_commit)
        compact_generator.verify_git_sources(mock_root, actual_commit)
        first_source = mock_root / compact_generator.SOURCE_FILES[0][0]
        first_source.write_text("dirty source\n", encoding="utf-8")
        try:
            compact_generator.verify_git_sources(mock_root, actual_commit)
        except ValueError as exc:
            assert "working-tree source differs" in str(exc)
        else:
            raise AssertionError("dirty commit-bound source unexpectedly passed")

    print("alpha.3 Core distribution and role planning tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
