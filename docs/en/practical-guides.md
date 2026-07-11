---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADP practical guides

English | [日本語](../ja/practical-guides.md)

Start with [Basic usage](basic-usage.md). Then choose the guide that matches your situation.

| Guide | Purpose | How it is used | Main result | Expected effect |
|---|---|---|---|---|
| [Multiple AI models](multi-model-deliberation.md) | use model diversity for important decisions | assign proposer, critic, validator, and facilitator roles across models | evidence-aware option comparison with preserved disagreement | reduces dependence on one model's framing |
| [One model, multiple chats](single-model-multi-chat.md) | separate roles while using one provider | distribute one versioned context package to several chats | structured findings returned to one facilitator chat | reduces conversational anchoring and context mixing |
| [One model, one chat](single-model-single-chat.md) | run a lightweight session quickly | separate phases and roles inside one conversation | recommendation, unresolved risks, and TODO items | gives the simplest introduction to MADP |
| [AI-driven development](ai-development.md) | control authority across software-development stages | separate analysis, edit, test, review, commit, merge, and release | validated changes plus explicit repository-action boundaries | prevents permission from silently expanding |
| [Context sharing and relay](context-relay.md) | transfer only the operative state | send a bounded context package and require a receipt | reproducible handoff with version and authority information | reduces context drift and obsolete-history reuse |
| [TODO lifecycle](todo-lifecycle.md) | track work without treating it as a decision | create, progress, block, defer, complete, or cancel TODO items | auditable work state and completion basis | makes unfinished work and dependencies visible |
| [Review workflow](review-workflow.md) | obtain independent evidence about quality and risk | issue a scoped review request and disposition each finding | findings, reproduction evidence, remediation status | separates review evidence from approval and merge authority |

## Recommended learning order

1. Basic usage.
2. One model, one chat.
3. One model, multiple chats.
4. Multiple models.
5. Context sharing and relay.
6. TODO lifecycle.
7. Review workflow.
8. AI-driven development when repository or external actions are involved.

## Selecting by risk

- **Low impact and reversible:** one model, one chat.
- **Moderate complexity or role conflict:** one model, multiple chats.
- **High impact, contested evidence, or important review:** multiple models.
- **External or irreversible action:** add authority checks, review, and an explicit user checkpoint regardless of discussion pattern.

## Shared output contract

Every practical workflow should make the following visible:

```yaml
workflow_output:
  issue_and_scope: REQUIRED
  fixed_requirements: REQUIRED
  evidence_and_assumptions: REQUIRED
  alternatives_or_findings: REQUIRED
  unresolved_risks: REQUIRED
  user_decision_status: REQUIRED
  todos: OPTIONAL
  authority_for_next_action: REQUIRED
```

A good workflow does not merely produce a longer answer. It produces clearer boundaries, better evidence, reproducible handoffs, and a safer next action.