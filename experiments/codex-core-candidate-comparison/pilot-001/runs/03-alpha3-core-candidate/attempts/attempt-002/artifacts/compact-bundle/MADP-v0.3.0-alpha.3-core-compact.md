---
bundle_version: MADP-CORE-COMPACT-BUNDLE-v1
protocol_version: MADP-v0.3.0-alpha.3
repository: Eruhitsuji/multi-ai-deliberation-protocol
source_commit: 2a29ddfebe4d9664d3a4043a01d8728fa525d049
profile: MADP_CORE_CANDIDATE
status: EXPERIMENTAL_COMPACT_BUNDLE
formal_release_evidence: false
source_count: 7
source_inventory_sha256: 9b63d53922c0f7475ba475419bb4a934f5aa48d912ff464a9bd8d527a58e2ee9
---

# MADP v0.3.0-alpha.3 Core Compact Bundle

This single-file bundle is an experimental distribution artifact for the MADP Core Candidate. It is not a PROTOCOL_LOAD_REPORT, validation receipt, formal FIELD_TRIAL artifact, release authorization, or execution authorization.

The embedded source bytes remain bound to the repository commit and per-file SHA-256 values recorded in the companion manifest.

## Embedded source 1: `protocol/MADP-v0.3.0-alpha.3.md`

<!-- MADP_SOURCE_BEGIN index=1 path=protocol/MADP-v0.3.0-alpha.3.md sha256=44755fdd831071c37d93b3d2ce9e77d655c2f25c24772792d32c1d24c675a517 bytes=12202 role=PROTOCOL -->

# Multi-AI Deliberation Protocol v0.3.0-alpha.3

Status: normative release-candidate content; not tagged or published.

This version extends `MADP-v0.3.0-alpha.2`. Alpha.2 authority, context, TODO, review, relay, and command behavior remains normative **only as incorporated by the alpha.3 compatibility rules below**. Alpha.3 does not make an inherited command normative while simultaneously making it unrepresentable.

## 1. Normative authority order

When sources conflict, report a specification defect and apply the stricter safety boundary. The order is:

1. platform, system, developer, and explicit user instructions;
2. alpha.3 schemas for document structure and the alpha.3 command registry for command names, arguments, aliases, and command metadata;
3. this alpha.3 protocol together with inherited alpha.2 behavior explicitly retained here;
4. documents explicitly marked `normative implementation profile`, which specialize but may not override levels 2–3;
5. the versioned glossary;
6. informative guides, translations, bootstrap prompts, and Agent Skills.

A normative profile has no independent authority to weaken a schema, registry, protocol rule, user approval requirement, privacy rule, or execution boundary.

## 2. Command namespace and alpha.2 compatibility

The alpha.3 registry is an `ALPHA2_CANONICAL_SUPERSET`.

- All 20 canonical alpha.2 commands remain canonical in alpha.3.
- Alpha.3 adds 31 canonical commands. The resulting namespace contains 51 canonical commands.
- A documented alias is input convenience only. It must never equal or shadow a canonical command.
- Canonical names take precedence over aliases.
- `status`, `resume`, and `pause` retain their alpha.2 canonical meanings.
- `session-status` reports alpha.3 session-specific state.
- `session-resume` resumes an interrupted or imported session and requires an exact expected state version.
- Help mode is exited only with `help-exit`; bare `RESUME` is not a help command.
- Unknown or ambiguous input fails closed and routes to command help.
- The parser records both `invoked_name` and resolved canonical `command`.

The alpha.3 registry version is `MADP-COMMAND-REGISTRY-v0.2`; alpha.2 used v0.1.

## 3. Revision and session binding

Every canonical session artifact must identify the session and the operative state revision, unless the artifact is explicitly defined as a reusable non-session profile.

At minimum:

- deliberation plans, role plans, claim ledgers, participant profiles, relays, ingestion records, normalization records, next-action cards, help packets, help responses, minutes, checkpoints, imports, and exports carry `session_id` and `source_state_version`;
- mutable artifact families carry their own positive `revision`;
- confirmation commands identify the artifact ID and exact revision;
- a confirmation for one revision cannot confirm another revision;
- imported or stale artifacts cannot silently replace current state;
- session or artifact ID reuse across divergent revisions is a collision requiring review.

A `USER_CONFIRMED` deliberation plan must record `confirmed_revision`, and it must equal the plan's current `revision`.

## 4. Operating modes and goal gate

A `DELIBERATION_PLAN` selects `LIGHT`, `STANDARD`, or `ASSURED`. The facilitator may propose a stricter mode when risk rises and must not silently lower the mode.

Before substantive deliberation, record topic, primary goal, central question, outputs, success criteria, scope, authority, and stop conditions. When `goal_gate` is `REQUIRED`, the named human first confirms the exact current plan revision with `goal-confirm`. Goal confirmation changes only the plan status; it does not activate the session.

A session becomes `ACTIVE` only after a separate `session-start` identifies the exact `session_id` and confirmed `deliberation_plan`. Before `session-start`, only planning, participant or role setup, reference-only status, and Help operations may occur. Substantive analysis, approval, import application, minutes approval, and other canonical-state transitions fail closed with `SESSION_NOT_STARTED`.

`NAMED_APPROVERS` requires a non-empty approver list. Silence never counts as consent.

## 5. Participant capabilities and independence

Participant types are `HUMAN`, `AI_MODEL`, `AI_ROLE_ACTOR`, `TEAM_PROXY`, and `OBSERVER`. Participation modes are `FULL_CONFORMANCE`, `ASSISTED_CONFORMANCE`, `OPINION_ONLY`, and `OBSERVER`.

