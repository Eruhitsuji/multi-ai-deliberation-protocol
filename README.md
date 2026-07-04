# Multi-AI Deliberation Protocol (MADP)

> Draft version: **v0.2.5-draft**

MADP is a service-neutral protocol for structured deliberation with AI systems, role-separated instances, human validators, and execution agents. It supports research, design, review, software development, and everyday decisions while keeping the user as the sole final decision-maker.

## Status and canonical files

This is a draft specification. Canonical repository documents are English.

- [`protocol/MADP-v0.2.5-draft.md`](protocol/MADP-v0.2.5-draft.md) — behavior, procedures, transitions, authorization
- [`protocol/GLOSSARY-v0.2.5-draft.md`](protocol/GLOSSARY-v0.2.5-draft.md) — normative term meanings and distinctions
- [`schemas/session-state-v0.2.5-draft.schema.yaml`](schemas/session-state-v0.2.5-draft.schema.yaml) — fields, types, required properties, enum spelling
- [`LICENSE`](LICENSE) — MIT License

README examples are informative. A conflict among authority domains is a specification defect and must be reported.

## Core principles

- The user is the sole final decision-maker.
- Majority vote alone is insufficient.
- Agreement among AI systems is convergence, not evidence.
- `SESSION_STATE` is the single logical source of truth.
- Share operative current state, not full conversation history.
- Separate deliberation outcome, user approval, and execution permission.
- Bind approval to a specific decision revision.
- AI participants may originate only unverified approval assertions.
- Unknown actions, empty scopes, and stale relay states fail closed.
- At most one facilitator may be active.

## Quick start

```text
Use MADP v0.2.5-draft.

Issue: Decide the minimum release contents for a small open-source project.
Fixed requirements:
- Keep the release small.
- The user is the final decision-maker.
Criteria:
- Usability
- Maintenance cost
- Extensibility

Start in MINIMAL / COMPACT mode.
Continue all non-blocked facilitator work in the same response.
Ask me only when user input, unavailable evidence, external transfer, or execution permission is required.
```

Before use, an AI should report which canonical files it actually read. A repository URL alone does not prove access. Raw file URLs pinned to a commit SHA are preferred for external review.

```yaml
protocol_load_status:
  requested: true
  confirmed_version: "0.2.5-draft"
  files_actually_read:
    - path: "protocol/MADP-v0.2.5-draft.md"
      result: "READ"
    - path: "protocol/GLOSSARY-v0.2.5-draft.md"
      result: "READ"
    - path: "schemas/session-state-v0.2.5-draft.schema.yaml"
      result: "READ"
  formal_schema_validation: false
  unread_or_unavailable_sections: []
```

## Minimal Session State

```yaml
session_state:
  meta:
    protocol: "MADP"
    protocol_version: "0.2.5-draft"
    schema_version: "0.2.5-draft"
    session_id: "MADP-EXAMPLE-001"
    state_version: 1
    parent_version: 0
    updated_at: "UNKNOWN"
    updated_by: "facilitator"

  goal: "Select a minimum release structure"

  current_issue:
    id: "ISSUE-001"
    status: "IN_PROGRESS"
    question: "Which files are required?"

  participants:
    - actor_id: "facilitator"
      type: "FACILITATOR"
      role: "FACILITATOR"
      status: "ACTIVE"

  decisions:
    - id: "DEC-001"
      revision: 1
      deliberation_outcome: "USER_DECISION_REQUIRED"
      approval_status: "PENDING"
      summary: "No release structure has been approved yet."

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

Validate with the versioned schema. An LLM-only review is `STRUCTURAL_CHECK_ONLY`, not formal validation.

## Condition example

```yaml
id: "COND-001"
statement: "Required tests pass"
applicability: "ACTIVE"
satisfaction: "IN_PROGRESS"
timing: "BEFORE_COMPLETION"
```

`SATISFIED` requires `basis`. `WAIVED_BY_USER` requires both `basis` and `user_confirmation`. `ACTIVE` to `NOT_APPLICABLE` changes require `applicability_basis`.

## Approval example

```yaml
approval:
  decision_id: "DEC-001"
  decision_revision: 2
  approver: "USER"
  assurance_level: "USER_CONFIRMED"
  assurance_origin: "USER_ACTION"
  occurred_at: "UNKNOWN"
  basis: "The user explicitly approved revision 2 in the current chat."
```

An AI may record only `UNVERIFIED_ASSERTION` on its own. Unverified assertions cannot authorize external, irreversible, privileged, or permission-escalated execution.

## Manual relay

The manual profile requires a marked `RELAY_BLOCK` containing metadata and `operative_session_state_snapshot`. The snapshot excludes full conversation history and obsolete detailed history, and is the operative source of truth for the receiving turn unless the receiver already holds newer official state.

Relay identity invariants:

```text
relay_block.session_id = relay_block.operative_session_state_snapshot.meta.session_id
relay_block.source_state_version = relay_block.operative_session_state_snapshot.meta.state_version
```

## Repository structure

```text
.
├── README.md
├── LICENSE
├── protocol/
│   ├── MADP-v0.2.5-draft.md
│   └── GLOSSARY-v0.2.5-draft.md
└── schemas/
    └── session-state-v0.2.5-draft.schema.yaml
```

Future `profiles/` define reusable domain rules. Future `templates/` are starter kits built on Core and Profiles, such as software review, literature research, and everyday decision support.

## Migration from v0.2.4-draft

This release contains breaking schema changes. Import old state explicitly:

- map old decision `status` to `deliberation_outcome`;
- initialize `approval_status` to `PENDING` unless a valid current approval is re-established;
- initialize `revision` to `1`;
- map old condition status to `satisfaction` and set `applicability: ACTIVE`, except old `NOT_APPLICABLE` maps to `applicability: NOT_APPLICABLE` and `satisfaction: PENDING`;
- treat old free-form permissions as ungranted requests requiring review.

Active sessions must not auto-upgrade.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
