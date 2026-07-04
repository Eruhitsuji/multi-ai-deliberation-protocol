# MADP Normative Glossary

> Applies to: **MADP v0.2.5-rc.1**

This glossary defines canonical operational meanings used by the Multi-AI Deliberation Protocol. Its purpose is to reduce interpretation drift across AI models, users, validators, and implementations.

## Interpretation rules

- A term marked **Normative: Yes** has the meaning defined here when used by MADP.
- The protocol document controls mandatory behavior. The schema controls machine-validatable structure, required fields, and enum spelling.
- A conflict among the schema, protocol, and this glossary is a specification defect and MUST be reported.
- Translations MAY explain a canonical term but MUST NOT redefine it.
- Canonical terms, YAML keys, enum values, prompt actions, and stable identifiers retain their exact English spelling.
- Informal synonyms MAY be used in user-facing prose only when they do not change the canonical meaning.

## User

**Canonical term:** `USER`  
**Category:** Actor  
**Normative:** Yes

**Definition:** The sole final decision-maker for the session. A facilitator, participant, vote, or model consensus cannot replace explicit user authority.

**Not equivalent to:** requester relay, facilitator, majority, model consensus.

**Related terms:** `FACILITATOR`, `approval`, `user decision`.

## Facilitator

**Canonical term:** `FACILITATOR`  
**Category:** Actor  
**Normative:** Yes

**Definition:** The actor responsible for maintaining `SESSION_STATE`, bounding issues, managing participation and authorization, integrating results, detecting divergence, and identifying the next action.

**Required behavior:** The facilitator has no final decision authority and MUST preserve user decisions and conditions.

**Not equivalent to:** user, final approver, independent reviewer.

## Participant

**Canonical term:** `PARTICIPANT`  
**Category:** Actor  
**Normative:** Yes

**Definition:** An actor assigned a bounded deliberation, review, validation, or execution purpose.

**Canonical status values:** `PROPOSED`, `AUTHORIZED`, `JOINING`, `ACTIVE`, `PAUSED`, `LEAVING`, `LEFT`, `REMOVED`, `FAILED`, `COMPLETED`.

**Required behavior:** A participant MUST NOT be added merely to increase agreement count or produce paraphrases.

**Status note:** `COMPLETED` means the participant's assigned work is finished and no additional action is expected from that participant unless it is reassigned.

## Role Actor

**Canonical term:** `ROLE_ACTOR`  
**Category:** Actor  
**Normative:** Yes

**Definition:** A role performed within the same model context as another role.

**Required behavior:** A Role Actor does not increase review independence and is not independent evidence.

**Not equivalent to:** separated model instance, external validator.

## Session State

**Canonical term:** `SESSION_STATE`  
**Category:** State management  
**Normative:** Yes

**Definition:** The single logical source of truth for the current MADP session.

**Required behavior:** A change in a prompt, issue card, roster, report, or handoff is not official until written back to `SESSION_STATE`.

## Derived View

**Canonical term:** `Derived View`  
**Category:** State management  
**Normative:** Yes

**Definition:** A presentation, prompt, issue card, roster, ledger, progress view, or handoff generated from `SESSION_STATE`.

**Not equivalent to:** an independent persistent source of truth.

## Official State

**Canonical term:** `official state`  
**Category:** State management  
**Normative:** Yes

**Definition:** The latest non-diverged state accepted as authoritative for the session.

**Required behavior:** An unresolved candidate state MUST NOT replace the official state.

## Candidate State

**Canonical term:** `candidate state`  
**Category:** State management  
**Normative:** Yes

**Definition:** A proposed successor state that has not yet been accepted or promoted as the official state.

## State Version

**Canonical term:** `state_version`  
**Category:** State management  
**Normative:** Yes

**Definition:** The sequence number assigned to a state snapshot within one `session_id`.

**Required behavior:** A normal successor increments the previous `state_version` by one.

## Parent Version

**Canonical term:** `parent_version`  
**Category:** State management  
**Normative:** Yes

**Definition:** The `state_version` from which the current state claims to have been derived.

**Required behavior:** For a normal update, `new.parent_version = old.state_version`.

## Common Ancestor

**Canonical term:** `common ancestor`  
**Category:** State management  
**Normative:** Yes

**Definition:** The latest official state from which two or more candidate states descend.

## Diverged

**Canonical term:** `DIVERGED`  
**Category:** State management  
**Normative:** Yes

**Definition:** A state relationship in which the received lineage does not match the currently authoritative lineage, or competing successor states cannot be treated as one sequential update.

**Required behavior:** Automatic overwrite is prohibited until resolution.

