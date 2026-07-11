---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Getting started with MADP

MADP structures multi-AI deliberation while keeping the user as the sole final decision-maker.

## Minimal flow

1. State the issue, fixed requirements, and evaluation criteria.
2. Assign a facilitator and bounded participant roles.
3. Share only the operative current state, not unnecessary conversation history.
4. Separate proposals, decisions, approvals, and execution permissions.
5. Require explicit user authorization for external or irreversible actions.

## Alpha.2 command pipeline

```text
Parse -> Normalize -> Validate -> Authorize -> Apply
```

Raw command text is never authoritative by itself. Use the versioned protocol and command registry for exact behavior.

## Start here

- Read [Core concepts](concepts.md).
- Read [Authority model](authority-model.md).
- Review [Commands](commands.md).
- For normative details, read [`protocol/MADP-v0.3.0-alpha.2.md`](../../protocol/MADP-v0.3.0-alpha.2.md).
