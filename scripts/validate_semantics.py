from __future__ import annotations

import sys

from madp_validation import ROOT, iter_yaml_cases, load_expected_code, load_yaml, make_validator, rel, semantic_errors


def _check_no_semantic_errors(label: str, instance: dict) -> bool:
    errors = semantic_errors(instance)
    if errors:
        print(f"{label}: unexpected semantic errors:", file=sys.stderr)
        for error in errors:
            print(f"  {error.code} at {error.path}: {error.message}", file=sys.stderr)
        return False
    return True


def main() -> int:
    validator = make_validator()

    for case in iter_yaml_cases(ROOT / "tests" / "valid"):
        instance = load_yaml(case)
        validator.validate(instance)
        if not _check_no_semantic_errors(rel(case), instance):
            return 1
        print(f"semantic valid: {rel(case)} PASS")

    semantic_cases = list(iter_yaml_cases(ROOT / "tests" / "semantic"))
    if not semantic_cases:
        print("tests/semantic: no semantic cases found", file=sys.stderr)
        return 1
    for case in semantic_cases:
        instance = load_yaml(case)
        validator.validate(instance)
        expected = load_expected_code(case)
        actual = semantic_errors(instance)
        actual_codes = {error.code for error in actual}
        if expected not in actual_codes:
            print(f"{rel(case)}: expected {expected}, got {sorted(actual_codes)}", file=sys.stderr)
            return 1
        print(f"semantic invalid: {rel(case)} PASS ({expected})")

    # The schema should catch this invariant, but the semantic validator must also know it.
    active_facilitator_case = ROOT / "tests" / "invalid" / "two-active-facilitators.yaml"
    if active_facilitator_case.exists():
        instance = load_yaml(active_facilitator_case)
        actual_codes = {error.code for error in semantic_errors(instance)}
        if "MULTIPLE_ACTIVE_FACILITATORS" not in actual_codes:
            print(
                f"{rel(active_facilitator_case)}: semantic validator did not report MULTIPLE_ACTIVE_FACILITATORS",
                file=sys.stderr,
            )
            return 1
        print(f"semantic invariant: {rel(active_facilitator_case)} PASS (MULTIPLE_ACTIVE_FACILITATORS)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

