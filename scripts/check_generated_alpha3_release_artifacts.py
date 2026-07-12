#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, re, sys, zipfile, yaml

SKILLS = ['madp-start', 'madp-facilitator', 'madp-participant', 'madp-recorder', 'madp-help']
SCHEMAS = ['deliberation', 'command', 'migration', 'session-portability', 'protocol-load-report', 'command-registry', 'validation-receipt', 'advanced-profiles']
BOOTSTRAPS = ['load-protocol-from-github.md', 'quick-start.md', 'verified-start.md', 'invite-limited-participant.md', 'help.md']


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory_digest(paths): return hashlib.sha256(('\n'.join(paths) + '\n').encode('utf-8')).hexdigest()

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
    required = ['manifest.yaml', 'validation-evidence.yaml', 'complete-protocol-bundle.txt'] + BOOTSTRAPS + [f'schemas/{x}.bundle.schema.yaml' for x in SCHEMAS] + [f'chatgpt-skills/{x}.zip' for x in SKILLS] + ['chatgpt-skills/madp-skill-pack.zip'] + [f'claude-project/.claude/skills/{x}/SKILL.md' for x in SKILLS]
    for rel in required:
        if not (directory / rel).is_file():
            problems.append(f'missing artifact: {rel}')

    manifest = {}
    if (directory / 'manifest.yaml').is_file():
        manifest = yaml.safe_load((directory / 'manifest.yaml').read_text(encoding='utf-8')) or {}
        if manifest.get('bundle_version') != 'MADP-ALPHA3-BUNDLE-v5': problems.append('manifest bundle version mismatch')
        if manifest.get('protocol_version') != 'MADP-v0.3.0-alpha.3' or manifest.get('source_commit') != args.source_commit: problems.append('manifest provenance mismatch')
        if manifest.get('protocol_load_report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2': problems.append('manifest load report version mismatch')
        if manifest.get('schema_bundle_count') != len(SCHEMAS): problems.append('manifest schema count mismatch')
        if manifest.get('explicit_session_start_required') is not True: problems.append('manifest explicit session-start policy missing')
        if manifest.get('validation_receipt_required_for_verified_evidence') is not True: problems.append('manifest validation receipt policy missing')
        source_sets = manifest.get('source_sets', {})
        load_profiles = manifest.get('load_profiles', {})
        profile_digests = manifest.get('source_inventory_digests', {})
        flat = [x for values in source_sets.values() for x in values]
        if len(flat) != len(set(flat)): problems.append('manifest source-set overlap')
        for profile in ('QUICK', 'VERIFIED', 'FIELD_TRIAL'):
            if profile not in load_profiles:
                problems.append(f'missing load profile: {profile}')
                continue
            expected = inventory_digest(sources_for(profile, source_sets, load_profiles))
            if profile_digests.get(profile) != expected: problems.append(f'profile digest mismatch: {profile}')
        if manifest.get('packaged_source_count') != len(set(flat)): problems.append('packaged source count mismatch')
        if manifest.get('canonical_command_count') != 51 or manifest.get('command_registry_policy') != 'ALPHA2_CANONICAL_SUPERSET': problems.append('manifest command policy mismatch')
        if (directory / 'validation-evidence.yaml').is_file() and manifest.get('validation_evidence_sha256') != sha(directory / 'validation-evidence.yaml'): problems.append('evidence digest mismatch')
        bundle = (directory / 'complete-protocol-bundle.txt').read_text(encoding='utf-8') if (directory / 'complete-protocol-bundle.txt').is_file() else ''
        file_rows = {x.get('path'): x for x in manifest.get('files', [])}
        if set(file_rows) != set(flat): problems.append('manifest packaged source set mismatch')
        for rel in file_rows:
            if f'BEGIN_FILE path={rel}' not in bundle or f'END_FILE path={rel}' not in bundle: problems.append(f'bundle boundary missing: {rel}')
        bootstrap_rows = {x.get('path'): x for x in manifest.get('bootstrap_files', [])}
        if set(bootstrap_rows) != set(BOOTSTRAPS): problems.append('manifest bootstrap file set mismatch')
        for name, row in bootstrap_rows.items():
            path = directory / name
            if path.is_file() and (row.get('sha256') != sha(path) or row.get('bytes') != path.stat().st_size or row.get('source_commit') != args.source_commit):
                problems.append(f'bootstrap provenance mismatch: {name}')

    loader = directory / 'load-protocol-from-github.md'
    if loader.is_file():
        data = frontmatter(loader); text = loader.read_text(encoding='utf-8')
        if data.get('bootstrap_role') != 'PROTOCOL_LOADER' or data.get('report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2': problems.append('generated loader metadata mismatch')
        if data.get('commit_template') != args.source_commit: problems.append('generated loader commit mismatch')
        if '{{MADP_' in text: problems.append('generated loader contains unresolved placeholder')
        for marker in ('report_id', 'revision', 'supersedes', 'HASH_VERIFIED', 'FIELD_TRIAL', 'Capability preflight', 'validation_receipt_refs', 'authorized_start_profiles: []'):
            if marker not in text: problems.append(f'generated loader marker missing: {marker}')

    for name in ('quick-start.md', 'verified-start.md'):
        path = directory / name
        if path.is_file():
            data = frontmatter(path); text = path.read_text(encoding='utf-8')
            if data.get('requires_protocol_load') is not True or data.get('required_load_report_version') != 'MADP-PROTOCOL-LOAD-REPORT-v2': problems.append(f'load gate metadata missing: {name}')
            if data.get('profile_source_binding_required') is not True: problems.append(f'profile source binding missing: {name}')
            if 'PROTOCOL_NOT_LOADED' not in text or 'PROFILE_SOURCE' not in text: problems.append(f'load gate failure response missing: {name}')
    verified = frontmatter(directory / 'verified-start.md') if (directory / 'verified-start.md').is_file() else {}
    if verified.get('required_schema_validation') != 'EXECUTED' or verified.get('required_provenance') != 'HASH_VERIFIED': problems.append('verified start assurance requirements missing')

    for skill in SKILLS:
        claude_path = directory / f'claude-project/.claude/skills/{skill}/SKILL.md'
        zip_path = directory / f'chatgpt-skills/{skill}.zip'
        if claude_path.is_file() and zip_path.is_file():
            with zipfile.ZipFile(zip_path) as archive:
                if archive.read(f'{skill}/SKILL.md') != claude_path.read_bytes(): problems.append(f'ChatGPT/Claude Skill drift: {skill}')
    if (directory / 'chatgpt-skills/madp-skill-pack.zip').is_file():
        with zipfile.ZipFile(directory / 'chatgpt-skills/madp-skill-pack.zip') as archive:
            if set(archive.namelist()) != {f'{skill}/SKILL.md' for skill in SKILLS}: problems.append('Skill pack set mismatch')
    for name in SCHEMAS:
        path = directory / f'schemas/{name}.bundle.schema.yaml'
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
            def walk(value):
                if isinstance(value, dict):
                    for key, item in value.items():
                        if key == '$ref' and not str(item).startswith('#'): problems.append(f'external ref in {path}: {item}')
                        walk(item)
                elif isinstance(value, list):
                    for item in value: walk(item)
            walk(data)
    if problems:
        for item in problems: print('FAIL:', item, file=sys.stderr)
        return 1
    print(f'generated alpha.3 release artifacts: PASS (profiled commit-pinned loader, v2 report, {len(SCHEMAS)} schemas, 5 symmetric Skills)')
    return 0


if __name__ == '__main__': raise SystemExit(main())
