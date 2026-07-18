# Human-Facing Workflow Macros for MADP v0.3.0-alpha.3

Status: experimental interface profile. Canonical alpha.3 commands remain the
normative machine operations.

## Rule

A Workflow Macro is a guided, non-atomic plan that expands into canonical
commands and explicit gates. It is not a command alias, does not bypass required
arguments, does not collapse revisions, and does not expand authority.

The machine record contains the canonical commands actually accepted. The macro
name may be recorded as UI provenance only.

## Common output

Before each step or gate, display:

```yaml
MACRO: init | register | capture | structure | review | decide | authorize | status
STEP: "<current step>"
CURRENT_STATE: "<state summary>"
HUMAN_DECISION_REQUIRED: "<decision or NONE>"
NEXT_ACTION: "<natural-language choice or exact command>"
CANONICAL_EXPANSION:
  - "<canonical command>"
```

## Macros

### `init`

Purpose: establish a bounded plan and explicitly start the session.

Typical sequence:

1. `goal-propose`;
2. human review of the exact plan revision;
3. `goal-confirm` with exact identifiers and state version;
4. a separate human start gate;
5. `session-start`.

`goal-confirm` never silently performs `session-start`.

### `register`

Purpose: record participants, participation mode, capabilities, correlation, and
analytical roles.

Typical commands:

- `participant-add`;
- `participant-update-capability` when needed;
- `participant-set-mode`;
- `role-assign` when analytical roles are useful.

Same-model or shared-source participants are not represented as independent by
default.

### `capture`

Purpose: create a bounded relay and preserve an external raw response.

Typical sequence:

1. `relay-create-plain` when a relay is needed;
2. human copy-and-paste outside MADP;
3. `response-ingest` for the raw response.

External participants receive no approval or execution authority.

### `structure`

Purpose: normalize an ingested response and create structured claims without
losing the raw record.

Typical sequence:

1. `response-normalize`;
2. human review of normalization differences;
3. `normalization-confirm`;
4. `claim-add`;
5. `claim-verify` when evidence is available.

### `review`

Purpose: request criticism, compare positions, identify missing evidence, and
preserve dissent.

Typical commands:

- `request-review`;
- `claim-verify`;
- `summarize-state`.

A review after Cross Exposure is not counted as an independent initial response.

### `decide`

Purpose: create a decision candidate and record the exact human disposition.

Typical sequence:

1. `propose-decision`;
2. show evidence limitations and unresolved dissent;
3. human chooses `approve`, `reject`, or `defer` for the exact revision.

Consensus is not substituted for the human decision.

### `authorize`

Purpose: evaluate and, when necessary, separately request authorization for an
external action.

Typical sequence:

1. `check-authority`;
2. if external action remains requested, `external-action` with exact scope;
3. separate trusted confirmation outside the macro where the environment
   requires it.

This macro never performs the external action itself.

### `status`

Purpose: explain the current workflow, exact alpha.3 session state, outstanding
work, and the next safe action.

Typical commands:

- `status`;
- `session-status` when a session ID exists;
- `todo-list` when TODO state is relevant.

## Failure behavior

Stop and request the missing value when a canonical command lacks a required
argument. Reject stale state versions, ambiguous targets, inferred approvers,
inferred exposure, or a macro expansion that would skip a required user gate.
