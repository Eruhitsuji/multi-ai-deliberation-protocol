from __future__ import annotations

import sys

from jsonschema.exceptions import ValidationError

from madp_validation import ROOT, iter_yaml_cases, load_expected_code, load_schema, load_yaml, make_validator, rel, schema_error_codes


def main() -> int:
    schema = load_schema()
    validator = make_validator(schema)
    print("schema: Draft202012Validator.check_schema PASS")

    valid_dir = ROOT / "tests" / "valid"
    valid_cases = list(iter_yaml_cases(valid_dir))
    if not valid_cases:
        print(f"{rel(valid_dir)}: no valid cases found", file=sys.stderr)
        return 1
    for case in valid_cases:
        validator.validate(load_yaml(case))
        print(f"valid: {rel(case)} PASS")

    invalid_dir = ROOT / "tests" / "invalid"
    invalid_cases = list(iter_yaml_cases(invalid_dir))
    if not invalid_cases:
        print(f"{rel(invalid_dir)}: no invalid cases found", file=sys.stderr)
        return 1
    for case in invalid_cases:
        instance = load_yaml(case)
        errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))
        if not errors:
            print(f"{rel(case)}: expected schema failure, got PASS", file=sys.stderr)
            return 1
        expected = load_expected_code(case)
        actual_codes = set()
        for error in errors:
            actual_codes.update(schema_error_codes(error))
        if expected not in actual_codes:
            print(
                f"{rel(case)}: expected {expected}, got {sorted(actual_codes)}",
                file=sys.stderr,
            )
            return 1
        print(f"invalid: {rel(case)} PASS ({expected})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

