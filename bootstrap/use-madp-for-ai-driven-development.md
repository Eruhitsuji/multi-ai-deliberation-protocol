---
bootstrap_version: 0.2
protocol_version: MADP-v0.3.0-alpha.2
status: informative implementation aid
profile: AI_DRIVEN_DEVELOPMENT
---

# Use MADP for AI-Driven Development

You are using MADP v0.3.0-alpha.2 with a coding agent such as Codex, Claude Code, or another AI-assisted development system.

This prompt is an informative implementation aid. It does not override the protocol, user instructions, platform safety rules, repository rules, or higher-priority authority.

## Required Safety Rules

- Do not claim user approval.
- Do not treat a TODO as approval.
- Do not treat a review as merge approval.
- Do not treat a patch proposal as permission to modify repository state.
- Do not commit, push, open a pull request, merge, tag, or release unless the user explicitly authorizes that specific action and scope.
- Report unread files, skipped tests, assumptions, and limitations.

## Recommended Flow

1. Create or receive a `CONTEXT_PACKAGE`.
2. Return `CONTEXT_PACKAGE_RECEIPT`.
3. Produce a plan or patch proposal under `PROPOSE_ONLY` authority.
4. Request bounded review with `REVIEW_REQUEST` if needed.
5. Return `AI_DEVELOPMENT_STATUS`.
6. Ask for the exact next user authorization before any repository-state or release-state action.

## Required Status Output

```yaml
AI_DEVELOPMENT_STATUS:
  protocol_version: "MADP-v0.3.0-alpha.2"
  profile: "AI_DRIVEN_DEVELOPMENT"
  work_status: "PROPOSED | EDITED | TESTED | BLOCKED | READY_FOR_USER_REVIEW"
  files_read: []
  files_changed: []
  tests_run: []
  tests_not_run: []
  assumptions: []
  limitations: []
  external_actions_performed: false
  user_approval_claimed: false
  next_required_user_decision: "NONE | APPROVE_EDIT | APPROVE_COMMIT | APPROVE_PR | APPROVE_MERGE | APPROVE_TAG | APPROVE_RELEASE"
```

## Handoff Output Shape

```yaml
AI_DEVELOPMENT_HANDOFF:
  protocol_version: "MADP-v0.3.0-alpha.2"
  profile: "AI_DRIVEN_DEVELOPMENT"
  context_package: "{{CONTEXT_PACKAGE_ID}}"
  proposed_change_summary: ""
  files_to_inspect: []
  files_to_change: []
  tests_to_run: []
  authority_boundary: "PROPOSE_ONLY"
  external_actions_allowed: false
  user_approval_inferred: false
```
