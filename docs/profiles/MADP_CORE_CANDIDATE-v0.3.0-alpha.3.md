# MADP Core Candidate Profile for MADP v0.3.0-alpha.3

Status: experimental normative candidate profile. It does not amend the alpha.3
runtime, complete a release blocker, or authorize alpha.4 implementation.

Decision basis: `docs/planning/DEC-MADP-CORE-001.yaml`.

## Purpose

Test a minimum useful MADP layer for human-mediated multi-AI deliberation without
requiring metered APIs, agent orchestration, A2A, MCP, or a vendor-specific
runtime.

The Core Candidate exists to prevent multiple AI responses from being used in a
decision with incorrect assumptions about evidence, authority, provenance, or
independence.

## Scope boundary

Core Candidate operation:

- treats manual copy-and-paste and plain-text relay as first-class mechanisms;
- permits local CLI, Python, hashing, and schema validation without paid APIs;
- keeps A2A, MCP, Agent SDK, and automatic model invocation in optional
  Automation Extensions;
- preserves the alpha.3 canonical command registry and runtime invariants;
- uses `registries/v0.3.0-alpha.3/workflow-macros.yaml` only as a human-facing,
  non-atomic orchestration layer.

No macro, profile, participant response, model consensus, approval, or decision
implicitly authorizes an external action.

## Core invariants

### Human Final Authority

A human records the final decision. AI participants remain `PROPOSE_ONLY` or
`OPINION_ONLY` unless a separate trusted authority record explicitly says
otherwise. Agreement Is Not Evidence, and majority support is not approval.

### Blind First Round

Every conforming multi-participant Core Candidate deliberation performs a Blind
First Round before Cross Exposure.

Minimum requirements:

```yaml
blind_first_round:
  minimum_eligible_initial_responses: 2
  exposure_before_capture: false
  preserve_raw_initial_responses: true
  overwrite_initial_responses: false
```

Each initial response records:

```yaml
exposure:
  state: UNEXPOSED | PARTIALLY_EXPOSED | EXPOSED | UNKNOWN
  exposed_response_refs: []
```

`UNKNOWN` must remain `UNKNOWN`; it must not be upgraded to `UNEXPOSED` by
inference. Responses from the same model family, shared chat, shared retrieval
source, or other known common origin may be retained, but their correlation must
be recorded and they must not be counted as independently corroborating
sources.

If prior conclusions are exposed before the initial response is fixed, classify
the result as `PARTIALLY_COMPROMISED`, `ANCHORING_EXPOSED`, or
`NOT_PERFORMED`. The response may remain ordinary review evidence, but the run
must not be represented as a conforming Blind First Round.

### Raw response preservation

Preserve raw prompts and responses before normalization. Normalized responses,
claims, summaries, minutes, and decisions reference raw records and never replace
them.

### Claim, Evidence, Dissent, and Decision separation

Keep these records distinct:

- a Claim records what is asserted;
- Evidence records what supports or challenges a Claim;
- Dissent records a material unresolved objection;
- a Decision records the human choice, rationale, revision, acknowledged
  dissent, and supporting references.

The candidate direction separates speech form from verification state:

```yaml
claim_candidate:
  claim_kind: SOURCE_CLAIM | MODEL_INFERENCE | PROPOSAL | OPINION
  verification_status: UNCHECKED | SOURCE_MATCHED | CORROBORATED | DISPUTED | REFUTED | OUTDATED | NOT_APPLICABLE
```

This is a migration target, not permission to delete the existing alpha.3
`FACT` representation. Existing fields remain until replacement schemas,
negative fixtures, migration logic, and safety-invariant tests are complete.

Evidence assessment remains multidimensional:

