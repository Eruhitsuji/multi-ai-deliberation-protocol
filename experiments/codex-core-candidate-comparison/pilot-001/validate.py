#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import sys
import yaml
from jsonschema import Draft202012Validator

PILOT_DIR = Path(__file__).resolve().parent
ROOT = PILOT_DIR.parents[2]
SCHEMA_PATH = ROOT / "schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml"
EXPERIMENT_PATH = PILOT_DIR / "experiment.yaml"
TASK_PATH = PILOT_DIR / "task/prompt.md"
BASELINE_COMMIT = "2a29ddfebe4d9664d3a4043a01d8728fa525d049"

sys.path.insert(0, str(ROOT / "scripts"))
from check_alpha3_core_candidate_experiments import comparison_semantic_errors  # noqa: E402


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    problems: list[str] = []

    schema = load_yaml(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    experiment = load_yaml(EXPERIMENT_PATH)

    validator = Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(experiment), key=lambda error: list(error.path))
    problems.extend(
        f"SCHEMA:{'/'.join(map(str, error.path)) or '<root>'}:{error.message}"
        for error in schema_errors
    )
    problems.extend(f"SEMANTIC:{item}" for item in comparison_semantic_errors(experiment))

    if experiment.get("formal_release_evidence") is not False:
        problems.append("BOUNDARY:formal_release_evidence must remain false")
    if experiment.get("conclusion", {}).get("alpha4_authorized") is not False:
        problems.append("BOUNDARY:alpha4_authorized must remain false")

    task = experiment.get("task", {})
    recorded_task_hash = task.get("prompt_sha256")
    actual_task_hash = sha256(TASK_PATH)
    task_text = TASK_PATH.read_text(encoding="utf-8")
    task_frozen = "Task status: `FROZEN`" in task_text

    if recorded_task_hash is not None and recorded_task_hash != actual_task_hash:
        problems.append("TASK:prompt_sha256 does not match task/prompt.md")
    if experiment.get("experiment_status") in {"READY_FOR_REVIEW", "HUMAN_REVIEWED"}:
        if not task_frozen:
            problems.append("TASK:ready experiment requires Task status FROZEN")
        if recorded_task_hash != actual_task_hash:
            problems.append("TASK:ready experiment requires the exact prompt hash")

    runs = experiment.get("runs", [])
    workflow_runs = {item.get("workflow"): item for item in runs if isinstance(item, dict)}
    for workflow in ("STANDARD_ALPHA3", "ALPHA3_CORE_CANDIDATE", "MARKDOWN_VALIDATOR"):
        run = workflow_runs.get(workflow)
        if run and run.get("tested_commit") != BASELINE_COMMIT:
            problems.append(f"BASELINE:{workflow} tested_commit must equal {BASELINE_COMMIT}")

    if problems:
        for problem in sorted(set(problems)):
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("Codex Core Candidate comparison pilot: PASS")
    print(f"task_sha256={actual_task_hash}")
    print(f"experiment_status={experiment.get('experiment_status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
