from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator

from madp_validation import ROOT, load_yaml, rel


CASES = [
    (
        ROOT / "schemas" / "v0.3.0-alpha.2" / "command.schema.yaml",
        ROOT / "fixtures" / "v0.3.0-alpha.2" / "command",
    ),
    (
        ROOT / "schemas" / "v0.3.0-alpha.2" / "todo.schema.yaml",
        ROOT / "fixtures" / "v0.3.0-alpha.2" / "todo",
    ),
    (
        ROOT / "schemas" / "v0.3.0-alpha.2" / "context-package.schema.yaml",
        ROOT / "fixtures" / "v0.3.0-alpha.2" / "context-package",
    ),
]


def iter_fixture_files(directory: Path):
    return sorted(path for path in directory.glob("*.y*ml") if path.is_file())


def validate_valid_cases(validator: Draft202012Validator, directory: Path) -> int:
    count = 0
    for path in iter_fixture_files(directory):
        instance = load_yaml(path)
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        if errors:
            details = "\n".join(
                f"  - {rel(path)}: {'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}"
                for error in errors
            )
            raise SystemExit(f"expected valid fixture failed validation:\n{details}")
        count += 1
    if count == 0:
        raise SystemExit(f"no valid fixtures found in {rel(directory)}")
    return count


def validate_invalid_cases(validator: Draft202012Validator, directory: Path) -> int:
    count = 0
    for path in iter_fixture_files(directory):
        instance = load_yaml(path)
        errors = list(validator.iter_errors(instance))
        if not errors:
            raise SystemExit(f"expected invalid fixture passed validation: {rel(path)}")
        count += 1
    if count == 0:
        raise SystemExit(f"no invalid fixtures found in {rel(directory)}")
    return count


def main() -> int:
    total_valid = 0
    total_invalid = 0
    for schema_path, fixture_root in CASES:
        schema = load_yaml(schema_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        total_valid += validate_valid_cases(validator, fixture_root / "valid")
        total_invalid += validate_invalid_cases(validator, fixture_root / "invalid")

    print("alpha.2 command/context/TODO fixtures: PASS")
    print(f"valid fixtures: {total_valid}")
    print(f"invalid fixtures: {total_invalid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
