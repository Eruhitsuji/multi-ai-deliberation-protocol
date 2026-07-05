# Multi-AI Deliberation Protocol v0.3.0-alpha.1

## Status

This document is an alpha prerelease specification. It is not stable. The user remains the sole final decision-maker. Convergence among AI participants is not evidence and does not create approval or execution authority.

## 1. Purpose

MADP defines a service-neutral protocol for structured deliberation, state transfer, approval binding, and fail-closed execution authorization across AI systems, role actors, human validators, and tools.

## 2. Authority domains

1. Versioned JSON Schemas control field names, types, required properties, and enum spelling.
2. This protocol controls behavior, transitions, authorization, migration, and conformance.
3. The versioned glossary controls normative term meanings.
4. README, bootstrap prompts, examples, and generated bundles are informative unless explicitly stated otherwise.

A conflict among authority domains MUST be reported and MUST NOT be silently resolved.

## 3. Core rules

- The user is the sole final decision-maker.
- Majority vote alone is insufficient.
- AI agreement is convergence, not evidence.
- `SESSION_STATE` is the sole logical source of truth.
- Deliberation outcome, user approval, permission grants, and execution are distinct.
- Unknown actions, stale state, empty scope, and ambiguous authority fail closed.
- Active sessions MUST NOT auto-upgrade across protocol versions.

## 4. Actors

Each participant has a machine-readable `type`, free-form `role`, and `status`.

At most one participant whose `type` is `FACILITATOR` may have `status: ACTIVE`. The invariant is evaluated from `type`, never from free-form `role` text.

Role actors inside one model/context have review independence `I0` and MUST NOT be represented as independent evidence.

## 5. State and roots

MADP v0.3 uses separate canonical document roots:

- `session_state` documents validate against the Session State root schema.
- `relay_block` documents validate against the Relay Block root schema.

A relay-only document is not required to contain `session_state` at the top level.

Persistent or transferred state uses monotonically increasing `state_version` and matching `parent_version`. A stale or split-brain state MUST NOT overwrite current state automatically.

## 6. Permission requests and grants

A permission request represents requested authority and MAY contain an unknown non-empty action identifier.

A permission grant represents active authority and is restricted to recognized core actions. Unknown actions MUST NOT be granted automatically.

Every permission grant MUST include:

- `action`;
- non-empty `scope`;
- `assurance_level`;
- `assurance_origin`.

Trusted active grants are limited to:

- `USER_CONFIRMED` with `assurance_origin: USER_ACTION`; or
- `EXTERNALLY_VERIFIED` with `assurance_origin: EXTERNAL_VALIDATION` and a non-empty `reference`.

AI-generated candidates MUST remain permission requests or state-change proposals and MUST NOT be promoted to active grants without trusted provenance.

## 7. Decisions and approvals

A decision contains a stable `id`, positive integer `revision`, deliberation outcome, approval status, and summary.

Approval MUST be bound to both `decision_id` and `decision_revision`.

Affirmative approval statuses are:

- `APPROVE`;
- `APPROVE_WITH_CONDITIONS`;
- `APPROVE_WITH_CHANGES`.

An affirmative approval MUST have trusted assurance. `UNVERIFIED_ASSERTION` cannot make an affirmative approval authoritative and cannot authorize execution.

An AI may record a recommendation, but it MUST NOT infer or fabricate user approval.

## 8. Execution gate

Execution MUST be denied unless all of the following hold:

1. the requested action is recognized;
2. a matching active permission grant exists;
3. scope is non-empty and covers the operation;
4. grant assurance and origin satisfy Section 6;
5. any required approval is bound to the current decision revision;
6. applicable conditions are satisfied with required assurance;
7. state and task bindings are current.

Approval alone does not grant execution permission.

## 9. Relay blocks and digest

A Relay Block contains metadata and an `operative_session_state_snapshot`.

The following invariants apply:

```text
relay_block.session_id = relay_block.operative_session_state_snapshot.meta.session_id
relay_block.source_state_version = relay_block.operative_session_state_snapshot.meta.state_version
```

`relay_block.snapshot_digest` is optional in alpha.1. When present, it contains:

- `canonicalization: MADP_JCS_V1`;
- `algorithm: SHA-256`;
- a 64-character lowercase hexadecimal value;
- provenance.

