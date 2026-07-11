---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Basic usage: choose a MADP workflow

English | [日本語](../ja/basic-usage.md)

> This is the recommended first entry point for new users. It is explanatory; normative rules remain in the versioned protocol, schemas, and registry.

## What MADP helps you do

MADP helps you use one or more AI chats without confusing analysis, decisions, approvals, and execution permission. A typical session produces:

- a clearly stated issue and fixed requirements;
- role-separated analysis;
- explicit assumptions and unresolved risks;
- a decision or recommendation bound to a revision;
- TODO items with lifecycle state;
- review evidence;
- a clear next action and authority boundary.

## Step 1: define the task

Write four items before opening additional chats:

```yaml
goal: "Choose a practical deployment architecture"
fixed_requirements:
  - "Must run on the existing server"
  - "Monthly cost must stay below the stated limit"
evaluation_criteria:
  - reliability
  - implementation effort
  - operating cost
out_of_scope:
  - vendor contract negotiation
```

## Step 2: choose a discussion pattern

| Pattern | Best for | Main benefit | Main cost |
|---|---|---|---|
| [Multiple AI models](multi-model-deliberation.md) | important decisions, model diversity, adversarial review | independent model biases and capabilities | more coordination |
| [One model, multiple chats](single-model-multi-chat.md) | role separation using one service | affordable independence between contexts | same underlying model bias |
| [One model, one chat](single-model-single-chat.md) | quick decisions and learning MADP | simplest operation | weakest independence |

## Step 3: assign minimum roles

Use only the roles needed for the task.

```yaml
roles:
  facilitator: "maintains the operative state and asks focused questions"
  proposer: "develops the strongest practical option"
  critic: "searches for failure modes and unsupported assumptions"
  validator: "checks evidence, constraints, and completion conditions"
```

The facilitator may summarize, but should not erase disagreement.

## Step 4: start with this prompt

```text
Use MADP as an explanatory workflow.

Goal: [goal]
Fixed requirements:
- [requirement]
Evaluation criteria:
- [criterion]
Out of scope:
- [item]

Act as FACILITATOR. Separate proposals, decisions, approvals, TODO items,
reviews, and execution permission. Keep a compact operative state. Do not
claim user approval or execute external actions without an explicit request.
First, restate the issue and propose the minimum participant roles.
```

## Step 5: run one deliberation cycle

1. The facilitator restates the issue and detects missing constraints.
2. Each participant produces an independent position.
3. The critic identifies risks, counterexamples, and missing evidence.
4. The facilitator compares options against the same criteria.
5. The user selects, rejects, defers, or requests another round.
6. The decision is recorded with a revision.
7. Follow-up work becomes TODO items, not implied approval.

## Expected output

```yaml
result:
  recommendation: "Option B"
  decision_status: USER_DECISION_REQUIRED
  decisive_reasons:
    - "meets the fixed deployment constraint"
    - "lowest operating risk"
  rejected_alternatives:
    - option: "Option A"
      reason: "violates the cost limit"
  unresolved_risks:
    - "load test evidence is still missing"
  next_steps:
    - "run a representative load test"
```

## When the session is complete

A useful stopping condition is reached when:

- all fixed requirements are either satisfied or explicitly waived by the user;
- major alternatives have been compared using the same criteria;
- unresolved uncertainty is visible;
- the user has made or deferred the decision;
- any implementation work is represented as TODO items;
- no external action is implied by the discussion result.

## Common mistakes

- Asking several chats to collaborate without giving them the same issue definition.
- Treating majority agreement as proof.
- Letting the facilitator invent user approval.
- Copying full chat histories instead of the operative state.
- Treating a review response as permission to merge, publish, or send.

## Continue with practical guides

After selecting a discussion pattern, use the domain guides for [AI-driven development](ai-development.md), [context sharing](context-relay.md), [TODO lifecycle](todo-lifecycle.md), and [review workflow](review-workflow.md).