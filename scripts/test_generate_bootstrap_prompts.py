from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import re

from madp_validation import ROOT, load_yaml_text
import generate_bootstrap_prompts as generator


SCRIPT = ROOT / "scripts" / "generate_bootstrap_prompts.py"
CHECK_SCRIPT = ROOT / "scripts" / "check_generated_bootstrap.py"
FIXTURE_REPOSITORY = "ExampleOwner/madp-fixture"
FIXTURE_SHA = "0123456789abcdef0123456789abcdef01234567"
FIXTURE_RUN_ID = "RC2_LOCAL_TEST"
FIXTURE_BUNDLE_URL = "https://ExampleOwner.github.io/madp-fixture/bootstrap/complete-protocol-bundle.txt"
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


def _bundle_manifest(output_dir: Path) -> dict[str, object]:
    path = output_dir / "bootstrap" / "complete-protocol-bundle.manifest.yaml"
    data = load_yaml_text(path.read_text(encoding="utf-8"), str(path))
    return data["complete_protocol_bundle"]


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


def _assert_bundle_outputs(output_dir: Path) -> None:
    bundle_path = output_dir / "bootstrap" / "complete-protocol-bundle.txt"
    if not bundle_path.exists():
        raise AssertionError("complete protocol bundle was not generated")
    bundle = bundle_path.read_text(encoding="utf-8")
    expected_metadata = "\n".join(
        [
            "BEGIN_MADP_BUNDLE_METADATA",
            f"bundle_format: {generator.BUNDLE_FORMAT}",
            f"protocol_version: {generator.PROTOCOL_VERSION}",
            f"source_repository: {FIXTURE_REPOSITORY}",
            f"source_commit: {FIXTURE_SHA}",
            f"canonical_file_count: {len(generator.CANONICAL_BUNDLE_FILES)}",
            "END_MADP_BUNDLE_METADATA",
            "",
            "BEGIN_FILE: README.md",
        ]
    )
    if not bundle.startswith(expected_metadata):
        raise AssertionError("bundle metadata envelope does not contain expected fixture provenance")
    required_boundaries = [
        "BEGIN_FILE: protocol/MADP-v0.2.5-rc.2.md",
        "BEGIN_FILE: protocol/GLOSSARY-v0.2.5-rc.2.md",
        "BEGIN_FILE: schemas/session-state-v0.2.5-rc.2.schema.yaml",
    ]
    for boundary in required_boundaries:
        if boundary not in bundle:
            raise AssertionError(f"bundle missing rc.2 boundary {boundary!r}")
    disallowed_rc1_paths = [
        "protocol/MADP-v0.2.5-rc.1.md",
        "protocol/GLOSSARY-v0.2.5-rc.1.md",
        "schemas/session-state-v0.2.5-rc.1.schema.yaml",
    ]
    for disallowed_path in disallowed_rc1_paths:
        if disallowed_path in bundle:
            raise AssertionError(f"bundle contains rc.1 canonical path {disallowed_path!r}")
    index = (output_dir / "index.html").read_text(encoding="utf-8")
    if "bootstrap/complete-protocol-bundle.txt" not in index:
        raise AssertionError("index.html does not link to complete protocol bundle")
    if "bootstrap/complete-protocol-bundle.manifest.yaml" not in index:
        raise AssertionError("index.html does not link to complete protocol bundle manifest")
    recovery = (output_dir / "bootstrap" / "recover-from-load-failure.md").read_text(encoding="utf-8")
    if FIXTURE_BUNDLE_URL not in recovery:
        raise AssertionError("recovery prompt does not contain resolved fixture bundle URL")
    manifest = _manifest(output_dir)
    bundle_entries = [
        entry
        for entry in manifest.get("files", [])
        if isinstance(entry, dict) and entry.get("path") == "bootstrap/complete-protocol-bundle.txt"
    ]
    if len(bundle_entries) != 1:
        raise AssertionError(f"expected one bundle manifest entry, got {len(bundle_entries)}")
    if bundle_entries[0].get("source_files") != generator.CANONICAL_BUNDLE_FILES:
        raise AssertionError("bundle manifest source_files mismatch")
    companion = _bundle_manifest(output_dir)
    if companion.get("source_commit") != FIXTURE_SHA:
        raise AssertionError("companion manifest source_commit mismatch")
    if companion.get("bundle_sha256") != generator._sha256(bundle):
        raise AssertionError("companion manifest bundle hash mismatch")


