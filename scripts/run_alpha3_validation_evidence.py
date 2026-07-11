#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, subprocess, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ('A3-CHECK-IMPLEMENTATION', 'scripts/check_alpha3_implementation.py', []),
    ('A3-CHECK-MIGRATION', 'scripts/check_alpha3_migration.py', []),
    ('A3-CHECK-TRANSLATION', 'scripts/check_alpha3_translation.py', []),
    ('A3-CHECK-USABILITY', 'scripts/check_alpha3_usability.py', []),
    ('A3-CHECK-PARSER', 'scripts/test_command_parser_v030_alpha3.py', []),
    ('A3-CHECK-COMMAND-COVERAGE', 'scripts/check_all_commands_v030_alpha3.py', []),
    ('A3-CHECK-RUNTIME', 'scripts/test_command_runtime_v030_alpha3.py', []),
]
STATIC_INPUTS = {
    'A3-CHECK-IMPLEMENTATION': [
        'schemas/v0.3.0-alpha.3/deliberation.schema.yaml',
        'schemas/v0.3.0-alpha.3/command.schema.yaml',
        'schemas/v0.3.0-alpha.3/migration.schema.yaml',
        'schemas/v0.3.0-alpha.3/session-portability.schema.yaml',
        'registries/v0.3.0-alpha.3/commands.yaml',
        'tests/v0.3.0-alpha.3/fixtures.yaml',
        'tests/v0.3.0-alpha.3/portability-fixtures.yaml',
        'docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml',
        'docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml',
    ],
    'A3-CHECK-MIGRATION': [
        'schemas/v0.3.0-alpha.3/migration.schema.yaml',
        'tests/v0.3.0-alpha.3/migration-fixtures.yaml',
        'tests/v0.3.0-alpha.3/migration-transformations.yaml',
        'scripts/migrate_v030_alpha2_to_alpha3.py',
    ],
    'A3-CHECK-TRANSLATION': ['docs/ja/v0.3.0-alpha.3/translation-manifest.yaml'],
    'A3-CHECK-USABILITY': [
        'tests/v0.3.0-alpha.3/usability-scenarios.yaml',
        'docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml',
        'docs/evaluation/MADP-v0.3.0-alpha.3-usability-plan.md',
    ],
    'A3-CHECK-PARSER': [
        'scripts/parse_command_v030_alpha3.py',
        'schemas/v0.3.0-alpha.3/command.schema.yaml',
        'registries/v0.3.0-alpha.3/commands.yaml',
    ],
    'A3-CHECK-COMMAND-COVERAGE': [
        'scripts/parse_command_v030_alpha3.py',
        'scripts/apply_command_v030_alpha3.py',
        'schemas/v0.3.0-alpha.3/command.schema.yaml',
        'registries/v0.3.0-alpha.3/commands.yaml',
    ],
    'A3-CHECK-RUNTIME': [
        'scripts/parse_command_v030_alpha3.py',
        'scripts/apply_command_v030_alpha3.py',
        'schemas/v0.3.0-alpha.3/command.schema.yaml',
        'registries/v0.3.0-alpha.3/commands.yaml',
    ],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scope_files() -> list[str]:
    prefixes = [
        'schemas/v0.3.0-alpha.3/',
        'registries/v0.3.0-alpha.3/',
        'bootstrap/alpha3/',
        'docs/ja/v0.3.0-alpha.3/',
        'tests/v0.3.0-alpha.3/',
        'skills/madp-',
        'dist/chatgpt/madp-',
    ]
    files = []
    for path in ROOT.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.suffix in {'.pyc', '.pyo'}:
            continue
        rel = str(path.relative_to(ROOT)).replace('\\', '/')
        if (
            rel.startswith('README-v0.3.0-alpha.3')
            or rel in {'.github/workflows/validate-alpha3.yml', 'skills/README.md'}
            or any(rel.startswith(x) for x in prefixes)
            or (rel.startswith('protocol/') and 'alpha.3' in rel)
            or (rel.startswith('docs/profiles/') and 'alpha.3' in rel)
            or (rel.startswith('docs/planning/') and 'alpha.3' in rel)
            or (rel.startswith('docs/evaluation/') and 'alpha.3' in rel)
            or (rel.startswith('docs/migration/') and 'alpha.3' in rel)
            or (rel.startswith('scripts/') and ('alpha3' in rel or 'v030_alpha3' in rel))
        ):
            files.append(rel)
    return sorted(files)


def translation_inputs() -> list[str]:
    document = yaml.safe_load(
        (ROOT / 'docs/ja/v0.3.0-alpha.3/translation-manifest.yaml').read_text(encoding='utf-8')
    )
    output = []
    for entry in document.get('entries', []):
        output.extend([entry['source'], entry['translation']])
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--repository-commit', required=True)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()

    records = []
    failed = False
    for check_id, script, extra in CHECKS:
        command = [sys.executable, str(ROOT / script), *extra]
        if check_id == 'A3-CHECK-USABILITY' and args.release:
            command.append('--release')
        process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        inputs = list(STATIC_INPUTS[check_id])
        if check_id == 'A3-CHECK-TRANSLATION':
            inputs += translation_inputs()
        input_hashes = {}
        for rel in sorted(set(inputs)):
            path = ROOT / rel
            if not path.is_file():
                process = subprocess.CompletedProcess(
                    process.args,
                    1,
                    process.stdout,
                    (process.stderr + f'\nmissing evidence input: {rel}').strip(),
                )
                break
            input_hashes[rel] = sha(path)
        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        status = 'PASS' if process.returncode == 0 else 'FAIL'
        records.append({
            'id': check_id,
            'command': ' '.join([Path(command[0]).name, *[str(x) for x in command[1:]]]),
            'checker_path': script,
            'checker_sha256': sha(ROOT / script),
            'return_code': process.returncode,
            'status': status,
            'input_sha256': input_hashes,
            'stdout': stdout,
            'stderr': stderr,
            'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
            'stderr_sha256': hashlib.sha256(stderr.encode('utf-8')).hexdigest(),
        })
        print(f'{check_id}: {status}')
        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)
        if process.returncode:
            failed = True

    manifest = {
        'evidence_version': 'MADP-ALPHA3-VALIDATION-EVIDENCE-v1',
        'protocol_version': 'MADP-v0.3.0-alpha.3',
        'repository_commit': args.repository_commit,
        'release_mode': args.release,
        'self_attested': False,
        'scope_sha256': {rel: sha(ROOT / rel) for rel in scope_files()},
        'checks': records,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding='utf-8')
    print(f'alpha.3 validation evidence written: {output} ({len(records)} checks)')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
