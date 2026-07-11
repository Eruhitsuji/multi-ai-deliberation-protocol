---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Commands

Alpha.2 defines 20 registry-backed commands. Exact arguments and authority boundaries are defined in [`registries/v0.3.0-alpha.2/commands.yaml`](../../registries/v0.3.0-alpha.2/commands.yaml).

## Syntax

```text
/madp <command> [--key value] [--key=value] [--flag]
```

LIST arguments may be repeated and accumulate values. Repeated SCALAR arguments are rejected.

## Groups

- Context and relay: `share-context`, `issue-relay`, `request-review`
- Read-only state: `summarize-state`, `check-authority`, `status`, `todo-list`
- Decision and workflow: `propose-decision`, `approve`, `reject`, `defer`, `prioritize`, `pause`, `resume`
- TODO: `todo-add`, `todo-update`, `todo-done`, `todo-defer`, `todo-promote`
- External boundary: `external-action`

## Examples

```text
/madp request-review --target_role VALIDATOR --review_focus schema --review_focus authority
/madp todo-add --title "Write tests" --priority HIGH
/madp todo-update --todo_id TODO-001 --status IN_PROGRESS
/madp todo-done --todo_id TODO-001 --completion_basis "CI passed"
```

Terminal TODO states (`DONE`, `CANCELLED`) are immutable. `external-action` remains non-executing in alpha.2.