def _assert_check_fails(output_dir: Path, expected_text: str) -> None:
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT), str(output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        raise AssertionError(f"expected generated checker failure containing {expected_text!r}")
    combined = result.stdout + result.stderr
    if expected_text not in combined:
        raise AssertionError(f"expected {expected_text!r} in checker output, got {combined!r}")


def _all_generated_text(output_dir: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(output_dir.rglob("*")):
        if path.is_file():
            files[str(path.relative_to(output_dir)).replace("\\", "/")] = path.read_text(encoding="utf-8")
    return files


def _expect_success(name: str, args: list[str], env: dict[str, str], expected: tuple[str, str, str, str]) -> None:
    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-") as directory:
        output_dir = Path(directory)
        result = _run([str(output_dir), *args], env)
        if result.returncode != 0:
            raise AssertionError(f"{name}: expected success, got {result.returncode}: {result.stderr}")
        _check_generated(output_dir)
        _assert_manifest(output_dir, *expected)
        if expected[0] == FIXTURE_REPOSITORY:
            _assert_bundle_outputs(output_dir)
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
            FIXTURE_RUN_ID,
            "--generated-by",
            "LOCAL",
        ],
        _base_env(),
        (FIXTURE_REPOSITORY, FIXTURE_SHA, FIXTURE_RUN_ID, "LOCAL"),
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
        _assert_bundle_outputs(output_dir)
        print("generator test: cli arguments override GitHub environment PASS")

    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-a-") as first, tempfile.TemporaryDirectory(
        prefix="madp-bootstrap-b-"
    ) as second:
        args = [
            "--repository",
            FIXTURE_REPOSITORY,
            "--commit-sha",
            FIXTURE_SHA,
            "--workflow-run-id",
            FIXTURE_RUN_ID,
            "--generated-by",
            "LOCAL",
        ]
        result_a = _run([first, *args], _base_env())
        result_b = _run([second, *args], _base_env())
        if result_a.returncode != 0 or result_b.returncode != 0:
            raise AssertionError("deterministic output test generation failed")
        if _all_generated_text(Path(first)) != _all_generated_text(Path(second)):
            raise AssertionError("same generator input produced different output")
        print("generator test: deterministic output PASS")

    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-root-") as directory:
        temp_root = Path(directory)
        for relative_path in generator.CANONICAL_BUNDLE_FILES:
            path = temp_root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text((ROOT / relative_path).read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        original_root = generator.ROOT
        try:
            generator.ROOT = temp_root
            first_hash = generator._sha256(
                generator._complete_protocol_bundle(
                    generator.CANONICAL_BUNDLE_FILES,
                    FIXTURE_REPOSITORY,
                    FIXTURE_SHA,
                )
            )
            readme = temp_root / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8") + "\nsource change for hash test 1111111111111111111111111111111111111111\n",
                encoding="utf-8",
            )
            second_bundle = generator._complete_protocol_bundle(
                generator.CANONICAL_BUNDLE_FILES,
                FIXTURE_REPOSITORY,
                FIXTURE_SHA,
            )
            second_hash = generator._sha256(second_bundle)
        finally:
            generator.ROOT = original_root
        if first_hash == second_hash:
            raise AssertionError("bundle hash did not change after source file change")
        metadata_source = re.search(r"^source_commit: (.+)$", second_bundle, re.MULTILINE)
        if not metadata_source or metadata_source.group(1) != FIXTURE_SHA:
            raise AssertionError("canonical body SHA changed bundle metadata source_commit")
        print("generator test: bundle hash changes when source changes PASS")

    with tempfile.TemporaryDirectory(prefix="madp-bootstrap-corrupt-") as directory:
        output_dir = Path(directory)
        result = _run(
            [
                str(output_dir),
                "--repository",
                FIXTURE_REPOSITORY,
                "--commit-sha",
                FIXTURE_SHA,
                "--workflow-run-id",
                FIXTURE_RUN_ID,
                "--generated-by",
                "LOCAL",
            ],
            _base_env(),
        )
        if result.returncode != 0:
            raise AssertionError("corruption tests setup failed")

        bundle_path = output_dir / "bootstrap" / "complete-protocol-bundle.txt"
        original_bundle = bundle_path.read_text(encoding="utf-8")
        metadata_end = original_bundle.index("END_MADP_BUNDLE_METADATA\n\n") + len("END_MADP_BUNDLE_METADATA\n\n")
        bundle_path.write_text(original_bundle[metadata_end:], encoding="utf-8", newline="\n")
        _assert_check_fails(output_dir, "metadata envelope must be at file start")

        bundle_path.write_text(original_bundle.replace(FIXTURE_SHA, ENV_SHA, 1), encoding="utf-8", newline="\n")
        _assert_check_fails(output_dir, "metadata source_commit mismatch")

        bundle_path.write_text(original_bundle, encoding="utf-8", newline="\n")
        manifest_path = output_dir / "bootstrap" / "complete-protocol-bundle.manifest.yaml"
        manifest_text = manifest_path.read_text(encoding="utf-8")
        manifest_path.write_text(manifest_text.replace("bundle_sha256: ", "bundle_sha256: 0", 1), encoding="utf-8")
        _assert_check_fails(output_dir, "bundle_sha256 mismatch")
        print("generator test: generated checker rejects corrupted bundle metadata PASS")

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
