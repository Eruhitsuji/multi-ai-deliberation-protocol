# MADP v0.3.0-alpha.4 — Practical Core Integration and Fix-Forward Delivery

Status: Core Usability, deterministic Core distribution, prerelease packaging, and exact-main release-candidate validation are merged to `main`. A read-only publication handoff is implemented on a feature branch. No tag, GitHub Release, Pages publication, or stable release is authorized by this status.

MADP v0.3.0-alpha.4 is a short-cycle prerelease line focused on reducing human operating burden while preserving explicit authority, evidence, provenance, and revision boundaries.

Implementation decisions:

- `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-002.yaml`
- `docs/planning/DEC-MADP-ALPHA4-003.yaml`
- `docs/planning/DEC-MADP-ALPHA4-004.yaml`
- `docs/planning/DEC-MADP-ALPHA4-005.yaml`
- `docs/planning/DEC-MADP-ALPHA4-006.yaml`

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

Alpha.4 defines two GitHub-first loading profiles:

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

The bundle embeds thirteen sources byte-for-byte and records repository, immutable commit, path, role, byte count, and SHA-256. Validation requires exact Git HEAD and commit-object parity, manifest validation, loader inventory validation, embedded-source validation, two-pass reproducibility, canonical regeneration, and privacy and authority checks.

The bundle may be used as `access_method: COMPLETE_BUNDLE`, but it is not a protocol-load report and does not prove that an AI system read every source.

### Prerelease candidate package

The candidate workflow generates:

- `MADP-v0.3.0-alpha.4-prerelease-candidate.zip`;
- a sidecar package manifest;
- a sidecar machine-generated integrity audit;
- an archive SHA-256 file.

The ZIP contains this README, release notes, MIT License, bootstrap files, the deterministic Core distribution, relevant alpha.4 schemas, an embedded manifest, an integrity audit, and internal `SHA256SUMS`.

The archive is generated twice with fixed timestamps, file permissions, path order, and compression settings. The checker rejects undeclared files, changed payloads, checksum mismatches, authority changes, unsafe paths, privacy findings, and noncanonical ZIP output.

### Exact-main release-candidate receipt

The release-readiness workflow adds:

- `MADP-v0.3.0-alpha.4-release-candidate.receipt.yaml`;
- explicit `PULL_REQUEST_HEAD` versus `MERGED_MAIN` classification;
- exact package archive, package manifest, and release-notes SHA-256 binding;
- a machine-readable record of retained checks, known limitations, and authority boundaries.

A pull-request receipt is validation evidence for that PR head only. The workflow also runs on the resulting `main` commit and must emit `source_ref_kind: MERGED_MAIN`, `branch_name: main`, and `status: MERGED_MAIN_CANDIDATE_VALIDATED` before publication authorization is considered.

### Read-only publication handoff

The publication-handoff workflow generates:

- `MADP-v0.3.0-alpha.4-publication-handoff.yaml`;
- `MADP-v0.3.0-alpha.4-publication-checklist.md`;
- the validated package, manifest, audit, archive digest, and release-candidate receipt.

The handoff binds the exact repository, commit, source classification, target tag, candidate hashes, release-notes hash, and rollback target. It records every required Human Final Authority action as incomplete and every publication boundary as false.

The workflow has `contents: read` permission only. It cannot create a tag, GitHub Release, Pages publication, stable release, or external action. Merge of the handoff PR is not publication authorization.

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

Human Final Authority remains required. A Human Decision is not external-action authorization. Generated packages, bundles, load reports, receipts, handoffs, validation results, and pull requests do not grant merge, tag, release, publication, or execution authority.

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

Alpha.4 follows `RELEASE_EARLY_FIX_FORWARD` for a single-primary-user phase. Candidate readiness, merge, exact-main validation, publication handoff, tag creation, GitHub Release publication, Pages publication, stable-release authorization, and formal release evidence remain separate states and actions.

## Known limitations

- Dynamic role assignment is not promoted into alpha.4.
- Skill adapters and broader user-facing installation packages are not updated.
- Broader alpha.3-to-alpha.4 migration coverage remains incomplete.
- A protocol-load report remains a reported observation unless independently verified.
- A bundle or ZIP package cannot prove complete model ingestion or conformance.
- The four-workflow comparison was terminated after one completed workflow; no comparative superiority is claimed.
- Formal release evidence and stable-release authorization are absent.
- The current published prerelease remains `MADP-v0.3.0-alpha.2`.

## Rollback

The immutable published rollback target is `MADP-v0.3.0-alpha.2` at tag `MADP-v0.3.0-alpha.2`.
