# Multi-AI Deliberation Protocol v0.2.5-rc.1

## Informative status note

This version is a release candidate. It is not final or stable, and the user has not yet approved a final release.

This release candidate has passed normal cross-chat relay, YAML serialization, and version-mismatch fail-closed tests. Other model families, additional abnormal cases, and broader interoperability remain under validation.

This note is informative and does not change the normative semantics of the protocol.

## 1. Purpose

The Multi-AI Deliberation Protocol (MADP) defines a service-neutral procedure for structured deliberation involving one or more AI systems, separated instances of the same model, role actors within one context, human or external validators, and execution agents.

MADP may be used for research, design, review, software development, operational planning, and everyday decisions. It aims to:

- exploit complementary model strengths;
- compensate for model limitations with other models, tools, evidence, experiments, or humans;
- avoid deciding solely by majority vote;
- support single-model as well as multi-model operation;
- allow participants and facilitators to join, leave, or change during a session;
- transfer current state rather than full conversation history;
- minimize model usage and user relay work;
- distinguish model convergence from external evidence;
- keep the user as the sole final decision-maker;
- separate deliberation permission from execution permission;
- support canonical English artifacts while interacting with users in their resolved language;
- support unconditional, conditional, and change-bearing approval.

## 2. Applicability

MADP may be used with:

- chat assistants;
- IDE assistants;
- coding agents;
- repository agents;
- workspace agents;
- automation agents;
- human or external validators.

Product names are examples only. The protocol does not depend on a specific provider.

## 3. Normative terms

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

- **User**: the sole final decision-maker.
- **Facilitator**: the actor that manages state, participants, authorization, budget, and progression.
- **AI Participant**: a separated model, chat, execution instance, or agent.
- **Role Actor**: a role played inside the same model or context. A Role Actor is not independent evidence.
- **Human or External Validator**: a human expert, official source, primary source, test, calculation, experiment, or audit mechanism.
- **Issue**: a bounded question being deliberated.
- **Session State**: the sole logical source of truth for the current session.
- **Operative Session State Snapshot**: the bounded current-state subset transferred for a receiving turn in the manual-relay profile.
- **Derived View**: a presentation, prompt, roster, issue card, or handoff generated from Session State.

### 3.1 Authority domains

[`GLOSSARY-v0.2.5-rc.1.md`](GLOSSARY-v0.2.5-rc.1.md) is normative for every term explicitly marked normative.

Authority is divided by domain:

1. the machine-readable schema controls field names, types, required properties, and enum spelling;
2. this protocol controls behavior, procedures, transitions, authorization, and conformance rules;
3. the glossary controls canonical term meanings and distinctions;
4. README text and examples are informative entry points;
5. translations and supplemental documents are informative unless explicitly marked otherwise.

A conflict among authority domains MUST be reported as a specification defect. It MUST NOT be silently resolved. Canonical English terms, schema identifiers, and enum values retain their exact spelling in translations.

## 4. Core principles

### 4.1 User authority

The user MUST remain the sole final decision-maker. Agreement among participants MUST NOT replace user approval.

### 4.2 No majority-only decisions

A proposal MUST NOT be accepted solely because more participants support it. A minority objection that identifies a material failure mode MUST be addressed through conditions, evidence, testing, redesign, or user judgment.

### 4.3 Convergence is not evidence

Agreement among AI systems or model instances is convergence, not independent evidence. It MUST NOT be counted as an increase in Evidence Level.

### 4.4 Current state, not full history

Participants SHOULD receive only the current relevant state:

- goal;
- fixed requirements;
- current decisions and their conditions;
- open issues;
- criteria;
- critical risks;
- required evidence;
- the assigned question;
- output constraints.

Full conversation history SHOULD NOT be copied by default.

### 4.5 Minimum sufficient deliberation

The facilitator SHOULD minimize participants, queries, rounds, prompt volume, response volume, user relay actions, chat switches, and file transfers without omitting decision-critical information.

### 4.6 Permission separation

Permission to deliberate MUST NOT imply permission to write files, run commands, commit, push, create pull requests, send external data, or modify external resources.

### 4.7 Single source of truth

`SESSION_STATE` MUST be the sole logical source of truth. Issue cards, rosters, prompts, ledgers, progress displays, and handoffs are derived views or transfer artifacts.

## 5. Rule priority

When instructions conflict, apply this order:

