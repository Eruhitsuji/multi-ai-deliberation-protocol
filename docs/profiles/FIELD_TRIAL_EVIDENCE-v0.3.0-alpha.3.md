# Field-Trial Evidence Profile for MADP v0.3.0-alpha.3

Status: normative evaluation profile for release-signoff evidence.

## Purpose

Store loader provenance, validation receipts, start-profile binding, and raw observations once per model run while keeping scenario-level outcomes independently reviewable.

## Evidence model

Use `schemas/v0.3.0-alpha.3/field-trial-evidence.schema.yaml`.

- `run_evidence` contains one record for one participant and run index.
- A run record owns the tested commit, active protocol load report, report receipt, start-profile binding, and raw observation inventory.
- `scenario_results` contains one result per tested scenario and references exactly one `run_id`.
- Each scenario lists the `observation_refs` needed to support its assessment.
- Global validation receipts may be shared across runs only when their artifact and schema bindings are identical.

## Invariants

1. A load report, profile binding, or raw observation is not copied into every scenario row.
2. A scenario cannot reference an unknown run or observation.
3. Every run must support at least one scenario result.
4. Participant ID plus run index is unique.
5. Every raw observation path remains repository-relative and carries an independently recomputed SHA-256.
6. The report receipt is bound to `trial://<run_id>/protocol-load-report`.
7. Metrics are recomputed from scenario rows; handwritten aggregate values are not authoritative.
8. Existing results-version 5 evidence is historical input and must be migrated before release use.

## Collection tooling

Use `docs/evaluation/MADP-v0.3.0-alpha.3-field-trial-collection-config.yaml` as the input template and `scripts/collect_field_trial_evidence_v030_alpha3.py` to prepare one run package.

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py prepare \
  --config collection-config.yaml \
  --output docs/evaluation/evidence/v0.3.0-alpha.3/RUN-001/package.yaml
```

The collector copies observation files, recomputes hashes, rebuilds repository validation receipts, creates the run-bound protocol-load-report receipt, and emits all eight scenario rows. A package remains `DRAFT` until all scenario assessments and observation references are complete. Only `READY` packages may be merged.

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py merge \
  --base-results docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml \
  --package RUN-001/package.yaml \
  --output combined-results.yaml
```

Merge recomputes metrics and leaves the result `IN_PROGRESS`; it never signs off or changes release state.

## Migration

Use:

```text
python scripts/migrate_field_trial_results_v5_to_v6.py \
  --input old-results.yaml \
  --output migrated-results.yaml
```

Migration deduplicates identical run-level evidence and turns each legacy raw observation into a run-scoped observation record. Conflicting load reports or profile bindings within one participant/run pair fail closed.

## Release boundary

This profile changes evidence representation and collection ergonomics only. It does not lower usability thresholds, convert historical observations into passing evidence, authorize release, or change decision authority.
