# Communication Alignment Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Purpose

Prevent intent, assumption, scope, assertion, state, and acceptance mismatches without duplicating the core goal gate, claim ledger, or revision rules.

## Alignment contract

Use `alignment_contract` from `advanced-profiles.schema.yaml` to record purpose, assumptions, scope, claim-label policy, acceptance criteria, and checkpoint policy.

Assumptions that materially affect a decision are marked `QUESTION_REQUIRED` until confirmed or rejected. The facilitator must not silently turn an unresolved assumption into fact.

## Scope checkpoints

Emit a `scope_check` when one of the following occurs:

- the configured revision interval is reached;
- a new policy or decision family appears;
- a new output type not present in the confirmed plan is introduced;
- the current topic appears outside the confirmed scope.

`SCOPE_EXPANSION` or `OUT_OF_SCOPE` requires a goal revision before substantive work on the expanded topic. `IN_SCOPE` may continue without a user pause when no material choice is required.

## Assertion policy

Internal model confidence is not directly observable evidence. Match assertion strength to provenance and verification status. Strong factual wording without adequate evidence is recorded as an assertion mismatch and routed to review.
