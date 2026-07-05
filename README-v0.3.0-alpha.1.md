# MADP v0.3.0-alpha.1 Prerelease README

> Published prerelease tag: `MADP-v0.3.0-alpha.1`
>
> Release merge commit: `c3c80a9fa48a5f93b46f742f08d6617100a1eb60`
>
> Historical `MADP-v0.2.5-rc.2` artifacts remain immutable and available for compatibility testing.

## Status

`MADP-v0.3.0-alpha.1` is a published alpha prerelease. It introduces authority hardening, separate Session State and Relay Block roots, migration evidence and audit contracts, generated self-contained schemas, migration fixtures, and the `MADP_JCS_V1` digest profile.

It does not claim production readiness, universal interoperability, live structured-output API compatibility, or a complete arbitrary-state migration engine. Incompatible changes may occur in later prereleases.

## Canonical sources

- `protocol/MADP-v0.3.0-alpha.1.md`
- `protocol/GLOSSARY-v0.3.0-alpha.1.md`
- `schemas/v0.3.0-alpha.1/definitions.schema.yaml`
- `schemas/v0.3.0-alpha.1/session-state.schema.yaml`
- `schemas/v0.3.0-alpha.1/relay-block.schema.yaml`
- `schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml`
- `schemas/v0.3.0-alpha.1/migration-audit.schema.yaml`

Canonical multi-file validation uses the schemas' absolute URN identifiers and an explicit local resource registry.

## Generated distributions

The following committed files are generated and must not be edited directly:

- `schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml`
- `schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml`
- `bootstrap/complete-protocol-bundle.txt`
- `bootstrap/migration-fixtures-bundle.txt`

Regenerate committed generated artifacts:

```bash
python scripts/generate_artifacts.py
```

Check byte-for-byte drift:

```bash
python scripts/generate_artifacts.py --check
```

The committed schema bundles are self-contained. The committed text files are reproducible source indexes marked as prerelease distribution indexes.

Generate a self-contained upload bundle containing the protocol, glossary, self-contained root schemas, migration evidence schema, and migration audit schema:

```bash
python scripts/generate_text_bundles.py \
  --output-dir tmp/generated-v030 \
  --source-commit <COMMIT_SHA>
```

This creates:

- `tmp/generated-v030/complete-protocol-bundle.full.txt`
- `tmp/generated-v030/complete-protocol-bundle.manifest.yaml`

Validate the generated bundle and every embedded source hash:

```bash
python scripts/check_complete_bundle_v030.py \
  tmp/generated-v030/complete-protocol-bundle.full.txt \
  tmp/generated-v030/complete-protocol-bundle.manifest.yaml
```

GitHub Actions generates the same files with the exact workflow commit SHA and uploads them as artifact `madp-v0.3.0-alpha.1-complete-bundle`.

## Validation

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the v0.3 alpha checks:

```bash
python scripts/check_traceability_v030.py
python scripts/run_schema_fixture_checks.py all --json
python scripts/check_migration_invariants_v030.py
python scripts/generate_artifacts.py --check
python scripts/check_schema_bundle_equivalence.py
python scripts/verify_jcs_vectors.py all --json
python scripts/check_release_readiness_v030.py
python scripts/generate_text_bundles.py --check --output-dir tmp/generated-v030
python scripts/check_complete_bundle_v030.py tmp/generated-v030/complete-protocol-bundle.full.txt tmp/generated-v030/complete-protocol-bundle.manifest.yaml
```

The existing rc.2 checks remain part of CI and must continue to pass.

The merge commit was validated successfully by GitHub Actions run `28734219309`.

## Migration fixtures

The fixture corpus is under `tests/migration/` and contains `MIG-FIX-001` through `MIG-FIX-010`.

Schema-layer checks cover rc.2 source validity, v0.3 Session State and Relay Block roots, migration evidence, and migration audit records. Fixture-oriented semantic checks cover:

- fabricated provenance;
- automatic facilitator conflict resolution;
- false pre-ingress digest claims;
- old-version writeback;
- unsafe official downcast.

These checks are not a general migration engine.

## MADP_JCS_V1

`tests/canonicalization/jcs-cv-001/` contains:

- `input-snapshot.yaml`;
- `parsed-data.json` for review only;
- `canonical.jcs`, the exact hashed byte stream;
- `sha256.txt`;
- `manifest.yaml`.

Current vector values:

```yaml
byte_length: 511
sha256: "f10c125bf6891d04d60caaf7f4f197f9f14f85655ef829dc9762f2d41d76bde1"
```

This is a single-implementation vector. Cross-language equality remains an RC-stage requirement.

## Release and authority boundaries

The tag `MADP-v0.3.0-alpha.1` identifies the published alpha prerelease. The tag must remain immutable.

Publication of this prerelease does not authorize:

- modifying or moving the published tag;
- modifying historical `MADP-v0.2.5-rc.2` canonical artifacts;
- treating AI convergence as user approval or execution authority;
- claiming production stability or universal interoperability.

The user remains the sole final decision-maker for future promotion, supersession, or stable release decisions.

## Known remaining work

- Add broader adversarial vectors and more complete semantic validation.
- Add cross-language JCS verification.
- Test live provider-specific structured-output interoperability.
- Resolve or separately document the GitHub Pages deployment configuration.
- Prepare a later RC only after the alpha evidence is sufficient.