Capability values are `SUPPORTED`, `UNSUPPORTED`, or `UNKNOWN`. The core capability set is stable; future capabilities may be added under the extension map without changing the core schema.

An `OPINION_ONLY` participant cannot be facilitator, state maintainer, approver, veto holder, executor, or direct canonical-state updater.

AI profiles identify provider, model label, and chat context. Role actors sharing one model and chat context must share one independence group and count as one evidence source.

## 6. Tolerant ingestion and strict canonicalization

For every received response:

1. preserve the raw response;
2. attempt exact parsing;
3. detect the observed format;
4. validate when possible;
5. request simpler reformatting when useful;
6. normalize only sufficiently clear meaning;
7. quarantine ambiguity or accept it as opinion-only when strict normalization is unsafe.

Allowed dispositions are `ACCEPTED_CONFORMANT`, `ACCEPTED_NORMALIZED`, `ACCEPTED_OPINION_ONLY`, `QUARANTINED_AMBIGUOUS`, `REJECTED_UNUSABLE`, and `STALE_RESPONSE`.

Normalization must not invent approval, permission, evidence, citation, confidence, identity, provenance, or a stronger claim. Canonical acceptance of a normalization requires a revision-bound confirmation. Natural-language intent may be used to prepare a canonical-command preview, but an authority-sensitive mutation must not infer missing IDs, revisions, selected actions, approvers, or expected state versions. The exact canonical command and arguments, or an equivalent revision-bound confirmation artifact, must be recorded before mutation.

## 7. Plain relay and adaptive roles

A `PLAIN_RELAY_PACKET` contains a concise topic, bounded role, context, questions, prohibited inferences, requested format, session ID, and source state version. It is `PROPOSE_ONLY`.

Roles are temporary analytical functions with lifecycle `PROPOSED`, `ACTIVE`, `PAUSED`, `RETIRED`, or `REASSIGNED`. Analytical role changes do not change facilitator, owner, approver, veto, or execution authority.

## 8. Claim ledger

Claims are typed as `FACT`, `SOURCE_CLAIM`, `MODEL_INFERENCE`, `PROPOSAL`, or `OPINION`.

A high or critical `FACT` or `SOURCE_CLAIM` with `UNVERIFIED` status must have `usable_for_decision: false`. This is a schema invariant, not merely a fixture lint rule.

## 9. Team decisions and minutes

Decision methods are `SINGLE_DECISION_OWNER`, `NAMED_APPROVERS`, `UNANIMOUS`, `MAJORITY`, `CONSENT_BASED`, `ADVISORY_ONLY`, and `EXTERNAL_GOVERNANCE`.

Direct and relayed statements are distinguished. Material dissent is preserved. Private input is not shared or recorded without permission.

Minutes are separate from canonical state. An `APPROVED` decision entry requires a positive decision revision and at least one named approver. `minutes-approve` succeeds only for the exact revision after the applicable human review state is recorded.

## 10. Help and user navigation

A Help assistant explains, diagnoses, and proposes repairs but cannot approve, execute, or claim a repair was applied.

Entering help records the prior phase. `help-exit` restores only that recorded phase at the expected source state version.

A `NEXT_ACTION_CARD` is emitted only at a legitimate pause and therefore has `action_required: true`. Its actor vocabulary is shared with Help responses: `USER`, `NAMED_HUMAN`, or `EXTERNAL_PARTICIPANT`.

## 11. Session portability

Import is two-stage:

1. `session-import` preserves the source and creates a `SESSION_IMPORT_REPORT`;
2. `session-import-confirm` names the exact report revision and selected action.

Before confirmation, canonical state remains unchanged. An import cannot silently merge, replace state, restore authority, or validate unread material.

## 12. Executable command and sequencing validation

Alpha.3 conformance requires more than registry and schema presence.

The reference parser must resolve all canonical commands and aliases without namespace collision. The bounded runtime must test at least:

- explicit `goal-confirm` followed by explicit `session-start`;
- rejection of substantive transitions before `session-start`;
- exact decision revision approval;
- goal revision confirmation;
- raw ingestion before normalization;
- normalization confirmation before canonical acceptance;
- minutes review before minutes approval;
- import report before import confirmation;
- exact session revision on resume and end;
- help entry and `help-exit`;
- no external execution.

## 13. Validation evidence and release readiness

A hand-written `DONE` field, free-text `VALID` statement, or model self-assessment is not machine evidence. Displaying an abbreviated artifact is allowed only when it is clearly marked as a view; the abbreviated view must not be claimed schema-valid unless the complete artifact bytes are separately identified.

Artifact validation uses `VALIDATION_RECEIPT` from `schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml`. A receipt binds an artifact locator, exact revision or version, canonicalization method, complete artifact hash, schema hash, executor type and version, result, and structured errors. Only a tool, deterministic runtime, or CI workflow may be the receipt executor.

`RAW_BYTES` hashes exact bytes. `MADP_CANONICAL_JSON_V1` hashes UTF-8 JSON with lexicographically sorted keys, no insignificant whitespace, preserved Unicode, and no non-finite numbers. The canonicalization choice is part of the receipt and cannot be inferred after hashing.

A VERIFIED or FIELD_TRIAL load report carries `schema_validation_records`. Each record binds one loaded repository target, target hash, artifact identity and version, schema path and hash, receipt ID, and result. `schemas_applicable`, `schemas_executed`, the validation records, `unvalidated_structured_sources`, and `validation_receipt_refs` must agree. A receipt reference without the corresponding receipt artifact is not evidence.

Formal usability evidence additionally binds the complete load report to its report schema, the selected start profile to its exact bytes, and the raw observation to a repository-relative file hash. The release checker recomputes these links; a structurally plausible but unbound receipt fails closed.

