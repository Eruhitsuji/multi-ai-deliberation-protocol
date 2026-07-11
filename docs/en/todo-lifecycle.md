---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# TODO lifecycle

English | [日本語](../ja/todo-lifecycle.md)

> This guide is explanatory. The schema and shared transition table are authoritative for machine validation.

## What a TODO means

A TODO records work that should be performed or investigated. It is not:

- a decision;
- an approval;
- execution permission;
- evidence that the work is correct;
- permission to merge or release.

## States

- `OPEN`: accepted work not yet started.
- `IN_PROGRESS`: actively being worked.
- `BLOCKED`: cannot continue without resolving a dependency.
- `DEFERRED`: intentionally postponed.
- `DONE`: completed with a recorded completion basis.
- `CANCELLED`: intentionally abandoned.

`DONE` and `CANCELLED` are terminal. In alpha.2 their metadata is immutable through the runtime.

## Typical transitions

```text
OPEN -> IN_PROGRESS -> DONE
OPEN -> BLOCKED -> IN_PROGRESS
OPEN -> DEFERRED -> OPEN
OPEN/IN_PROGRESS/BLOCKED/DEFERRED -> CANCELLED
```

Use `todo-done` rather than a generic status update to enter `DONE`, because completion requires an explicit basis.

## Good completion basis

A completion basis should be verifiable and specific:

```yaml
completion_basis:
  - parser regression tests passed
  - authority counterexamples reproduced as closed
  - CI run 123456 completed successfully
```

Weak bases such as “looks done” or “AI says complete” should not be treated as strong evidence.

## Blocking information

When marking a TODO as `BLOCKED`, record:

- what is missing;
- who or what can resolve it;
- whether user input is required;
- the next safe action that can still proceed.

## Promotion

Promoting a TODO creates a proposal or decision candidate. It does not approve the promoted item. Keep the promoted artifact in a proposed state until the applicable authority acts.

## Audit rules

- Preserve stable TODO identifiers.
- Do not reuse identifiers after deletion or cancellation.
- Record status changes and completion basis.
- Reject invalid transitions.
- Do not rewrite terminal items to alter the historical record.
