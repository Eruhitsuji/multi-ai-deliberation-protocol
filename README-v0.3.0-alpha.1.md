# MADP v0.3.0-alpha.1 Development README

> Development branch: `feature/v0.3.0-alpha.1`
>
> Public current release candidate remains `MADP-v0.2.5-rc.2` until a separate user-authorized merge, tag, and release are completed.

## Status

`MADP-v0.3.0-alpha.1` is an unreleased development prerelease. It introduces authority hardening, separate Session State and Relay Block roots, migration evidence and audit contracts, generated self-contained schemas, migration fixtures, and the `MADP_JCS_V1` digest profile.

It does not yet claim production readiness, universal interoperability, live structured-output API compatibility, or a complete arbitrary-state migration engine.

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

The following files are generated and must not be edited directly:

- `schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml`
- `schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml`
- `bootstrap/complete-protocol-bundle.txt`
- `bootstrap/migration-fixtures-bundle.txt`

Regenerate all committed generated artifacts:

```bash
python scripts/generate_artifacts.py
```

Check byte-for-byte drift:

```bash
python scripts/generate_artifacts.py --check
```

The schema bundles are self-contained. The committed text bundles are currently reproducible source indexes marked `GENERATED_DISTRIBUTION_DRAFT_INDEX_ONLY`; they are not yet complete upload bundles containing every source file body.

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
```

The existing rc.2 checks remain part of CI and must continue to pass.

## Migration fixtures

The fixture corpus is under `tests/migration/` and currently contains `MIG-FIX-001` through `MIG-FIX-010`.

Schema-layer checks cover rc.2 source validity, v0.3 Session State and Relay Block roots, migration evidence, and migration audit records. Fixture-oriented semantic checks currently cover:

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

## Authority boundaries

Implementation work on the feature branch does not authorize:

- merging to `main`;
- creating or moving a tag;
- publishing a GitHub Release;
- modifying historical `MADP-v0.2.5-rc.2` canonical artifacts.

Published historical tags remain immutable.

## Known remaining work

- Observe and repair actual GitHub Actions results.
- Produce a truly self-contained text upload bundle, not only a generated source index.
- Add broader adversarial vectors and complete semantic validation.
- Add cross-language JCS verification.
- Complete final protocol/schema/fixture traceability review.
- Update the main `README.md` when alpha.1 is ready to become the repository's promoted prerelease target.
