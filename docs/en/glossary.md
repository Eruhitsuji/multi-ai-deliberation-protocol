---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Explanatory glossary

English | [日本語](../ja/glossary.md)

> This glossary is explanatory. For normative meanings, use `protocol/GLOSSARY-v0.3.0-alpha.2.md`.

## Approval

A user-confirmed acceptance bound to a specific decision revision. Approval is not execution permission.

## Authority boundary

The limit on what an actor or command may do. Examples include read-only, propose-only, user-confirmed internal state change, and separately authorized external action.

## Command block

The normalized structured representation of a raw MADP command after parsing. It records command identity, issuer, arguments, authority boundary, and intended effects.

## Completion basis

Recorded evidence supporting why a TODO entered `DONE`. It should be specific and verifiable.

## Context package

A bounded transfer of operative state and relevant artifacts. It does not transfer authority by itself.

## Decision

A selected outcome or conclusion, versioned by revision. A decision may still require user approval.

## Execution permission

Action-specific authorization to perform an external or consequential operation. It is distinct from analysis, proposal, review, and approval.

## Fail closed

Reject or stop when required evidence, identity, scope, state freshness, or authority cannot be verified.

## Grant

A user-originated authorization artifact with action, scope, assurance, and activity state. Alpha.2 internal grants are single-use by default.

## Non-normative

Useful explanatory material that does not override the canonical protocol, schema, or registry.

## Proposal

A candidate change or outcome that has not been approved merely because it was produced by an AI or promoted from a TODO.

## Relay

A structured transfer between actors or AI instances. Relay content may carry context, tasks, or evidence but not implicit approval.

## Review response

A structured record of what a reviewer inspected, tested, found, and recommends. It is evidence, not merge approval.

## State version

A monotonic identifier for a versioned state document. Consumers should not silently replace newer official state with older transferred state.

## TODO

A tracked unit of work. A TODO is not a decision, approval, or execution permission.

## Trusted assurance

An assurance level and origin combination accepted by the applicable runtime or policy, such as user confirmation originating from an actual user action.