1. the user's current explicit instruction, stop, or revocation;
2. current fixed requirements in `SESSION_STATE`;
3. current decisions, conditions, and permissions in `SESSION_STATE`;
4. mandatory rules in this protocol;
5. defaults of the selected mode;
6. facilitator recommendations.

Silence, lack of response, topic continuation, questions about a proposal, partial agreement, or vague affirmation MUST NOT be treated as approval.

## 6. Actors and responsibilities

### 6.1 Facilitator

The facilitator MUST:

1. maintain the goal and bounded issues;
2. maintain `SESSION_STATE` and state versions;
3. preserve fixed requirements and decision conditions;
4. assign roles and detect capability gaps;
5. add participants only for a defined purpose;
6. remove or pause participants no longer needed;
7. create minimum sufficient prompts;
8. integrate answers into decisions, conditions, open items, and risks;
9. distinguish design questions from evidence or experiment questions;
10. manage usage and user-operation budgets;
11. state the user's next action clearly;
12. detect state divergence;
13. separate facilitation summaries from facilitator opinions;
14. continue all non-blocked facilitator-internal work within the same response.

The facilitator has no final decision authority.

### 6.2 Participants

Participants SHOULD:

- state their position;
- separate agreements from objections;
- identify critical and self-owned failure modes;
- present the strongest counterargument fairly;
- state minimum acceptable conditions;
- separate inference from verified fact;
- propose evidence or experiments when discussion alone is insufficient;
- stay within the assigned issue;
- avoid unnecessary repetition.

## 7. Execution locations and orchestration

Execution locations:

- `SAME_CONTEXT`: role switching inside one context;
- `SEPARATE_INSTANCE`: another chat, session, or instance of the same service or model;
- `EXTERNAL_SERVICE`: another provider, account domain, or data-handling boundary.

Orchestration modes:

- `DIRECT_ORCHESTRATION`;
- `USER_RELAY`;
- `SINGLE_MODEL_ORCHESTRATION`;
- `HYBRID_ORCHESTRATION`.

The facilitator MUST NOT claim to have used an AI, tool, source, or execution environment that was not actually used.

## 8. Review profile

### 8.1 Review Independence

- `I0`: same model and same context with role switching;
- `I1`: same model in separated chats or instances;
- `I2`: different models or model families;
- `I3`: AI plus a human expert or independent validation actor.

This describes configuration, not correctness.

### 8.2 Evidence Level

- `E0`: no external evidence;
- `E1`: external information used but not verified;
- `E2`: primary, official, or otherwise reliable sources checked;
- `E3`: cross-validation through independent sources, recalculation, reproduction, or experiment.

### 8.3 Context Isolation

- `C0`: shared conversation history and prior answers;
- `C1`: prior conclusions, objections, and current state shared;
- `C2`: only the common issue, premises, and criteria shared;
- `C3`: source acquisition and analysis process also independent.

Convergence labels MAY include:

- `SAME_MODEL_CROSS_INSTANCE_CONVERGENCE`;
- `SAME_MODEL_CROSS_INSTANCE_DIVERGENCE`;
- `CROSS_MODEL_CONVERGENCE`;
- `CROSS_MODEL_DIVERGENCE`.

They MUST NOT be described as proof.

## 9. Session State

### 9.1 Authority

`SESSION_STATE` is the single logical source of truth.

A change made in a derived view MUST be written back to Session State before it is treated as official. In the manual-relay profile, the enclosed Operative Session State Snapshot is authoritative for the receiving turn unless the receiver already holds a newer official state.

Derived views MUST NOT retain independent persistent fields that have no corresponding state location. Temporary presentation fields SHOULD be marked `TRANSIENT` when ambiguity is possible.

### 9.2 Exchange format

Human-facing explanation SHOULD use Markdown. Machine-transferable state MUST use UTF-8 YAML 1.2 restricted to the JSON-compatible subset when YAML is used.

- duplicate mapping keys MUST be rejected;
- tab indentation MUST NOT be used;
- enum values MUST be explicit strings;
- implementations MUST NOT rely on YAML 1.1 implicit booleans such as `YES`, `NO`, `ON`, or `OFF`;
- unsafe-size integer identifiers SHOULD be represented as strings;
- invisible control characters MUST be rejected or reported.

### 9.3 State versioning

For persistent, transferred, or concurrent sessions, the following fields are required:

