# Source and Participant Independence Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile. It specializes independence assessment without changing decision authority.

## Purpose

Prevent a deliberation from treating correlated sources, model roles, or retrieval paths as independent evidence merely because they appear as separate participants.

## Required record

Use `independence_record` from `schemas/v0.3.0-alpha.3/advanced-profiles.schema.yaml` for every source or participant whose independence affects aggregation, verification, or review routing.

At minimum record provider, model family, data origin, retrieval provider, context origin, prompt lineage, independence group, and unknowns.

## Rules

1. Multiple roles sharing one model and chat context belong to one independence group.
2. Same-provider or same-retrieval outputs are not automatically independent.
3. Unknown lineage is recorded as unknown, not silently treated as independent.
4. Participant count and independence-group count are reported separately.
5. A majority of correlated outputs is not verified evidence and is not approval.
6. Reliability weighting may use externally measured task-specific evidence, but model self-confidence alone must not determine authority or truth.
7. Low independence, material disagreement, or weak provenance triggers review escalation rather than automatic majority resolution.

## Aggregation boundary

This profile may propose an aggregation result, specialist review, or additional evidence request. It cannot approve a decision, suppress minority dissent, or execute an action.
