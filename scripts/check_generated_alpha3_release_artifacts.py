#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, sys, yaml

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory'); ap.add_argument('--source-commit',required=True); args=ap.parse_args()
    d=Path(args.directory); problems=[]
    required=['manifest.yaml','complete-protocol-bundle.txt','quick-start.md','verified-start.md','invite-limited-participant.md','help.md','schemas/deliberation.bundle.schema.yaml','schemas/command.bundle.schema.yaml','schemas/migration.bundle.schema.yaml']
    for r in required:
        if not (d/r).is_file(): problems.append(f'missing generated artifact: {r}')
    if (d/'manifest.yaml').is_file():
        m=yaml.safe_load((d/'manifest.yaml').read_text())
        if m.get('protocol_version')!='MADP-v0.3.0-alpha.3': problems.append('manifest protocol version mismatch')
        if m.get('source_commit')!=args.source_commit: problems.append('manifest source commit mismatch')
        if len(m.get('files',[]))<15: problems.append('manifest load set incomplete')
        bundle=(d/'complete-protocol-bundle.txt').read_text() if (d/'complete-protocol-bundle.txt').is_file() else ''
        for f in m.get('files',[]):
            if f'BEGIN_FILE path={f["path"]}' not in bundle or f'END_FILE path={f["path"]}' not in bundle: problems.append(f'bundle boundary missing: {f["path"]}')
        verified=(d/'verified-start.md').read_text() if (d/'verified-start.md').is_file() else ''
        if args.source_commit not in verified or 'MADP-v0.3.0-alpha.3' not in verified: problems.append('verified prompt is not commit pinned')
    for name in ['deliberation','command','migration']:
        p=d/f'schemas/{name}.bundle.schema.yaml'
        if p.is_file():
            data=yaml.safe_load(p.read_text())
            text=p.read_text()
            if '$ref:' in text:
                # Internal refs are permitted; external refs are not.
                def walk(x):
                    if isinstance(x,dict):
                        for k,v in x.items():
                            if k=='$ref' and not str(v).startswith('#'): problems.append(f'external ref in {p}: {v}')
                            walk(v)
                    elif isinstance(x,list):
                        for v in x: walk(v)
                walk(data)
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print('generated alpha.3 release artifacts: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
