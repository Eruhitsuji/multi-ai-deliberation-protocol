# MADP v0.3.0-alpha.3 Dynamic Role Assignment

Status: experimental planning profile. It creates an advisory role plan and never grants approval or execution authority.

## Purpose

Create a deterministic starting plan from the AI services and chat contexts actually available to the human operator. The planner considers capability, availability, usage preference, cost mode, independence group, and known correlation.

It does not claim that a vendor, model family, separate chat, or retrieval source is globally independent.

## Roles

The initial planner supports:

- `FACILITATOR`
- `PROPOSER`
- `CRITIC`
- `EVIDENCE_REVIEWER`
- `RECORDER`

All assignments remain `PROPOSE_ONLY`, `OPINION_ONLY`, or `RECORD_ONLY`. Human Final Authority remains mandatory.

## Blind First Round

When Blind First Round is required, the planner first tries to select the requested number of generation-capable services from distinct, non-correlated independence groups.

If it cannot, it may return a useful degraded plan:

```yaml
status: DEGRADED
blind_first_round:
  status: PLAN_DEGRADED
```

A degraded plan must not be relabeled as a conforming Blind First Round. The human may add a service, change the task, or accept an explicitly nonconforming ordinary review.

## Input

Use the example at:

```text
docs/evaluation/MADP-v0.3.0-alpha.3-dynamic-role-input-example.yaml
```

Each service records an explicit `chat_context_id` and `independence_group`. Separate chats using the same model family may still share one independence group when their origin is materially correlated.

## Generation and validation

```bash
python scripts/generate_alpha3_dynamic_role_plan.py input.yaml role-plan.yaml
python scripts/check_alpha3_dynamic_role_plan.py role-plan.yaml
```

The algorithm is deterministic. Equal scores use `service_id` ascending as the tie breaker.

## Limits

The planner does not:

- call any AI service;
- create chats;
- transfer confidential information;
- verify service capabilities independently;
- authorize external actions;
- decide that model agreement is evidence;
- complete `A3-REL-001`;
- authorize alpha.4.
