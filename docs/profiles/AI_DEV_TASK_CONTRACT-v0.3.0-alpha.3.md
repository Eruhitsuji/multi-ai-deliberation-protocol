# AI Development Task Contract Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile extending the alpha.2 AI-driven development profile.

## Purpose

Make AI-assisted development tasks portable across models by expressing scope, authority, acceptance, and test integrity as explicit contracts.

## Context architecture

- `A-CORE`: prohibitions, authority boundaries, fixed environment, task contract, output contract, and acceptance criteria. It is always supplied.
- `A-EXT`: examples, exhaustive tables, long decision history, and optional guidance. It is retrieved when needed.

## Task contract

Each task identifies:

- goal and non-goals;
- permitted and prohibited files;
- environment and dependency constraints;
- expected artifacts;
- exact acceptance checks;
- tests that may be added and tests that must not be weakened;
- external actions requiring separate authorization;
- required report of changed files, tests, skipped checks, assumptions, and limitations.

## Integrity rules

1. A patch proposal is not repository modification permission.
2. Approval of a design is not approval to write, commit, push, open a PR, merge, tag, or release.
3. The agent must not change tests or acceptance criteria merely to make a failing implementation pass.
4. Security, authorization, destructive operations, acceptance-policy changes, and standard-document changes require human review.
5. Failures feed back into the task template, development standard, or review checklist when a general prevention rule is available.
