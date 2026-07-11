---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Practical guide: deliberation with multiple AI models

English | [日本語](../ja/multi-model-deliberation.md)

## Purpose

Use different AI models as role-separated participants when the decision benefits from diverse training data, reasoning styles, tool access, or failure modes. This pattern is useful for architecture selection, research synthesis, policy comparison, risk analysis, and high-impact reviews.

## Expected benefits

- exposes model-specific assumptions and blind spots;
- reduces dependence on one provider's preferred framing;
- creates stronger adversarial review;
- separates synthesis from source opinions;
- produces auditable disagreement instead of a flattened consensus.

Model diversity is not proof. Agreement still requires evidence.

## Recommended roles

```yaml
participants:
  - id: MODEL-A
    role: PROPOSER
    assignment: "build the strongest feasible recommendation"
  - id: MODEL-B
    role: CRITIC
    assignment: "find failure modes, counterexamples, and hidden costs"
  - id: MODEL-C
    role: VALIDATOR
    assignment: "check evidence quality and fixed requirements"
  - id: FACILITATOR
    role: FACILITATOR
    assignment: "maintain state, compare outputs, preserve disagreements"
```

The facilitator may be another model or the user. It must not give one participant hidden authority over the others.

## Preparation

Create one shared context package containing:

- goal and decision question;
- fixed requirements and exclusions;
- evaluation criteria and weights, if any;
- known facts with source references;
- current decision revision;
- required output format;
- authority explicitly granted and withheld.

Send the same package to every participant. Add role-specific instructions separately.

## Participant prompt template

```text
You are PARTICIPANT [ID] in an MADP deliberation.
Role: [ROLE]
Scope: [ASSIGNMENT]

Use only the supplied context package as operative shared state.
Do not infer user approval, execution permission, or facts not supported by evidence.
Return:
1. position;
2. evidence and assumptions;
3. risks and counterarguments;
4. confidence and uncertainty;
5. questions for other roles;
6. proposed changes to the operative state.
```

## Step-by-step workflow

1. **Independent round.** Each model responds before seeing the others.
2. **Receipt check.** Confirm the protocol version, context revision, and role understood by each participant.
3. **Cross-examination.** Give each model only the relevant competing claims and ask it to challenge or revise its position.
4. **Evidence reconciliation.** Separate factual conflicts, value conflicts, and scope misunderstandings.
5. **Facilitator synthesis.** Build a comparison matrix without using majority vote as the deciding rule.
6. **User checkpoint.** Ask the user to choose, request more evidence, or defer.
7. **Record outcome.** Bind the decision to a revision and convert follow-up work into TODO items.

## Example comparison result

```yaml
deliberation_result:
  options:
    - id: A
      strengths: ["fastest implementation"]
      weaknesses: ["single point of failure"]
      fixed_requirements_met: true
    - id: B
      strengths: ["best fault isolation"]
      weaknesses: ["higher operational complexity"]
      fixed_requirements_met: true
  disagreements:
    - topic: "expected traffic growth"
      type: EVIDENCE_GAP
      positions:
        MODEL-A: "low growth"
        MODEL-B: "uncertain and potentially high"
  recommendation: B
  recommendation_basis:
    - "risk criterion has higher priority than implementation speed"
  user_decision_required: true
```

## Quality controls

- Randomize participant order when possible.
- Do not tell later participants which model produced a claim.
- Require citations or explicit `UNVERIFIED` labels for external facts.
- Preserve minority findings that identify severe risks.
- Use the same evaluation criteria for all options.
- Request a fresh validator after major revisions.

## Failure patterns

- **Consensus cascade:** later models copy the first answer. Prevent it with an independent first round.
- **Model prestige bias:** the facilitator favors a famous model. Compare evidence, not identity.
- **Context drift:** participants receive different requirements. Use versioned context packages and receipts.
- **False independence:** several interfaces use the same underlying model. Record provider/model identity when relevant.
- **Authority leakage:** a participant says "approved" or "ready to merge." Treat it only as an unverified assertion.

## Completion criteria

Finish when the user has a comparison grounded in shared criteria, material disagreements are visible, evidence gaps are either resolved or accepted, and the final action boundary is explicit.