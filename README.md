# Multi-AI Deliberation Protocol (MADP)

> Draft version: **v0.2.4-draft**

MADP is a service-neutral protocol for structured deliberation with one or more AI systems, role-separated instances of the same model, human validators, and execution agents. It is designed for research, design, review, software development, and everyday decisions.

The protocol helps participants use different model strengths without treating model agreement as proof. The user remains the sole final decision-maker.

## Status

This repository contains a draft specification. The canonical language is English. Future translations may be added under `docs/<language-code>/`; translations are informative unless explicitly marked otherwise.

The canonical normative document is:

- [`protocol/MADP-v0.2.4-draft.md`](protocol/MADP-v0.2.4-draft.md)

The machine-readable session-state schema is:

- [`schemas/session-state.schema.yaml`](schemas/session-state.schema.yaml)

## Core principles

- The user is the sole final decision-maker.
- Deliberation is not decided by majority vote alone.
- Agreement among AI systems is convergence, not independent evidence.
- `SESSION_STATE` is the single logical source of truth.
- Share the current state, not the entire conversation history.
- Use the minimum number of participants, queries, rounds, and user relay actions needed.
- Separate deliberation permission from execution permission.
- Do not end a turn while non-blocked facilitator work remains.
- User-facing language follows the resolved interaction language; canonical files and schema identifiers remain English.
- Users may approve normally, approve with conditions, approve with changes, defer, or reject.
- Decision conditions separate applicability (`ACTIVE`, `INACTIVE`, `NOT_APPLICABLE`) from satisfaction (`PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED_BY_USER`, `FAILED`).

## Quick start for humans

1. Give an AI the canonical protocol file or a reachable repository reference.
2. Provide the Protocol Capsule below.
3. State the issue, fixed requirements, criteria, and any execution or privacy limits.
4. Ask the AI to initialize a minimal `SESSION_STATE` and proceed until user input, external evidence, another participant, or completion is required.
5. Make the final decision using one of the supported decision forms.

Example start request:

```text
Use MADP v0.2.4-draft for this issue.

Issue: Decide the minimum release contents for a small open-source project.
Fixed requirements:
- Keep the first release small.
- The user is the final decision-maker.
Criteria:
- Usability
- Maintenance cost
- Extensibility

Start in MINIMAL / COMPACT mode with one ROLE_ACTOR.
Continue all non-blocked facilitator work in the same response.
Ask me only when a user decision or unavailable input is required.
```

## Quick start for AI systems

Before using MADP:

1. Read `protocol/MADP-v0.2.4-draft.md`.
2. Confirm the protocol version.
3. Confirm these rules:
   - the user is the final decision-maker;
   - majority vote alone is insufficient;
   - `SESSION_STATE` is the single source of truth;
   - facilitator-internal work must continue in the same response unless blocked;
   - interaction language and canonical artifact language are separate;
   - conditional approval must remain conditional in state.
4. Use `schemas/session-state.schema.yaml` when machine validation is available.
5. Do not infer the complete protocol from this README alone.

Suggested loading confirmation:

```yaml
protocol_load_status:
  requested: true
  loaded: true
  confirmed_version: "0.2.4-draft"
  confirmed_rules:
    - "user_is_final_decider"
    - "majority_vote_disabled"
    - "session_state_is_source_of_truth"
    - "turn_completion_rule_enabled"
    - "conditional_approval_preserved"
  unread_or_unavailable_sections: []
```

## Protocol Capsule

```yaml
protocol_capsule:
  protocol: "MADP"
  version: "0.2.4-draft"
  user_is_final_decider: true
  majority_vote: false
  source_of_truth: "SESSION_STATE"
  default_start_policy: "DO_NOT_START"
  default_depth: "MINIMAL"
  default_record_format: "COMPACT"
  query_only_when_needed: true
  prompt_action_required: true
  handoff_policy: "ON_TRANSFER_OR_COMPRESSION"
  turn_completion_rule_enabled: true
  canonical_document_language: "en"
  interaction_language: "AUTO"
  conditional_approval_supported: true
```

## Minimal `SESSION_STATE` example

```yaml
session_state:
  meta:
    protocol: "MADP"
    protocol_version: "0.2.4-draft"
    session_id: "MADP-EXAMPLE-001"
    state_version: 1
    parent_version: 0
    updated_at: "UNKNOWN"
    updated_by: "facilitator"

  language:
    interaction: "AUTO"
    canonical_documents: "en"
    generated_artifacts: "en"

  goal: "Select a minimum release structure"

  fixed:
    - id: "FIX-001"
      statement: "Keep the first release small"

  current_issue:
    id: "ISSUE-001"
    status: "IN_PROGRESS"
    question: "Which files are required for the first release?"
    acceptance_conditions:
      - "A human can start from the README"
      - "An AI can identify the canonical protocol"

  participants:
    - actor_id: "facilitator"
      type: "FACILITATOR"
      role: "FACILITATOR"
      status: "ACTIVE"

  next_step:
    internal:
      actor: "FACILITATOR"
      task: "Evaluate the minimum structure"
      blocking_input: null
    user:
      action_required: false
      prompt_action: "NO_ACTION_REQUIRED"
      task: null
      response_format: null
```

Validate it against [`schemas/session-state.schema.yaml`](schemas/session-state.schema.yaml) when validation tooling is available.

## User decision forms

```text
APPROVE
```

```text
APPROVE_WITH_CONDITIONS:
- Canonical files must be written in English.
- Completion requires all required tests to pass.
```

```text
APPROVE_WITH_CHANGES:
- Replace the proposed storage format with YAML.
```

```text
DEFER
```

```text
REJECT
```

Clear spelling variants may be normalized when the intent is unambiguous. Ambiguous decisions must not be guessed.

## Repository structure and canonical files

```text
.
├── README.md
├── LICENSE
├── protocol/
│   └── MADP-v0.2.4-draft.md
└── schemas/
    └── session-state.schema.yaml
```

This four-file release is intentionally minimal. When the repository grows, detailed file listings should move to a dedicated index or manifest. The README should remain an entry point that identifies canonical and required files.

## Language policy

- Canonical repository documents: English.
- Schema keys, enum values, prompt types, and stable identifiers: English.
- User-facing explanations: the user's explicitly requested or automatically resolved interaction language.
- Short quotations, code, identifiers, or file names do not by themselves trigger a language switch.
- Japanese translations, when added, should use `docs/ja/` rather than `docs/jp/`.

## License

Licensed under the Apache License, Version 2.0. See [`LICENSE`](LICENSE).