```yaml
evidence_assessment:
  source_role: DIRECT_RECORD | PRIMARY | SECONDARY | TERTIARY | USER_STATEMENT | MODEL_ONLY | UNKNOWN
  claim_fit: DIRECT | PARTIAL | INDIRECT | UNSUPPORTED | UNKNOWN
  freshness: CURRENT | POTENTIALLY_STALE | STALE | TIME_INDEPENDENT | UNKNOWN
  traceability: SNAPSHOT_HASHED | RETRIEVABLE | CITATION_ONLY | NONE
  source_independence: INDEPENDENTLY_CORROBORATED | SINGLE_SOURCE | DERIVED_FROM_SAME_ORIGIN | UNKNOWN
```

A display summary may be derived in an Assured profile, but Core does not require
or trust a single composite evidence score.

### Dissent state and disposition

Do not collapse unresolved state into a resolution reason.

```yaml
dissent_candidate:
  status: OPEN | RESOLVED | SUPERSEDED
  disposition: NONE | ACCEPTED | INCORPORATED | REJECTED_WITH_RATIONALE | OVERRIDDEN_BY_HUMAN | WITHDRAWN | REPLACED
```

For example, `status: OPEN` with `disposition: OVERRIDDEN_BY_HUMAN` records that
the objection remains unresolved and that the human knowingly proceeded.

### Revision-bound decision and authorization

Approval binds to the exact decision revision. A decision, approval, and
Execution Authorization are separate. Execution Authorization is optional when
there is no external action, but the semantic separation is always preserved.

## Minimum records

A Core Candidate run preserves at least:

1. protocol binding;
2. participant and correlation register;
3. question, scope, and authority boundary;
4. raw initial responses and exposure records;
5. Cross Exposure and revision records, when used;
6. Claim and Evidence records sufficient for the decision;
7. Dissent records;
8. a revision-bound human Decision Record.

Minimum protocol binding:

```yaml
protocol_binding:
  protocol_version: MADP-v0.3.0-alpha.3
  source_ref: repository-commit-or-release
  source_digest: "<sha256 or documented unavailable status>"
  profile_path: docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md
```

A formal FIELD_TRIAL or Assured run additionally uses the complete alpha.3 load
report, profile binding, validation receipts, raw observation inventory, and
recomputation requirements. The minimum Core binding does not substitute for
those release-evidence controls.

## Human-facing interaction contract

At every legitimate pause, show:

```yaml
CURRENT_STATE: "..."
CURRENT_QUESTION: "..."
FACILITATOR_ACTION: "..."
HUMAN_DECISION_REQUIRED: "... or NONE"
NEXT_ACTION: "..."
CANONICAL_EXPANSION: []
```

Natural-language choices may be offered, but the accepted action is recorded as
canonical command invocations with exact IDs, revisions, and state versions.

## Workflow Macro use

The human-facing macros are `init`, `register`, `capture`, `structure`, `review`,
`decide`, `authorize`, and `status`.

Macros are not aliases and are not atomic. They may stop at an explicit user or
validation gate. Every executed step is recorded using the existing canonical
command name. Missing required arguments are requested rather than inferred.

See `docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md` and
`registries/v0.3.0-alpha.3/workflow-macros.yaml`.

## Conformance and graceful degradation

A run may be useful without being fully conforming. Report the reason precisely.

```yaml
core_candidate_conformance:
  status: CONFORMING | DEGRADED | NONCONFORMING | NOT_EVALUATED
  reasons: []
```

Blind First Round failure, missing raw records, inferred exposure, unbound
approval, or authority ambiguity prevents `CONFORMING`. Degraded evidence may be
retained for ordinary review, but must not be relabeled as formal FIELD_TRIAL
evidence or used to complete a release blocker.

## Comparative evaluation

Compare this profile with standard alpha.3, ordinary manual comparison, and a
Markdown-plus-validator workflow. Measure completion time, human actions,
canonical commands, corrections, unclear next actions, authority and stale-state
errors, Blind First Round status, dissent preservation, decision reconstruction,
and user burden.

alpha.4 remains deferred until comparative evidence supports a version change.
