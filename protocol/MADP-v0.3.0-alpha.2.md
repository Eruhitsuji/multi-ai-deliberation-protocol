# Multi-AI Deliberation Protocol v0.3.0-alpha.2

## Status

This document is an alpha prerelease specification. It is not stable. The user remains the sole final decision-maker. Convergence among AI participants is not evidence and does not create approval or execution authority.

This alpha.2 draft extends alpha.1 with command, context relay, and TODO planning concepts. The additions are intended for review and validation before release.

## 1. Purpose

MADP defines a service-neutral protocol for structured deliberation, state transfer, context relay, command handling, approval binding, TODO tracking, and fail-closed execution authorization across AI systems, role actors, human validators, users, and tools.

MADP is not limited to debate or consensus-building. It also defines safe, auditable ways to transfer operative context, constraints, evidence, commands, and task state between AI systems or AI chat sessions.

## 2. Authority domains

1. Versioned JSON Schemas control field names, types, required properties, and enum spelling.
2. This protocol controls behavior, transitions, authorization, migration, command processing, TODO lifecycle, and conformance.
3. The versioned glossary controls normative term meanings.
4. README, bootstrap prompts, examples, planning documents, and generated bundles are informative unless explicitly stated otherwise.

A conflict among authority domains MUST be reported and MUST NOT be silently resolved.

## 3. Core rules

- The user is the sole final decision-maker.
- Majority vote alone is insufficient.
- AI agreement is convergence, not evidence.
- `SESSION_STATE` is the sole logical source of truth for session state.
- Deliberation outcome, TODO creation, command parsing, user approval, permission grants, and execution are distinct.
- A TODO is not a decision.
- A decision is not approval.
- Approval is not execution permission.
- Unknown actions, stale state, empty scope, malformed commands, and ambiguous authority fail closed.
- Active sessions MUST NOT auto-upgrade across protocol versions.

## 4. Actors

Each participant has a machine-readable `type`, free-form `role`, and `status`.

At most one participant whose `type` is `FACILITATOR` may have `status: ACTIVE`. The invariant is evaluated from `type`, never from free-form `role` text.

Role actors inside one model/context have review independence `I0` and MUST NOT be represented as independent evidence.

## 5. State and roots

MADP v0.3 uses separate canonical document roots:

- `session_state` documents validate against the Session State root schema.
- `relay_block` documents validate against the Relay Block root schema.
- `context_package` documents validate against the Context Package root schema when used.
- `command_block` documents validate against the Command Block root schema when used.
- `todo_list` documents validate against the TODO List root schema when used.

A relay-only document is not required to contain `session_state` at the top level.

Persistent or transferred state uses monotonically increasing `state_version` and matching `parent_version`. A stale or split-brain state MUST NOT overwrite current state automatically.

## 6. Permission requests and grants

A permission request represents requested authority and MAY contain an unknown non-empty action identifier.

A permission grant represents active authority and is restricted to recognized core actions. Unknown actions MUST NOT be granted automatically.

Every permission grant MUST include:

- `action`;
- non-empty `scope`;
- `assurance_level`;
- `assurance_origin`.

Trusted active grants are limited to:

- `USER_CONFIRMED` with `assurance_origin: USER_ACTION`; or
- `EXTERNALLY_VERIFIED` with `assurance_origin: EXTERNAL_VALIDATION` and a non-empty `reference`.

AI-generated candidates MUST remain permission requests or state-change proposals and MUST NOT be promoted to active grants without trusted provenance.

## 7. Decisions and approvals

A decision contains a stable `id`, positive integer `revision`, deliberation outcome, approval status, and summary.

Approval MUST be bound to both `decision_id` and `decision_revision`.

Affirmative approval statuses are:

- `APPROVE`;
- `APPROVE_WITH_CONDITIONS`;
- `APPROVE_WITH_CHANGES`.

An affirmative approval MUST have trusted assurance. `UNVERIFIED_ASSERTION` cannot make an affirmative approval authoritative and cannot authorize execution.

An AI may record a recommendation, but it MUST NOT infer or fabricate user approval.

## 8. Execution gate

Execution MUST be denied unless all of the following hold:

1. the requested action is recognized;
2. a matching active permission grant exists;
3. scope is non-empty and covers the operation;
4. grant assurance and origin satisfy Section 6;
5. any required approval is bound to the current decision revision;
6. applicable conditions are satisfied with required assurance;
7. state and task bindings are current;
8. any command that requested the operation parsed and validated successfully;
9. the command authority classification permits the requested class of operation.

Approval alone does not grant execution permission. A valid command alone does not grant execution permission.

## 9. Relay blocks and relay modes

A Relay Block contains metadata and an `operative_session_state_snapshot`.

The following invariants apply:

