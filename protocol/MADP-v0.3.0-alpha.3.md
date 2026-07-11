# Multi-AI Deliberation Protocol v0.3.0-alpha.3

Status: normative implementation draft.

This document extends MADP v0.3.0-alpha.2. Unchanged alpha.2 authority, command, context, TODO, review, and relay rules remain normative.

## 1. Objectives

Alpha.3 adds inclusive and guided deliberation across participants with different capabilities, multiple humans, external AI systems, and support chats. Participation may be permissive, but canonical integration remains strict.

## 2. Operating modes

A `DELIBERATION_PLAN` selects `LIGHT`, `STANDARD`, or `ASSURED`. The facilitator may propose a stricter mode when risk rises and must not silently lower the mode.

## 3. Goal gate

Before substantive deliberation, record the topic, primary goal, central question, final outputs, success criteria, scope, decision authority, and stop conditions. When `goal_gate` is `REQUIRED`, substantive rounds start only after the named human authority confirms the current revision.

## 4. Participant capability and participation modes

Participant types are `HUMAN`, `AI_MODEL`, `AI_ROLE_ACTOR`, `TEAM_PROXY`, and `OBSERVER`. Participation modes are `FULL_CONFORMANCE`, `ASSISTED_CONFORMANCE`, `OPINION_ONLY`, and `OBSERVER`.

A participant that cannot read URLs, files, ZIP archives, YAML, or JSON may still provide bounded free-text opinions. An `OPINION_ONLY` participant may not act as facilitator, canonical state maintainer, approver, veto holder, or executor and may not directly update canonical state.

## 5. Tolerant ingestion and strict canonicalization

For every received response:

1. preserve the raw response;
2. attempt exact parsing;
3. detect the observed format;
4. validate when possible;
5. request simpler reformatting when useful;
6. normalize only sufficiently clear meaning;
7. quarantine ambiguity or accept the contribution as opinion-only when strict normalization is unsafe.

Allowed dispositions are `ACCEPTED_CONFORMANT`, `ACCEPTED_NORMALIZED`, `ACCEPTED_OPINION_ONLY`, `QUARANTINED_AMBIGUOUS`, `REJECTED_UNUSABLE`, and `STALE_RESPONSE`.

Normalization must not invent approval, execution permission, evidence, citations, confidence, identity, or a stronger claim.

## 6. Plain relay

A `PLAIN_RELAY_PACKET` contains a concise topic, bounded role, context summary, questions, prohibited inferences, and a requested natural-language response format. It is `PROPOSE_ONLY` and grants no canonical or execution authority.

## 7. Adaptive roles

Roles are temporary analytical functions, not permanent personas. Their lifecycle is `PROPOSED`, `ACTIVE`, `PAUSED`, `RETIRED`, or `REASSIGNED`.

The facilitator may adapt analytical roles and must record the reason and role budget. It must not independently change facilitator authority, decision owners, approvers, veto authority, execution authority, or the confirmed goal. Multiple roles in one model and chat remain one independence group.

## 8. Claim ledger

Material assertions are typed as `FACT`, `SOURCE_CLAIM`, `MODEL_INFERENCE`, `PROPOSAL`, or `OPINION`, with importance, provenance, verification status, contradictions, and decision usability. High or critical unverified factual claims cannot be the sole basis of an approved decision.

## 9. Multi-human team deliberation

Decision methods are `SINGLE_DECISION_OWNER`, `NAMED_APPROVERS`, `UNANIMOUS`, `MAJORITY`, `CONSENT_BASED`, `ADVISORY_ONLY`, and `EXTERNAL_GOVERNANCE`.

Silence never counts as consent. Direct and relayed statements are distinguished. Organizational, deliberation, and authority roles are separate. Material dissent is preserved. Private input is not shared, relayed, or recorded without permission. Asynchronous comments identify the state revision reviewed.

## 10. Minutes and records

`SESSION_MINUTES` are separate from canonical state. Status values are `AUTO_GENERATED_DRAFT`, `HUMAN_REVIEW_PENDING`, `HUMAN_REVIEWED`, `APPROVED_RECORD`, and `SUPERSEDED`. Detail levels are `QUICK`, `STANDARD`, and `AUDIT`.

Minutes distinguish discussion summaries, proposals, approved decisions and approvers, dissent, unresolved points, action items, claim references, redactions, and limitations. AI-generated minutes remain drafts until the applicable human review policy is satisfied.

## 11. Help assistant

A MADP Help assistant may explain protocol, diagnose workflow problems, generate copyable prompts, and propose repairs. It may not claim a proposed repair was applied, approve decisions, change canonical state, or execute external actions. It must not assume access to another chat without a supplied `HELP_CONTEXT_PACKET`.

In-session help pauses substantive progression without adding the help exchange as claims or decisions. `RESUME` returns to the prior phase.

## 12. User navigation

A user-facing pause is allowed only for a required human decision, missing required information, an external relay or response, a safety or authority boundary, materially different paths, or a budget boundary. Ending an internal round alone is not a valid pause reason.

Every valid pause emits a `NEXT_ACTION_CARD` that states the current location, responsible actor, one primary action, accepted inputs, what happens next, and alternatives such as skip, help, or end.

## 13. Round types

Rounds may be `DIVERGENCE`, `CRITIQUE`, `EVIDENCE_COLLECTION`, `RECONCILIATION`, or `DECISION_PREPARATION`. Use the smallest useful set of active roles.

## 14. Skill adapters

ChatGPT instructions, Claude Skills, and generic bootstrap prompts are informative adapters and do not override normative protocol artifacts. Adapters expose tool capabilities, default to `PROPOSE_ONLY`, and are checked for version drift.

## 15. Conformance

Alpha.3 conformance requires raw-response preservation, no authority escalation during normalization, capability-aware role assignment, team authority and dissent preservation, concrete next-action guidance, separation of minutes and canonical state, and explicit limitations when tools or validation were unavailable.
