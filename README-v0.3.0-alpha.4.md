# MADP v0.3.0-alpha.4 — Practical Core Integration and Fix-Forward Delivery

Status: Core Usability Slice 1 is merged to `main`; the GitHub-first bootstrap and deterministic Core distribution slice is implemented on a feature branch. This version is not release-ready, tagged, published, or a stable release.

MADP v0.3.0-alpha.4 is a short-cycle prerelease line focused on reducing human operating burden while preserving explicit authority, evidence, provenance, and revision boundaries.

Implementation decisions:

- `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-002.yaml`
- `docs/planning/DEC-MADP-ALPHA4-003.yaml`

## Current implementation

### Core Usability

The merged Core Usability slice provides:

- a normative additive extension over alpha.3;
- eight versioned, non-atomic Workflow Macros;
- macro expansion into canonical alpha.3 commands;
- separate Claim kind and verification status;
- multidimensional Evidence;
- raw-response preservation;
- separate dissent state and human disposition;
- revision-bound Human Final Authority Decisions;
- separate external-action authorization;
- non-destructive migration from legacy `FACT` records.

Core artifacts:

- [`protocol/MADP-v0.3.0-alpha.4-core-usability.md`](protocol/MADP-v0.3.0-alpha.4-core-usability.md)
- [`docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md`](docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md)
- [`registries/v0.3.0-alpha.4/workflow-macros.yaml`](registries/v0.3.0-alpha.4/workflow-macros.yaml)
- [`schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml`](schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml)

### Bootstrap and protocol loading

Alpha.4 now defines two GitHub-first loading profiles:

- `QUICK`: seven required sources, source-referenced provenance, and an explicit report when schema validation is unavailable;
- `VERIFIED`: twelve required sources, executed schema validation, and SHA-256-verified provenance.

Use:

1. [`bootstrap/alpha4/load-protocol-from-github.md`](bootstrap/alpha4/load-protocol-from-github.md)
2. [`bootstrap/alpha4/quick-start.md`](bootstrap/alpha4/quick-start.md) or [`bootstrap/alpha4/verified-start.md`](bootstrap/alpha4/verified-start.md)
3. an active `MADP-PROTOCOL-LOAD-REPORT-v3`
4. an exact `PROFILE_SOURCE_BINDING`

The loader fails closed when required sources, commit binding, provenance, or profile binding are incomplete.

### Deterministic Core distribution

GitHub Actions generate:

- `MADP-v0.3.0-alpha.4-core-distribution.md`
- `MADP-v0.3.0-alpha.4-core-distribution.manifest.yaml`

The bundle embeds thirteen sources byte-for-byte and records repository, immutable commit, path, role, byte count, and SHA-256.

Validation requires:

- exact Git HEAD and commit-object source parity;
- manifest schema validation;
- loader inventory digest validation;
- embedded-source validation;
- two-pass byte reproducibility;
- complete canonical regeneration;
- privacy, evidence, and authority boundaries.

The generated bundle may be used as `access_method: COMPLETE_BUNDLE`, but the bundle itself is not a protocol-load report and does not prove that an AI system read every source.

## Workflow Macros

The registered macros are:

- `init`
- `register`
- `capture`
- `structure`
- `review`
- `decide`
- `authorize`
- `status`

Macros are guided workflows, not canonical commands, aliases, atomic transactions, or authority grants.

## Evidence and authority

Agreement among AI systems is not evidence. AI agreement, vote count, or convergence cannot replace the human decision.

Human Final Authority remains required. A Human Decision is not external-action authorization. Generated bundles, load reports, validation results, and pull requests do not grant merge, release, publication, or execution authority.

## Compatibility

This implementation:

- preserves the alpha.3 canonical command namespace;
- does not modify alpha.3 schemas;
- preserves legacy `FACT` records;
- leaves alpha.3 artifacts historical and unchanged;
- adds only versioned alpha.4 artifacts.

## GitHub-first development

GitHub branches, pull requests, Actions, generated artifacts, and artifact downloads are first-class. A local checkout is optional.

## Release model

Alpha.4 follows `RELEASE_EARLY_FIX_FORWARD` for a single-primary-user phase. Tagging, GitHub Release creation, Pages publication, and stable-release authorization remain separate actions.

## Known limitations

- The generated distribution is a workflow artifact candidate, not a published release package.
- Dynamic role assignment is not promoted into alpha.4 by this slice.
- Skill adapters and broader user-facing installation packages are not updated yet.
- A protocol-load report remains a reported observation unless independently verified.
- A bundle cannot prove complete model ingestion or conformance.
- The four-workflow comparison was terminated after one completed workflow; no comparative superiority is claimed.
- Formal release evidence and stable-release authorization are absent.
- The current published prerelease remains `MADP-v0.3.0-alpha.2`.

## Rollback

The immutable published rollback target is `MADP-v0.3.0-alpha.2` at tag `MADP-v0.3.0-alpha.2`.
