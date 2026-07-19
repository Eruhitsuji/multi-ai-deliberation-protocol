# Human-Facing Workflow Macros for MADP v0.3.0-alpha.4

Status: normative interface profile for the alpha.4 Core Usability slice.

Canonical alpha.3 commands remain the machine operations. Workflow Macros are
versioned guided workflows and never aliases. Macros are guided workflows, not
commands or transactions.

## Common interaction card

Before a macro step or gate, show:

```yaml
MACRO: init | register | capture | structure | review | decide | authorize | status
STEP: "<step ID>"
CURRENT_STATE: "<state summary>"
HUMAN_DECISION_REQUIRED: "<decision or NONE>"
NEXT_ACTION: "<natural-language choice or exact command>"
CANONICAL_EXPANSION:
  - "<canonical alpha.3 command>"
```

## General rules

- Record every accepted command with exact IDs, revisions, and state versions.
- Do not infer missing arguments.
- Do not skip a human or validation gate.
- Stop on stale state, ambiguous target, authority mismatch, or unknown exposure.
- Preserve raw prompts and responses before normalization.
- A macro never expands approval, merge, release, publication, or execution authority.

## `init`

Purpose: establish a bounded plan and separately start the session.

Required sequence:

1. `goal-propose`
2. `HUMAN_CONFIRM_EXACT_PLAN_REVISION`
3. `goal-confirm`
4. `HUMAN_START_SESSION`
5. `session-start`

`goal-confirm` never performs `session-start`.

## `register`

Purpose: register participants, participation mode, capabilities, correlation,
and analytical roles.

Sequence:

1. `participant-add`
2. optional `participant-update-capability`
3. `participant-set-mode`
4. optional `role-assign`

Same-model, shared-chat, or shared-source participants are not independent by
default. Registration grants no approval or execution authority.

## `capture`

Purpose: relay a bounded question and preserve a raw response.

Sequence:

1. optional `relay-create-plain`
2. `HUMAN_MANUAL_RELAY`
3. `response-ingest`

External participants remain proposal-only or opinion-only.

## `structure`

Purpose: normalize a response and create Claim records without replacing raw
data.

Sequence:

1. `response-normalize`
2. `HUMAN_REVIEW_NORMALIZATION_DIFF`
3. `normalization-confirm`
4. `claim-add`
5. optional `claim-verify`

Unknown values remain unknown.

## `review`

Purpose: request criticism, assess evidence, identify missing support, and
preserve material dissent.

Sequence:

1. `request-review`
2. optional `claim-verify`
3. `summarize-state`

Post-exposure agreement is not an independent initial response.

## `decide`

Purpose: propose a decision and record the exact Human Final Authority
disposition.

Sequence:

1. `propose-decision`
2. `HUMAN_REVIEW_EVIDENCE_AND_DISSENT`
3. exactly one of `approve`, `reject`, or `defer`

The decision binds to the exact revision. Consensus is not substituted for the
human decision.

## `authorize`

Purpose: check authority and separately request authorization for an external
action.

Sequence:

1. `check-authority`
2. optional `external-action`
3. `SEPARATE_TRUSTED_EXECUTION_CONFIRMATION`

This macro never performs the external action.

## `status`

Purpose: show workflow state, session state, outstanding work, and the next safe
action.

Sequence:

1. `status`
2. optional `session-status`
3. optional `todo-list`

The macro is reference-only and does not mutate state.

## Trace record

Each invocation uses the alpha.4 Core Usability record schema and stores the
macro, accepted canonical commands, encountered gates, state versions,
completion status, and stop reason.
