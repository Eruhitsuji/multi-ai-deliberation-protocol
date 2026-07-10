---
status: planning
protocol_version: MADP-v0.3.0-alpha.2-planning
base_release: MADP-v0.3.0-alpha.1
scope_lock: proposed
---

# MADP v0.3.0-alpha.2 Scope Plan

This document defines the proposed implementation scope for `MADP-v0.3.0-alpha.2`.

The alpha.2 theme is **Command and Context Relay Layer**. The release should extend MADP beyond multi-AI deliberation into safe context sharing, command handling, and future-work tracking while preserving the alpha.1 authority and validation guarantees.

## Goals

- Support MADP as a protocol for both deliberation and AI-to-AI or chat-to-chat information sharing.
- Define structured commands for users and AI participants.
- Add TODO tracking for future discussion, design, implementation, validation, and release work.
- Require command parsing, normalization, validation, and authority classification before any command changes state.
- Preserve the rule that AI consensus, TODO creation, and command suggestions are not user approval.

## Non-Goals for alpha.2

- Do not add command aliases or abbreviations.
- Do not add macro commands.
- Do not permit automatic external execution.
- Do not redesign the full authority model.
- Do not require every existing alpha.1 artifact to contain command history.
- Do not treat TODO items as decisions or approvals.

## Proposed Artifacts

### CONTEXT_PACKAGE

`CONTEXT_PACKAGE` is a lightweight artifact for sharing context with another AI system or another chat session without requiring a full deliberation relay.

Minimum fields:

```yaml
CONTEXT_PACKAGE:
  package_id: "CTX-001"
  purpose: "Share current project context with another AI."
  source: "USER_PROVIDED | AI_SUMMARIZED | MIXED"
  confidence: "USER_CONFIRMED | AI_SUMMARIZED | UNVERIFIED"
  target_role: "REVIEWER | IMPLEMENTER | VALIDATOR | ASSISTANT"
  contents:
    goal: ""
    background: []
    constraints: []
    decisions_so_far: []
    open_questions: []
    relevant_files: []
    known_limitations: []
  usage_rules:
    authority_boundary: "REFERENCE_ONLY | PROPOSE_ONLY"
    may_propose_changes: true
    may_execute_external_actions: false
```

### COMMAND_BLOCK

`COMMAND_BLOCK` is the canonical form of a parsed MADP command. Raw command text is not authoritative by itself.

Minimum fields:

```yaml
COMMAND_BLOCK:
  command_id: "CMD-001"
  command_version: "MADP-COMMAND-v0.1"
  command: "todo-add"
  command_class: "AI_COMMAND | USER_COMMAND | TODO_COMMAND | EXTERNAL_ACTION_COMMAND"
  issued_by: "USER | FACILITATOR | PARTICIPANT | SYSTEM"
  issued_at: "UNKNOWN"
  raw_input: "/madp todo-add --title \"Define COMMAND_BLOCK\" --priority HIGH"
  parse_status: "PARSED | PARSE_ERROR | NEEDS_ARGUMENTS"
  validation_status: "SCHEMA_VALID | SCHEMA_INVALID | NOT_VALIDATED"
  authority_status: "USER_CONFIRMED | PROPOSE_ONLY | REQUIRES_USER_CONFIRMATION | DENIED"
  arguments: {}
  effects:
    intended: []
    prohibited: []
```

### TODO_ITEM and TODO_LIST

`TODO_ITEM` records future work or future discussion without converting it into a decision or approval.

Minimum fields:

```yaml
TODO_ITEM:
  todo_id: "TODO-001"
  type: "DISCUSSION | DESIGN | SCHEMA | IMPLEMENTATION | VALIDATION | DOCUMENTATION | RELEASE | SAFETY"
  title: "Define user-facing command syntax"
  status: "OPEN | IN_PROGRESS | BLOCKED | DONE | DEFERRED | CANCELLED"
  priority: "HIGH | MEDIUM | LOW"
  owner: "USER | FACILITATOR | PARTICIPANT | UNSPECIFIED"
  related_issue: null
  related_decision: null
  blocking_reason: null
  created_by: "USER | FACILITATOR | PARTICIPANT | SYSTEM"
  created_at: "UNKNOWN"
```

