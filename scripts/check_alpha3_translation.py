#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'docs/ja/v0.3.0-alpha.3/translation-manifest.yaml'

def git_blob_sha1(data: bytes) -> str:
    header=f'blob {len(data)}\0'.encode('ascii')
    return hashlib.sha1(header+data).hexdigest()

def main():
    problems=[]
    data=yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
    if data.get('protocol_version')!='MADP-v0.3.0-alpha.3': problems.append('translation protocol version mismatch')
    if data.get('normative_language')!='en' or data.get('translation_language')!='ja': problems.append('translation language metadata invalid')
    if data.get('hash_algorithm')!='git-blob-sha1': problems.append('translation hash algorithm mismatch')
    entries=data.get('entries',[])
    if len(entries)<8: problems.append('translation manifest incomplete')
    for e in entries:
        src=ROOT/e['source']; tr=ROOT/e['translation']
        if not src.is_file(): problems.append(f"missing source: {e['source']}"); continue
        if not tr.is_file(): problems.append(f"missing translation: {e['translation']}"); continue
        digest=git_blob_sha1(src.read_bytes())
        if digest!=e.get('source_git_blob_sha1'): problems.append(f"stale translation source hash: {e['source']} expected={e.get('source_git_blob_sha1')} actual={digest}")
        if e.get('status')!='COMPLETE': problems.append(f"translation not complete: {e['translation']}")
        text=tr.read_text(encoding='utf-8')
        if 'alpha.3' not in text and 'MADP' not in text: problems.append(f"translation lacks version context: {e['translation']}")
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print(f'alpha.3 Japanese translation audit: PASS ({len(entries)} entries)')
    return 0
if __name__=='__main__': raise SystemExit(main())