## Split-brain

**Canonical term:** `split-brain`  
**Category:** State management  
**Normative:** Yes

**Definition:** Two or more materially different candidate states for the same session that declare the same parent state.

**Required behavior:** No candidate may be automatically promoted, overwritten, or mechanically merged before explicit conflict resolution.

**Not equivalent to:** identical copies, a stale state, a normal sequential update.

**Example:** Candidate A and Candidate B both use `parent_version: 4` and `state_version: 5`, but contain conflicting decisions.

## Merge

**Canonical term:** `MERGE`  
**Category:** State management  
**Normative:** Yes

**Definition:** An explicit conflict-resolution operation that constructs a successor from selected content in multiple diverged states.

**Required behavior:** Material conflicting fields require an explicit resolution basis. A merge is not permission to silently combine incompatible decisions.

## Promotion

**Canonical term:** `promotion`  
**Category:** State management  
**Normative:** Yes

**Definition:** Acceptance of a candidate state as the new official state.

## Proposal

**Canonical term:** `proposal`  
**Category:** Decision  
**Normative:** Yes

**Definition:** A candidate direction, design, action, or resolution presented for evaluation or approval.

## Approve

**Canonical term:** `APPROVE`  
**Category:** Decision  
**Normative:** Yes

**Definition:** The proposal is accepted without modification or additional conditions.

## Approve with Conditions

**Canonical term:** `APPROVE_WITH_CONDITIONS`  
**Category:** Decision  
**Normative:** Yes

**Definition:** The proposal's basic direction is accepted, while execution, adoption, or completion remains subject to preserved conditions.

**Required behavior:** It MUST NOT be collapsed into unconditional approval.

**Not equivalent to:** `APPROVE_WITH_CHANGES`.

## Approve with Changes

**Canonical term:** `APPROVE_WITH_CHANGES`  
**Category:** Decision  
**Normative:** Yes

**Definition:** The proposal itself is modified as part of approval.

**Not equivalent to:** adding execution or completion conditions to an otherwise unchanged proposal.

## Compatible Approval Condition

**Canonical term:** `COMPATIBLE_APPROVAL_CONDITION`  
**Category:** Decision  
**Normative:** Yes

**Definition:** A condition that preserves the selected proposal's basic direction and does not materially alter option comparison, authority, cost, data sharing, or critical risk.

**Required behavior:** It MAY be integrated without another confirmation when its meaning is clear.

## Decision-changing Approval Condition

**Canonical term:** `DECISION_CHANGING_APPROVAL_CONDITION`  
**Category:** Decision  
**Normative:** Yes

**Definition:** A proposed condition that materially changes the proposal, comparison among options, cost, authority, data sharing, or critical risk.

**Required behavior:** Impact analysis and user reconfirmation are required.

## Decision Condition

**Canonical term:** `decision condition`  
**Category:** Condition  
**Normative:** Yes

**Definition:** A condition attached to a user's approval or decision.

**Not equivalent to:** an artifact acceptance criterion.

## Acceptance Condition

**Canonical term:** `acceptance condition`  
**Category:** Condition  
**Normative:** Yes

**Definition:** A criterion used to determine whether an issue, output, implementation, or artifact meets its completion standard.

## Applicability

**Canonical term:** `applicability`  
**Category:** Condition  
**Normative:** Yes

**Definition:** Whether a decision condition currently applies.

**Canonical values:** `ACTIVE`, `NOT_APPLICABLE`.

**Required behavior:** Changing from `ACTIVE` to `NOT_APPLICABLE` relaxes a gate and requires `applicability_basis`.

## Satisfaction

**Canonical term:** `satisfaction`  
**Category:** Condition  
**Normative:** Yes

**Definition:** The fulfillment state of a decision condition.

**Canonical values:** `PENDING`, `IN_PROGRESS`, `SATISFIED`, `WAIVED_BY_USER`, `FAILED`.

**Required behavior:** `SATISFIED` requires `basis`. `WAIVED_BY_USER` requires both `basis` and `user_confirmation`.

## Deliberation Round

**Canonical term:** `deliberation round`  
**Category:** Deliberation  
**Normative:** Yes

**Definition:** A cycle that begins when the facilitator assigns a bounded question to one or more participants and ends when their answers are available for integration.

**Not equivalent to:** facilitator-only integration, state update, user decision, formatting correction, or corrective turn.

## Review Independence

**Canonical term:** `Review Independence`  
**Category:** Review profile  
**Normative:** Yes

**Definition:** A configuration label describing separation among reviewing actors, from `I0` through `I3`. It does not measure correctness.

