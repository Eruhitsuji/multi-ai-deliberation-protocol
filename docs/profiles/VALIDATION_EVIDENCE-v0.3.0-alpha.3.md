# Validation Evidence Profile for MADP v0.3.0-alpha.3

Status: normative implementation profile for VERIFIED and FIELD_TRIAL evidence. It does not grant decision or execution authority.

## Purpose

Replace free-text claims such as `VALID` or `schema checked` with receipts that a deterministic checker can recompute from exact artifact and schema bytes.

## Receipt generation

Use `scripts/generate_validation_receipt_v030_alpha3.py` or an equivalent deterministic implementation.

A `VALIDATION_RECEIPT` records:

- an artifact ID and either an exact positive revision or a version string;
- an artifact locator;
- `RAW_BYTES` or `MADP_CANONICAL_JSON_V1` canonicalization;
- artifact and schema SHA-256 values;
- the validator name and version;
- `PASS`, `FAIL`, or `NOT_EXECUTED`;
- structured validation errors and limitations.

`MADP_CANONICAL_JSON_V1` is UTF-8 JSON with keys sorted lexicographically, no insignificant whitespace, Unicode preserved, and non-finite numbers forbidden.

## Load-report schema-validation records

A VERIFIED or FIELD_TRIAL `PROTOCOL_LOAD_REPORT` includes `schema_validation_records`. Each record binds one loaded target to one schema and one receipt:

```yaml
- target_ref: repo://registries/v0.3.0-alpha.3/commands.yaml
  target_sha256: <sha256>
  schema_path: schemas/v0.3.0-alpha.3/command-registry.schema.yaml
  schema_sha256: <sha256>
  receipt_ref: VAL-REGISTRY-A3
  result: PASS
```

The sets in `schemas_applicable` and `schemas_executed`, the validation records, and `validation_receipt_refs` must agree. A receipt ID without a corresponding receipt artifact is not evidence.

## Release evidence

For release sign-off, the usability checker recomputes:

1. the load-report schema result and canonical report hash;
2. every referenced receipt schema;
3. each repository target and schema hash;
4. the target's JSON Schema result;
5. the selected start-profile hash;
6. the raw-observation file hash.

Model self-report is never a receipt executor. A post-hoc deterministic validation may establish structural validity, but it does not retroactively prove that a model actually read a source or understood its meaning; retrieval and usability evidence remain separate.

## Failure handling

A failed validation emits a `FAIL` receipt with structured errors. Missing artifact bytes, missing schema bytes, mismatched hashes, unresolved receipt references, or unvalidated applicable targets prevent VERIFIED/FIELD_TRIAL completion.
