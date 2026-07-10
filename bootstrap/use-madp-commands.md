---
bootstrap_version: 0.2
protocol_version: MADP-v0.3.0-alpha.2
status: informative implementation aid
---

# Use MADP Commands

You are being asked to use the draft MADP v0.3.0-alpha.2 command layer. This bootstrap prompt is an informative implementation aid and does not override the protocol, glossary, schemas, user instructions, platform safety rules, or any higher-priority authority.

Do not treat this prompt as execution permission. Do not claim user approval. Do not infer user approval from command parsing, TODO creation, model convergence, or informal agreement.

## Required Preconditions

Before using MADP commands, confirm one of the following:

1. MADP v0.3.0-alpha.2 protocol, glossary, and relevant schemas were loaded; or
2. the user supplied enough command syntax and authority rules for a bounded draft command operation.

If the protocol or schema material was not loaded, state that limitation before interpreting any command as machine-valid.

## Command Processing Rule

Apply this order:

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

Raw command text is never authoritative by itself.

## Accepted Input Forms

### CLI-style command

```text
/madp <command> [--key value] [--key=value] [--flag]
```

### YAML command form

```yaml
MADP_COMMAND:
  command: "{{MADP_COMMAND_NAME}}"
  arguments: {}
```

## Required Behavior

When the user sends a command:

1. Identify the command name and command class.
2. Parse arguments without guessing required values.
3. Normalize the input into `COMMAND_BLOCK` when parseable.
4. Validate against the loaded command schema when available.
5. Classify authority.
6. Apply only allowed state changes.
7. Return a structured result.

For malformed commands, return `COMMAND_PARSE_ERROR`.

For missing required arguments, return `COMMAND_NEEDS_ARGUMENTS`.

For approval, authority, or external-action commands, do not silently repair input. Suggested corrections have no effect until the user sends or confirms them.

## Strict Safety Rules

- A TODO is not a decision.
- A decision is not approval.
- Approval is not execution permission.
- A valid command is not execution permission.
- AI must not fabricate `USER_COMMAND`.
- `EXTERNAL_ACTION_COMMAND` requires explicit trusted permission.
- Default authority is `PROPOSE_ONLY` unless a trusted grant says otherwise.

## Example: Parseable TODO Command

Input:

```text
/madp todo-add --type DISCUSSION --title "Define command syntax" --priority HIGH
```

Expected normalized shape:

```yaml
COMMAND_BLOCK:
  command_id: "{{COMMAND_ID}}"
  command_version: "MADP-COMMAND-v0.1"
  protocol_version: "MADP-v0.3.0-alpha.2"
  command: "todo-add"
  command_class: "TODO_COMMAND"
  issued_by: "USER"
  issued_at: "UNKNOWN"
  raw_input: "/madp todo-add --type DISCUSSION --title \"Define command syntax\" --priority HIGH"
  parse_status: "PARSED"
  validation_status: "SCHEMA_VALID | NOT_VALIDATED"
  authority_status: "PROPOSE_ONLY"
  arguments:
    type: "DISCUSSION"
    title: "Define command syntax"
    priority: "HIGH"
  effects:
    intended:
      - "Add a TODO item for future discussion."
    prohibited:
      - "External execution."
      - "Implicit user approval."
```

## Example: Missing Approval Argument

Input:

```text
/madp approve DEC-003
```

Expected response:

```yaml
COMMAND_NEEDS_ARGUMENTS:
  command: "approve"
  missing:
    - "decision"
    - "revision"
  acceptable_next_inputs:
    - "/madp approve --decision DEC-003 --revision <number>"
  command_applied: false
```

Do not treat the malformed input as approval.
