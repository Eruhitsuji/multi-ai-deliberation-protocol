---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Context sharing and relay

English | [日本語](../ja/context-relay.md)

> This guide is explanatory. Context transfer does not grant authority.

## Why bounded context matters

Copying an entire conversation is noisy, expensive, and can reintroduce obsolete decisions. MADP instead transfers the operative state needed for the next task.

A context package should answer:

- What is the current goal?
- What has already been decided?
- What remains unresolved?
- Which artifacts are relevant?
- Which authority is available?
- Which actions remain prohibited?

## Recommended package contents

```yaml
context_package:
  protocol_version: MADP-v0.3.0-alpha.2
  purpose: independent review
  current_state:
    goal: review the command runtime
    branch: feature/example
    commit: 0123456789abcdef0123456789abcdef01234567
  artifacts:
    - path: scripts/apply_command.py
      role: implementation
    - path: scripts/test_command_runtime.py
      role: regression tests
  unresolved:
    - verify grant replay protection
  authority:
    allowed: [read, test, review]
    prohibited: [edit, commit, push, merge, tag, release]
```

## Receipt discipline

The receiver should produce a receipt that records:

- files actually available and read;
- missing or unread files;
- understood goal and constraints;
- state version or commit identity;
- authority understood;
- ambiguities or conflicts.

A receipt confirms understanding only. It does not prove that the transferred claims are true and does not authorize action.

## Relay modes

- `DELIBERATION`: continue structured reasoning.
- `INFORMATION_TRANSFER`: deliver bounded facts or artifacts.
- `REVIEW_REQUEST`: ask for independent review.
- `TASK_HANDOFF`: transfer responsibility for a scoped task.
- `EVIDENCE_TRANSFER`: transfer validation or research evidence.
- `RECOVERY`: reconstruct state after load or relay failure.

## Staleness and conflict

Fail closed when the receiver already has a newer official state, when commit identities conflict, or when the package claims authority not supported by the active user instruction.

Do not infer approval from:

- the presence of a context package;
- agreement among AIs;
- a prior review marked successful;
- a TODO marked complete;
- a branch being mergeable.