- `session_id`;
- `state_version`;
- `parent_version`;
- `updated_at`.

A normal update follows:

```text
new.parent_version = old.state_version
new.state_version = old.state_version + 1
```

If the received `parent_version` does not match the current local `state_version`, the state is `DIVERGED`. Automatic overwrite is prohibited.

If multiple successor states share the same parent, treat the session as split-brain. Conflicting decisions MUST NOT be promoted before explicit resolution.

Conflict options:

- `KEEP_LOCAL`;
- `KEEP_RECEIVED`;
- `MERGE`;
- `ABORT_UPDATE`.

A lower `state_version` received through relay MUST be rejected as stale. Timestamps MUST NOT determine state authority, version ordering, or a conflict winner.

### 9.4 Time fields

When an exact clock value is available, time values MUST use RFC 3339. When unavailable, use `UNKNOWN`; do not invent a pseudo-timestamp.

`occurred_at` MAY be `UNKNOWN`. A tool MAY separately record a known `recorded_at` value. Timestamps are audit metadata only and MUST NOT determine approval validity, state authority, version ordering, or conflict resolution.

## 10. Language policy

### 10.1 Canonical artifact language

The default canonical document language is English.

Canonical protocol documents, schemas, YAML keys, enum values, stable identifiers, prompt types, and template IDs SHOULD be English unless the user explicitly selects another canonical language for a repository or project.

Translations MAY be provided under `docs/<ISO-639-1-language-code>/`. Japanese SHOULD use `docs/ja/`, not `docs/jp/`.

Unless explicitly stated otherwise, translations are informative and the canonical version controls in case of conflict.

### 10.2 Interaction language

The facilitator SHOULD select user-facing interaction language using this priority:

1. current explicit user language instruction;
2. `SESSION_STATE.language.interaction`;
3. the user's most recent clear primary natural language;
4. the session's initial primary language;
5. environment default;
6. English.

Code, identifiers, filenames, and short quotations alone MUST NOT trigger a language switch.

User-facing explanations, progress, decisions, errors, and action guides SHOULD use the resolved interaction language. Canonical identifiers MAY remain English.

Participant prompt and response languages MAY differ when doing so improves model performance or source fidelity, but the facilitator SHOULD integrate the result in the user's interaction language.

## 11. Initiation and authorization

Initiation sources:

- `USER_REQUESTED`;
- `FACILITATOR_PROPOSED`;
- `STANDING_AUTHORIZATION`.

Authorization bases:

- `DIRECT_USER_INSTRUCTION`;
- `EXPLICIT_ONE_TIME_APPROVAL`;
- `VALID_STANDING_AUTHORIZATION`.

Defaults:

```text
DEFAULT_START_POLICY: DO_NOT_START
SILENCE_IS_APPROVAL: FALSE
TOPIC_CONTINUATION_IS_APPROVAL: FALSE
DEFAULT_EXECUTION_PERMISSION: PROPOSE_ONLY
```

When the user directly requests deliberation, no additional start approval is required, but limits on external services, cost, sensitive data, and execution permissions remain in force.

A facilitator-proposed deliberation MUST disclose reason, target issue, expected benefit, participants, external services, transferred information, cost, user-operation impact, and proposed budget. It MUST NOT begin before explicit approval unless standing authorization covers it.

### 11.1 Permission requests and grants

A permission request MAY preserve any non-empty action identifier so an unknown operation can be represented without misclassification. Only core actions recognized by the identified protocol version are grantable by default:

- `READ_EXTERNAL`;
- `SEND_EXTERNAL_DATA`;
- `WRITE_FILE`;
- `RUN_COMMAND`;
- `COMMIT`;
- `PUSH`;
- `CREATE_PR`;
- `SEND_MESSAGE`;
- `MODIFY_EXTERNAL_RESOURCE`.

An unknown action MUST be denied and escalated to the user rather than mapped to a similar known action.

A permission request is not a permission grant. Actual authorization MUST be recorded only in `permission_grants`. Request status values are `PENDING`, `DENIED`, `USER_ESCALATION_REQUIRED`, `RESOLVED`, and `WITHDRAWN`; `GRANTED` is not a request status.

An unknown action MAY remain recorded in a permission request, but any action outside the recognized grantable core action set MUST be denied for grant purposes. It MAY be reconsidered only through user escalation or a future protocol version that recognizes the action.

