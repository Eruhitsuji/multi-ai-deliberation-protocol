# Migration from MADP-v0.3.0-alpha.2 to alpha.3

Migration is additive. The alpha.2 source state remains immutable evidence; alpha.3 artifacts are derived records.

## Invariants

- Preserve the original alpha.2 state or artifact reference.
- Do not infer user or team approval.
- Do not increase participant authority.
- Convert an alpha.2 role actor to an `AI_ROLE_ACTOR` participant with `independence_level: I0` unless stronger provenance is separately established.
- Preserve TODO, decision, review, context, and relay identifiers.
- Record unknown capability values as `UNKNOWN`; do not guess them.
- Record information loss and limitations.
- Keep rollback available by retaining the source artifact.

## Suggested mapping

| alpha.2 concept | alpha.3 target |
|---|---|
| facilitator or participant actor | `participant_profile` |
| role label | `role_assignment_plan` entry |
| relay response | raw response plus `response_ingest_record` |
| informal objective | `deliberation_plan` with `goal_status: PENDING` until confirmed |
| review findings | claim ledger entries or normalized opinion |
| TODO | unchanged TODO reference; not promoted to decision |

The migration record validates the process but does not itself prove that every target artifact is semantically correct. Human review is required for material ambiguity.
