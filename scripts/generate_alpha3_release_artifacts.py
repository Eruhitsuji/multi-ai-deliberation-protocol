#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, re, shutil, zipfile, yaml

ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
LOADER_SOURCE=ROOT/'bootstrap/alpha3/load-protocol-from-github.md'
BOOTSTRAP_FILES=['load-protocol-from-github.md','quick-start.md','verified-start.md','invite-limited-participant.md','help.md']
SCHEMAS=['deliberation','command','migration','session-portability']
SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help']

def frontmatter(path:Path):
    text=path.read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    if not m: raise ValueError(f'missing YAML frontmatter: {path}')
    data=yaml.safe_load(m.group(1))
    if not isinstance(data,dict): raise ValueError(f'invalid YAML frontmatter: {path}')
    return data

LOADER_META=frontmatter(LOADER_SOURCE)
SOURCE_SETS=LOADER_META.get('source_sets',{})
LOAD_PROFILES=LOADER_META.get('load_profiles',{})
PROFILE_DIGESTS=LOADER_META.get('source_inventory_digests',{})

def sources_for_profile(profile:str):
    cfg=LOAD_PROFILES.get(profile)
    if not isinstance(cfg,dict): raise ValueError(f'unknown load profile: {profile}')
    rows=[]
    for set_name in cfg.get('required_sets',[]):
        values=SOURCE_SETS.get(set_name)
        if not isinstance(values,list): raise ValueError(f'unknown source set: {set_name}')
        rows.extend(values)
    return rows

def inventory_digest(paths:list[str]):
    return hashlib.sha256(('\n'.join(paths)+'\n').encode('utf-8')).hexdigest()

ALL_SOURCES=[]
for set_name,values in SOURCE_SETS.items():
    if not isinstance(values,list): raise ValueError(f'invalid source set: {set_name}')
    for rel in values:
        if rel not in ALL_SOURCES: ALL_SOURCES.append(rel)

def digest(path:Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def deterministic_zip(path:Path, entries:list[tuple[str,bytes]]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(entries):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,data)

def generate(out:Path,repository:str,commit:str,evidence:Path):
    if not re.fullmatch(r'[0-9a-fA-F]{40}',commit):
        raise ValueError('source commit must be 40 hexadecimal characters')
    if '/' not in repository: raise ValueError('repository must be owner/name')
    if not SOURCE_SETS or not LOAD_PROFILES: raise ValueError('loader source sets or profiles missing')
    flattened=[x for values in SOURCE_SETS.values() for x in values]
    if len(flattened)!=len(set(flattened)): raise ValueError('source paths must belong to exactly one source set')
    for profile in LOAD_PROFILES:
        paths=sources_for_profile(profile)
        if PROFILE_DIGESTS.get(profile)!=inventory_digest(paths):
            raise ValueError(f'profile inventory digest mismatch: {profile}')
    missing=[x for x in ALL_SOURCES if not (ROOT/x).is_file()]
    if missing: raise FileNotFoundError('missing packaged source files: '+', '.join(missing))
    if not evidence.is_file(): raise FileNotFoundError('validation evidence manifest missing')
    ev=yaml.safe_load(evidence.read_text(encoding='utf-8'))
    if ev.get('repository_commit')!=commit or any(x.get('status')!='PASS' for x in ev.get('checks',[])):
        raise ValueError('validation evidence does not prove this commit')

    owner,repo=repository.split('/',1)
    out.mkdir(parents=True,exist_ok=True)
    (out/'schemas').mkdir(exist_ok=True)
    (out/'chatgpt-skills').mkdir(exist_ok=True)
    (out/'claude-project/.claude/skills').mkdir(parents=True,exist_ok=True)

    replacements={
        '{{MADP_GITHUB_OWNER}}':owner,
        '{{MADP_GITHUB_REPOSITORY}}':repo,
        '{{MADP_COMMIT_SHA}}':commit,
    }
    loader=LOADER_SOURCE.read_text(encoding='utf-8')
    for old,new in replacements.items(): loader=loader.replace(old,new)
    (out/'load-protocol-from-github.md').write_text(loader,encoding='utf-8')
    for name in ['quick-start.md','verified-start.md','invite-limited-participant.md','help.md']:
        shutil.copy2(ROOT/f'bootstrap/alpha3/{name}',out/name)

    files=[{'path':rel,'sha256':digest(ROOT/rel),'bytes':(ROOT/rel).stat().st_size} for rel in ALL_SOURCES]
    bootstrap_files=[{'path':name,'sha256':digest(out/name),'bytes':(out/name).stat().st_size,'source_commit':commit} for name in BOOTSTRAP_FILES]
    manifest={
        'bundle_version':'MADP-ALPHA3-BUNDLE-v4',
        'protocol_version':VERSION,
        'repository':repository,
        'source_commit':commit,
        'protocol_load_report_version':'MADP-PROTOCOL-LOAD-REPORT-v2',
        'inventory_digest_algorithm':'sha256-newline-paths-v1',
        'source_sets':SOURCE_SETS,
        'load_profiles':LOAD_PROFILES,
        'source_inventory_digests':PROFILE_DIGESTS,
        'packaged_source_count':len(ALL_SOURCES),
        'command_registry_policy':'ALPHA2_CANONICAL_SUPERSET',
        'canonical_command_count':51,
        'validation_evidence_sha256':digest(evidence),
        'files':files,
        'bootstrap_files':bootstrap_files,
    }
    (out/'manifest.yaml').write_text(yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True),encoding='utf-8')
    shutil.copy2(evidence,out/'validation-evidence.yaml')
    parts=['BEGIN_MADP_BUNDLE_METADATA',yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True).rstrip(),'END_MADP_BUNDLE_METADATA']
    for rel in ALL_SOURCES:
        parts += [f'BEGIN_FILE path={rel}',(ROOT/rel).read_text(encoding='utf-8').rstrip(),f'END_FILE path={rel}']
    (out/'complete-protocol-bundle.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')

    for name in SCHEMAS:
        src=ROOT/f'schemas/v0.3.0-alpha.3/{name}.schema.yaml'
        data=yaml.safe_load(src.read_text(encoding='utf-8'))
        def walk(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    if k=='$ref' and not str(v).startswith('#'): raise ValueError(f'external ref in {src}: {v}')
                    walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(data)
        (out/f'schemas/{name}.bundle.schema.yaml').write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')

    pack=[]
    for skill in SKILLS:
        data=(ROOT/f'skills/{skill}/SKILL.md').read_bytes()
        deterministic_zip(out/f'chatgpt-skills/{skill}.zip',[(f'{skill}/SKILL.md',data)])
        pack.append((f'{skill}/SKILL.md',data))
        dest=out/f'claude-project/.claude/skills/{skill}'
        dest.mkdir(parents=True,exist_ok=True)
        (dest/'SKILL.md').write_bytes(data)
    deterministic_zip(out/'chatgpt-skills/madp-skill-pack.zip',pack)
    return manifest

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output')
    ap.add_argument('--repository',default='Eruhitsuji/multi-ai-deliberation-protocol')
    ap.add_argument('--source-commit',required=True)
    ap.add_argument('--validation-evidence',required=True)
    a=ap.parse_args()
    try: m=generate(Path(a.output),a.repository,a.source_commit,Path(a.validation_evidence))
    except Exception as e:
        print('FAIL:',e)
        return 1
    print(f'alpha.3 release artifacts generated: {len(m["files"])} packaged sources, 3 load profiles, 5 bootstrap files, 5 Skills, 4 schemas')
    return 0

if __name__=='__main__': raise SystemExit(main())
