#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,re,sys,zipfile,yaml

SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help']
SCHEMAS=['deliberation','command','migration','session-portability']
BOOTSTRAPS=['load-protocol-from-github.md','quick-start.md','verified-start.md','invite-limited-participant.md','help.md']

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory_digest(paths): return hashlib.sha256(('\n'.join(paths)+'\n').encode('utf-8')).hexdigest()
def frontmatter(path):
    text=path.read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    return yaml.safe_load(m.group(1)) if m else {}

def sources_for(profile,source_sets,load_profiles):
    rows=[]
    for set_name in load_profiles[profile]['required_sets']: rows.extend(source_sets[set_name])
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('directory')
    ap.add_argument('--source-commit',required=True)
    a=ap.parse_args()
    d=Path(a.directory)
    problems=[]
    req=['manifest.yaml','validation-evidence.yaml','complete-protocol-bundle.txt']+BOOTSTRAPS+[f'schemas/{x}.bundle.schema.yaml' for x in SCHEMAS]+[f'chatgpt-skills/{x}.zip' for x in SKILLS]+['chatgpt-skills/madp-skill-pack.zip']+[f'claude-project/.claude/skills/{x}/SKILL.md' for x in SKILLS]
    for rel in req:
        if not (d/rel).is_file(): problems.append(f'missing artifact: {rel}')
    manifest={}
    if (d/'manifest.yaml').is_file():
        manifest=yaml.safe_load((d/'manifest.yaml').read_text(encoding='utf-8')) or {}
        if manifest.get('bundle_version')!='MADP-ALPHA3-BUNDLE-v4': problems.append('manifest bundle version mismatch')
        if manifest.get('protocol_version')!='MADP-v0.3.0-alpha.3' or manifest.get('source_commit')!=a.source_commit: problems.append('manifest provenance mismatch')
        if manifest.get('protocol_load_report_version')!='MADP-PROTOCOL-LOAD-REPORT-v2': problems.append('manifest load report version mismatch')
        source_sets=manifest.get('source_sets',{})
        load_profiles=manifest.get('load_profiles',{})
        profile_digests=manifest.get('source_inventory_digests',{})
        flat=[x for values in source_sets.values() for x in values]
        if len(flat)!=len(set(flat)): problems.append('manifest source-set overlap')
        for profile in ('QUICK','VERIFIED','FIELD_TRIAL'):
            if profile not in load_profiles: problems.append(f'missing load profile: {profile}'); continue
            expected=inventory_digest(sources_for(profile,source_sets,load_profiles))
            if profile_digests.get(profile)!=expected: problems.append(f'profile digest mismatch: {profile}')
        if manifest.get('packaged_source_count')!=len(set(flat)): problems.append('packaged source count mismatch')
        if manifest.get('canonical_command_count')!=51 or manifest.get('command_registry_policy')!='ALPHA2_CANONICAL_SUPERSET': problems.append('manifest command policy mismatch')
        if (d/'validation-evidence.yaml').is_file() and manifest.get('validation_evidence_sha256')!=sha(d/'validation-evidence.yaml'): problems.append('evidence digest mismatch')
        bundle=(d/'complete-protocol-bundle.txt').read_text(encoding='utf-8') if (d/'complete-protocol-bundle.txt').is_file() else ''
        file_rows={x.get('path'):x for x in manifest.get('files',[])}
        if set(file_rows)!=set(flat): problems.append('manifest packaged source set mismatch')
        for rel,row in file_rows.items():
            if f'BEGIN_FILE path={rel}' not in bundle or f'END_FILE path={rel}' not in bundle: problems.append(f'bundle boundary missing: {rel}')
        bootstrap_rows={x.get('path'):x for x in manifest.get('bootstrap_files',[])}
        if set(bootstrap_rows)!=set(BOOTSTRAPS): problems.append('manifest bootstrap file set mismatch')
        for name,row in bootstrap_rows.items():
            q=d/name
            if q.is_file() and (row.get('sha256')!=sha(q) or row.get('bytes')!=q.stat().st_size or row.get('source_commit')!=a.source_commit):
                problems.append(f'bootstrap provenance mismatch: {name}')

    loader=d/'load-protocol-from-github.md'
    if loader.is_file():
        data=frontmatter(loader); text=loader.read_text(encoding='utf-8')
        if data.get('bootstrap_role')!='PROTOCOL_LOADER' or data.get('report_version')!='MADP-PROTOCOL-LOAD-REPORT-v2': problems.append('generated loader metadata mismatch')
        if data.get('commit_template')!=a.source_commit: problems.append('generated loader commit mismatch')
        if '{{MADP_' in text: problems.append('generated loader contains unresolved placeholder')
        for marker in ('report_id','revision','supersedes','HASH_VERIFIED','FIELD_TRIAL'):
            if marker not in text: problems.append(f'generated loader marker missing: {marker}')

    for name in ('quick-start.md','verified-start.md'):
        q=d/name
        if q.is_file():
            data=frontmatter(q); text=q.read_text(encoding='utf-8')
            if data.get('requires_protocol_load') is not True or data.get('required_load_report_version')!='MADP-PROTOCOL-LOAD-REPORT-v2': problems.append(f'load gate metadata missing: {name}')
            if data.get('profile_source_binding_required') is not True: problems.append(f'profile source binding missing: {name}')
            if 'PROTOCOL_NOT_LOADED' not in text or 'PROFILE_SOURCE' not in text: problems.append(f'load gate failure response missing: {name}')
    verified=frontmatter(d/'verified-start.md') if (d/'verified-start.md').is_file() else {}
    if verified.get('required_schema_validation')!='EXECUTED' or verified.get('required_provenance')!='HASH_VERIFIED': problems.append('verified start assurance requirements missing')

    for skill in SKILLS:
        cp=d/f'claude-project/.claude/skills/{skill}/SKILL.md'
        zp=d/f'chatgpt-skills/{skill}.zip'
        if cp.is_file() and zp.is_file():
            with zipfile.ZipFile(zp) as z:
                if z.read(f'{skill}/SKILL.md')!=cp.read_bytes(): problems.append(f'ChatGPT/Claude Skill drift: {skill}')
    if (d/'chatgpt-skills/madp-skill-pack.zip').is_file():
        with zipfile.ZipFile(d/'chatgpt-skills/madp-skill-pack.zip') as z:
            if set(z.namelist())!={f'{s}/SKILL.md' for s in SKILLS}: problems.append('Skill pack set mismatch')
    for name in SCHEMAS:
        q=d/f'schemas/{name}.bundle.schema.yaml'
        if q.is_file():
            data=yaml.safe_load(q.read_text(encoding='utf-8'))
            def walk(x):
                if isinstance(x,dict):
                    for k,v in x.items():
                        if k=='$ref' and not str(v).startswith('#'): problems.append(f'external ref in {q}: {v}')
                        walk(v)
                elif isinstance(x,list):
                    for v in x: walk(v)
            walk(data)
    if problems:
        for item in problems: print('FAIL:',item,file=sys.stderr)
        return 1
    print('generated alpha.3 release artifacts: PASS (profiled commit-pinned loader, v2 report, 4 schemas, 5 symmetric Skills)')
    return 0

if __name__=='__main__': raise SystemExit(main())