Each required validation command is executed by the evidence runner. It emits a validation evidence manifest containing the command, result, return code, checker hash, input hashes, and output hashes. The release audit verifies that manifest against the current scripts.

The implementation-status file declares required checks and blockers; it does not self-attest that those checks passed.

## 14. Skill adapters and translations

The canonical Agent Skills set contains `madp-start`, `madp-facilitator`, `madp-participant`, `madp-recorder`, and `madp-help`. ChatGPT instruction adapters and Claude distributions must cover the same five roles from the shared source.

Translation audit proves source freshness and configured marker coverage. It does not by itself prove full semantic equivalence; that limitation must be explicit.

## 15. Conformance summary

Alpha.3 conformance requires:

- inherited command compatibility without name collisions;
- revision- and session-bound artifacts;
- no authority escalation during parsing, normalization, migration, or import;
- capability-aware and independence-aware participation;
- schema-enforced material-claim, load-report, validation-receipt, registry, and approval invariants;
- runtime-tested `goal-confirm` to `session-start` sequencing and fail-closed pre-start behavior;
- receipt-bound and independently recomputed validation evidence, plus evidence-backed release audits;
- explicit limitations when validation, tools, files, or translations were not fully verified.

<!-- MADP_SOURCE_END path=protocol/MADP-v0.3.0-alpha.3.md -->

## Embedded source 2: `registries/v0.3.0-alpha.3/commands.yaml`

<!-- MADP_SOURCE_BEGIN index=2 path=registries/v0.3.0-alpha.3/commands.yaml sha256=e1abf46d51e645ddb7ebc2d14028e83087db2eae27710ffe6bac1e6a7fcea35f bytes=27478 role=COMMAND_REGISTRY -->
registry_version: MADP-COMMAND-REGISTRY-v0.2
protocol_version: MADP-v0.3.0-alpha.3
status: release-candidate-content
canonical_name_policy: lowercase-kebab-case
composition:
  policy: ALPHA2_CANONICAL_SUPERSET
  inherited_registry_version: MADP-COMMAND-REGISTRY-v0.1
  inherited_protocol_version: MADP-v0.3.0-alpha.2
  inherited_alpha2_commands:
  - share-context
  - issue-relay
  - request-review
  - summarize-state
  - check-authority
  - propose-decision
  - approve
  - reject
  - defer
  - prioritize
  - pause
  - resume
  - status
  - todo-add
  - todo-list
  - todo-update
  - todo-done
  - todo-defer
  - todo-promote
  - external-action
  added_alpha3_commands:
  - session-start
  - session-status
  - session-checkpoint-create
  - session-resume
  - session-export
  - session-import
  - session-import-confirm
  - session-end
  - participant-add
  - participant-update-capability
  - participant-set-mode
  - goal-propose
  - goal-confirm
  - role-assign
  - role-pause
  - role-retire
  - relay-create-plain
  - response-ingest
  - response-normalize
  - normalization-confirm
  - claim-add
  - claim-verify
  - minutes-generate
  - minutes-review
  - minutes-approve
  - minutes-redact
  - minutes-export
  - help
  - help-context-create
  - help-exit
  - team-approval-record
alias_policy:
  aliases_are_input_convenience_only: true
  canonical_command_must_be_recorded: true
  canonical_names_take_precedence: true
  aliases_must_not_change_authority: true
  unknown_or_ambiguous_alias: DENY_AND_SHOW_HELP
command_groups:
- group: SESSION
  purpose: Session lifecycle and state reporting.
- group: CONTEXT
  purpose: Context packaging.
- group: RELAY
  purpose: Bounded relays.
- group: REVIEW
  purpose: Review requests.
- group: AUTHORITY
  purpose: Authority classification.
- group: DECISION
  purpose: Decision proposals and human decisions.
- group: TODO
  purpose: TODO lifecycle.
- group: EXTERNAL
  purpose: External-action requests without execution.
- group: PLANNING
  purpose: Goal planning and confirmation.
- group: PARTICIPANT
  purpose: Participant and capability management.
- group: ROLE
  purpose: Analytical role lifecycle.
- group: INGESTION
  purpose: Response ingestion and normalization.
- group: EVIDENCE
  purpose: Claim ledger operations.
- group: RECORDS
  purpose: Minutes and records.
- group: TEAM
  purpose: Named team approvals.
- group: HELP
  purpose: Protocol help.
- group: PORTABILITY
  purpose: User-managed session files.
aliases:
- alias: start
  command: session-start
- alias: checkpoint
  command: session-checkpoint-create
- alias: save
  command: session-export
- alias: backup
  command: session-export
- alias: load
  command: session-import
- alias: restore
  command: session-import
- alias: end
  command: session-end
- alias: minutes
  command: minutes-generate
- alias: export-minutes
  command: minutes-export
