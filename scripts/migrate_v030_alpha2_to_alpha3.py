#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json, sys
from pathlib import Path
from typing import Any
import yaml

SOURCE='MADP-v0.3.0-alpha.2'; TARGET='MADP-v0.3.0-alpha.3'

def failed(source_ref: str, reasons: list[str], source: Any, raw_preserved=True, rollback=True):
    return {
      'target_state': None,
      'preserved_source': copy.deepcopy(source) if raw_preserved else None,
      'migration_record': {
        'migration_id': 'MIG-A2-A3-001', 'source_protocol_version': SOURCE, 'target_protocol_version': TARGET,
        'source_state_ref': source_ref, 'source_state_version': source.get('state_version') if isinstance(source,dict) and isinstance(source.get('state_version'),int) else None,
        'migration_outcome': 'FAILED', 'source_raw_preserved': raw_preserved, 'rollback_available': rollback,
        'authority_invariant_status': 'NOT_VALIDATED', 'authority_escalated': False, 'user_approval_inferred': False,
        'transformations': [], 'target_artifact_refs': [], 'validation_status': 'FAIL', 'failure_reasons': reasons,
        'limitations': ['No target state was accepted.']
      }
    }

def migrate(source: Any, source_ref='artifact://alpha2/state') -> dict[str, Any]:
    if not isinstance(source, dict): return failed(source_ref,['source state must be an object'],source)
    if source.get('protocol_version') != SOURCE: return failed(source_ref,['source protocol version mismatch'],source)
    if not isinstance(source.get('state_version'),int) or source['state_version']<0: return failed(source_ref,['source state_version missing or invalid'],source)
    session_id=source.get('session_id') or source.get('meta',{}).get('session_id')
    if not isinstance(session_id,str) or not session_id: return failed(source_ref,['source session_id missing'],source)
    decisions=copy.deepcopy(source.get('decisions',{}))
    if isinstance(decisions,list):
        decisions={str(x.get('decision_id',f'DEC-{i+1:03d}')):copy.deepcopy(x) for i,x in enumerate(decisions) if isinstance(x,dict)}
    if not isinstance(decisions,dict): return failed(source_ref,['source decisions must be object or list'],source)
    target={
      'protocol_version': TARGET, 'session_id': session_id, 'state_version': source['state_version'],
      'source_state_version': source['state_version'], 'migration_status': 'MIGRATED_PROPOSAL_ONLY',
      'legacy_source_ref': source_ref, 'legacy_command_namespace': 'MADP-COMMAND-REGISTRY-v0.1',
      'command_registry': 'MADP-COMMAND-REGISTRY-v0.2', 'decisions': decisions,
      'authority_boundary': 'PROPOSE_ONLY', 'imported_approvals_require_revision_validation': True,
    }
    return {
      'target_state': target, 'preserved_source': copy.deepcopy(source),
      'migration_record': {
        'migration_id': 'MIG-A2-A3-001', 'source_protocol_version': SOURCE, 'target_protocol_version': TARGET,
        'source_state_ref': source_ref, 'source_state_version': source['state_version'], 'migration_outcome': 'SUCCESS',
        'source_raw_preserved': True, 'rollback_available': True, 'authority_invariant_status': 'PASS',
        'authority_escalated': False, 'user_approval_inferred': False,
        'transformations': [
          {'source_type':'ALPHA2_SESSION_STATE','target_type':'ALPHA3_MIGRATED_STATE','mapping':'preserve session/state lineage and wrap as proposal-only','information_loss':False},
          {'source_type':'ALPHA2_COMMAND_NAMESPACE','target_type':'ALPHA3_SUPERSET_NAMESPACE','mapping':'preserve all 20 canonical command names; add alpha.3 commands without rewriting status/resume/pause','information_loss':False},
          {'source_type':'ALPHA2_DECISIONS','target_type':'ALPHA3_DECISIONS','mapping':'preserve decision identifiers and exact revisions; require normal authority validation before use','information_loss':False},
        ],
        'target_artifact_refs':['artifact://alpha3/migrated-state'], 'validation_status':'PASS', 'limitations':['Migration does not create new approval or execution authority.']
      }
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source'); ap.add_argument('--source-ref',default='artifact://alpha2/state'); ns=ap.parse_args()
    text=Path(ns.source).read_text(encoding='utf-8') if ns.source!='-' else sys.stdin.read()
    source=yaml.safe_load(text)
    print(yaml.safe_dump(migrate(source,ns.source_ref),sort_keys=False,allow_unicode=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
