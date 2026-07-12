
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