commands:
- command: share-context
  group: CONTEXT
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - purpose
  optional_arguments:
  - target_role
  - source_session_id
  - include_files
  - limitations
  test_arguments:
    purpose: handoff
  effect_summary: Prepare a context package without granting authority.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: issue-relay
  group: RELAY
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - relay_mode
  - target_role
  optional_arguments:
  - include_state
  - include_evidence
  - limitations
  test_arguments:
    relay_mode: PLAIN
    target_role: reviewer
  effect_summary: Prepare a bounded relay without granting authority.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: request-review
  group: REVIEW
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - review_focus
  optional_arguments:
  - artifacts
  - target_role
  - context_package
  test_arguments:
    review_focus: authority-boundary
  effect_summary: Request bounded review findings.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: summarize-state
  group: SESSION
  command_class: AI_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments: []
  optional_arguments:
  - focus
  - since
  - include_todos
  test_arguments: {}
  effect_summary: Summarize current state without mutation.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: check-authority
  group: AUTHORITY
  command_class: AI_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments:
  - action
  optional_arguments:
  - scope
  - grant_ref
  test_arguments:
    action: write-file
  effect_summary: Classify whether an action is allowed.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: propose-decision
  group: DECISION
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - decision
  optional_arguments:
  - rationale
  - alternatives
  - risks
  test_arguments:
    decision: DEC-001
  effect_summary: Propose a decision candidate.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: approve
  group: DECISION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - decision
  - revision
  optional_arguments:
  - scope
  - conditions
  test_arguments:
    decision: DEC-001
    revision: 1
  effect_summary: Record approval for an exact decision revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: reject
  group: DECISION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - target
  optional_arguments:
  - reason
  test_arguments:
    target: DEC-001
  effect_summary: Record explicit rejection.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: defer
  group: DECISION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - target
  optional_arguments:
  - until
  - reason
  test_arguments:
    target: TODO-001
  effect_summary: Record explicit deferral.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: prioritize
  group: DECISION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - target
  - priority
  optional_arguments:
  - reason
  test_arguments:
    target: TODO-001
    priority: HIGH
  effect_summary: Set user-visible priority.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: pause
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments: []
  optional_arguments:
  - reason
  test_arguments: {}
  effect_summary: Pause workflow progression.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: resume
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments: []
  optional_arguments:
  - scope
  test_arguments: {}
  effect_summary: Resume a paused workflow within prior authority.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: status
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments: []
  optional_arguments:
  - scope
  test_arguments: {}
  effect_summary: Report current workflow status.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-add
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - title
  optional_arguments:
  - type
  - priority
  - owner
  - related_issue
  - related_decision
  test_arguments:
    title: Follow up
  effect_summary: Add a TODO item.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-list
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments: []
  optional_arguments:
  - status
  - owner
  - priority
  test_arguments: {}
  effect_summary: List TODO items.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-update
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - todo_id
  optional_arguments:
  - title
  - status
  - priority
  - owner
  - blocking_reason
  test_arguments:
    todo_id: TODO-001
  effect_summary: Update TODO metadata.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-done
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - todo_id
  - completion_basis
  optional_arguments:
  - evidence
  test_arguments:
    todo_id: TODO-001
    completion_basis: verified
  effect_summary: Mark a TODO done with a basis.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-defer
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - todo_id
  optional_arguments:
  - until
  - reason
  test_arguments:
    todo_id: TODO-001
  effect_summary: Defer a TODO.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: todo-promote
  group: TODO
  command_class: TODO_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - todo_id
  - target_type
  optional_arguments:
  - rationale
  - confirmation_ref
  test_arguments:
    todo_id: TODO-001
    target_type: PROPOSAL
  effect_summary: Promote a TODO without approving it.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: external-action
  group: EXTERNAL
  command_class: EXTERNAL_ACTION_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - action
  - scope
  optional_arguments:
  - reason
  - confirmation_ref
  - dry_run
  test_arguments:
    action: write-file
    scope: artifact.md
  effect_summary: Request confirmation for an external action.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-start
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - session_id
  - deliberation_plan
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
    deliberation_plan: PLAN-001
  effect_summary: Start a session from a confirmed plan.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-status
  group: SESSION
  command_class: SESSION_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments:
  - session_id
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
  effect_summary: Report alpha.3 session state.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-checkpoint-create
  group: SESSION
  command_class: RECORD_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - label
  - source_state_version
  optional_arguments: []
  test_arguments:
    label: before-review
    source_state_version: 1
  effect_summary: Create a revision-bound checkpoint.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-resume
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - session_id
  - expected_state_version
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
    expected_state_version: 1
  effect_summary: Resume an exact session state.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-export
  group: PORTABILITY
  command_class: RECORD_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - session_export_request
  optional_arguments: []
  test_arguments:
    session_export_request: EXPORT-001
  effect_summary: Prepare a portable session export.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-import
  group: PORTABILITY
  command_class: PORTABILITY_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - source_file
  optional_arguments: []
  test_arguments:
    source_file: session.yaml
  effect_summary: Validate a supplied session file without state replacement.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-import-confirm
  group: PORTABILITY
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - import_id
  - report_revision
  - selected_action
  optional_arguments: []
  test_arguments:
    import_id: IMPORT-001
    report_revision: 1
    selected_action: CREATE_NEW_SESSION
  effect_summary: Confirm an exact import report revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: session-end
  group: SESSION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - session_id
  - expected_state_version
  - end_reason
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
    expected_state_version: 1
    end_reason: complete
  effect_summary: End an exact session state.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: participant-add
  group: PARTICIPANT
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - participant_profile
  optional_arguments: []
  test_arguments:
    participant_profile: PARTICIPANT-001
  effect_summary: Register a participant profile.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: participant-update-capability
  group: PARTICIPANT
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - participant_id
  - capabilities
  optional_arguments: []
  test_arguments:
    participant_id: AI-001
    capabilities: CAP-SET-001
  effect_summary: Update observed capability metadata.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: participant-set-mode
  group: PARTICIPANT
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - participant_id
  - participation_mode
  optional_arguments: []
  test_arguments:
    participant_id: AI-001
    participation_mode: OPINION_ONLY
  effect_summary: Set participation mode.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: goal-propose
  group: PLANNING
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - deliberation_plan
  optional_arguments: []
  test_arguments:
    deliberation_plan: PLAN-001
  effect_summary: Propose a deliberation goal revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: goal-confirm
  group: PLANNING
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - plan_id
  - revision
  - source_state_version
  optional_arguments: []
  test_arguments:
    plan_id: PLAN-001
    revision: 1
    source_state_version: 1
  effect_summary: Confirm an exact goal revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: role-assign
  group: ROLE
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - role_assignment
  optional_arguments: []
  test_arguments:
    role_assignment: ROLE-001
  effect_summary: Assign a bounded analytical role.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: role-pause
  group: ROLE
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - role_id
  optional_arguments:
  - source_state_version
  test_arguments:
    role_id: ROLE-001
  effect_summary: Pause an analytical role.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: role-retire
  group: ROLE
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - role_id
  - reason
  optional_arguments:
  - source_state_version
  test_arguments:
    role_id: ROLE-001
    reason: complete
  effect_summary: Retire an analytical role.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: relay-create-plain
  group: RELAY
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - plain_relay_packet
  optional_arguments: []
  test_arguments:
    plain_relay_packet: RELAY-001
  effect_summary: Create a bounded plain-text relay.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: response-ingest
  group: INGESTION
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - session_id
  - source_state_version
  - raw_response_ref
  - participant_id
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
    source_state_version: 1
    raw_response_ref: artifact://raw/1
    participant_id: AI-001
  effect_summary: Preserve and classify a response.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: response-normalize
  group: INGESTION
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - ingest_id
  - source_state_version
  - normalization_record
  optional_arguments: []
  test_arguments:
    ingest_id: ING-001
    source_state_version: 1
    normalization_record: NORM-001
  effect_summary: Create an auditable normalization proposal.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: normalization-confirm
  group: INGESTION
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - normalization_id
  - source_state_version
  - status
  optional_arguments: []
  test_arguments:
    normalization_id: NORM-001
    source_state_version: 1
    status: CONFIRMED
  effect_summary: Confirm an exact normalization.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: claim-add
  group: EVIDENCE
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - claim
  optional_arguments: []
  test_arguments:
    claim: CLAIM-001
  effect_summary: Add a typed claim.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: claim-verify
  group: EVIDENCE
  command_class: AI_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - claim_id
  - verification_status
  optional_arguments:
  - source_state_version
  test_arguments:
    claim_id: CLAIM-001
    verification_status: VERIFIED
  effect_summary: Record claim verification.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: minutes-generate
  group: RECORDS
  command_class: RECORD_COMMAND
  default_authority_boundary: PROPOSE_ONLY
  required_arguments:
  - session_id
  - source_state_version
  - detail_level
  optional_arguments: []
  test_arguments:
    session_id: SESSION-001
    source_state_version: 1
    detail_level: STANDARD
  effect_summary: Generate draft minutes.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: minutes-review
  group: RECORDS
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - minutes_id
  - revision
  - review_status
  optional_arguments: []
  test_arguments:
    minutes_id: MIN-001
    revision: 1
    review_status: HUMAN_REVIEWED
  effect_summary: Record human review of a minutes revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: minutes-approve
  group: RECORDS
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - minutes_id
  - revision
  optional_arguments: []
  test_arguments:
    minutes_id: MIN-001
    revision: 1
  effect_summary: Approve an exact reviewed minutes revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: minutes-redact
  group: RECORDS
  command_class: RECORD_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - minutes_id
  - redactions
  optional_arguments:
  - revision
  test_arguments:
    minutes_id: MIN-001
    redactions: REDACTION-001
  effect_summary: Redact permitted content with an audit note.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: minutes-export
  group: RECORDS
  command_class: RECORD_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - minutes_id
  - format
  optional_arguments:
  - revision
  test_arguments:
    minutes_id: MIN-001
    format: MARKDOWN
  effect_summary: Export a selected minutes revision.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: help
  group: HELP
  command_class: HELP_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments:
  - question
  optional_arguments: []
  test_arguments:
    question: next-action
  effect_summary: Enter protocol help without substantive authority.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: help-context-create
  group: HELP
  command_class: HELP_COMMAND
  default_authority_boundary: REFERENCE_ONLY
  required_arguments:
  - help_context_packet
  optional_arguments: []
  test_arguments:
    help_context_packet: HELP-CONTEXT-001
  effect_summary: Create minimal context for a Help chat.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: help-exit
  group: HELP
  command_class: USER_COMMAND
  default_authority_boundary: USER_CONFIRMED
  required_arguments:
  - help_request_id
  - source_state_version
  optional_arguments: []
  test_arguments:
    help_request_id: HELP-001
    source_state_version: 1
  effect_summary: Exit Help and restore the recorded phase.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.