A grant MUST include a non-empty scope with at least `context_id` and `target`. Missing or empty scope means `DENY`. A serialized grant MUST include duration. Grant duration is `ONE_SHOT`, `ISSUE`, or `STANDING`; if the user did not specify duration, the recorder MUST write `ISSUE`. `STANDING` requires explicit scope, a revocation method, and MUST NOT inherit across scopes.

## 12. External services and manual relay

Before using an external service, disclose service or model, information and files to be sent, cost or quota impact, possible storage or training use when known, and required user operation.

The user manually sending prepared content authorizes only that specific transfer. It does not approve the proposal inside the transferred content and does not grant execution permission.

In the manual-relay profile, every cross-chat or cross-service transfer MUST use a `RELAY_BLOCK` containing:

- `session_id`;
- `source_state_version`;
- `target_participant`;
- `purpose`;
- `expected_response`;
- an Operative Session State Snapshot;
- explicit begin and end markers.

The snapshot contains current metadata, session summary, language, usage budget, participants, current issue, current decisions, unresolved or active conditions, permission requests, permission grants, unresolved points, artifacts, and next steps. It excludes full conversation history and obsolete detailed history. The snapshot is the operative source of truth for the receiving turn unless the receiver already holds a newer official state.

Relay identity invariants:

```text
relay_block.session_id = relay_block.operative_session_state_snapshot.meta.session_id
relay_block.source_state_version = relay_block.operative_session_state_snapshot.meta.state_version
```

The receiver MUST reject a relay whose state version is older than the currently held official state. A returned response type MUST match `expected_response`. Any action induced by a relay is evaluated using the originating actor's permission, not automatically using the facilitator's permission.

A user-relay cycle SHOULD be:

1. facilitator emits a purpose-specific `RELAY_BLOCK`;
2. user sends it to the specified destination;
3. participant responds in the expected form;
4. user returns the response;
5. facilitator verifies target, response type, and state version;
6. facilitator integrates only valid results.

## 13. Deliberation modes

### 13.1 Depth

- `MINIMAL`: normally one issue, one participant, one query, one deliberation round;
- `STANDARD`: multiple rounds and richer state management.

### 13.2 Record format

- `COMPACT`: small issues, daily use, short reviews;
- `DETAILED`: long-running, high-risk, multi-issue, development, or complex participation.

Depth and record format are independent.

### 13.3 Daily profile

Recommended defaults:

```text
USE_CASE_PROFILE: DAILY
DELIBERATION_DEPTH: MINIMAL
RECORD_FORMAT: COMPACT
participant_queries.default: 0
participant_queries.maximum: 1
```

### 13.4 Minimal flow

1. bound the issue;
2. minimize Session State;
3. choose one actor able to detect the most important missing perspective;
4. combine related questions into one request;
5. integrate the response;
6. check premises, criteria, conditions, and critical risks;
7. complete facilitator-internal work in the same response;
8. stop or ask the user when appropriate;
9. add another actor, evidence request, or experiment only when a distinct purpose remains.

## 14. Deliberation rounds and turns

A deliberation round begins when the facilitator assigns an issue or question to one or more participants and ends when their answers are available for integration.

The following do not count as deliberation rounds:

- facilitator-internal integration;
- Session State updates;
- presentation of user options;
- user decisions;
- formatting corrections;
- corrective turns caused by an improper earlier stop.

Recommended efficiency metrics:

- `deliberation_rounds`;
- `facilitator_turns`;
- `user_decision_turns`;
- `corrective_turns`;
- `user_relay_actions`;
- `chat_switches`;
- `file_transfers`.

## 15. Turn completion rule

The facilitator MUST continue within the same response when the next actor is the current facilitator and no unavailable user input, participant response, file, evidence, tool result, permission, or safety decision is required.

A response may end only when at least one condition holds:

1. specific user input or decision is required;
2. another participant or chat response is required;
3. a file, source, experiment, or tool result is required;
4. the issue is complete;
5. the issue is blocked;
6. the user defers, rejects, or stops;
7. safety or authorization prevents continuation.

A facilitator MUST NOT leave a non-blocked internal task as the only next action for the user.

## 16. Next-step separation

Internal processing and user action MUST be represented separately when recorded.

Example:

```yaml
next_step:
  internal:
    actor: "FACILITATOR"
    task: "Integrate reviewer findings"
    blocking_input: null
  user:
    action_required: false
    prompt_action: "NO_ACTION_REQUIRED"
    task: null
    response_format: null
```

