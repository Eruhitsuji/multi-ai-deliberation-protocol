# Field-Trial Collection Profile for MADP v0.3.0-alpha.3

Status: normative evaluation-support profile. It does not alter protocol authority or release thresholds.

## Purpose

Turn one practical model run into a reproducible, run-normalized evidence package without manually copying the protocol load report, validation receipts, profile binding, or observation hashes into every scenario row.

## Tool

Use `scripts/collect_field_trial_evidence_v030_alpha3.py`.

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py prepare \
  --config collection-config.yaml \
  --output docs/evaluation/evidence/v0.3.0-alpha.3/RUN-001/package.yaml
```

The output must remain inside the repository so observation paths can be repository-relative and independently rehashed.

## Prepare behavior

`prepare`:

1. requires the tested commit to equal the checked-out commit;
2. reads an active `COMPLETE` `FIELD_TRIAL` protocol load report;
3. rebuilds repository validation receipts from the actual target and schema bytes;
4. creates a receipt for the normalized load report;
5. verifies the selected start profile is authorized and hash-matched;
6. copies observation files into the package directory and records SHA-256 values;
7. creates all eight scenario rows;
8. marks the package `READY` only when every scenario has observation references and complete review fields.

A package with missing scenario assessments is `DRAFT`. `DRAFT` is valid collection work but cannot be merged as formal trial evidence.

## Check and merge

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py check \
  --package RUN-001/package.yaml \
  --require-ready
```

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py merge \
  --base-results docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml \
  --package RUN-001/package.yaml \
  --package RUN-002/package.yaml \
  --output combined-results.yaml
```

`merge` rejects conflicting participants, receipts, run IDs, and trial IDs. It recomputes aggregate metrics and leaves the combined document `IN_PROGRESS` with no sign-off. Human sign-off and release-state changes remain separate authority-sensitive actions.

## Normalization boundary

The collector may rebuild `validation_receipt_refs` so they contain exactly the receipts generated from `schema_validation_records` plus the run-bound protocol-load-report receipt. This normalization is disclosed as `REBUILT_VALIDATION_RECEIPT_REFERENCE_SET`; it does not change the tested commit, loaded source hashes, report status, report revision, or start-profile authority.

## Safety invariants

- The collector does not fabricate missing source hashes or unread protocol content.
- It does not mark a `DRAFT` package `READY`.
- It does not approve trial results, complete A3-REL-001, set `release_ready`, tag, release, publish, or promote Pages.
- Raw observation bytes remain authoritative; later hash mismatch fails closed.
- Collection packages use `MADP-FIELD-TRIAL-COLLECTION-v1` and `schemas/v0.3.0-alpha.3/field-trial-collection.schema.yaml`.
