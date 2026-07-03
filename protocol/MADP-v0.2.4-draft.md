# Multi-AI Deliberation Protocol v0.2.4-draft

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
- **Derived View**: a presentation, prompt, roster, issue card, or handoff generated from Session State.

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

A change made in a derived view MUST be written back to Session State before it is treated as an official state change.

Derived views MUST NOT retain independent persistent fields that have no corresponding state location. Temporary presentation fields SHOULD be marked `TRANSIENT` when ambiguity is possible.

### 9.2 Exchange format

Human-facing explanation SHOULD use Markdown. Machine-transferable current state SHOULD use YAML conforming to `schemas/session-state.schema.yaml` when possible.

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

If multiple successor states share the same parent, treat the session as split-brain. Conflicting decisions MUST NOT be promoted to final state before resolution.

Conflict options:

- `KEEP_LOCAL`;
- `KEEP_RECEIVED`;
- `MERGE`;
- `ABORT_UPDATE`.

### 9.4 Time fields

When an exact clock value is available, `updated_at` MUST use RFC 3339.

When exact time is unavailable, use:

```yaml
updated_at: "UNKNOWN"
```

Do not invent a partial pseudo-timestamp. Optional date or timezone context MAY be stored separately and MUST NOT be used for version ordering.

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
```

When the user directly requests deliberation, no additional start approval is required, but the facilitator MUST still respect limits on external services, cost, sensitive data, and execution permissions.

A facilitator-proposed deliberation MUST disclose:

- reason;
- target issue;
- expected benefit;
- participants or roles;
- external services;
- information to send;
- cost or usage impact;
- user-operation impact;
- proposed budget.

It MUST NOT begin before explicit approval unless valid standing authorization covers it.

## 12. External services and relay

Before using an external service, disclose:

- service or model;
- information and files to be sent;
- cost or quota impact;
- possible storage or training use when known;
- required user operation.

In `USER_RELAY`, the user manually sending the prepared content may serve as approval for that specific transfer.

A user-relay cycle SHOULD be:

1. facilitator generates a purpose-specific prompt;
2. user sends it to the specified destination;
3. participant responds;
4. user returns the response;
5. facilitator verifies state version and integrates the result;
6. facilitator generates another prompt only if needed.

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

At the beginning of a user-facing response, the facilitator SHOULD display the action type and whether action is required. When a user decision is needed, the detailed decision packet SHOULD appear near the end as one contiguous block.

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

Clear spelling variants MAY be normalized when the intent is unambiguous. Ambiguous decisions MUST NOT be guessed.

### 18.1 Approve

The proposal is approved without modification or additional conditions.

### 18.2 Approve with conditions

The proposal's basic direction is approved, but specified conditions must be preserved and satisfied according to their timing. Conditional approval MUST NOT be collapsed into unconditional approval.

A decision condition MUST separate **applicability** from **satisfaction**.

Condition applicability values are:

- `ACTIVE`: the condition currently applies;
- `INACTIVE`: the condition exists but does not currently apply;
- `NOT_APPLICABLE`: the condition does not apply to this decision or lifecycle.

Condition satisfaction values are:

- `PENDING`: fulfillment has not started or cannot yet be evaluated;
- `IN_PROGRESS`: fulfillment is currently being worked on or continuously maintained;
- `SATISFIED`: fulfillment is complete;
- `WAIVED_BY_USER`: the user explicitly waived the condition;
- `FAILED`: the condition was violated or cannot be fulfilled.

`ADOPTED` MUST NOT be used as a condition satisfaction value. Adoption is represented by the parent decision, approval provenance, or both.

An `ONGOING` condition normally remains `applicability: ACTIVE` and `satisfaction: IN_PROGRESS` until its applicable lifecycle ends. A future guard condition that cannot yet be evaluated normally remains `satisfaction: PENDING`.

Condition timing may be:

- `BEFORE_START`;
- `BEFORE_EXECUTION`;
- `BEFORE_EXTERNAL_ACTION`;
- `BEFORE_COMPLETION`;
- `ONGOING`.

An approval condition is **compatible** when it:

- does not contradict the selected proposal;
- does not materially change comparison with rejected options;
- does not introduce a new critical risk;
- does not expand cost, authority, or data sharing beyond authorization;
- can be represented as a decision, acceptance, deferred, or future condition.

Compatible conditions MAY be integrated in the same facilitator turn without another user confirmation.

A condition is **decision-changing** when it materially alters the proposal, option comparison, cost, authority, external data sharing, or critical risk. Decision-changing conditions require impact analysis and user reconfirmation.

Ambiguous or unsatisfiable conditions MUST NOT be silently converted into unconditional approval.

### 18.3 Approve with changes

The proposal itself is modified. The modified proposal becomes the approved decision only after the requested changes are interpreted and, where material ambiguity exists, reconfirmed.

## 19. Decisions, completion, and future scope

### 19.1 Decision conditions

Conditions without which a decision would be incomplete or invalid SHOULD be stored in `decision_conditions`. Each structured decision condition MUST include `applicability` and `satisfaction`.

A completed decision process does not necessarily mean that all ongoing conditions are closed. When this distinction matters, the decision SHOULD record:

```yaml
lifecycle:
  decision_process: "COMPLETED"
  condition_monitoring: "ACTIVE"