Completed issue:

```yaml
next_step:
  internal: null
  user:
    action_required: false
    prompt_action: "NO_ACTION_REQUIRED"
    task: null
    response_format: null
```

String values such as `NONE` SHOULD NOT be used in place of null.

## 17. Prompt Action and user guidance

Valid `PROMPT_ACTION` values:

- `REPLY_IN_CURRENT_CHAT`;
- `START_NEW_CHAT`;
- `CONTINUE_EXISTING_CHAT`;
- `JOIN_NEW_PARTICIPANT`;
- `RETURN_RESULT`;
- `TRANSFER_FACILITATOR`;
- `RESOLVE_STATE_CONFLICT`;
- `NO_ACTION_REQUIRED`.

`NO_PROMPT_NEEDED` is deprecated because a prompt may be unnecessary while a user response is still required.

`ACTION_REQUIRED` is separately recorded as `YES` or `NO`.

At the beginning of a user-facing response, the facilitator SHOULD display the action type and whether action is required.

Required protocol output MUST NOT be followed by unrelated platform notices, product promotions, account-setting guidance, advertisements, or links that are not necessary for the issue. When a hosting platform appends such material outside the participant's controllable output, it SHOULD be treated as non-protocol content and excluded from state integration. When a user decision is needed, the detailed decision packet SHOULD appear near the end as one contiguous block.

A decision packet SHOULD contain:

- decision needed;
- why user judgment is required;
- options;
- advantages;
- disadvantages;
- acceptance or decision conditions;
- recommendation when appropriate;
- exact response format.

## 18. User decisions and approval

Supported normalized decisions:

- `APPROVE`;
- `APPROVE_WITH_CONDITIONS`;
- `APPROVE_WITH_CHANGES`;
- `DEFER`;
- `REJECT`.

Clear spelling variants MAY be normalized when intent is unambiguous. Ambiguous decisions MUST NOT be guessed.

### 18.1 Deliberation outcome and approval status

A decision MUST separate participant deliberation from user approval.

`deliberation_outcome` values:

- `OPEN`;
- `CONSENSUS`;
- `CONDITIONAL_CONSENSUS`;
- `EXPERIMENT_CONSENSUS`;
- `USER_DECISION_REQUIRED`;
- `BLOCKED`;
- `REJECTED`.

`approval_status` values:

- `PENDING`;
- `APPROVE`;
- `APPROVE_WITH_CONDITIONS`;
- `APPROVE_WITH_CHANGES`;
- `DEFER`;
- `REJECT`.

A consensus outcome MUST NOT authorize execution. Execution gates read user approval and permission, never deliberation outcome alone.

### 18.2 Decision revision and approval binding

Every decision has a positive integer `revision`. Any change to canonical decision content MUST increment the revision. Revisions are monotonic and MUST NOT be reused.

An approval record MUST be bound to both `decision_id` and `decision_revision`. It is valid only when:

```text
approval.decision_id = decision.id
approval.decision_revision = decision.revision
```

A revision mismatch invalidates the approval and requires renewed user decision. A content digest MAY strengthen this rule where tooling exists but is not required in this draft.

### 18.3 Approval assurance

`assurance_level` values:

- `UNVERIFIED_ASSERTION`;
- `USER_CONFIRMED`;
- `EXTERNALLY_VERIFIED`.

`assurance_origin` values:

- `AI_RECORDED`;
- `USER_ACTION`;
- `VALIDATOR_VERIFIED`.

`UNVERIFIED_ASSERTION` uses `assurance_origin: AI_RECORDED`. `USER_CONFIRMED` uses `assurance_origin: USER_ACTION`. `EXTERNALLY_VERIFIED` uses `assurance_origin: VALIDATOR_VERIFIED` and requires a reference.

An AI participant MAY originate only `UNVERIFIED_ASSERTION`. `USER_CONFIRMED` requires explicit user confirmation in the current operating context. `EXTERNALLY_VERIFIED` requires an independently verifiable record. A schema can require the reference field, but it cannot prove the reference exists or is authentic.

`UNVERIFIED_ASSERTION` MUST NOT authorize external, irreversible, privileged, or permission-escalated execution. A basis or reference describes where the claim came from but does not itself establish assurance.

### 18.4 Decision conditions

