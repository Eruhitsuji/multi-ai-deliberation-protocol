#!/usr/bin/env python3
from __future__ import annotations

import json

from madp_validation import ROOT, load_yaml
from todo_transitions_v030_alpha2 import ALLOWED_TRANSITIONS

CASES = ROOT / "tests" / "todo-lifecycle-v0.3.0-alpha.2" / "cases.yaml"


def evaluate(case: dict) -> tuple[str, list[str]]:
    reasons: list[str] = []
    source = case["from"]
    target = case["to"]
    operation = case["operation"]

    if operation == "todo-promote":
        if not case.get("confirmation_ref"):
            reasons.append("TODO_PROMOTE_REQUIRES_USER_CONFIRMATION")
    else:
        if target not in ALLOWED_TRANSITIONS.get(source, set()):
            reasons.append(f"TODO_INVALID_STATUS_TRANSITION:{source}->{target}")
        if target == "DONE":
            if operation != "todo-done":
                reasons.append("TODO_DONE_REQUIRES_TODO_DONE_COMMAND")
            if not case.get("completion_basis"):
                reasons.append("TODO_DONE_REQUIRES_COMPLETION_BASIS")

    return ("DENY" if reasons else "ALLOW"), reasons


def main() -> int:
    document = load_yaml(CASES)
    failures: list[dict] = []
    results: list[dict] = []
    for case in document["cases"]:
        actual, reasons = evaluate(case)
        matched = actual == case["expected"]
        result = {
            "case_id": case["case_id"],
            "expected": case["expected"],
            "actual": actual,
            "reasons": reasons,
            "result": "PASS" if matched else "FAIL",
        }
        results.append(result)
        if not matched:
            failures.append(result)

    print(json.dumps({"suite": "alpha.2 TODO lifecycle", "result": "FAIL" if failures else "PASS", "cases": results}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
