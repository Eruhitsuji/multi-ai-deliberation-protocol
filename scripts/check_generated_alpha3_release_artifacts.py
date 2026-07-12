#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import re
import sys
import zipfile
import yaml

SKILLS = ['madp-start', 'madp-facilitator', 'madp-participant', 'madp-recorder', 'madp-help']
SCHEMAS = [
    'deliberation', 'command', 'migration', 'session-portability',
    'protocol-load-report', 'command-registry', 'validation-receipt', 'advanced-profiles',
    'field-trial-evidence', 'field-trial-collection',
]
BOOTSTRAPS = ['load-protocol-from-github.md', 'quick-start.md', 'verified-start.md', 'invite-limited-participant.md', 'help.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_digest(paths):
    return hashlib.sha256(('\n'.join(paths) + '\n').encode('utf-8')).hexdigest()


def frontmatter(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def sources_for(profile, source_sets, load_profiles):
    rows = []
    for set_name in load_profiles[profile]['required_sets']:
        rows.extend(source_sets[set_name])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    directory = Path(args.directory)
    problems = []
    required = (
        ['manifest.yaml', 'validation-evidence.yaml', 'complete-protocol-bundle.txt']
        + BOOTSTRAPS
        + [f'schemas/{name}.bundle.schema.yaml' for name in SCHEMAS]
        + [f'chatgpt-skills/{name}.zip' for name in SKILLS]
        + ['chatgpt-skills/madp-skill-pack.zip']
        + [f'claude-project/.claude/skills/{name}/SKILL.md' for name in SKILLS]
    )
    for rel in required:
        if not (directory / rel).is_file():
            problems.append(f'missing artifact: {rel}')

    manifest = {}
    if (directory / 'manifest.yaml').is_file():
        manifest = yaml.safe_load((directory / 'manifest.yaml').read_text(encoding='utf-8')) or {}
        if manifest.get('bundle_version') != 'MADP-ALPHA3-BUNDLE-v8':
            problems.append('manifest bundle version mismatch')
        if manifest.get('protocol_version') != 'MADP-v0.3.0-alpha.3' or manifest.get('source_commit') != args.source_commit:
            problems.append('manifest provenance mismatch')
        if manifest.get('protocol_load_report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2':
            problems.append('manifest load report version mismatch')
        if manifest.get('field_trial_evidence_version') != 'MADP-FIELD-TRIAL-EVIDENCE-v2':
            problems.append('manifest field-trial evidence version mismatch')
        if manifest.get('field_trial_collection_version') != 'MADP-FIELD-TRIAL-COLLECTION-v1':
            problems.append('manifest field-trial collection version mismatch')
        if manifest.get('validation_evidence_version') != 'MADP-ALPHA3-VALIDATION-EVIDENCE-v4':
            problems.append('manifest validation evidence version mismatch')
        if manifest.get('receipt_bound_field_trial_evidence') is not True:
            problems.append('receipt-bound field-trial evidence marker missing')
        if manifest.get('run_normalized_field_trial_evidence') is not True:
            problems.append('run-normalized field-trial evidence marker missing')
        if manifest.get('validation_receipt_generator_path') != 'scripts/generate_validation_receipt_v030_alpha3.py':
            problems.append('validation receipt generator path mismatch')
        if manifest.get('field_trial_collector_path') != 'scripts/collect_field_trial_evidence_v030_alpha3.py':
            problems.append('field-trial collector path mismatch')
        if manifest.get('field_trial_collection_config_path') != 'docs/evaluation/MADP-v0.3.0-alpha.3-field-trial-collection-config.yaml':
            problems.append('field-trial collection config path mismatch')
        if manifest.get('formal_field_trial_receipt_schema') != 'schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml':
            problems.append('formal field-trial receipt schema mismatch')
        if manifest.get('formal_field_trial_evidence_schema') != 'schemas/v0.3.0-alpha.3/field-trial-evidence.schema.yaml':
            problems.append('formal field-trial evidence schema mismatch')
        if manifest.get('formal_field_trial_collection_schema') != 'schemas/v0.3.0-alpha.3/field-trial-collection.schema.yaml':
            problems.append('formal field-trial collection schema mismatch')

        source_sets = manifest.get('source_sets', {})
        load_profiles = manifest.get('load_profiles', {})
        profile_digests = manifest.get('source_inventory_digests', {})
        flat = [item for values in source_sets.values() for item in values]
        if len(flat) != len(set(flat)):
            problems.append('manifest source-set overlap')
        for profile in ('QUICK', 'VERIFIED', 'FIELD_TRIAL'):
            if profile not in load_profiles:
                problems.append(f'missing load profile: {profile}')
                continue
            expected = inventory_digest(sources_for(profile, source_sets, load_profiles))
            if profile_digests.get(profile) != expected:
                problems.append(f'profile digest mismatch: {profile}')
        for profile in ('VERIFIED', 'FIELD_TRIAL'):
            if 'VALIDATION_TOOLS' not in load_profiles.get(profile, {}).get('required_sets', []):
                problems.append(f'{profile} does not require validation tools')
        if manifest.get('packaged_source_count') != len(set(flat)):
            problems.append('packaged source count mismatch')
        if manifest.get('canonical_command_count') != 51 or manifest.get('command_registry_policy') != 'ALPHA2_CANONICAL_SUPERSET':
            problems.append('manifest command policy mismatch')
        if manifest.get('explicit_session_start_required') is not True:
            problems.append('explicit session start marker missing')
        if manifest.get('validation_receipt_required_for_verified_evidence') is not True:
            problems.append('validation receipt marker missing')
        if manifest.get('schema_bundle_count') != len(SCHEMAS):
            problems.append('schema bundle count mismatch')
        if manifest.get('advanced_profile_count') != 9:
            problems.append('advanced profile count mismatch')
        if (directory / 'validation-evidence.yaml').is_file():
            if manifest.get('validation_evidence_sha256') != sha(directory / 'validation-evidence.yaml'):
                problems.append('evidence digest mismatch')
            evidence = yaml.safe_load((directory / 'validation-evidence.yaml').read_text(encoding='utf-8')) or {}
            if (
                evidence.get('evidence_version') != 'MADP-ALPHA3-VALIDATION-EVIDENCE-v4'
                or evidence.get('receipt_check_required') is not True
                or evidence.get('run_normalized_field_trial_evidence') is not True
            ):
                problems.append('packaged validation evidence contract mismatch')

        bundle = (directory / 'complete-protocol-bundle.txt').read_text(encoding='utf-8') if (directory / 'complete-protocol-bundle.txt').is_file() else ''
        file_rows = {item.get('path'): item for item in manifest.get('files', [])}
        if set(file_rows) != set(flat):
            problems.append('manifest packaged source set mismatch')
        for rel, row in file_rows.items():
            if f'BEGIN_FILE path={rel}' not in bundle or f'END_FILE path={rel}' not in bundle:
                problems.append(f'bundle boundary missing: {rel}')
            if not re.fullmatch(r'[0-9a-f]{64}', str(row.get('sha256', ''))):
                problems.append(f'invalid packaged source hash: {rel}')

        bootstrap_rows = {item.get('path'): item for item in manifest.get('bootstrap_files', [])}
        if set(bootstrap_rows) != set(BOOTSTRAPS):
            problems.append('manifest bootstrap file set mismatch')
        for name, row in bootstrap_rows.items():
            path = directory / name
            if path.is_file() and (
                row.get('sha256') != sha(path)
                or row.get('bytes') != path.stat().st_size
                or row.get('source_commit') != args.source_commit
            ):
                problems.append(f'bootstrap provenance mismatch: {name}')

    loader = directory / 'load-protocol-from-github.md'
    if loader.is_file():
        data = frontmatter(loader)
        text = loader.read_text(encoding='utf-8')
        if data.get('bootstrap_role') != 'PROTOCOL_LOADER' or data.get('report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2':
            problems.append('generated loader metadata mismatch')
        if data.get('commit_template') != args.source_commit:
            problems.append('generated loader commit mismatch')
        if '{{MADP_' in text:
            problems.append('generated loader contains unresolved placeholder')
        for marker in ('report_id', 'revision', 'supersedes', 'HASH_VERIFIED', 'FIELD_TRIAL', 'schema_validation_records', 'validation_receipt_refs'):
            if marker not in text:
                problems.append(f'generated loader marker missing: {marker}')

    for name in ('quick-start.md', 'verified-start.md'):
        path = directory / name
        if path.is_file():
            data = frontmatter(path)
            text = path.read_text(encoding='utf-8')
            if data.get('requires_protocol_load') is not True or data.get('required_load_report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2':
                problems.append(f'load gate metadata missing: {name}')
            if data.get('profile_source_binding_required') is not True:
                problems.append(f'profile source binding missing: {name}')
            if 'PROTOCOL_NOT_LOADED' not in text or 'PROFILE_SOURCE' not in text:
                problems.append(f'load gate failure response missing: {name}')
    verified = frontmatter(directory / 'verified-start.md') if (directory / 'verified-start.md').is_file() else {}
    if verified.get('required_schema_validation') != 'EXECUTED' or verified.get('required_provenance') != 'HASH_VERIFIED':
        problems.append('verified start assurance requirements missing')

    for skill in SKILLS:
        claude = directory / f'claude-project/.claude/skills/{skill}/SKILL.md'
        zip_path = directory / f'chatgpt-skills/{skill}.zip'
        if claude.is_file() and zip_path.is_file():
            with zipfile.ZipFile(zip_path) as archive:
                if archive.read(f'{skill}/SKILL.md') != claude.read_bytes():
                    problems.append(f'ChatGPT/Claude Skill drift: {skill}')
    pack = directory / 'chatgpt-skills/madp-skill-pack.zip'
    if pack.is_file():
        with zipfile.ZipFile(pack) as archive:
            if set(archive.namelist()) != {f'{skill}/SKILL.md' for skill in SKILLS}:
                problems.append('Skill pack set mismatch')

    for name in SCHEMAS:
        path = directory / f'schemas/{name}.bundle.schema.yaml'
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding='utf-8'))

            def walk(value):
                if isinstance(value, dict):
                    for key, item in value.items():
                        if key == '$ref' and not str(item).startswith('#'):
                            problems.append(f'external ref in {path}: {item}')
                        walk(item)
                elif isinstance(value, list):
                    for item in value:
                        walk(item)

            walk(data)

    if problems:
        for item in problems:
            print('FAIL:', item, file=sys.stderr)
        return 1
    print(
        'generated alpha.3 release artifacts: PASS '
        '(profiled commit-pinned loader, v2 report, v4 validation evidence, 10 schemas, run-normalized receipt-bound field trials, collection contract, 5 symmetric Skills)'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