A decision condition uses separate applicability and satisfaction fields.

Applicability:

- `ACTIVE`;
- `NOT_APPLICABLE`.

Satisfaction:

- `PENDING`;
- `IN_PROGRESS`;
- `SATISFIED`;
- `WAIVED_BY_USER`;
- `FAILED`.

When applicability is not `ACTIVE`, satisfaction is retained for history but does not satisfy or fail the execution gate. A change from `ACTIVE` to `NOT_APPLICABLE` relaxes a gate and MUST include `applicability_basis`. `SATISFIED` MUST include `basis`. `WAIVED_BY_USER` MUST include both `basis` and `user_confirmation`. The minimum user confirmation records `assurance_level: USER_CONFIRMED` and MAY include a reference.

Condition timing may be `BEFORE_START`, `BEFORE_EXECUTION`, `BEFORE_EXTERNAL_ACTION`, `BEFORE_COMPLETION`, or `ONGOING`.

If an `ONGOING` condition becomes `FAILED`, affected execution MUST block and the matter MUST return to user review. The facilitator MUST NOT automatically rewrite the user's decision as rejected.

### 18.5 Approval forms

`APPROVE` accepts the current decision revision without added conditions.

`APPROVE_WITH_CONDITIONS` accepts the direction while preserving conditions. It MUST NOT be collapsed into unconditional approval.

`APPROVE_WITH_CHANGES` modifies canonical decision content, increments its revision, and requires approval of the resulting revision.

## 19. Decisions, completion, and future scope

Decision conditions belong in `decision_conditions`. Issue or artifact completion criteria belong in `acceptance_conditions`. Deferred items, future directions, and out-of-scope items MUST remain distinct.

A decision is executable only when all applicable gate conditions for the requested action are satisfied or validly waived, approval assurance meets the action's threshold, and a matching permission grant exists.

## 20. Dynamic participation

Participants MAY join, pause, leave, fail, or be removed.

Compact participant statuses:

- `ACTIVE`;
- `PAUSED`;
- `LEFT`;
- `FAILED`;
- `COMPLETED`.

Detailed statuses MAY additionally include:

- `PROPOSED`;
- `AUTHORIZED`;
- `JOINING`;
- `LEAVING`;
- `REMOVED`.

`COMPLETED` means the participant's assigned work is finished and no additional action is expected from that participant unless it is reassigned.

Add a participant only when there is a defined purpose, such as a capability gap, new issue, unassessed critical objection, unavailable current actor, or user instruction.

Do not add participants merely to increase agreement count or produce paraphrases.

## 21. Join isolation

### 21.1 Independent review

Use:

```text
JOIN_MODE: INDEPENDENT_REVIEW
CONTEXT_ISOLATION: C2
```

Provide the issue, goal, fixed requirements, criteria, evidence pack, and restrictions. Do not normally reveal previous conclusions or convergence direction.

### 21.2 Convergence review

Use:

```text
JOIN_MODE: CONVERGENCE_REVIEW
CONTEXT_ISOLATION: C1
```

Provide current decisions, critical objections, open items, and the exact difference to evaluate.

## 22. Leaving and facilitator transfer

There MUST be at most one `ACTIVE` facilitator. Zero active facilitators are allowed during initialization, transfer, blocked recovery, or after completion; normal facilitator work MUST NOT proceed in that state. The schema expresses this with Draft 2020-12 `contains`, `minContains`, and `maxContains`, but older validators may ignore `maxContains`; the semantic invariant remains mandatory.

A user appointment of a facilitator is a facilitator-independent recovery transition and MAY be processed while no facilitator is active.

A transfer MUST use the latest Session State and a `PENDING` transfer record identifying `from`, `to`, and the source state version. Concurrent official state updates are prohibited during transfer. A transfer that would create two active facilitators MUST be rejected. If transfer fails and leaves zero facilitators, user appointment is required.

The incoming facilitator SHOULD confirm protocol and state versions, fixed requirements, decisions and conditions, open issues, participant status, authorization, missing information, conflicts, and next action. A state mismatch MUST be resolved before normal work continues.

## 23. Handoff policy

Default:

```text
HANDOFF_OUTPUT_POLICY: ON_TRANSFER_OR_COMPRESSION
```

Generate a Handoff Capsule or full handoff only when:

- moving to another chat or AI;
- changing facilitator;
- compressing a long context;
- full Session State cannot be transferred;
- preparing recovery state;
- the user requests it.

