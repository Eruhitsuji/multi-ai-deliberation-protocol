---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Practical guide: one AI model in one chat

English | [日本語](../ja/single-model-single-chat.md)

## Purpose

Use a single chat as a lightweight MADP session when speed and simplicity matter more than independent participants. This pattern is suitable for personal decisions, early planning, brainstorming, requirement clarification, and learning the protocol.

## Benefits and limitations

Benefits:

- no handoff overhead;
- one visible operative state;
- fast iteration with the user;
- easy conversion of conclusions into TODO items.

Limitations:

- participant roles are simulated within one context;
- later reasoning is strongly anchored by earlier messages;
- self-review is weaker than an independent review;
- the model may collapse disagreements too quickly.

## Recommended operating mode

Use explicit phases instead of asking the model to "debate itself" continuously.

```text
Phase 1: issue clarification
Phase 2: independent option generation
Phase 3: critic pass
Phase 4: validator pass
Phase 5: facilitator synthesis
Phase 6: user decision
Phase 7: TODO and next-action recording
```

## Starter prompt

```text
Use a lightweight MADP workflow in this single chat.

Goal: [goal]
Fixed requirements:
- [requirement]
Evaluation criteria:
- [criterion]

Run clearly separated phases. In each phase, label the active role.
Do not revise earlier outputs silently. Preserve material disagreements,
mark unsupported facts UNVERIFIED, and stop before any external action.
The user remains the sole final decision-maker.
```

## Detailed workflow

### 1. Clarify the issue

The facilitator restates the goal, identifies ambiguities, and creates a compact state.

```yaml
operative_state:
  issue: "Choose a backup strategy"
  fixed_requirements:
    - "recovery point objective below 24 hours"
    - "no additional always-on server"
  criteria: [recovery reliability, cost, maintenance effort]
  decision_status: OPEN
```

### 2. Generate options

Ask the model to produce options without evaluating them yet. This reduces premature convergence.

### 3. Run a critic pass

Tell the chat to freeze the option descriptions and inspect failure modes, hidden assumptions, and missing evidence.

### 4. Run a validator pass

Check each option against every fixed requirement. A claim that depends on unknown information should remain `UNVERIFIED`.

### 5. Synthesize

The facilitator creates a comparison table, records minority concerns, and distinguishes a recommendation from a user decision.

### 6. User decision

The user may approve a specific revision, reject it, ask for another cycle, or defer.

### 7. Record follow-up work

Convert unresolved evidence, experiments, or implementation work into TODO items.

## Example final output

```yaml
session_result:
  recommendation:
    revision: 1
    option: "encrypted daily object-storage backup"
    basis:
      - "meets the no-server constraint"
      - "lowest maintenance burden"
  user_decision: PENDING
  unresolved:
    - "restore duration has not been measured"
  todos:
    - id: TODO-001
      title: "run a full restore test"
      status: OPEN
  authority:
    external_action_allowed: false
```

## Techniques that improve quality

- Ask for two or three options before evaluation.
- Insert a visible divider between roles.
- Require the critic to quote the exact claim it challenges.
- Ask the validator to check a requirement matrix row by row.
- Use a fresh chat for final review when the stakes increase.
- Summarize the operative state periodically, but do not delete unresolved findings.

## Common failure patterns

- Role labels change, but the reasoning remains one continuous opinion.
- The model treats its own recommendation as user approval.
- Earlier constraints disappear from later messages.
- A TODO is marked complete because a plan exists, not because evidence exists.
- The chat proceeds from planning to external execution without a new request.

## When to switch to another pattern

Switch to multiple chats or multiple models when the decision is high impact, disagreement is material, evidence is contested, a security or release boundary is involved, or independent review would change user confidence.