# MADP v0.3.0-alpha.4 — Practical Core Integration and Fix-Forward Delivery

Status: **PUBLISHED GITHUB PRERELEASE**

`MADP-v0.3.0-alpha.4` is published as a GitHub Prerelease. The immutable tag points to exact commit `3333c66b8b9873581af3f621615a7e1f7fc20e0a`.

Release: https://github.com/Eruhitsuji/multi-ai-deliberation-protocol/releases/tag/MADP-v0.3.0-alpha.4

Pages publication, stable-release authorization, formal release evidence, and latest-stable designation remain absent. The rollback target remains `MADP-v0.3.0-alpha.2`.

MADP v0.3.0-alpha.4 is a short-cycle prerelease focused on reducing human operating burden while preserving explicit authority, evidence, provenance, and revision boundaries.

Implementation and publication decisions:

- `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-002.yaml`
- `docs/planning/DEC-MADP-ALPHA4-003.yaml`
- `docs/planning/DEC-MADP-ALPHA4-004.yaml`
- `docs/planning/DEC-MADP-ALPHA4-005.yaml`
- `docs/planning/DEC-MADP-ALPHA4-006.yaml`
- `docs/planning/DEC-MADP-ALPHA4-007.yaml`
- `docs/planning/DEC-MADP-ALPHA4-008.yaml`

## Published release

The published prerelease includes five verified assets:

- `MADP-v0.3.0-alpha.4-prerelease-candidate.zip`
- `MADP-v0.3.0-alpha.4-prerelease-candidate.manifest.yaml`
- `MADP-v0.3.0-alpha.4-prerelease-integrity-audit.yaml`
- `MADP-v0.3.0-alpha.4-prerelease-candidate.zip.sha256`
- `MADP-v0.3.0-alpha.4-release-candidate.receipt.yaml`

Publication completed through a fail-closed GitHub Actions process. The successful run regenerated the exact-target assets, verified the authorized SHA-256 values, confirmed the tag binding, checked GitHub's stored asset digests, published with `prerelease: true`, and preserved the previous latest-stable and rollback states.

The one-time write-capable publication workflows are retired after publication. A read-only published-state audit remains to detect tag, Release-mode, asset-inventory, or asset-digest drift.

## Core Usability

The Core Usability slice provides:

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

## Bootstrap and protocol loading

Alpha.4 defines two GitHub-first loading profiles:

- `QUICK`: seven required sources, source-referenced provenance, and an explicit report when schema validation is unavailable;
- `VERIFIED`: twelve required sources, executed schema validation, and SHA-256-verified provenance.

Use:

1. [`bootstrap/alpha4/load-protocol-from-github.md`](bootstrap/alpha4/load-protocol-from-github.md)
2. [`bootstrap/alpha4/quick-start.md`](bootstrap/alpha4/quick-start.md) or [`bootstrap/alpha4/verified-start.md`](bootstrap/alpha4/verified-start.md)
3. an active `MADP-PROTOCOL-LOAD-REPORT-v3`
4. an exact `PROFILE_SOURCE_BINDING`

The loader fails closed when required sources, commit binding, provenance, or profile binding are incomplete.

## Deterministic Core distribution

GitHub Actions generate:

- `MADP-v0.3.0-alpha.4-core-distribution.md`
- `MADP-v0.3.0-alpha.4-core-distribution.manifest.yaml`

The bundle embeds thirteen sources byte-for-byte and records repository, immutable commit, path, role, byte count, and SHA-256. Validation requires exact Git HEAD and commit-object parity, manifest validation, loader inventory validation, embedded-source validation, two-pass reproducibility, canonical regeneration, and privacy and authority checks.

The bundle may be used as `access_method: COMPLETE_BUNDLE`, but it is not a protocol-load report and does not prove that an AI system read every source.

## Prerelease package and receipts

The deterministic package contains this README, release notes, MIT License, bootstrap files, the Core distribution, relevant alpha.4 schemas, an embedded manifest, an integrity audit, and internal `SHA256SUMS`.

The package is generated with fixed timestamps, file permissions, path order, and compression settings. Validation rejects undeclared files, changed payloads, checksum mismatches, authority changes, unsafe paths, privacy findings, and noncanonical output.

The release-candidate receipt records:

- exact package archive SHA-256;
- exact package-manifest SHA-256;
- release-notes SHA-256;
- known limitations;
- retained checks;
- authority boundaries;
- explicit `PULL_REQUEST_HEAD` versus `MERGED_MAIN` classification.

## Publication handoff

The retained read-only publication-handoff workflow generates an exact-commit-bound handoff and checklist. It cannot create or change tags, Releases, Pages, stable-release status, or formal release evidence.

The handoff remains useful for auditing the source commit, target tag, package hashes, receipt hash, release-notes hash, and rollback target. It is not publication authority.

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

Human Final Authority remains required. A Human Decision is not external-action authorization. Generated packages, bundles, load reports, receipts, handoffs, validation results, and pull requests do not independently grant merge, tag, release, publication, or execution authority.

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

Alpha.4 follows `RELEASE_EARLY_FIX_FORWARD` for a single-primary-user phase. The prerelease is published, while Pages publication, stable-release authorization, formal release evidence, and any future superseding release remain separate states and actions.

## Known limitations

- Dynamic role assignment is not promoted into alpha.4.
- Skill adapters and broader installer-facing packages are not updated.
- Broader alpha.3-to-alpha.4 migration coverage remains incomplete.
- A protocol-load report remains a reported observation unless independently verified.
- A bundle or ZIP package cannot prove complete model ingestion or conformance.
- The four-workflow comparison was terminated after one completed workflow; no comparative superiority is claimed.
- Formal release evidence and stable-release authorization are absent.

## Rollback

The immutable published rollback target remains `MADP-v0.3.0-alpha.2` at tag `MADP-v0.3.0-alpha.2`.
