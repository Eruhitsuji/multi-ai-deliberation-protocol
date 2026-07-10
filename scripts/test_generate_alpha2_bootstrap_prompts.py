from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile

from madp_validation import ROOT, load_yaml_text
import generate_alpha2_bootstrap_prompts as generator

SCRIPT = ROOT / "scripts" / "generate_alpha2_bootstrap_prompts.py"
CHECK = ROOT / "scripts" / "check_generated_alpha2_bootstrap.py"
REPOSITORY = "ExampleOwner/madp-alpha2-fixture"
SHA = "0123456789abcdef0123456789abcdef01234567"
RUN_ID = "ALPHA2_LOCAL_TEST"
EXPECTED_ALPHA2_BOOTSTRAP_FILES = [
    "use-madp-commands.md",
    "share-context-with-ai.md",
    "request-review.md",
    "use-madp-for-ai-driven-development.md",
]


def env_clean() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GITHUB_REPOSITORY", "GITHUB_SHA", "GITHUB_RUN_ID", "GITHUB_ACTIONS"):
        env.pop(name, None)
    return env


def run_generator(output: Path, env: dict[str, str] | None = None):
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
    if generator.PROTOCOL_VERSION != "MADP-v0.3.0-alpha.2":
        raise AssertionError("alpha.2 generator protocol version mismatch")
    if generator.ALPHA2_BOOTSTRAP_FILES != EXPECTED_ALPHA2_BOOTSTRAP_FILES:
        raise AssertionError("alpha.2 bootstrap file list mismatch")

    with tempfile.TemporaryDirectory(prefix="madp-alpha2-bootstrap-") as directory:
        output = Path(directory)
        result = run_generator(output)
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        check(output)

        manifest = load_yaml_text(
            (output / "bootstrap" / "alpha2-manifest.yaml").read_text(encoding="utf-8"),
            "alpha2 generated manifest",
        )["generated_alpha2_bootstrap"]
        if manifest["protocol_version"] != generator.PROTOCOL_VERSION:
            raise AssertionError("manifest protocol_version mismatch")
        if manifest["source_repository"] != REPOSITORY:
            raise AssertionError("manifest source_repository mismatch")
        if manifest["source_commit"] != SHA:
            raise AssertionError("manifest source_commit mismatch")
        if manifest["status"] != "draft implementation aid":
            raise AssertionError("manifest status mismatch")
        if [item["path"] for item in manifest["files"]] != [f"bootstrap/{name}" for name in EXPECTED_ALPHA2_BOOTSTRAP_FILES]:
            raise AssertionError("manifest alpha.2 file list mismatch")

        generated = read_all(output)
        for name in generator.ALPHA2_BOOTSTRAP_FILES:
            text = generated[f"bootstrap/{name}"]
            if generator.PROTOCOL_VERSION not in text:
                raise AssertionError(f"missing alpha.2 version marker in {name}")
            if "Generated alpha.2 draft prompt" not in text:
                raise AssertionError(f"missing generated metadata in {name}")
        if "AI_DEVELOPMENT_STATUS" not in generated["bootstrap/use-madp-for-ai-driven-development.md"]:
            raise AssertionError("generated AI development prompt missing status marker")
        if "complete-protocol-bundle.txt" in "\n".join(generated):
            raise AssertionError("alpha.2 draft generator must not emit alpha.1 complete bundle")

    with tempfile.TemporaryDirectory(prefix="madp-alpha2-bootstrap-a-") as first, tempfile.TemporaryDirectory(prefix="madp-alpha2-bootstrap-b-") as second:
        first_path = Path(first)
        second_path = Path(second)
        if run_generator(first_path).returncode != 0 or run_generator(second_path).returncode != 0:
            raise AssertionError("deterministic generation setup failed")
        if read_all(first_path) != read_all(second_path):
            raise AssertionError("same inputs produced different alpha.2 generated output")

    env = env_clean()
    env.update(
        {
            "GITHUB_REPOSITORY": "ActualOwner/actual-alpha2-repository",
            "GITHUB_SHA": "fedcba9876543210fedcba9876543210fedcba98",
            "GITHUB_RUN_ID": "ALPHA2_ENV_RUN",
            "GITHUB_ACTIONS": "true",
        }
    )
    with tempfile.TemporaryDirectory(prefix="madp-alpha2-bootstrap-env-") as directory:
        output = Path(directory)
        result = subprocess.run([sys.executable, str(SCRIPT), str(output)], cwd=ROOT, env=env, text=True, capture_output=True)
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        check(output)
        manifest = load_yaml_text(
            (output / "bootstrap" / "alpha2-manifest.yaml").read_text(encoding="utf-8"),
            "environment alpha2 manifest",
        )["generated_alpha2_bootstrap"]
        if manifest["source_repository"] != "ActualOwner/actual-alpha2-repository":
            raise AssertionError("environment repository fallback failed")
        if manifest["generated_by"] != "GitHub Actions":
            raise AssertionError("environment generated_by fallback failed")

    print("bootstrap generator tests: MADP-v0.3.0-alpha.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