`TODO_LIST` is an ordered or filtered collection of `TODO_ITEM` records.

## Proposed Relay Mode Extension

Add `relay_mode` to `RELAY_BLOCK` or define it as a compatible optional field for alpha.2.

```yaml
relay_mode:
  enum:
    - DELIBERATION
    - INFORMATION_TRANSFER
    - REVIEW_REQUEST
    - TASK_HANDOFF
    - EVIDENCE_TRANSFER
    - RECOVERY
```

Default migration rule:

```yaml
if relay_mode is absent in alpha.1 material:
  assume: DELIBERATION
```

## Proposed Command Classes

### AI_COMMAND

Commands that ask an AI participant or assistant to produce an artifact, review, summary, relay, or proposal.

Initial commands:

- `share-context`
- `issue-relay`
- `request-review`
- `summarize-state`
- `check-authority`
- `propose-decision`

### USER_COMMAND

Commands that record user-facing choices or requests.

Initial commands:

- `approve`
- `reject`
- `defer`
- `prioritize`
- `pause`
- `resume`
- `status`

Special rule for `approve`:

```yaml
approve:
  required:
    - decision
    - revision
  rules:
    - "Approval must bind to a specific decision id and revision."
    - "Approval does not authorize external execution."
    - "Approval must not be inferred from casual agreement."
```

### TODO_COMMAND

Commands for managing future work.

Initial commands:

- `todo-add`
- `todo-list`
- `todo-update`
- `todo-done`
- `todo-defer`
- `todo-promote`

### EXTERNAL_ACTION_COMMAND

Commands involving external actions such as file writes, commits, releases, email, networked operations, or tool-driven changes.

alpha.2 should define the class but should not add automatic execution semantics.

Default rule:

```yaml
EXTERNAL_ACTION_COMMAND:
  default_authority: REQUIRES_USER_CONFIRMATION
  may_execute_without_explicit_permission: false
```

## Command Input Syntax

alpha.2 should support two input forms.

### CLI-style surface syntax

```text
/madp <command> [--key value] [--key=value] [--flag]
```

Examples:

```text
/madp status
/madp todo-add --type DISCUSSION --title "COMMAND_BLOCK syntaxを決める" --priority HIGH
/madp request-review --target VALIDATOR --focus schema --focus authority
/madp approve --decision DEC-003 --revision 2
```

### YAML command form

```yaml
MADP_COMMAND:
  command: "todo-add"
  arguments:
    type: "DISCUSSION"
    title: "Define command syntax"
    priority: "HIGH"
```

## Command Processing Rules

Command processing must follow this order:

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

Rules:

- Raw command text is never authoritative by itself.
- All commands must normalize into `COMMAND_BLOCK` before state changes.
- Malformed commands must not be partially applied.
- Unknown commands and unknown options must be rejected.
- Missing required arguments must return `COMMAND_NEEDS_ARGUMENTS`.
- Parse errors must return `COMMAND_PARSE_ERROR`.
- AI must not silently repair commands that affect approval, authority, or external actions.
- Suggested corrected commands have no effect until the user sends them.
- State-changing commands must produce an auditable `COMMAND_BLOCK`.

## Error Artifacts

### COMMAND_PARSE_ERROR

```yaml
COMMAND_PARSE_ERROR:
  input: "/madp approve DEC-003"
  reason: "approve requires explicit --decision and --revision arguments."
  missing_arguments:
    - "revision"
  suggested_correction:
    - "/madp approve --decision DEC-003 --revision <number>"
  command_applied: false
```

### COMMAND_NEEDS_ARGUMENTS

```yaml
COMMAND_NEEDS_ARGUMENTS:
  command: "todo-done"
  missing:
    - "todo_id"
    - "completion_basis"
  command_applied: false
```

