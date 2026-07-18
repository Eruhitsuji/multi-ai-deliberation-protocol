# MADP v0.3.0-alpha.3 Blind First Round Operational Test

Status: experimental operational test for the Core Candidate. It does not replace
formal FIELD_TRIAL evidence.

## What this test measures

Blind First Round measures direct cross-participant exposure inside the recorded
deliberation. It does not prove that model training data, retrieval providers,
system prompts, or world knowledge are globally independent.

A response is eligible only when its raw form is fixed before another
participant's conclusion is directly disclosed.

## Required sequence

1. Freeze one question, scope, authority boundary, and information set.
2. Calculate one `information_set_hash`.
3. Give the same bounded information set to each initial participant.
4. Do not include another participant's conclusion in the initial prompt.
5. Preserve each raw response and SHA-256 before Cross Exposure.
6. Record participant, chat context, independence group, and known correlation.
7. Only after initial capture, disclose the other responses.
8. Request criticism, missing evidence, failure conditions, and revisions.
9. Preserve changed, retained, and withdrawn claims.
10. Integrate independent convergence, correlated convergence, and residual
    dissent separately.

## Status classification

### VALID

Use `VALID` only when:

- at least two raw initial responses exist;
- each was captured before Cross Exposure;
- each exposure state is `UNEXPOSED`;
- raw response references and hashes are present;
- `eligible_initial_response_count` matches the eligible records;
- the run does not infer unknown exposure as unexposed.

`VALID` describes the blind procedure, not source independence. Two valid blind
responses may still be correlated.

### PARTIALLY_COMPROMISED

Use `PARTIALLY_COMPROMISED` when some participants remained unexposed but one or
more received partial prior conclusions or contaminated context.

Retain the responses, but set:

```yaml
conformance_eligible: false
```

### ANCHORING_EXPOSED

Use `ANCHORING_EXPOSED` when prior conclusions were directly visible before the
initial response was fixed. The response may be ordinary review evidence but not
blind-round evidence.

### NOT_PERFORMED

Use `NOT_PERFORMED` when no blind initial round occurred. Do not reconstruct one
from later messages.

### NOT_APPLICABLE

Use `NOT_APPLICABLE` only for a genuinely single-participant or non-comparative
workflow where Blind First Round was outside the declared design.

The `ALPHA3_CORE_CANDIDATE` workflow requires Blind First Round, so a
multi-participant Core Candidate run cannot use `NOT_APPLICABLE` and claim
conformance.

## Correlation and convergence

Record known shared origins:

- same model family;
- shared chat context;
- shared retrieval source;
- copied prompt containing prior conclusions;
- common generated summary;
- unknown origin.

Use `INDEPENDENT_CONVERGENCE` only when at least two independence groups support
the convergence claim. Otherwise use `CORRELATED_CONVERGENCE`, `MIXED`,
`NO_CONVERGENCE`, or `NOT_EVALUATED`.

Agreement is not evidence. Blind agreement is still evaluated against source
quality, traceability, freshness, claim fit, and correlation.

## Negative operational cases

The executable fixture set includes cases that must fail semantic validation:

- a run labeled `VALID` containing an `EXPOSED` initial response;
- an `INDEPENDENT_CONVERGENCE` claim with only one independence group;
- a ready comparison missing one of the four workflows;
- a Core Candidate run claiming conformance after a compromised round.

The fixture set also includes an honest degraded case. A compromised run is
allowed when it is labeled accurately and not counted as conforming evidence.

## Validation

The operational records use:

```text
schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml
tests/v0.3.0-alpha.3/core-candidate-experiment-fixtures.yaml
```

Run:

```bash
python scripts/check_alpha3_core_candidate_experiments.py
```