- command: team-approval-record
  group: TEAM
  command_class: TEAM_COMMAND
  default_authority_boundary: REQUIRES_USER_CONFIRMATION
  required_arguments:
  - decision_id
  - approver_id
  - decision_revision
  optional_arguments: []
  test_arguments:
    decision_id: DEC-001
    approver_id: USER-001
    decision_revision: 1
  effect_summary: Record a named human approval.
  safety_notes:
  - Parsing or recording this command does not expand authority.
  prohibited_effects:
  - External execution without separate trusted permission.

<!-- MADP_SOURCE_END path=registries/v0.3.0-alpha.3/commands.yaml -->

## Embedded source 3: `registries/v0.3.0-alpha.3/workflow-macros.yaml`

<!-- MADP_SOURCE_BEGIN index=3 path=registries/v0.3.0-alpha.3/workflow-macros.yaml sha256=e34b65eeed58ead09272b3932b101490cd69781e57caf561c48610cbd6c138e2 bytes=3443 role=WORKFLOW_MACRO_REGISTRY -->
registry_version: MADP-WORKFLOW-MACRO-REGISTRY-v0.1
protocol_version: MADP-v0.3.0-alpha.3
status: experimental-profile
canonical_command_registry: registries/v0.3.0-alpha.3/commands.yaml
record_canonical_commands: true
macros_are_aliases: false
macros_are_atomic: false
missing_arguments_policy: REQUEST_EXACT_VALUE
stale_state_policy: REJECT
macros:
  - macro: init
    purpose: Establish a confirmed plan and explicitly start a session.
    steps:
      - command: goal-propose
      - gate: HUMAN_CONFIRM_EXACT_PLAN_REVISION
      - command: goal-confirm
      - gate: HUMAN_START_SESSION
      - command: session-start
    required_invariants:
      - GOAL_CONFIRM_DOES_NOT_START_SESSION
      - EXACT_PLAN_AND_STATE_BINDING
      - HUMAN_FINAL_AUTHORITY
  - macro: register
    purpose: Register participants, modes, capabilities, correlation, and roles.
    steps:
      - command: participant-add
      - command: participant-update-capability
        optional: true
      - command: participant-set-mode
      - command: role-assign
        optional: true
    required_invariants:
      - SAME_MODEL_NOT_INDEPENDENT_BY_DEFAULT
      - PARTICIPATION_DOES_NOT_GRANT_APPROVAL
  - macro: capture
    purpose: Relay a bounded question and preserve the raw response.
    steps:
      - command: relay-create-plain
        optional: true
      - gate: HUMAN_MANUAL_RELAY
      - command: response-ingest
    required_invariants:
      - RAW_RESPONSE_FIRST
      - EXTERNAL_PARTICIPANT_NO_APPROVAL_AUTHORITY
      - SOURCE_STATE_BINDING
  - macro: structure
    purpose: Normalize a response and record claims without replacing raw data.
    steps:
      - command: response-normalize
      - gate: HUMAN_REVIEW_NORMALIZATION_DIFF
      - command: normalization-confirm
      - command: claim-add
      - command: claim-verify
        optional: true
    required_invariants:
      - RAW_RESPONSE_PRESERVED
      - NORMALIZATION_REVISION_BOUND
      - UNKNOWN_REMAINS_UNKNOWN
  - macro: review
    purpose: Critique claims, identify missing evidence, and preserve dissent.
    steps:
      - command: request-review
      - command: claim-verify
        optional: true
      - command: summarize-state
    required_invariants:
      - AGREEMENT_IS_NOT_EVIDENCE
      - POST_EXPOSURE_AGREEMENT_NOT_INDEPENDENT
      - MATERIAL_DISSENT_VISIBLE
  - macro: decide
    purpose: Propose a decision and record the exact human disposition.
    steps:
      - command: propose-decision
      - gate: HUMAN_REVIEW_EVIDENCE_AND_DISSENT
      - one_of_commands:
          - approve
          - reject
          - defer
    required_invariants:
      - HUMAN_FINAL_AUTHORITY
      - EXACT_DECISION_REVISION
      - DECISION_NOT_EXECUTION_AUTHORIZATION
  - macro: authorize
    purpose: Check authority and separately request an external action.
    steps:
      - command: check-authority
      - command: external-action
        optional: true
      - gate: SEPARATE_TRUSTED_EXECUTION_CONFIRMATION
    required_invariants:
      - APPROVAL_NOT_EXECUTION_AUTHORIZATION
      - MACRO_NEVER_EXECUTES_EXTERNAL_ACTION
      - EXACT_ACTION_SCOPE
  - macro: status
    purpose: Show workflow state, session state, outstanding work, and next action.
    steps:
      - command: status
      - command: session-status
        optional: true
      - command: todo-list
        optional: true
    required_invariants:
      - REFERENCE_ONLY
      - NO_STATE_MUTATION

