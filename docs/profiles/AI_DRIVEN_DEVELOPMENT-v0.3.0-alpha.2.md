# AI-Driven Development Profile for MADP v0.3.0-alpha.2

> Profile version: `MADP-AI-DEV-PROFILE-v0.3.0-alpha.2`
>
> Protocol version: `MADP-v0.3.0-alpha.2`
>
> Status: draft implementation profile.

## Purpose

This profile defines how MADP v0.3.0-alpha.2 draft artifacts are used with coding agents such as Codex, Claude Code, or other AI-assisted development systems.

It covers:

- coding-task context handoff;
- bounded code review;
- patch proposal;
- test and limitation reporting;
- human authorization boundaries for repository state changes.

## Core Rules

```text
A TODO is not a decision.
A decision is not approval.
Approval is not execution permission.
A review is not merge approval.
A patch proposal is not repository modification permission.
```

## Allowed by Default

A coding agent may, within available context and tool permissions:

- inspect accessible files;
- summarize relevant code;
- produce a `CONTEXT_PACKAGE`;
- return a `CONTEXT_PACKAGE_RECEIPT`;
- propose a patch;
- draft tests;
- report results and limitations;
- prepare a suggested commit message;
- request bounded review with `REVIEW_REQUEST`;
- produce review findings with `REVIEW_RESPONSE`.

## Requires Explicit User Authorization

The following actions require explicit user authorization for the specific action and scope:

- modifying repository files;
- committing;
- pushing;
- opening a pull request;
- merging a pull request;
- creating a tag;
- publishing a release;
- changing protocol publication status.

## Required Status Report

A coding agent should report:

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

## Recommended Workflow

1. Build or receive `CONTEXT_PACKAGE`.
2. Return `CONTEXT_PACKAGE_RECEIPT`.
3. Produce plan and patch proposal under `PROPOSE_ONLY` authority.
4. Run available checks only when allowed by the environment and task scope.
5. Return `AI_DEVELOPMENT_STATUS`.
6. Request review with `REVIEW_REQUEST` if needed.
7. Receive `REVIEW_RESPONSE`.
8. Ask the user for the specific next external action authorization.
9. Perform only the explicitly authorized action.
10. Report changed files, tests, skipped checks, assumptions, and remaining limitations.
