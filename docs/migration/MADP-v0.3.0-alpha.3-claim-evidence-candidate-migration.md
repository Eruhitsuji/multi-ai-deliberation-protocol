# MADP v0.3.0-alpha.3 Claim and Evidence Candidate Migration

Status: experimental migration design. It does not change the alpha.3 runtime or
remove existing fields.

## Purpose

Test the separation proposed by `DEC-MADP-CORE-001`:

- speech form describes what kind of assertion was made;
- verification status describes what review has established;
- Evidence records support or challenge separately;
- Dissent and Decision remain separate records.

During this experiment, existing `FACT` records remain intact. The candidate
package is additive and references preserved source records.

## Candidate records

A candidate Claim uses:

```yaml
claim_kind: SOURCE_CLAIM | MODEL_INFERENCE | PROPOSAL | OPINION
verification_status: UNCHECKED | SOURCE_MATCHED | CORROBORATED | DISPUTED | REFUTED | OUTDATED | NOT_APPLICABLE
```

Claim kind never proves truth. A `SOURCE_CLAIM` may remain `UNCHECKED`,
`DISPUTED`, or `REFUTED`. A `MODEL_INFERENCE` may be well supported, but it does
not become a source quotation.

Evidence uses independent dimensions:

```yaml
assessment:
  source_role: DIRECT_RECORD | PRIMARY | SECONDARY | TERTIARY | USER_STATEMENT | MODEL_ONLY | UNKNOWN
  claim_fit: DIRECT | PARTIAL | INDIRECT | UNSUPPORTED | UNKNOWN
  freshness: CURRENT | POTENTIALLY_STALE | STALE | TIME_INDEPENDENT | UNKNOWN
  traceability: SNAPSHOT_HASHED | RETRIEVABLE | CITATION_ONLY | NONE
  source_independence: INDEPENDENTLY_CORROBORATED | SINGLE_SOURCE | DERIVED_FROM_SAME_ORIGIN | UNKNOWN
```

No composite score is required.

## Preservation invariant

Migration is non-destructive.

```yaml
existing_fact_records_preserved: true
source_fact_preserved: true
```

The migration record references the legacy FACT record and a new candidate Claim.
It never overwrites, deletes, or silently rewrites the source.

## Migration procedure

1. Preserve the exact legacy FACT record and revision.
2. Identify the asserted statement without changing its meaning.
3. Map the speech form to a candidate `claim_kind`.
4. Copy the prior verification status conservatively.
5. Attach raw-response and source references.
6. Add Evidence records separately.
7. Review whether verification status may change.
8. Record ambiguities and human-review requirements.
9. Keep Dissent and Decision references outside the Claim assertion.

## Mapping status

### EXACT

Use `EXACT` only when the speech-form mapping is unambiguous. The ambiguity list
must be empty.

### PARTIAL

Use `PARTIAL` when one legacy record combines assertion type, source attribution,
verification, or recommendation semantics. Human review is required.

### QUARANTINED

Use `QUARANTINED` when a safe target cannot be determined. Preserve the source,
record the ambiguity, require human review, and exclude the target from automated
decision support until reviewed.

## Verification changes

There is no automatic verification upgrade.

A migration may preserve the prior status with:

```yaml
verification_change_basis: PRESERVED
```

When the before and after values differ, `PRESERVED` is invalid.

An upgrade from `UNCHECKED` to `SOURCE_MATCHED` or `CORROBORATED`, or from
`SOURCE_MATCHED` to `CORROBORATED`, requires:

```yaml
verification_change_basis: EVIDENCE_REVIEWED
```

A conservative downgrade may use:

```yaml
verification_change_basis: DOWNGRADED_FOR_UNCERTAINTY
```

Only `UNCHECKED`, `DISPUTED`, `REFUTED`, or `OUTDATED` are valid uncertainty
downgrade targets.

UNKNOWN remains UNKNOWN. Missing provenance, source independence, freshness, or
claim fit is not upgraded by inference.

## Candidate corroboration rule

`CORROBORATED` requires supporting Evidence that explicitly records
`source_independence: INDEPENDENTLY_CORROBORATED`.

Multiple responses from one shared model, chat, retrieval origin, generated
summary, or unknown common source do not satisfy that condition merely because
their wording agrees.

## Failure and rollback

Schema-invalid records are rejected.

Semantic failures are retained as failed migration attempts with their source
FACT records unchanged. The experimental checker rejects at least:

- unknown Evidence references;
- Evidence pointing to an unknown Claim;
- verification changes labeled `PRESERVED`;
- upgrades without reviewed Evidence;
- `EXACT` mappings with ambiguities;
- `QUARANTINED` mappings without human review;
- hashed traceability without a digest.

No failed candidate record may be substituted for the preserved source FACT.

## Validation

Use:

```text
schemas/v0.3.0-alpha.3/experimental/claim-evidence-candidate.schema.yaml
tests/v0.3.0-alpha.3/core-candidate-experiment-fixtures.yaml
```

Run:

```bash
python scripts/check_alpha3_core_candidate_experiments.py
```

This experiment must succeed before any proposal removes or reinterprets the
existing alpha.3 `FACT` representation.