<!-- MADP_SOURCE_END path=registries/v0.3.0-alpha.3/workflow-macros.yaml -->

## Embedded source 4: `docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md`

<!-- MADP_SOURCE_BEGIN index=4 path=docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md sha256=0f9e2007407e8c565b0c128bdcdaa678b4b5ed3a0aeb76f76bff35460a6ccfc1 bytes=7754 role=CORE_PROFILE -->
# MADP Core Candidate Profile for MADP v0.3.0-alpha.3

Status: experimental normative candidate profile. It does not amend the alpha.3
runtime, complete a release blocker, or authorize alpha.4 implementation.

Decision basis: `docs/planning/DEC-MADP-CORE-001.yaml`.

## Purpose

Test a minimum useful MADP layer for human-mediated multi-AI deliberation without
requiring metered APIs, agent orchestration, A2A, MCP, or a vendor-specific
runtime.

The Core Candidate exists to prevent multiple AI responses from being used in a
decision with incorrect assumptions about evidence, authority, provenance, or
independence.

## Scope boundary

Core Candidate operation:

- treats manual copy-and-paste and plain-text relay as first-class mechanisms;
- permits local CLI, Python, hashing, and schema validation without paid APIs;
- keeps A2A, MCP, Agent SDK, and automatic model invocation in optional
  Automation Extensions;
- preserves the alpha.3 canonical command registry and runtime invariants;
- uses `registries/v0.3.0-alpha.3/workflow-macros.yaml` only as a human-facing,
  non-atomic orchestration layer.

No macro, profile, participant response, model consensus, approval, or decision
implicitly authorizes an external action.

## Core invariants

### Human Final Authority

A human records the final decision. AI participants remain `PROPOSE_ONLY` or
`OPINION_ONLY` unless a separate trusted authority record explicitly says
otherwise. Agreement Is Not Evidence, and majority support is not approval.

### Blind First Round

Every conforming multi-participant Core Candidate deliberation performs a Blind
First Round before Cross Exposure.

Minimum requirements:

```yaml
blind_first_round:
  minimum_eligible_initial_responses: 2
  exposure_before_capture: false
  preserve_raw_initial_responses: true
  overwrite_initial_responses: false
```