`TRANSPORT_VERIFIED` additionally requires a non-empty external verification reference. `POST_INGRESS_BASELINE` proves only a new local forward-integrity baseline and MUST NOT be described as proof of pre-ingress integrity, sender identity, or transport completeness.

## 10. MADP_JCS_V1

`MADP_JCS_V1` uses RFC 8785 JSON Canonicalization Scheme over the MADP JSON-compatible data model.

Allowed values are objects with string keys, arrays, strings, booleans, null, and integers from `-9007199254740991` through `9007199254740991`.

Before canonicalization, implementations MUST reject:

- duplicate mapping keys;
- non-string mapping keys;
- floating-point values, NaN, and Infinity;
- YAML aliases and anchors;
- custom YAML tags;
- tabs used for indentation;
- disallowed control characters.

The canonical byte stream is UTF-8 without BOM. SHA-256 output uses exactly 64 lowercase hexadecimal characters.

## 11. Protocol loading evidence

A protocol load report distinguishes retrieval from verification. It SHOULD record access result, access method, byte length, content hash when available, and verification status.

A self-attested `READ` statement is not external proof that the complete content was read. Formal schema validation MUST NOT be claimed unless an actual validator was executed. A validation receipt SHOULD identify validator, schema, instance, result, and error count.

## 12. Migration from v0.2.5-rc.2

Migration is forward-only and atomic.

Normative migration invariants:

- `AMI-001`: no automatic authority increase;
- `AMI-002`: no fabricated provenance;
- `AMI-003`: no silent assurance-category reclassification;
- `AMI-004`: a post-ingress digest establishes only a local forward baseline;
- `AMI-005`: downgrade or rollback MUST NOT recreate a known unsafe authoritative state.

Migration rules:

- `MIG-001`: a legacy user-confirmed grant may become an active v0.3 grant only when independent provenance evidence is supplied.
- `MIG-002`: a legacy grant with unknown provenance is removed from active grants and represented as `USER_ESCALATION_REQUIRED`.
- `MIG-003`: `EXTERNALLY_VERIFIED` without a reference is not converted to `USER_CONFIRMED`; it requires evidence or new user confirmation.
- `MIG-004`: affirmative approval with unverified assurance is safely downgraded to `PENDING`.
- `MIG-005`: multiple active facilitators abort migration and require user selection.
- `MIG-006`: legacy states are accepted only as migration input; successful output is written only in the target version.
- `MIG-007`: local digest computation after ingress MUST be labeled `POST_INGRESS_BASELINE`.

Official migration results are `COMPLETED`, `REJECTED`, or `ABORTED`. `PARTIAL` is prohibited. A completed migration may include `quarantined_items` when every output object conforms to the target version.

An aborted migration MUST leave the authoritative source state unchanged. Its attempt record is stored outside the source state.

## 13. Error namespace

Migration-specific errors use the `MIG_` prefix. The alpha.1 registry includes:

- `MIG_LEXICAL_SOURCE_INVALID`;
- `MIG_SOURCE_SCHEMA_INVALID`;
- `MIG_MULTIPLE_ACTIVE_FACILITATORS`;
- `MIG_UNKNOWN_GRANT_PROVENANCE`;
- `MIG_FABRICATED_PROVENANCE`;
- `MIG_AUTHORITY_CATEGORY_RECLASSIFICATION`;
- `MIG_AUTOMATIC_FACILITATOR_RESOLUTION`;
- `MIG_FALSE_DIGEST_PROVENANCE`;
- `MIG_VERSION_NOT_UPDATED`;
- `MIG_UNSAFE_OFFICIAL_DOWNCAST`;
- `MIG_TARGET_SCHEMA_INVALID`;
- `MIG_TARGET_SEMANTIC_INVALID`;
- `MIG_AUDIT_INCOMPLETE`.

## 14. Alpha limitations

Alpha.1 defines the security model, canonical schemas, migration contract, fixture corpus, and digest contract. It does not claim:

- arbitrary automatic rc.2 migration;
- complete semantic validation;
- cross-language digest interoperability;
- universal cross-model portability;
- structured-output API compatibility;
- production readiness.

## 15. Release authority

Implementation completion, merge, tagging, and release publication are separate actions. Published historical tags are immutable. Each action requires explicit user authorization.