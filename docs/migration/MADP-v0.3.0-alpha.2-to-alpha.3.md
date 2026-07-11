# Migration from MADP v0.3.0-alpha.2 to v0.3.0-alpha.3

Status: normative migration profile.

## Command compatibility

Alpha.3 does not replace the alpha.2 command namespace. It imports all 20 alpha.2 canonical commands and adds 31 commands.

| Alpha.2 input | Alpha.3 treatment |
| --- | --- |
| `status` | remains canonical broad status |
| `resume` | remains canonical pause/resume workflow command |
| `pause` | remains canonical workflow pause |
| all other alpha.2 commands | remain canonical with inherited safety behavior |

`session-status`, `session-resume`, and `help-exit` are separate alpha.3 commands. No migration may rewrite `status` or `resume` merely because earlier alpha.3 draft aliases used those spellings.

## State transformation

The reference migration script:

1. verifies the source protocol version;
2. preserves the source object;
3. retains session ID and state version;
4. wraps the source state as legacy evidence;
5. marks the target as `MIGRATED_PROPOSAL_ONLY`;
6. preserves or reduces authority;
7. emits a migration record for success, partial, failed, or quarantined outcomes.

A failed migration is still recordable. `source_raw_preserved` and `rollback_available` are factual booleans, not schema constants. A `SUCCESS` record, however, requires preserved source, passed authority invariants, no authority escalation, no inferred approval, and validation PASS.

## Revision binding

Migrated alpha.3 artifacts must carry session and source-state revision. Existing alpha.2 approvals remain bound to their original decision revision and are not broadened.

## Rollback

Rollback means retaining a usable source representation. When rollback is unavailable, record `rollback_available: false` and a failure reason; do not suppress the migration record.
