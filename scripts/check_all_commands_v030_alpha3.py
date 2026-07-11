#!/usr/bin/env python3
import json, shlex
from parse_command_v030_alpha3 import registry, normalize
from apply_command_v030_alpha3 import HANDLER_STRATEGIES

def encode(v):
    if isinstance(v, (dict,list)): return json.dumps(v, separators=(',',':'))
    if isinstance(v, bool): return 'true' if v else 'false'
    return str(v)

def main():
    data=registry(); commands=data['commands']; names={x['command'] for x in commands}
    alpha2=set(data['composition']['inherited_alpha2_commands'])
    required_alpha2={'share-context','issue-relay','request-review','summarize-state','check-authority','propose-decision','approve','reject','defer','prioritize','pause','resume','status','todo-add','todo-list','todo-update','todo-done','todo-defer','todo-promote','external-action'}
    assert alpha2==required_alpha2, sorted(alpha2^required_alpha2)
    aliases={x['alias']:x['command'] for x in data['aliases']}
    assert not (set(aliases)&names), 'alias collides with canonical command'
    assert 'status' not in aliases and 'resume' not in aliases and 'pause' not in aliases
    assert set(HANDLER_STRATEGIES)==names
    for entry in commands:
        parts=['/madp',entry['command']]
        for key,value in entry.get('test_arguments',{}).items():
            values=value if isinstance(value,list) else [value]
            for item in values: parts += [f'--{key}', encode(item)]
        raw=' '.join(shlex.quote(p) for p in parts)
        parsed=normalize(raw, issued_by='USER' if entry['command_class']=='USER_COMMAND' or entry['command'] in {'approve','reject','defer','prioritize','pause','resume','status'} else 'SYSTEM')
        assert 'command_block' in parsed, (entry['command'], raw, parsed)
        assert parsed['command_block']['command']==entry['command']
    for alias,target in aliases.items():
        entry=next(x for x in commands if x['command']==target)
        parts=['/madp',alias]
        for key,value in entry.get('test_arguments',{}).items():
            values=value if isinstance(value,list) else [value]
            for item in values: parts += [f'--{key}', encode(item)]
        parsed=normalize(' '.join(shlex.quote(p) for p in parts), issued_by='USER')
        assert 'command_block' in parsed and parsed['command_block']['command']==target and parsed['command_block']['alias_used']
    print(f'MADP-v0.3.0-alpha.3 all-command coverage: PASS ({len(names)} canonical, {len(aliases)} aliases)')
    return 0
if __name__=='__main__': raise SystemExit(main())
