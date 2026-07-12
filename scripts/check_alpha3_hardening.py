#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, re, sys, yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'MADP-v0.3.0-alpha.3'
SCHEMAS = {
    'load_report': ROOT / 'schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml',
    'registry': ROOT / 'schemas/v0.3.0-alpha.3/command-registry.schema.yaml',
    'validation_receipt': ROOT / 'schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml',
    'advanced_profiles': ROOT / 'schemas/v0.3.0-alpha.3/advanced-profiles.schema.yaml',
}
PROFILE_MARKERS = {
    'docs/profiles/SOURCE_AND_PARTICIPANT_INDEPENDENCE-v0.3.0-alpha.3.md': ['independence group', 'majority', 'self-confidence'],
    'docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md': ['BLIND_INITIAL_POSITION', 'CROSS_EXPOSURE', 'ANCHORING_EXPOSED'],
    'docs/profiles/GENAI_USE_GOVERNANCE-v0.3.0-alpha.3.md': ['information classification', 'incident', 'AI is not'],
    'docs/profiles/AI_DEV_TASK_CONTRACT-v0.3.0-alpha.3.md': ['A-CORE', 'A-EXT', 'must not change tests'],
    'docs/profiles/COMMUNICATION_ALIGNMENT-v0.3.0-alpha.3.md': ['alignment_contract', 'scope_check', 'assertion'],
    'docs/profiles/ASSURANCE_MODES-v0.3.0-alpha.3.md': ['NORMAL', 'REVIEW_REQUIRED', 'STRICT'],
    'docs/profiles/OPINION_MAPPING_EXTENSION-v0.3.0-alpha.3.md': ['AGREE', 'not `approve`', 'advisory'],
    'docs/profiles/DISSENT_LIFECYCLE-v0.3.0-alpha.3.md': ['OPEN', 'REDACTED', 'original-record hash'],
    'docs/profiles/SESSION_RETENTION_AND_RECOVERY-v0.3.0-alpha.3.md': ['recovery-point objective', 'restore test', 'key succession'],
}


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def inventory_digest(paths: list[str]) -> str:
    return hashlib.sha256(('\n'.join(paths) + '\n').encode('utf-8')).hexdigest()


def frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def first_error(validator, artifact):
    errors = sorted(validator.iter_errors(artifact), key=lambda e: list(e.path))
    return errors[0].message if errors else None


def main() -> int:
    problems = []
    validators = {}
    for name, path in SCHEMAS.items():
        if not path.is_file():
            problems.append(f'missing schema: {path.relative_to(ROOT)}')
            continue
        try:
            schema = load(path)
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(schema)
        except Exception as exc:
            problems.append(f'invalid schema {name}: {exc}')

    registry_path = ROOT / 'registries/v0.3.0-alpha.3/commands.yaml'
    if 'registry' in validators and registry_path.is_file():
        error = first_error(validators['registry'], load(registry_path))
        if error:
            problems.append(f'command registry schema failure: {error}')
        registry = load(registry_path)
        commands = [x['command'] for x in registry.get('commands', [])]
        aliases = [x['alias'] for x in registry.get('aliases', [])]
        if len(commands) != len(set(commands)):
            problems.append('duplicate canonical command')
        if len(aliases) != len(set(aliases)):
            problems.append('duplicate alias')
        if set(commands) & set(aliases):
            problems.append('alias/canonical collision')
        declared = set(registry['composition']['inherited_alpha2_commands']) | set(registry['composition']['added_alpha3_commands'])
        if set(commands) != declared:
            problems.append('registry composition lists do not equal command entries')

    fixture_path = ROOT / 'tests/v0.3.0-alpha.3/hardening-fixtures.yaml'
    if not fixture_path.is_file():
        problems.append('missing hardening fixtures')
    elif len(validators) == len(SCHEMAS):
        fixtures = load(fixture_path)
        mapping = {
            'protocol_load_report': 'load_report',
            'validation_receipt': 'validation_receipt',
            'advanced_profiles': 'advanced_profiles',
        }
        for section, schema_name in mapping.items():
            validator = validators[schema_name]
            for index, artifact in enumerate(fixtures[section].get('valid', []), 1):
                error = first_error(validator, artifact)
                if error:
                    problems.append(f'valid {section} fixture {index} failed: {error}')
            for case in fixtures[section].get('invalid', []):
                artifact = case.get('artifact')
                if first_error(validator, artifact) is None:
                    problems.append(f'invalid fixture unexpectedly passed: {case.get("id")}')

    loader_path = ROOT / 'bootstrap/alpha3/load-protocol-from-github.md'
    if loader_path.is_file():
        metadata = frontmatter(loader_path)
        source_sets = metadata.get('source_sets', {})
        profiles = metadata.get('load_profiles', {})
        digests = metadata.get('source_inventory_digests', {})
        flat = [path for values in source_sets.values() for path in values]
        if len(flat) != len(set(flat)):
            problems.append('loader source-set overlap')
        for rel in flat:
            if not (ROOT / rel).is_file():
                problems.append(f'loader references missing source: {rel}')
        for profile in ('QUICK', 'VERIFIED', 'FIELD_TRIAL'):
            paths = []
            for set_name in profiles.get(profile, {}).get('required_sets', []):
                paths.extend(source_sets.get(set_name, []))
            if digests.get(profile) != inventory_digest(paths):
                problems.append(f'loader digest mismatch: {profile}')
        core = source_sets.get('CORE', [])
        for required in [
            'schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml',
            'schemas/v0.3.0-alpha.3/command-registry.schema.yaml',
            'schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml',
        ]:
            if required not in core:
                problems.append(f'loader CORE missing hardening schema: {required}')
        advanced = source_sets.get('ADVANCED_PROFILES', [])
        if 'schemas/v0.3.0-alpha.3/advanced-profiles.schema.yaml' not in advanced:
            problems.append('loader ADVANCED_PROFILES missing schema')
        text = loader_path.read_text(encoding='utf-8')
        for marker in ['Capability preflight', 'authorized_start_profiles: []', 'validation_receipt_refs', 'unvalidated_structured_sources', 'complete protocol bundle upload']:
            if marker not in text:
                problems.append(f'loader hardening marker missing: {marker}')

    protocol = (ROOT / 'protocol/MADP-v0.3.0-alpha.3.md').read_text(encoding='utf-8')
    for marker in ['Goal confirmation changes only the plan status', 'SESSION_NOT_STARTED', 'VALIDATION_RECEIPT', 'must not infer missing IDs']:
        if marker not in protocol:
            problems.append(f'protocol hardening marker missing: {marker}')

    for rel, markers in PROFILE_MARKERS.items():
        path = ROOT / rel
        if not path.is_file():
            problems.append(f'missing advanced profile: {rel}')
            continue
        text = path.read_text(encoding='utf-8')
        for marker in markers:
            if marker not in text:
                problems.append(f'profile marker missing {marker!r}: {rel}')

    if problems:
        for problem in problems:
            print('FAIL:', problem, file=sys.stderr)
        return 1
    print('alpha.3 field-trial hardening: PASS (4 schemas, loader fail-closed recovery, explicit session start, 9 advanced profiles)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