Each initial response records:

```yaml
exposure:
  state: UNEXPOSED | PARTIALLY_EXPOSED | EXPOSED | UNKNOWN
  exposed_response_refs: []
```

`UNKNOWN` must remain `UNKNOWN`; it must not be upgraded to `UNEXPOSED` by
inference. Responses from the same model family, shared chat, shared retrieval
source, or other known common origin may be retained, but their correlation must
be recorded and they must not be counted as independently corroborating
sources.

If prior conclusions are exposed before the initial response is fixed, classify
the result as `PARTIALLY_COMPROMISED`, `ANCHORING_EXPOSED`, or
`NOT_PERFORMED`. The response may remain ordinary review evidence, but the run
must not be represented as a conforming Blind First Round.

### Raw response preservation

Preserve raw prompts and responses before normalization. Normalized responses,
claims, summaries, minutes, and decisions reference raw records and never replace
them.

### Claim, Evidence, Dissent, and Decision separation

Keep these records distinct:

- a Claim records what is asserted;
- Evidence records what supports or challenges a Claim;
- Dissent records a material unresolved objection;
- a Decision records the human choice, rationale, revision, acknowledged
  dissent, and supporting references.

The candidate direction separates speech form from verification state:

```yaml
claim_candidate:
  claim_kind: SOURCE_CLAIM | MODEL_INFERENCE | PROPOSAL | OPINION
  verification_status: UNCHECKED | SOURCE_MATCHED | CORROBORATED | DISPUTED | REFUTED | OUTDATED | NOT_APPLICABLE
```

This is a migration target, not permission to delete the existing alpha.3
`FACT` representation. Existing fields remain until replacement schemas,
negative fixtures, migration logic, and safety-invariant tests are complete.

Evidence assessment remains multidimensional:

```yaml
evidence_assessment:
  source_role: DIRECT_RECORD | PRIMARY | SECONDARY | TERTIARY | USER_STATEMENT | MODEL_ONLY | UNKNOWN
  claim_fit: DIRECT | PARTIAL | INDIRECT | UNSUPPORTED | UNKNOWN
  freshness: CURRENT | POTENTIALLY_STALE | STALE | TIME_INDEPENDENT | UNKNOWN
  traceability: SNAPSHOT_HASHED | RETRIEVABLE | CITATION_ONLY | NONE
  source_independence: INDEPENDENTLY_CORROBORATED | SINGLE_SOURCE | DERIVED_FROM_SAME_ORIGIN | UNKNOWN
```

A display summary may be derived in an Assured profile, but Core does not require
or trust a single composite evidence score.

### Dissent state and disposition

Do not collapse unresolved state into a resolution reason.

```yaml
dissent_candidate:
  status: OPEN | RESOLVED | SUPERSEDED
  disposition: NONE | ACCEPTED | INCORPORATED | REJECTED_WITH_RATIONALE | OVERRIDDEN_BY_HUMAN | WITHDRAWN | REPLACED
```

For example, `status: OPEN` with `disposition: OVERRIDDEN_BY_HUMAN` records that
the objection remains unresolved and that the human knowingly proceeded.

### Revision-bound decision and authorization

Approval binds to the exact decision revision. A decision, approval, and
Execution Authorization are separate. Execution Authorization is optional when
there is no external action, but the semantic separation is always preserved.

## Minimum records

A Core Candidate run preserves at least:

1. protocol binding;
2. participant and correlation register;
3. question, scope, and authority boundary;
4. raw initial responses and exposure records;
5. Cross Exposure and revision records, when used;
6. Claim and Evidence records sufficient for the decision;
7. Dissent records;
8. a revision-bound human Decision Record.

Minimum protocol binding:

```yaml
protocol_binding:
  protocol_version: MADP-v0.3.0-alpha.3
  source_ref: repository-commit-or-release
  source_digest: "<sha256 or documented unavailable status>"
  profile_path: docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md
```

A formal FIELD_TRIAL or Assured run additionally uses the complete alpha.3 load
report, profile binding, validation receipts, raw observation inventory, and
recomputation requirements. The minimum Core binding does not substitute for
those release-evidence controls.

## Human-facing interaction contract

At every legitimate pause, show:

```yaml
CURRENT_STATE: "..."
CURRENT_QUESTION: "..."
FACILITATOR_ACTION: "..."
HUMAN_DECISION_REQUIRED: "... or NONE"
NEXT_ACTION: "..."
CANONICAL_EXPANSION: []
```

Natural-language choices may be offered, but the accepted action is recorded as
canonical command invocations with exact IDs, revisions, and state versions.

## Workflow Macro use

The human-facing macros are `init`, `register`, `capture`, `structure`, `review`,
`decide`, `authorize`, and `status`.

Macros are not aliases and are not atomic. They may stop at an explicit user or
validation gate. Every executed step is recorded using the existing canonical
command name. Missing required arguments are requested rather than inferred.

See `docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md` and
`registries/v0.3.0-alpha.3/workflow-macros.yaml`.

## Conformance and graceful degradation

A run may be useful without being fully conforming. Report the reason precisely.

```yaml
core_candidate_conformance:
  status: CONFORMING | DEGRADED | NONCONFORMING | NOT_EVALUATED
  reasons: []
```

Blind First Round failure, missing raw records, inferred exposure, unbound
approval, or authority ambiguity prevents `CONFORMING`. Degraded evidence may be
retained for ordinary review, but must not be relabeled as formal FIELD_TRIAL
evidence or used to complete a release blocker.

## Comparative evaluation

