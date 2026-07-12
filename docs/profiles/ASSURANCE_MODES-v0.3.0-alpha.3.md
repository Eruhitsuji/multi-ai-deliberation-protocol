# Assurance Modes Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Modes

- `NORMAL`: ordinary reversible deliberation with standard revision and authority controls.
- `REVIEW_REQUIRED`: progress may continue in proposal form, but the affected transition cannot be attested as validated until review is complete.
- `STRICT`: fail closed for missing evidence, stale revision, unresolved authority, or required independent validation.

Use `assurance_state` from `advanced-profiles.schema.yaml`.

## Escalation and de-escalation

A human, AI facilitator, policy, or runtime may propose escalation. Escalation does not grant the proposer new authority. De-escalation from `STRICT` requires an independent validation basis. The facilitator must not validate its own de-escalation merely because it proposed the original concern.

A human may override a protocol recommendation when higher-priority rules allow it, but the resulting state is recorded as `OVERRIDDEN_WITH_DISSENT`, not `VALIDATED_NORMAL`.

## Authority separation

- human decision authority decides what the organization chooses;
- deterministic transition validation decides whether the recorded transition satisfies MADP conditions;
- AI facilitation remains `PROPOSE_ONLY` unless a separate rule grants a narrower role;
- platform safety rules may refuse prohibited assistance independently of MADP decision authority.
