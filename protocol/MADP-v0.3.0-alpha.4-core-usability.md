# MADP v0.3.0-alpha.4 Core Usability Extension

Status: implementation slice for review. This document is normative for the
alpha.4 Core Usability slice, but it is not a complete prerelease publication.

This extension builds on `MADP-v0.3.0-alpha.3`. Unless this document explicitly
changes a rule, the alpha.3 rule remains in force.

## Purpose

The Core Usability slice makes the smallest practical human-mediated workflow
explicit without weakening authority, provenance, or evidence boundaries.

It standardizes:

- eight non-atomic Workflow Macros;
- additive Claim and Evidence records;
- separate dissent state and human disposition;
- a revision-bound Human Final Authority decision;
- explicit separation between a decision and external-action authorization.

## Workflow Macros

The registered macros are:

`init`, `register`, `capture`, `structure`, `review`, `decide`, `authorize`,
and `status`.

A macro is a guided workflow, not a canonical command, alias, transaction, or
authority grant. Every accepted machine operation is recorded using a canonical
alpha.3 command. A macro may stop before completion at a human gate, validation
gate, missing-argument gate, stale-state rejection, or authority boundary.

A complete macro execution records:

- macro execution ID;
- source and resulting state versions;
- accepted canonical commands in order;
- encountered gates;
- completion status and stop reason.

Missing identifiers, revisions, approvers, scope, state versions, exposure
status, or authorization data must be requested rather than inferred.

## Claim and Evidence

Alpha.4 separates what a statement is from how well it has been verified.

`claim_kind` is one of:

- `SOURCE_CLAIM`
- `MODEL_INFERENCE`
- `PROPOSAL`
- `OPINION`

`verification_status` is one of:

- `UNCHECKED`
- `SOURCE_MATCHED`
- `CORROBORATED`
- `DISPUTED`
- `REFUTED`
- `OUTDATED`
- `NOT_APPLICABLE`

Existing alpha.3 `FACT` records remain valid historical and compatibility
inputs. Migration creates a new Claim record while preserving the original
record and revision. It must not silently upgrade verification.

Every Claim references at least one preserved raw response. Structured records
never replace the raw response.

Evidence remains multidimensional and records source role, claim fit,
freshness, traceability, and source independence. A single composite score is
not required and must not be treated as proof.

## Dissent

Dissent state and human disposition are separate.

`status` is one of `OPEN`, `RESOLVED`, or `SUPERSEDED`.

`disposition` is one of:

- `NONE`
- `ACCEPTED`
- `INCORPORATED`
- `REJECTED_WITH_RATIONALE`
- `OVERRIDDEN_BY_HUMAN`
- `WITHDRAWN`
- `REPLACED`

An `OPEN` dissent may be `OVERRIDDEN_BY_HUMAN`. That means the objection
remains unresolved and the human knowingly proceeded. It must remain visible in
the decision record.

## Human decision and external action

A Decision is revision-bound and records a Human Final Authority choice,
evidence references, acknowledged dissent, unresolved dissent, and rationale.

AI agreement, vote count, or convergence cannot replace the human decision.
Agreement among AI systems is not evidence.

A Decision does not itself authorize an external action. External-action status
is recorded as one of:

- `NOT_REQUESTED`
- `REQUIRES_SEPARATE_RECORD`
- `GRANTED_BY_SEPARATE_RECORD`

When status is `GRANTED_BY_SEPARATE_RECORD`, an exact authorization record
reference is required. The macro does not perform the action.

## Compatibility

This slice:

- preserves the alpha.3 canonical command namespace;
- does not remove or reinterpret existing alpha.3 artifacts;
- preserves legacy `FACT` records;
- introduces no breaking change to alpha.3 schemas;
- adds alpha.4 records and fixtures under versioned paths.

## Conformance

The executable checker validates schema structure and semantic invariants,
including bidirectional Claim/Evidence references, dissent visibility,
migration preservation, macro command ordering, and Human Final Authority.

A schema-valid record may still be semantically nonconforming. Semantic
failures must be reported and must not be relabeled as formal release evidence.

## Release boundary

This implementation slice does not create a tag, GitHub Release, Pages
publication, stable release, or formal release evidence.