## Safety Rules

- A TODO is not a decision.
- A decision is not approval.
- Approval is not execution permission.
- AI must not fabricate `USER_COMMAND`.
- AI may propose a command, but proposed commands have no authority until sent or confirmed by the user.
- External actions require explicit permission separate from command parsing and schema validity.
- AI consensus or multi-participant agreement is not user approval.

## Proposed Schemas

Add canonical alpha.2 schemas:

```text
schemas/v0.3.0-alpha.2/command.schema.yaml
schemas/v0.3.0-alpha.2/todo.schema.yaml
schemas/v0.3.0-alpha.2/context-package.schema.yaml
```

Add generated bundled schemas if practical:

```text
schemas/generated/command-v0.3.0-alpha.2.bundle.schema.yaml
schemas/generated/todo-v0.3.0-alpha.2.bundle.schema.yaml
schemas/generated/context-package-v0.3.0-alpha.2.bundle.schema.yaml
```

## Proposed Bootstrap Additions

Add bootstrap prompts for command and context use:

```text
bootstrap/use-madp-commands.md
bootstrap/share-context-with-ai.md
bootstrap/request-review.md
```

These prompts should remain informative implementation aids and must not override protocol authority rules.

## Migration Considerations

alpha.1 to alpha.2 migration should be conservative:

- Existing alpha.1 session states remain valid when command fields are absent.
- Existing alpha.1 relay blocks default to `relay_mode: DELIBERATION` when absent.
- Existing sessions start with an empty command history unless command history is explicitly supplied.
- Existing sessions start with an empty TODO list unless TODO items are explicitly supplied.
- Adding TODOs does not alter decisions or approvals.
- Adding `CONTEXT_PACKAGE` does not grant execution authority.

## Proposed Validation Fixtures

Add fixtures covering:

- valid CLI-style command normalization
- invalid CLI-style command parse errors
- missing argument handling
- valid YAML command form
- invalid unknown command
- invalid unknown option
- strict `approve` command binding
- TODO lifecycle: add, list, update, done, defer, promote
- context package with reference-only authority
- relay mode migration default

## Initial alpha.2 TODO List

```yaml
TODO_LIST:
  protocol_version: "MADP-v0.3.0-alpha.2-planning"
  items:
    - todo_id: "TODO-CMD-001"
      type: "DESIGN"
      title: "Define COMMAND_BLOCK structure"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-002"
      type: "DESIGN"
      title: "Define command parsing and normalization rules"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-003"
      type: "DESIGN"
      title: "Define user-facing commands"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-004"
      type: "DESIGN"
      title: "Define AI-facing commands"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-005"
      type: "DESIGN"
      title: "Define TODO_ITEM and TODO_LIST lifecycle"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-006"
      type: "SCHEMA"
      title: "Add schemas for command, todo, and context package artifacts"
      priority: "MEDIUM"
      status: "OPEN"
    - todo_id: "TODO-CMD-007"
      type: "BOOTSTRAP"
      title: "Add command and context sharing bootstrap prompts"
      priority: "MEDIUM"
      status: "OPEN"
    - todo_id: "TODO-CMD-008"
      type: "SAFETY"
      title: "Define anti-fabrication and authority boundaries for commands"
      priority: "HIGH"
      status: "OPEN"
    - todo_id: "TODO-CMD-009"
      type: "MIGRATION"
      title: "Define alpha.1 to alpha.2 migration behavior"
      priority: "MEDIUM"
      status: "OPEN"
```

## Suggested Implementation Order

1. Add this planning document.
2. Draft `MADP-v0.3.0-alpha.2.md` and `GLOSSARY-v0.3.0-alpha.2.md`.
3. Add schemas for `COMMAND_BLOCK`, `TODO_ITEM`, and `CONTEXT_PACKAGE`.
4. Add validation fixtures and checker scripts.
5. Add bootstrap command/context prompts.
6. Add migration fixtures.
7. Update traceability and readiness checks.
