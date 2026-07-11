---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Practical guide: one AI model across multiple chats

English | [日本語](../ja/single-model-multi-chat.md)

## Purpose

Use separate chats with the same model to create bounded roles and partially independent contexts. This is useful when only one provider is available but you still want proposer, critic, validator, and facilitator separation.

## What this pattern improves

- reduces immediate conversational anchoring;
- keeps role instructions and evidence scopes separate;
- allows a fresh chat to review an earlier chat's output;
- makes handoffs and context packages explicit;
- costs less operational effort than coordinating several providers.

It does not remove shared-model bias. Treat the chats as context-separated roles, not fully independent experts.

## Suggested chat layout

```text
Chat 1: FACILITATOR / operative state
Chat 2: PROPOSER / solution design
Chat 3: CRITIC / failure analysis
Chat 4: VALIDATOR / evidence and completion checks
```

For smaller tasks, use three chats by combining facilitator and proposer.

## Preparation

1. Create the issue definition in the facilitator chat.
2. Generate a compact context package with a version number.
3. Copy the same package into each participant chat.
4. Add only the participant's role instruction.
5. Require each chat to return a receipt naming the context version it used.

## Context package example

```yaml
context_package:
  id: CTX-ARCH-001
  revision: 2
  goal: "Select a deployment design"
  fixed_requirements:
    - "one existing server"
    - "rollback within five minutes"
  evidence:
    - id: E-01
      statement: "current peak load is 40 requests/second"
      assurance: USER_PROVIDED
  unresolved_questions:
    - "expected load after launch"
  authority:
    allowed: ["analyze", "propose", "review"]
    not_allowed: ["edit", "send", "merge", "publish"]
```

## Role prompts

### Proposer chat

```text
Act as PROPOSER. Produce two feasible options from context package CTX-ARCH-001 revision 2. Compare implementation effort, reliability, and rollback behavior. Do not decide for the user.
```

### Critic chat

```text
Act as CRITIC. Assume the proposal may fail. Identify hidden assumptions, operational failure modes, security issues, and evidence gaps. Return concrete counterexamples and tests.
```

### Validator chat

```text
Act as VALIDATOR. Check each claim against the fixed requirements and supplied evidence. Mark unsupported claims UNVERIFIED. State whether the completion conditions are met.
```

## Workflow

1. Run the proposer without showing critic output.
2. Give the proposal and original context to the critic.
3. Give both responses and the original context to the validator.
4. Return only structured findings to the facilitator chat.
5. Update the operative state and increment its revision.
6. If requirements changed, issue a new context package to every active chat.
7. Ask the user for the actual decision.

## Expected result

The facilitator should produce:

- a comparison of options;
- preserved proposer/critic disagreements;
- evidence status per major claim;
- a recommended next step;
- user decision status;
- TODO items for unresolved work.

## Preventing context drift

- Put the context ID and revision at the top of every message.
- Reject responses based on an older revision when the change is material.
- Do not paste entire conversations between chats.
- Transfer claims, evidence, findings, and decisions in structured form.
- Record which chat produced each finding, but do not treat identity as authority.

## Common failure patterns

- Reusing one chat for several roles without clearing prior instructions.
- Letting the facilitator paraphrase away a critic's severe finding.
- Updating only one participant after a requirement change.
- Assuming a fresh chat is independent of the underlying model.
- Copying a statement such as "approved" without a trusted user action.

## Completion criteria

Finish when every active chat used the same operative revision, material findings were reconciled, the user made or deferred the decision, and implementation or external actions remain separately authorized.