```

`decision_process` values are `IN_PROGRESS` and `COMPLETED`. `condition_monitoring` values are `NOT_REQUIRED`, `ACTIVE`, `CLOSED`, and `BLOCKED`.

Long procedures or evidence SHOULD be kept outside the current state and referenced through `evidence_refs` rather than copied into every state snapshot.

### 19.2 Acceptance conditions

Issue or artifact completion criteria SHOULD be stored in `acceptance_conditions`.

### 19.3 Deferred items

A deferred item has been considered but intentionally postponed. It SHOULD include a reason and, where possible, `reconsider_when` triggers.

### 19.4 Future direction

A future direction is a possible future path that is not yet an implementation commitment.

### 19.5 Out of scope

An out-of-scope item is not decided by the current issue.

Current decisions, deferred items, future directions, and out-of-scope items MUST NOT be conflated.

## 20. Dynamic participation

Participants MAY join, pause, leave, fail, or be removed.

Compact participant statuses:

- `ACTIVE`;
- `PAUSED`;
- `LEFT`;
- `FAILED`.

Detailed statuses MAY additionally include:

- `PROPOSED`;
- `AUTHORIZED`;
- `JOINING`;
- `LEAVING`;
- `REMOVED`.

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

A separate leave packet is optional. Use one only when unresolved work, unintegrated evidence, material objections, or handoff warnings remain.

A facilitator transfer MUST use the latest Session State. The incoming facilitator SHOULD confirm:

- protocol version;
- state version;
- fixed requirements;
- decisions and conditions;
- open issues;
- participant status;
- authorization;
- missing information;
- detected conflicts;
- next action.

A state mismatch MUST be resolved before normal work continues.

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

A software issue SHOULD record, when relevant:

- repository;
- branch or worktree;
- base revision;
- target and related files;
- acceptance criteria;
- constraints;
- prohibited changes;
- allowed commands;
- required tests;
- current failures;
- rollback method;
- write policy.

Generating code alone does not complete an issue. Completion SHOULD consider tests, build, static analysis, security, rollback, and user approval.

### 25.1 Single-writer rule

Default:

```text
MAX_ACTIVE_WRITERS_PER_WORKSPACE: 1
```

Multiple writers are permitted only when work is safely isolated by separate branches, worktrees, repositories, non-overlapping targets, or explicit locking.

### 25.2 Permission escalation

Execution permission MUST be granted per issue and scope. File writing, command execution, commits, pushes, pull requests, and external resource modification SHOULD be separately authorized.

Default boundary:

```text
approval_boundary: PROPOSE_ONLY
```

## 26. Usage budget and escalation

A Usage Budget MAY include:

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

## 28. Consensus states

Supported issue states include:

- `CONSENSUS`;
- `CONDITIONAL_CONSENSUS`;
- `EXPERIMENT_CONSENSUS`;
- `USER_DECISION_REQUIRED`;
- `OPEN`;
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

## 30. Protocol distribution and loading

Canonical files MAY be distributed through GitHub, GitLab, Codeberg, internal Git, or another version-controlled store.

A URL or file reference does not prove the model read it. A loading confirmation SHOULD identify:

- confirmed protocol version;
- canonical file read;
- major rules understood;
- unread or unavailable sections;
- template or schema used.

A running session SHOULD lock its protocol version. New repository versions MUST NOT auto-upgrade an active session without a change summary, impact analysis, user approval, and state migration where needed.

## 31. Initial canonical repository

The minimum canonical release consists of:

```text
README.md
LICENSE
protocol/MADP-v0.2.4-draft.md
schemas/session-state.schema.yaml
```

The README remains an entry point. If the repository grows, detailed file listings SHOULD move to an index or manifest that distinguishes required, optional, current, historical, and deprecated files.

## 32. Known validation limits

At v0.2.4-draft, the following areas may require further testing:

- cross-model Session State transfer;
- YAML damage or omission tolerance;
- concurrent successor states and conflict resolution;
- live facilitator transfer;
- coding-agent permission enforcement;
- single-writer operation;
- loading canonical files from a hosted repository;
- beginning from Protocol Capsule alone;
- large, multi-issue, multi-participant sessions.

## 33. Governing summary

- The user decides.
- Majority alone does not decide.
- AI agreement is not evidence.
- Session State is the single source of truth.
- Share current state, not full history.
- Continue non-blocked facilitator work in the same response.
- Separate internal work from user action.
- Preserve conditional approval as conditional.
- Separate canonical artifact language from interaction language.
- Use handoff only for transfer, compression, recovery, or explicit request.
- Add participants only for a defined purpose.
- Stop adding AI opinions when evidence, experiment, expert review, or user judgment is more appropriate.
