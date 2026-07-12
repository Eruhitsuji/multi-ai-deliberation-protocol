#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, subprocess, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
KNOWN = {'A3-REL-001', 'A3-REL-002', 'A3-REL-003', 'A3-REL-004', 'A3-REL-005'}
REQUIRED_CHECKS = {
    'A3-CHECK-IMPLEMENTATION', 'A3-CHECK-HARDENING', 'A3-CHECK-MIGRATION', 'A3-CHECK-TRANSLATION',
    'A3-CHECK-USABILITY', 'A3-CHECK-PARSER', 'A3-CHECK-COMMAND-COVERAGE', 'A3-CHECK-RUNTIME',
}
FORBIDDEN_STAGING_PATHS = ('.madp-finalize', '.madp-patch', '.madp-source-sync')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    return {str(path.relative_to(root)).replace('\\', '/'): sha(path) for path in sorted(root.rglob('*')) if path.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence-manifest', required=True)
    parser.add_argument('--repository-commit', required=True)
    parser.add_argument('--release-directory-a', required=True)
    parser.add_argument('--release-directory-b', required=True)
    parser.add_argument('--allow-blockers', default='')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--main-field-trial', action='store_true')
    modes.add_argument('--require-main', action='store_true')
    args = parser.parse_args()
    problems = []

    for rel in FORBIDDEN_STAGING_PATHS:
        if (ROOT / rel).exists(): problems.append(f'forbidden staging path remains in release source: {rel}')

    allowed = {item for item in args.allow_blockers.split(',') if item}
    status = yaml.safe_load((ROOT / 'docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml').read_text(encoding='utf-8'))
    if status.get('protocol_version') != 'MADP-v0.3.0-alpha.3': problems.append('protocol version mismatch')
    if status.get('implementation_status') != 'RELEASE_CANDIDATE_CONTENT_READY': problems.append('content status mismatch')
    policy = status.get('validation_policy', {})
    if policy.get('self_attestation_is_release_evidence') is not False or policy.get('machine_generated_evidence_manifest_required') is not True:
        problems.append('unsafe validation evidence policy')
    if 'automated_checks' in status: problems.append('handwritten automated_checks map cannot be release evidence')

    blockers = {item['id']: item['status'] for item in status.get('release_blockers', [])}
    if set(blockers) != KNOWN: problems.append('release blocker set mismatch')
    active = {key for key, value in blockers.items() if value != 'DONE'}
    if active != allowed: problems.append(f'unexpected active blockers: {sorted(active)} expected {sorted(allowed)}')

    evidence_path = Path(args.evidence_manifest)
    if not evidence_path.is_file():
        problems.append('validation evidence manifest missing')
    else:
        evidence = yaml.safe_load(evidence_path.read_text(encoding='utf-8'))
        if evidence.get('evidence_version') != 'MADP-ALPHA3-VALIDATION-EVIDENCE-v2' or evidence.get('self_attested') is not False:
            problems.append('invalid evidence format')
        if evidence.get('repository_commit') != args.repository_commit: problems.append('evidence commit mismatch')
        if bool(evidence.get('release_mode')) != bool(args.require_main): problems.append('evidence release mode mismatch')
        scope = evidence.get('scope_sha256', {})
        if not scope: problems.append('evidence scope hash set missing')
        for rel, digest in scope.items():
            source_path = ROOT / rel
            if not source_path.is_file() or sha(source_path) != digest: problems.append(f'evidence scope hash mismatch: {rel}')
        rows = {item.get('id'): item for item in evidence.get('checks', [])}
        if set(rows) != REQUIRED_CHECKS: problems.append('evidence check set mismatch')
        for check_id, row in rows.items():
            checker_path = ROOT / row.get('checker_path', '')
            if row.get('status') != 'PASS' or row.get('return_code') != 0: problems.append(f'evidence check failed: {check_id}')
            if not checker_path.is_file() or sha(checker_path) != row.get('checker_sha256'): problems.append(f'checker hash mismatch: {check_id}')
            if hashlib.sha256((row.get('stdout') or '').encode()).hexdigest() != row.get('stdout_sha256'): problems.append(f'stdout evidence hash mismatch: {check_id}')
            if hashlib.sha256((row.get('stderr') or '').encode()).hexdigest() != row.get('stderr_sha256'): problems.append(f'stderr evidence hash mismatch: {check_id}')
            for rel, digest in row.get('input_sha256', {}).items():
                input_path = ROOT / rel
                if not input_path.is_file() or sha(input_path) != digest: problems.append(f'input hash mismatch: {check_id}:{rel}')

    release_a = Path(args.release_directory_a)
    release_b = Path(args.release_directory_b)
    if not release_a.is_dir() or not release_b.is_dir():
        problems.append('both generated release directories are required')
    else:
        if tree_hashes(release_a) != tree_hashes(release_b): problems.append('release artifact generation is not reproducible')
        bound = release_a / 'validation-evidence.yaml'
        if not bound.is_file() or not evidence_path.is_file() or sha(bound) != sha(evidence_path): problems.append('release artifact is not bound to supplied evidence')
        process = subprocess.run([sys.executable, str(ROOT / 'scripts/check_generated_alpha3_release_artifacts.py'), str(release_a), '--source-commit', args.repository_commit], cwd=ROOT, text=True, capture_output=True)
        if process.returncode != 0: problems.append('generated artifact validation failed: ' + (process.stderr.strip() or process.stdout.strip()))

    if args.require_main:
        mode = 'final main'
        if status.get('integration_status') != 'MERGED_TO_MAIN': problems.append('final audit requires MERGED_TO_MAIN')
        if status.get('evaluation_status') != 'COMPLETE': problems.append('final audit requires evaluation_status COMPLETE')
        if active: problems.append('final audit cannot have blockers')
        if status.get('release_ready') is not True: problems.append('final audit requires release_ready true')
    elif args.main_field_trial:
        mode = 'main field trial'
        if status.get('integration_status') != 'MERGED_TO_MAIN': problems.append('field-trial audit requires MERGED_TO_MAIN')
        if status.get('evaluation_status') != 'FIELD_TRIAL_IN_PROGRESS': problems.append('field-trial audit requires FIELD_TRIAL_IN_PROGRESS')
        if status.get('release_ready') is not False: problems.append('field trial must not claim release_ready')
        if blockers.get('A3-REL-001') != 'FIELD_TRIAL_IN_PROGRESS': problems.append('A3-REL-001 must remain FIELD_TRIAL_IN_PROGRESS')
        if blockers.get('A3-REL-005') != 'WAITING_FOR_FIELD_TRIAL': problems.append('A3-REL-005 must wait for field trial completion')
    else:
        mode = 'branch'
        if status.get('integration_status') != 'IMPLEMENTATION_BRANCH': problems.append('branch audit requires IMPLEMENTATION_BRANCH')
        if status.get('release_ready') is not False: problems.append('branch must not claim release_ready')

    if problems:
        for problem in problems: print('FAIL:', problem, file=sys.stderr)
        return 1
    print('MADP-v0.3.0-alpha.3 evidence-backed release audit: PASS' + f' ({mode}; blockers={sorted(allowed)})')
    return 0


if __name__ == '__main__': raise SystemExit(main())