Compare this profile with standard alpha.3, ordinary manual comparison, and a
Markdown-plus-validator workflow. Measure completion time, human actions,
canonical commands, corrections, unclear next actions, authority and stale-state
errors, Blind First Round status, dissent preservation, decision reconstruction,
and user burden.

alpha.4 remains deferred until comparative evidence supports a version change.

<!-- MADP_SOURCE_END path=docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md -->

## Embedded source 5: `docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md`

<!-- MADP_SOURCE_BEGIN index=5 path=docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md sha256=44d1260fbd4c399489dfce8643d44c693027a64812708e9b254d4326e95fc34e bytes=3664 role=MACRO_PROFILE -->
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

<!-- MADP_SOURCE_END path=docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md -->

## Embedded source 6: `docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md`

<!-- MADP_SOURCE_BEGIN index=6 path=docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md sha256=2c37b00f7482ed130af1f992201ccf4e86f9d2ee1b8a81c761b9812ee4be02bd bytes=1445 role=BLIND_PROFILE -->
# Blind First-Round Review Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Purpose

Reduce anchoring and conformity by separating an independent initial position from later cross-exposure and revision.

## Sequence

1. `BLIND_INITIAL_POSITION`: provide the question, evidence scope, and authority boundary without prior participant conclusions.
2. `CROSS_EXPOSURE`: disclose the other positions and request the strongest criticism, failure conditions, and missing evidence.
3. `REVISION`: record claims changed, retained, or withdrawn and the reason for each change.
4. `INTEGRATION`: compare independent convergence, correlated convergence, and residual dissent.

## Required controls

- Bind each round to one session ID, source state version, information-set hash, and participant independence group.
- Preserve the raw initial response before normalization.
- Do not count multiple roles in one shared chat as independent initial positions.
- Do not describe agreement reached only after cross-exposure as independent convergence.
- A participant may remain `OPINION_ONLY`; review participation does not grant approval authority.
- Material dissent remains visible through integration and minutes.

## Failure handling

If the initial round accidentally reveals prior conclusions, classify the run as `ANCHORING_EXPOSED`; it may remain useful as ordinary review evidence but not blind-round evidence.

<!-- MADP_SOURCE_END path=docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md -->

## Embedded source 7: `bootstrap/alpha3/quick-start.md`

<!-- MADP_SOURCE_BEGIN index=7 path=bootstrap/alpha3/quick-start.md sha256=c8f94142b5133dd51d6ad8dc207ff810099f6d0ed4660de40e0ba374ad739de8 bytes=3525 role=BOOTSTRAP -->
---
bootstrap_version: 0.8-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: QUICK
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v2
accepted_load_profiles:
  QUICK: ba8c4b88c55de4d73ea82292fcaa38d2825096f3e08df041985bdab57be692c0
  VERIFIED: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
  FIELD_TRIAL: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
required_repository: Eruhitsuji/multi-ai-deliberation-protocol
profile_source_binding_required: true
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in QUICK mode

This profile configures a protocol that has already been loaded. It does not load or reconstruct MADP rules.

Before starting, identify the highest active, non-superseded `PROTOCOL_LOAD_REPORT` revision and require a `PROFILE_SOURCE_BINDING` containing the repository, commit, path, source reference, exact profile SHA-256, and source inventory digest.

The load report must:

- use `MADP-PROTOCOL-LOAD-REPORT-v2`;
- be for `MADP-v0.3.0-alpha.3`;
- have a positive revision, `active: true`, and not be superseded by a later active revision;
- use the official repository named in frontmatter;
- have the same repository and commit as `PROFILE_SOURCE_BINDING`;
- use an accepted load profile and exact inventory digest from frontmatter;
- be `COMPLETE`, with every selected source recorded once as `READ`;
- have `all_required_files_read: true` and `inferred_unread_content: false`;
- have `SOURCE_REFERENCED` or `HASH_VERIFIED` provenance;
- authorize `bootstrap/alpha3/quick-start.md` from the same repository and commit;
- bind the authorized profile hash to the exact bytes named by `PROFILE_SOURCE_BINDING`;
- satisfy `schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml` when validation is available;
- have `authorized_start_profiles: []` whenever the report is `INCOMPLETE`.

A FIELD_TRIAL report is eligible for formal evidence only when its schema-validation records and referenced receipts are preserved and independently recomputable.

If the report or binding is missing, stale, self-attested, mismatched, or incomplete, do not infer protocol behavior and do not start a session. Return:

```yaml
MADP_BOOTSTRAP_STATUS:
  status: PROTOCOL_NOT_LOADED
  reason: MISSING_OR_INVALID_ACTIVE_LOAD_REPORT | PROFILE_SOURCE_MISMATCH
  protocol_version: MADP-v0.3.0-alpha.3
  required_loader: bootstrap/alpha3/load-protocol-from-github.md
  next_action: Load or recover the protocol, then provide the latest active report and matching PROFILE_SOURCE_BINDING.
```

After the gate passes, establish session ID, current state version, a revisioned deliberation plan, human decision authority, and the smallest useful role set. Default authority is `PROPOSE_ONLY`.

`goal-confirm` changes only the exact plan revision to `USER_CONFIRMED`. It does not start substantive work. Emit a Next Action Card requesting the separate exact `session-start`. Only after `session-start` succeeds may the phase become `ACTIVE` and substantive deliberation begin.

Preserve alpha.2 canonical commands: `status`, `pause`, and `resume` are not aliases. Use `session-status`, `session-resume`, and `help-exit` for their explicit alpha.3 operations. Every accepted artifact is bound to the session and source state revision.

If schema validation was not executed, preserve that limitation in session state and do not describe the session as VERIFIED or ASSURED.

<!-- MADP_SOURCE_END path=bootstrap/alpha3/quick-start.md -->
