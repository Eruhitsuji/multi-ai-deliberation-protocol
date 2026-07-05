from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile

from madp_validation import ROOT, load_yaml_text
import generate_bootstrap_prompts as generator

SCRIPT = ROOT / "scripts" / "generate_bootstrap_prompts.py"
CHECK = ROOT / "scripts" / "check_generated_bootstrap.py"
REPOSITORY = "ExampleOwner/madp-fixture"
SHA = "0123456789abcdef0123456789abcdef01234567"
RUN_ID = "ALPHA1_LOCAL_TEST"


def env_clean() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GITHUB_REPOSITORY", "GITHUB_SHA", "GITHUB_RUN_ID", "GITHUB_ACTIONS"):
        env.pop(name, None)
    return env


def run_generator(output: Path, extra: list[str] | None = None, env: dict[str, str] | None = None):
    args = [
        sys.executable,
        str(SCRIPT),
        str(output),
        "--repository",
        REPOSITORY,
        "--commit-sha",
        SHA,
        "--workflow-run-id",
        RUN_ID,
        "--generated-by",
        "LOCAL",
    ]
    if extra:
        args.extend(extra)
    return subprocess.run(args, cwd=ROOT, env=env or env_clean(), text=True, capture_output=True)


def check(output: Path) -> None:
    result = subprocess.run([sys.executable, str(CHECK), str(output)], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def read_all(output: Path) -> dict[str, str]:
    return {
        str(path.relative_to(output)).replace("\\", "/"): path.read_text(encoding="utf-8")
        for path in sorted(output.rglob("*"))
        if path.is_file()
    }


def main() -> int:
    if generator.PROTOCOL_VERSION != "MADP-v0.3.0-alpha.1":
        raise AssertionError("generator protocol version mismatch")
    if len(generator.CANONICAL_BUNDLE_FILES) != 7:
        raise AssertionError("alpha.1 bootstrap must contain seven canonical files")

    with tempfile.TemporaryDirectory(prefix="madp-alpha-bootstrap-") as directory:
        output = Path(directory)
        result = run_generator(output)
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        check(output)

        manifest = load_yaml_text(
            (output / "bootstrap" / "manifest.yaml").read_text(encoding="utf-8"),
            "generated manifest",
        )["generated_bootstrap"]
        if manifest["protocol_version"] != generator.PROTOCOL_VERSION:
            raise AssertionError("manifest protocol_version mismatch")
        if manifest["source_repository"] != REPOSITORY:
            raise AssertionError("manifest source_repository mismatch")
        if manifest["source_commit"] != SHA:
            raise AssertionError("manifest source_commit mismatch")

        bundle = (output / "bootstrap" / "complete-protocol-bundle.txt").read_text(encoding="utf-8")
        if f"canonical_file_count: {len(generator.CANONICAL_BUNDLE_FILES)}" not in bundle:
            raise AssertionError("bundle canonical_file_count mismatch")
        for path in generator.CANONICAL_BUNDLE_FILES:
            if f"BEGIN_FILE: {path}" not in bundle or f"END_FILE: {path}" not in bundle:
                raise AssertionError(f"bundle missing boundary for {path}")
        if "MADP-v0.2.5-rc.2" in (output / "bootstrap" / "load-protocol-from-github.md").read_text(encoding="utf-8"):
            raise AssertionError("generated load prompt still references rc.2")

    with tempfile.TemporaryDirectory(prefix="madp-alpha-bootstrap-a-") as first, tempfile.TemporaryDirectory(prefix="madp-alpha-bootstrap-b-") as second:
        first_path = Path(first)
        second_path = Path(second)
        if run_generator(first_path).returncode != 0 or run_generator(second_path).returncode != 0:
            raise AssertionError("deterministic generation setup failed")
        if read_all(first_path) != read_all(second_path):
            raise AssertionError("same inputs produced different generated output")

    env = env_clean()
    env.update(
        {
            "GITHUB_REPOSITORY": "ActualOwner/actual-repository",
            "GITHUB_SHA": "fedcba9876543210fedcba9876543210fedcba98",
            "GITHUB_RUN_ID": "ENV_RUN",
            "GITHUB_ACTIONS": "true",
        }
    )
    with tempfile.TemporaryDirectory(prefix="madp-alpha-bootstrap-env-") as directory:
        output = Path(directory)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(output)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        check(output)
        manifest = load_yaml_text(
            (output / "bootstrap" / "manifest.yaml").read_text(encoding="utf-8"),
            "environment manifest",
        )["generated_bootstrap"]
        if manifest["source_repository"] != "ActualOwner/actual-repository":
            raise AssertionError("environment repository fallback failed")
        if manifest["generated_by"] != "GitHub Actions":
            raise AssertionError("environment generated_by fallback failed")

    print("bootstrap generator tests: MADP-v0.3.0-alpha.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
