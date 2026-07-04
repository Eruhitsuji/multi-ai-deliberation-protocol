from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile

from madp_validation import ROOT, load_yaml_text


SCRIPT = ROOT / "scripts" / "generate_bootstrap_prompts.py"
CHECK_SCRIPT = ROOT / "scripts" / "check_generated_bootstrap.py"
FIXTURE_REPOSITORY = "ExampleOwner/madp-fixture"
FIXTURE_SHA = "0123456789abcdef0123456789abcdef01234567"
ENV_REPOSITORY = "ActualOwner/actual-repository"
ENV_SHA = "fedcba9876543210fedcba9876543210fedcba98"


def _base_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GITHUB_REPOSITORY", "GITHUB_SHA", "GITHUB_RUN_ID", "GITHUB_ACTIONS"):
        env.pop(name, None)
    return env


def _run(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        env=env or _base_env(),
        text=True,
        capture_output=True,
        check=False,
    )


def _check_generated(output_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT), str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def _manifest(output_dir: Path) -> dict[str, object]:
    path = output_dir / "bootstrap" / "manifest.yaml"
    data = load_yaml_text(path.read_text(encoding="utf-8"), str(path))
    return data["generated_bootstrap"]


def _assert_manifest(
    output_dir: Path,
    repository: str,
    sha: str,
    workflow_run_id: str,
    generated_by: str,
) -> None:
    manifest = _manifest(output_dir)
    expected = {
        "source_repository": repository,
        "source_commit": sha.lower(),
        "workflow_run_id": workflow_run_id,
        "generated_by": generated_by,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise AssertionError(f"{key}: expected {value!r}, got {manifest.get(key)!r}")


def _assert_no_text(output_dir: Path, forbidden: str) -> None:
    for path in (output_dir / "bootstrap").glob("*.md"):
        if forbidden in path.read_text(encoding="utf-8"):
            raise AssertionError(f"{path}: found forbidden text {forbidden!r}")


def _expect_success(name: str, args: list[str], env: dict[str, str], expected: tuple[str, str, str, str]) -> None:
    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-") as directory:
        output_dir = Path(directory)
        result = _run([str(output_dir), *args], env)
        if result.returncode != 0:
            raise AssertionError(f"{name}: expected success, got {result.returncode}: {result.stderr}")
        _check_generated(output_dir)
        _assert_manifest(output_dir, *expected)
        print(f"generator test: {name} PASS")


def _expect_failure(name: str, args: list[str], env: dict[str, str]) -> None:
    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-") as directory:
        output_dir = Path(directory)
        result = _run([str(output_dir), *args], env)
        if result.returncode == 0:
            raise AssertionError(f"{name}: expected failure, got success")
        print(f"generator test: {name} PASS")


def main() -> int:
    _expect_success(
        "cli arguments only",
        [
            "--repository",
            FIXTURE_REPOSITORY,
            "--commit-sha",
            FIXTURE_SHA.upper(),
            "--workflow-run-id",
            "LOCAL_FIXTURE_RUN",
            "--generated-by",
            "LOCAL",
        ],
        _base_env(),
        (FIXTURE_REPOSITORY, FIXTURE_SHA, "LOCAL_FIXTURE_RUN", "LOCAL"),
    )

    env = _base_env()
    env.update(
        {
            "GITHUB_REPOSITORY": ENV_REPOSITORY,
            "GITHUB_SHA": ENV_SHA,
            "GITHUB_RUN_ID": "ENV_RUN",
            "GITHUB_ACTIONS": "true",
        }
    )
    _expect_success(
        "github environment fallback",
        [],
        env,
        (ENV_REPOSITORY, ENV_SHA, "ENV_RUN", "GitHub Actions"),
    )

    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-") as directory:
        output_dir = Path(directory)
        env = _base_env()
        env.update(
            {
                "GITHUB_REPOSITORY": ENV_REPOSITORY,
                "GITHUB_SHA": ENV_SHA,
                "GITHUB_RUN_ID": "ENV_RUN",
                "GITHUB_ACTIONS": "true",
            }
        )
        result = _run(
            [
                str(output_dir),
                "--repository",
                FIXTURE_REPOSITORY,
                "--commit-sha",
                FIXTURE_SHA,
                "--workflow-run-id",
                "CLI_RUN",
                "--generated-by",
                "LOCAL",
            ],
            env,
        )
        if result.returncode != 0:
            raise AssertionError(f"cli priority: expected success, got {result.returncode}: {result.stderr}")
        _check_generated(output_dir)
        _assert_manifest(output_dir, FIXTURE_REPOSITORY, FIXTURE_SHA, "CLI_RUN", "LOCAL")
        _assert_no_text(output_dir, ENV_REPOSITORY)
        _assert_no_text(output_dir, ENV_SHA)
        print("generator test: cli arguments override GitHub environment PASS")

    env = _base_env()
    env.update({"GITHUB_REPOSITORY": ENV_REPOSITORY, "GITHUB_SHA": ENV_SHA})
    _expect_failure(
        "empty cli repository does not fallback",
        ["--repository", "", "--commit-sha", FIXTURE_SHA],
        env,
    )
    _expect_failure(
        "invalid repository",
        ["--repository", "bad/repo/extra", "--commit-sha", FIXTURE_SHA],
        _base_env(),
    )
    _expect_failure(
        "invalid sha",
        ["--repository", FIXTURE_REPOSITORY, "--commit-sha", "not-a-sha"],
        _base_env(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