```text
relay_block.session_id = relay_block.operative_session_state_snapshot.meta.session_id
relay_block.source_state_version = relay_block.operative_session_state_snapshot.meta.state_version
```

alpha.2 adds an optional `relay_mode` field. When absent in alpha.1 material, the migration default is `DELIBERATION`.

Recognized relay modes are:

- `DELIBERATION`: transfer state for participant deliberation.
- `INFORMATION_TRANSFER`: transfer context without requiring a deliberation outcome.
- `REVIEW_REQUEST`: request bounded review from another AI or role actor.
- `TASK_HANDOFF`: transfer current task state to another AI or chat session.
- `EVIDENCE_TRANSFER`: transfer evidence and verification context.
- `RECOVERY`: recover from failed or partial protocol loading.

## 10. Context packages

A `CONTEXT_PACKAGE` is a lightweight artifact for sharing context with another AI system or chat session without requiring a full deliberation relay.

A context package SHOULD include:

- `package_id`;
- `purpose`;
- `source`;
- `confidence`;
- `target_role`;
- `contents`;
- `usage_rules`.

Context packages MUST NOT grant execution authority. A receiving AI MUST treat `usage_rules.authority_boundary` as a limit, not as evidence of user approval.

A context package MAY support review, summarization, implementation planning, or task handoff. It MUST distinguish user-provided facts from AI summaries and unverified material when that distinction is known.

## 11. Command layer

A MADP command is a structured request to inspect state, share context, request review, manage TODOs, record user choices, or request an external action.

Raw command text is never authoritative by itself. A command becomes processable only after it has been parsed, normalized into a `COMMAND_BLOCK`, validated, and classified for authority.

Command processing MUST follow this order:

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

A `COMMAND_BLOCK` SHOULD include:

- `command_id`;
- `command_version`;
- `command`;
- `command_class`;
- `issued_by`;
- `issued_at`;
- `raw_input`;
- `parse_status`;
- `validation_status`;
- `authority_status`;
- `arguments`;
- `effects`.

Recognized command classes are:

- `AI_COMMAND`;
- `USER_COMMAND`;
- `TODO_COMMAND`;
- `EXTERNAL_ACTION_COMMAND`.

Malformed commands MUST NOT be partially applied. Unknown commands and unknown options MUST be rejected. Missing required arguments MUST return `COMMAND_NEEDS_ARGUMENTS`. Parse errors MUST return `COMMAND_PARSE_ERROR`.

AI systems MUST NOT silently repair commands that affect approval, authority, or external actions. Suggested corrections have no effect until the user sends or confirms them.

## 12. Command input syntax

alpha.2 recognizes two command input surfaces.

### 12.1 CLI-style surface syntax

```text
/madp <command> [--key value] [--key=value] [--flag]
```

Repeated options MAY represent lists when defined by the command. Unknown options MUST be rejected. Values containing spaces SHOULD be quoted. Implementations MUST NOT guess omitted required arguments for approval, authority, or external-action commands.

Examples:

```text
/madp status
/madp todo-add --type DISCUSSION --title "Define COMMAND_BLOCK syntax" --priority HIGH
/madp request-review --target VALIDATOR --focus schema --focus authority
/madp approve --decision DEC-003 --revision 2
```

### 12.2 YAML command form

```yaml
MADP_COMMAND:
  command: "todo-add"
  arguments:
    type: "DISCUSSION"
    title: "Define command syntax"
    priority: "HIGH"
```

The YAML form MUST still be normalized into `COMMAND_BLOCK` before any state change.

## 13. User commands

`USER_COMMAND` records user-facing choices or requests. AI systems MUST NOT fabricate `USER_COMMAND`.

Initial user commands are:

- `approve`;
- `reject`;
- `defer`;
- `prioritize`;
- `pause`;
- `resume`;
- `status`.

`approve` is strict:

- it MUST bind to a specific decision id;
- it MUST bind to a specific decision revision;
- it MUST NOT be inferred from casual agreement;
- it MUST NOT authorize external execution by itself.

## 14. AI commands

`AI_COMMAND` asks an AI participant or assistant to produce an artifact, review, summary, relay, or proposal.

Initial AI commands are:

- `share-context`;
- `issue-relay`;
- `request-review`;
- `summarize-state`;
- `check-authority`;
- `propose-decision`.

AI commands default to `PROPOSE_ONLY` unless an explicit trusted grant authorizes more.

## 15. TODO commands and TODO lifecycle

`TODO_ITEM` records future work or future discussion. TODO creation is not approval and does not modify decisions by itself.

A TODO item SHOULD include:

- `todo_id`;
- `type`;
- `title`;
- `status`;
- `priority`;
- `owner`;
- `related_issue`;
- `related_decision`;
- `blocking_reason`;
- `created_by`;
- `created_at`.

Recognized TODO statuses are:

