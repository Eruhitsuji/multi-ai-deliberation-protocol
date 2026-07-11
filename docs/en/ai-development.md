---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# AI-driven development with MADP

English | [日本語](../ja/ai-development.md)

> This guide is explanatory. The normative authority and command rules remain in the versioned protocol, schemas, and registry.

## Purpose

MADP separates the stages of AI-assisted software work so that progress at one stage does not silently grant authority for the next stage.

```text
analysis -> proposal -> edit -> test -> review -> commit -> push -> PR -> merge -> tag -> release
```

Each arrow is a boundary. An AI may be authorized to edit files without being authorized to commit, push, merge, tag, or publish.

## Recommended workflow

1. **Load the protocol context.** Record the version and files actually read.
2. **Define the issue.** State the goal, fixed requirements, exclusions, and acceptance criteria.
3. **Create TODO items.** A TODO records work; it does not approve a decision.
4. **Analyze and propose.** Preserve alternatives, evidence, assumptions, and unresolved risks.
5. **Authorize edits separately.** Editing permission must be explicit and scoped.
6. **Run validation.** Record commands, exit codes, and relevant results.
7. **Request independent review.** A review response is evidence, not merge approval.
8. **Ask for repository actions separately.** Commit, push, PR, merge, tag, and release remain distinct.

## Minimum handoff package

When handing work to another AI, include:

- protocol version;
- current goal and scope;
- branch or commit identity;
- files changed or proposed;
- validation already run;
- unresolved TODO items;
- authority already granted and authority explicitly not granted;
- exact next requested action.

## Example authority statement

```yaml
authority:
  allowed:
    - inspect repository files
    - propose changes
    - edit files on the named branch
    - run local validation
  not_allowed:
    - push
    - merge
    - create tags
    - publish a release
```

## Review discipline

A strong review should include:

- files actually read;
- checks actually run;
- findings with severity and evidence;
- reproduction steps;
- recommended changes and tests;
- a clear statement that no external action was performed.

## Failure-safe behavior

Stop or fail closed when:

- the active branch or target repository is ambiguous;
- required files could not be read;
- user approval is asserted but not verified;
- the command scope is empty or broader than authorized;
- state or review evidence is stale;
- an external action is requested without action-specific authorization.