## Evidence Level

**Canonical term:** `Evidence Level`  
**Category:** Review profile  
**Normative:** Yes

**Definition:** A label describing external support and verification, from `E0` through `E3`.

**Required behavior:** Agreement among AI systems does not by itself increase Evidence Level.

## Context Isolation

**Canonical term:** `Context Isolation`  
**Category:** Review profile  
**Normative:** Yes

**Definition:** A label describing how much previous analysis or conclusion is shared with a participant, from `C0` through `C3`.

## Handoff

**Canonical term:** `handoff`  
**Category:** Transfer  
**Normative:** Yes

**Definition:** Transfer of current work or responsibility to another chat, context, model, facilitator, or recovery process.

**Required behavior:** Ordinary same-context progression is not a handoff.

## Handoff Capsule

**Canonical term:** `Handoff Capsule`  
**Category:** Transfer  
**Normative:** Yes

**Definition:** A compressed transfer artifact containing the minimum current information needed when full `SESSION_STATE` cannot or should not be transferred.

## Same-context Role Switch

**Canonical term:** `same-context role switch`  
**Category:** Transfer  
**Normative:** Yes

**Definition:** A role change within the same model context.

**Required behavior:** It is not a handoff and does not increase review independence.

## Cross-model Transfer

**Canonical term:** `cross-model transfer`  
**Category:** Transfer  
**Normative:** Yes

**Definition:** Transfer of a role or facilitator responsibility to a different model context.

**Required behavior:** Current state and version lineage must be verified before normal work continues.

## Prompt Action

**Canonical term:** `PROMPT_ACTION`  
**Category:** User interaction  
**Normative:** Yes

**Definition:** The standardized action type indicating where or how the next required interaction occurs.

**Canonical values:** `REPLY_IN_CURRENT_CHAT`, `START_NEW_CHAT`, `CONTINUE_EXISTING_CHAT`, `JOIN_NEW_PARTICIPANT`, `RETURN_RESULT`, `TRANSFER_FACILITATOR`, `RESOLVE_STATE_CONFLICT`, `NO_ACTION_REQUIRED`.

## Action Required

**Canonical term:** `ACTION_REQUIRED`  
**Category:** User interaction  
**Normative:** Yes

**Definition:** A separate yes/no indication of whether the user must act now. It is not inferred solely from `PROMPT_ACTION`.

## Propose Only

**Canonical term:** `PROPOSE_ONLY`  
**Category:** Software operation  
**Normative:** Yes

**Definition:** The default authorization boundary under which an actor may analyze and propose changes but may not modify files, run unauthorized commands, commit, push, open pull requests, or alter external resources.

## Active Writer

**Canonical term:** `active writer`  
**Category:** Software operation  
**Normative:** Yes

**Definition:** An actor currently authorized to modify a particular workspace or overlapping target.

**Required behavior:** The default maximum is one active writer per workspace unless isolation or locking makes concurrent writing safe.

## Formal Schema Validation

**Canonical term:** `FORMAL_SCHEMA_VALIDATION`  
**Category:** Validation  
**Normative:** Yes

**Definition:** Execution of an actual JSON Schema validator against an identified schema version and instance.

**Required behavior:** A result may be described as validation `PASSED` only when the validator completed successfully with no validation errors.

## Structural Check Only

**Canonical term:** `STRUCTURAL_CHECK_ONLY`  
**Category:** Validation  
**Normative:** Yes

**Definition:** Inspection of apparent keys, values, types, and structure without executing an actual JSON Schema validator.

**Required behavior:** It MUST NOT be reported as formal schema validation or as validation `PASSED`.

## Majority Vote Alone Is Insufficient

**Canonical term:** `majority_vote_alone_is_insufficient`  
**Category:** Decision rule  
**Normative:** Yes

**Definition:** A proposal cannot be accepted solely because more participants support it. Material minority objections must still be addressed.

**Avoid:** `majority_vote_disabled`, because it may be misread as a complete prohibition of voting.


## Deliberation Outcome

**Canonical term:** `deliberation_outcome`  
**Category:** Decision  
**Normative:** Yes

**Definition:** The result of participant deliberation independently of whether the user approved it.

**Canonical values:** `OPEN`, `CONSENSUS`, `CONDITIONAL_CONSENSUS`, `EXPERIMENT_CONSENSUS`, `USER_DECISION_REQUIRED`, `BLOCKED`, `REJECTED`.

**Required behavior:** It MUST NOT by itself authorize execution.

## Approval Status

**Canonical term:** `approval_status`  
**Category:** Decision  
**Normative:** Yes

