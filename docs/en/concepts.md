---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Core concepts

## Separation of meanings

```text
TODO != decision
decision != approval
approval != execution permission
review != merge approval
agreement != evidence
```

## Roles

- **USER**: sole final decision-maker.
- **FACILITATOR**: coordinates the deliberation and operative state.
- **PARTICIPANT**: contributes bounded analysis or proposals.
- **VALIDATOR / REVIEWER**: checks evidence, structure, or implementation without inheriting execution authority.
- **EXECUTION AGENT**: acts only within separately granted permission.

## Operative state

Share the smallest current state needed for the receiving actor. Context packages, review requests, and relay artifacts transfer information; they do not transfer authority.

## Fail-closed behavior

Unknown commands, malformed documents, stale or unsupported authority assertions, and external actions without explicit permission must not be applied.