Do not emit a Handoff Capsule during ordinary same-context progression when it merely duplicates Session State.

Same-context role switching is not a handoff.

## 24. Capability profiles

Capability profiles are optional and on-demand.

Create or update them when:

- role assignment failed;
- a new capability is required;
- tool-access differences matter;
- cost or quota matters;
- the user requests it;
- observed results reveal strengths or limitations.

Observed performance SHOULD be preferred over unsupported self-description.

## 25. Software-development profile

A software issue SHOULD record repository, branch or worktree, base revision, target and related files, acceptance criteria, constraints, prohibited changes, allowed commands, required tests, current failures, rollback method, and write policy.

Generating code alone does not complete an issue. Completion SHOULD consider tests, build, static analysis, security, rollback, and user approval.

### 25.1 Single-writer rule

Default:

```text
MAX_ACTIVE_WRITERS_PER_WORKSPACE: 1
```

Multiple writers are permitted only when work is safely isolated by separate branches, worktrees, repositories, non-overlapping targets, or explicit locking.

### 25.2 Permission escalation

Execution permission MUST be granted per action, issue or session context, target, and duration. File writing, command execution, commits, pushes, pull requests, external communication, and external resource modification MUST NOT be inferred from general approval.

Default boundary:

```text
approval_boundary: PROPOSE_ONLY
```

A relay proposal from a `PROPOSE_ONLY` actor remains a proposal and MUST NOT be laundered into facilitator execution authority.

## 26. Usage budget and escalation

A Usage Budget MAY include:

- `token_limit`: a nonnegative integer or null;
- `cost_limit`: a nonnegative number or null;
- `currency`: a string or null;
- `status`: `AVAILABLE`, `LIMITED`, `EXHAUSTED`, or `UNKNOWN`;
- AI queries;
- deliberation rounds;
- response length;
- user relay actions;
- chat switches;
- file transfers.

Recommended escalation:

1. facilitator analysis;
2. one purpose-selected participant;
3. another participant only if a material unresolved issue remains;
4. evidence, experiment, expert, or user judgment when more AI opinions are not useful.

Budget overrides SHOULD state the reason, expected new information, user-operation impact, and stop condition.

## 27. Stop conditions

Stop or move to user judgment when:

- no material unresolved issue remains;
- execution and acceptance conditions are explicit;
- known critical objections are assessed;
- no additional participant has a distinct purpose;
- the remaining issue is a user value judgment;
- further responses are likely to be paraphrases;
- evidence or experiment is more appropriate;
- the budget or authorization expires;
- the user stops the process.

## 28. Supported deliberation outcomes

`current_issue.status` values are:

- `OPEN`;
- `IN_PROGRESS`;
- `BLOCKED`;
- `COMPLETED`;
- `DEFERRED`.

`decision.deliberation_outcome` values are:

- `OPEN`;
- `CONSENSUS`;
- `CONDITIONAL_CONSENSUS`;
- `EXPERIMENT_CONSENSUS`;
- `USER_DECISION_REQUIRED`;
- `BLOCKED`;
- `REJECTED`.

These states describe the deliberation outcome, not proof of factual truth.

## 29. Prompt completeness

Before sending a compressed participant prompt, check that it contains, as relevant:

- goal;
- task;
- fixed requirements;
- decisions;
- decision conditions;
- open items;
- criteria;
- critical risks;
- restrictions;
- no hidden dependency on prior conversation;
- defined abbreviations;
- protocol version;
- state version.

If decision-critical information is missing, use `ASK_USER`, `BLOCKED`, or `EVIDENCE_REQUIRED` rather than guessing.

## 30. Protocol distribution, loading, and validation

Canonical files MAY be distributed through a version-controlled store. A URL or file reference does not prove the model read it. A loading confirmation SHOULD identify confirmed protocol version, files actually read, access method, unread sections, and formal validation status.

Validation terminology:

- `FORMAL_SCHEMA_VALIDATION`: executed with an identified JSON Schema validator and schema version;
- `SEMANTIC_VALIDATION`: normative cross-object and historical invariants were evaluated;
- `STRUCTURAL_CHECK_ONLY`: apparent keys, types, and structure were inspected without formal execution;
- `NOT_VERIFIED`: neither sufficient structural nor formal validation occurred.

