#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, shutil, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
LOAD_SET=[
 'README-v0.3.0-alpha.2.md',
 'protocol/MADP-v0.3.0-alpha.2.md',
 'protocol/GLOSSARY-v0.3.0-alpha.2.md',
 'README-v0.3.0-alpha.3.md',
 'protocol/MADP-v0.3.0-alpha.3.md',
 'protocol/GLOSSARY-v0.3.0-alpha.3.md',
 'schemas/v0.3.0-alpha.3/deliberation.schema.yaml',
 'schemas/v0.3.0-alpha.3/command.schema.yaml',
 'schemas/v0.3.0-alpha.3/migration.schema.yaml',
 'registries/v0.3.0-alpha.3/commands.yaml',
 'docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md',
 'docs/profiles/MADP_HELP-v0.3.0-alpha.3.md',
 'docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md',
 'docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md',
 'docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md',
]
SCHEMAS=[
 'schemas/v0.3.0-alpha.3/deliberation.schema.yaml',
 'schemas/v0.3.0-alpha.3/command.schema.yaml',
 'schemas/v0.3.0-alpha.3/migration.schema.yaml',
]

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def generate(out:Path, repository:str, commit:str):
    if len(commit)!=40 or any(c not in '0123456789abcdefABCDEF' for c in commit): raise ValueError('source commit must be 40 hexadecimal characters')
    missing=[x for x in LOAD_SET if not (ROOT/x).is_file()]
    if missing: raise FileNotFoundError('missing load-set files: '+', '.join(missing))
    out.mkdir(parents=True,exist_ok=True); (out/'schemas').mkdir(exist_ok=True)
    files=[]
    for rel in LOAD_SET:
        p=ROOT/rel; files.append({'path':rel,'sha256':digest(p),'bytes':p.stat().st_size})
    manifest={'bundle_version':'MADP-ALPHA3-BUNDLE-v1','protocol_version':VERSION,'repository':repository,'source_commit':commit,'files':files}
    (out/'manifest.yaml').write_text(yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True),encoding='utf-8')
    parts=['BEGIN_MADP_BUNDLE_METADATA',yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True).rstrip(),'END_MADP_BUNDLE_METADATA']
    for rel in LOAD_SET:
        parts += [f'BEGIN_FILE path={rel}',(ROOT/rel).read_text(encoding='utf-8').rstrip(),f'END_FILE path={rel}']
    (out/'complete-protocol-bundle.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
    owner,repo=repository.split('/',1)
    rows=[]
    for rel in LOAD_SET:
        url=f'https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{rel}'
        rows.append(f'- `{rel}`\n  {url}')
    verified = (
        "---\n"
        "bootstrap_version: 0.4\n"
        f"protocol_version: {VERSION}\n"
        "usage_mode: VERIFIED\n"
        f"repository_commit: {commit}\n"
        "---\n\n# Load MADP alpha.3 verified bundle\n\n"
        "Read every file below from the same immutable commit. Report READ, PARTIALLY_READ, or FAILED for each file. Do not infer unread content.\n\n"
        + "\n".join(rows)
        + "\n\nDo not begin substantive deliberation until all required files are read, the deliberation goal is confirmed when required, participant authority is explicit, and schema validation limitations are reported. Default authority is PROPOSE_ONLY.\n"
    )
    (out/'verified-start.md').write_text(verified,encoding='utf-8')
    shutil.copy2(ROOT/'bootstrap/alpha3/quick-start.md',out/'quick-start.md')
    shutil.copy2(ROOT/'bootstrap/alpha3/invite-limited-participant.md',out/'invite-limited-participant.md')
    shutil.copy2(ROOT/'bootstrap/alpha3/help.md',out/'help.md')
    for rel in SCHEMAS:
        data=yaml.safe_load((ROOT/rel).read_text(encoding='utf-8'))
        refs=[]
        def walk(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    if k=='$ref': refs.append(v)
                    walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(data)
        bad=[r for r in refs if not str(r).startswith('#')]
        if bad: raise ValueError(f'non-standalone refs in {rel}: {bad}')
        name=Path(rel).name.replace('.schema.yaml','.bundle.schema.yaml')
        (out/'schemas'/name).write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
    return manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output'); ap.add_argument('--repository',default='Eruhitsuji/multi-ai-deliberation-protocol'); ap.add_argument('--source-commit',required=True); args=ap.parse_args()
    try: manifest=generate(Path(args.output),args.repository,args.source_commit)
    except Exception as e: print(f'FAIL: {e}',file=sys.stderr); return 1
    print(f'alpha.3 release artifacts generated: {len(manifest["files"])} source files')
    return 0
if __name__=='__main__': raise SystemExit(main())