- `OPEN`;
- `IN_PROGRESS`;
- `BLOCKED`;
- `DONE`;
- `DEFERRED`;
- `CANCELLED`.

Initial TODO commands are:

- `todo-add`;
- `todo-list`;
- `todo-update`;
- `todo-done`;
- `todo-defer`;
- `todo-promote`.

`todo-promote` converts a TODO into a formal issue or discussion target. It MUST NOT convert the TODO into an approved decision.

## 16. External action commands

`EXTERNAL_ACTION_COMMAND` identifies a command involving file writes, commits, releases, messages, network operations, tool-driven changes, or other external actions.

alpha.2 defines the class but does not grant automatic execution semantics.

Default rule:

```yaml
EXTERNAL_ACTION_COMMAND:
  default_authority: REQUIRES_USER_CONFIRMATION
  may_execute_without_explicit_permission: false
```

External actions require explicit trusted permission separate from parse success, schema validity, TODO status, AI recommendation, and user approval of decision text.

## 17. Command error artifacts

`COMMAND_PARSE_ERROR` reports malformed syntax.

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

`COMMAND_NEEDS_ARGUMENTS` reports missing required arguments after command identification.

```yaml
COMMAND_NEEDS_ARGUMENTS:
  command: "todo-done"
  missing:
    - "todo_id"
    - "completion_basis"
  command_applied: false
```

These artifacts are non-authoritative reports. Suggested corrections MUST NOT be applied until the user sends or confirms them.

## 18. MADP_JCS_V1

`MADP_JCS_V1` uses RFC 8785 JSON Canonicalization Scheme over the MADP JSON-compatible data model.

Allowed values are objects with string keys, arrays, strings, booleans, null, and integers from `-9007199254740991` through `9007199254740991`.

Before canonicalization, implementations MUST reject:

- duplicate mapping keys;
- non-string mapping keys;
- floating-point values, NaN, and Infinity;
- YAML aliases and anchors;
- custom YAML tags;
- tabs used for indentation;
- disallowed control characters.

The canonical byte stream is UTF-8 without BOM. SHA-256 output uses exactly 64 lowercase hexadecimal characters.

## 19. Protocol loading evidence

A protocol load report distinguishes retrieval from verification. It SHOULD record access result, access method, byte length, content hash when available, and verification status.

A self-attested `READ` statement is not external proof that the complete content was read. Formal schema validation MUST NOT be claimed unless an actual validator was executed. A validation receipt SHOULD identify validator, schema, instance, result, and error count.

## 20. Migration from v0.3.0-alpha.1

Migration is forward-only and conservative.

Normative migration invariants from alpha.1 continue to apply:

- `AMI-001`: no automatic authority increase;
- `AMI-002`: no fabricated provenance;
- `AMI-003`: no silent assurance-category reclassification;
- `AMI-004`: a post-ingress digest establishes only a local forward baseline;
- `AMI-005`: downgrade or rollback MUST NOT recreate a known unsafe authoritative state.

alpha.2 migration rules:

- `MIG-A2-001`: alpha.1 relay blocks without `relay_mode` default to `DELIBERATION`.
- `MIG-A2-002`: alpha.1 session states without command history remain valid with empty or absent command history.
- `MIG-A2-003`: alpha.1 session states without TODO lists remain valid with empty or absent TODO lists.
- `MIG-A2-004`: adding a TODO list MUST NOT alter decisions, approvals, or permission grants.
- `MIG-A2-005`: adding a context package MUST NOT grant execution authority.
- `MIG-A2-006`: command history MUST NOT be fabricated during migration.

Official migration results remain `COMPLETED`, `REJECTED`, or `ABORTED`. `PARTIAL` is prohibited.

## 21. Error namespace

Migration-specific errors use the `MIG_` prefix. Command-specific errors use the `CMD_` prefix. TODO-specific errors use the `TODO_` prefix.

Initial alpha.2 additions include:

- `CMD_PARSE_ERROR`;
- `CMD_UNKNOWN_COMMAND`;
- `CMD_UNKNOWN_OPTION`;
- `CMD_MISSING_REQUIRED_ARGUMENT`;
- `CMD_SCHEMA_INVALID`;
- `CMD_AUTHORITY_DENIED`;
- `TODO_UNKNOWN_ID`;
- `TODO_INVALID_STATUS_TRANSITION`.

## 22. Alpha limitations

Alpha.2 defines proposed command, context package, TODO, and relay mode concepts. It does not claim:

- production readiness;
- complete parser interoperability;
- command alias support;
- macro command support;
- automatic external execution;
- complete semantic validation;
- universal cross-model portability;
- structured-output API compatibility.

## 23. Release authority

Implementation completion, merge, tagging, and release publication are separate actions. Published historical tags are immutable. Each action requires explicit user authorization.