A manual profile without semantic validation MUST NOT claim full semantic conformance unless an equivalent human checklist was executed and recorded.

### 30.1 Normative semantic invariants

At minimum, semantic validation checks:

- duplicate stable identifiers;
- active facilitator count greater than one;
- invalid state lineage or stale relay version;
- relay block session or state version mismatch with the enclosed Operative Session State Snapshot;
- invalid decision-revision approval binding;
- AI-originated assurance above `UNVERIFIED_ASSERTION`;
- external approval reference existence or authenticity not independently verified;
- unverified approval used for privileged or external execution;
- missing or empty permission scope;
- unknown action granted without user escalation;
- invalid condition transitions or missing required basis;
- returned relay response type differing from `expected_response`.

Stable error codes include:

- `DUPLICATE_IDENTIFIER`;
- `MULTIPLE_ACTIVE_FACILITATORS`;
- `STALE_STATE_VERSION`;
- `RELAY_SNAPSHOT_MISMATCH`;
- `INVALID_STATE_LINEAGE`;
- `APPROVAL_REVISION_MISMATCH`;
- `INVALID_ASSURANCE_ORIGIN`;
- `EXTERNAL_REFERENCE_NOT_VERIFIED`;
- `INSUFFICIENT_APPROVAL_ASSURANCE`;
- `EMPTY_PERMISSION_SCOPE`;
- `UNKNOWN_ACTION_DENIED`;
- `CONDITION_BASIS_REQUIRED`;
- `RELAY_RESPONSE_TYPE_MISMATCH`.

### 30.2 Minimum conformance vectors

An implementation claiming semantic validation MUST agree with these vectors:

1. two active facilitators: fail with `MULTIPLE_ACTIVE_FACILITATORS`;
2. approval bound to revision 2 while decision is revision 3: fail with `APPROVAL_REVISION_MISMATCH`;
3. AI-originated `USER_CONFIRMED`: fail with `INVALID_ASSURANCE_ORIGIN`;
4. `ACTIVE` to `NOT_APPLICABLE` without `applicability_basis`: fail with `CONDITION_BASIS_REQUIRED`;
5. unknown permission action: retain the request but deny the grant with `UNKNOWN_ACTION_DENIED`;
6. permission request using `GRANTED`: fail schema validation;
7. relay block whose `session_id` or `source_state_version` differs from its snapshot metadata: fail with `RELAY_SNAPSHOT_MISMATCH`;
8. relay version lower than current official version: fail with `STALE_STATE_VERSION`.

A running session SHOULD lock protocol and schema versions. New repository versions MUST NOT auto-upgrade an active session without a change summary, impact analysis, user approval, and migration where needed.

## 31. Initial canonical repository

The minimum canonical release consists of:

```text
README.md
LICENSE
protocol/MADP-v0.2.5-rc.1.md
protocol/GLOSSARY-v0.2.5-rc.1.md
schemas/session-state-v0.2.5-rc.1.schema.yaml
```

The README is an entry point. Protocol, schema, and glossary versions SHOULD be pinned together for a release. Immutable review references SHOULD use a commit SHA or content-addressed reference rather than a mutable branch or movable tag.

## 32. Known validation limits

This release candidate still requires operational testing for cross-model transfer, relay truncation, concurrent successor states, live facilitator recovery, permission enforcement, large sessions, approval assurance across products, and consistency of semantic validators.

Deferred to v0.3 include mandatory canonical serialization and content digests, cryptographic approval signatures, mandatory immutable external approval anchors, namespaced permission registries, split-brain candidate references, formal Handoff Capsule schema, active-writer lock state, PEP deployment profiles, reference validator implementation, multi-approver quorum, and automatic migration.

## 33. Governing summary

- The user decides.
- Majority alone does not decide.
- AI agreement is not evidence.
- Session State is the single source of truth.
- Share current state, not full history.
- Continue non-blocked facilitator work in the same response.
- Separate internal work from user action.
- Preserve conditional approval as conditional.
- Separate deliberation outcome from user approval.
- Bind approval to the exact decision revision.
- Never permit AI-originated high assurance.
- Treat unknown actions and empty scopes as denied.
- Permit at most one active facilitator.
- Separate canonical artifact language from interaction language.
- Use handoff only for transfer, compression, recovery, or explicit request.
- Add participants only for a defined purpose.
- Stop adding AI opinions when evidence, experiment, expert review, or user judgment is more appropriate.
