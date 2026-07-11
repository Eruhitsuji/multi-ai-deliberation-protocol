---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Authority model

MADP separates information, approval, and permission.

## Authority boundaries

- `REFERENCE_ONLY`: information may be read; state is not changed.
- `PROPOSE_ONLY`: an AI may propose, but application requires trusted user authorization.
- `REQUIRES_USER_CONFIRMATION`: the requested action waits for a trusted, scoped confirmation.
- `USER_CONFIRMED`: the user issued the applicable command or confirmation.
- `DENIED`: the command must not be applied.

## Trusted grants

Alpha.2 validates grant issuer, scope, action, assurance level, assurance origin, active state, and replay status. Grants are single-use by default.

## External actions

The alpha.2 runtime does not execute external actions. A command, approval, review result, or context package cannot by itself authorize commit, push, merge, tag, release, message sending, or external-resource modification.

## Audit behavior

Accepted commands may produce a versioned audit event. Rejected commands do not alter the versioned state or command history.