**Definition:** The user's disposition toward a specific decision revision.

**Canonical values:** `PENDING`, `APPROVE`, `APPROVE_WITH_CONDITIONS`, `APPROVE_WITH_CHANGES`, `DEFER`, `REJECT`.

## Current Issue Status

**Canonical term:** `current_issue.status`
**Category:** Issue
**Normative:** Yes

**Canonical values:** `OPEN`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `DEFERRED`.

**Definition:** The workflow state of the current issue. It is separate from `decision.deliberation_outcome`.

## Decision Revision

**Canonical term:** `decision revision`  
**Category:** Decision  
**Normative:** Yes

**Definition:** A positive, monotonic identifier for canonical decision content. Any canonical content change creates a new revision.

## Approval Assurance

**Canonical term:** `assurance_level`  
**Category:** Authorization  
**Normative:** Yes

**Canonical values:** `UNVERIFIED_ASSERTION`, `USER_CONFIRMED`, `EXTERNALLY_VERIFIED`.

**Required behavior:** AI participants may originate only `UNVERIFIED_ASSERTION`. Unverified assertions do not authorize external, irreversible, privileged, or permission-escalated execution.

## Assurance Origin

**Canonical term:** `assurance_origin`
**Category:** Authorization
**Normative:** Yes

**Canonical values:** `AI_RECORDED`, `USER_ACTION`, `VALIDATOR_VERIFIED`.

**Required behavior:** `UNVERIFIED_ASSERTION` uses `AI_RECORDED`; `USER_CONFIRMED` uses `USER_ACTION`; `EXTERNALLY_VERIFIED` uses `VALIDATOR_VERIFIED` and requires a reference. Schema can require the reference field but cannot prove reference existence or authenticity.

## Operative Session State Snapshot

**Canonical term:** `Operative Session State Snapshot`  
**Category:** Relay  
**Normative:** Yes

**Definition:** A bounded snapshot containing the current state required for the receiving turn, excluding full conversation history and obsolete detailed history.

**Required contents:** `meta`, `session`, `language`, `usage_budget`, `participants`, `current_issue`, `decisions`, `conditions`, `permission_requests`, `permission_grants`, `unresolved_points`, `artifacts`, and `next_step`.

**Required behavior:** The snapshot is the operative source of truth for the receiving turn unless the receiver already holds a newer official state.

## Relay Block

**Canonical term:** `RELAY_BLOCK`  
**Category:** Relay  
**Normative:** Yes

**Definition:** The manual-profile transport envelope containing relay metadata and an Operative Session State Snapshot.

**Required behavior:** `relay_block.session_id` must equal `operative_session_state_snapshot.meta.session_id`, and `relay_block.source_state_version` must equal `operative_session_state_snapshot.meta.state_version`.

## Permission Request

**Canonical term:** `permission request`  
**Category:** Authorization  
**Normative:** Yes

**Definition:** A request naming an intended action and scope. Unknown action identifiers may be retained as requests but are denied by default.

**Canonical status values:** `PENDING`, `DENIED`, `USER_ESCALATION_REQUIRED`, `RESOLVED`, `WITHDRAWN`.

**Required behavior:** A permission request is not a permission grant. `GRANTED` is not a request status, and actual authorization is recorded only in `permission_grants`.

## Permission Grant

**Canonical term:** `permission grant`  
**Category:** Authorization  
**Normative:** Yes

**Definition:** Explicit authorization for a recognized action, non-empty scope, and defined duration.

**Canonical action values:** `READ_EXTERNAL`, `SEND_EXTERNAL_DATA`, `WRITE_FILE`, `RUN_COMMAND`, `COMMIT`, `PUSH`, `CREATE_PR`, `SEND_MESSAGE`, `MODIFY_EXTERNAL_RESOURCE`.

**Canonical duration values:** `ONE_SHOT`, `ISSUE`, `STANDING`.

**Required behavior:** Unknown actions are not grantable by default. A serialized grant MUST include duration; when the user does not specify duration, the recorder writes `ISSUE`.

## Usage Budget

**Canonical term:** `usage_budget`
**Category:** Budget
**Normative:** Yes

**Definition:** A structured limit or availability record for model usage, cost, and related operational budget.

**Canonical status values:** `AVAILABLE`, `LIMITED`, `EXHAUSTED`, `UNKNOWN`.

## Semantic Validation

**Canonical term:** `SEMANTIC_VALIDATION`  
**Category:** Validation  
**Normative:** Yes

**Definition:** Evaluation of normative cross-object, authority, lineage, and historical invariants that JSON Schema alone does not establish.
