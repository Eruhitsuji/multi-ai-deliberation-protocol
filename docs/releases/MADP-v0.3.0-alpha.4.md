# MADP v0.3.0-alpha.4 release notes

Status: **PUBLISHED GITHUB PRERELEASE**

Published tag: `MADP-v0.3.0-alpha.4`

Exact tag target: `3333c66b8b9873581af3f621615a7e1f7fc20e0a`

Release: https://github.com/Eruhitsuji/multi-ai-deliberation-protocol/releases/tag/MADP-v0.3.0-alpha.4

Pages publication, stable-release authorization, formal release evidence, and latest-stable designation remain absent. The rollback target remains `MADP-v0.3.0-alpha.2`.

## Theme

**Practical Core Integration and Fix-Forward Delivery**

Alpha.4 is a short-cycle prerelease line intended for a single primary user. It prioritizes practical use and rapid correction while retaining Human Final Authority, explicit action authorization, honest evidence classification, and immutable source provenance.

## Implemented

### Core Usability

- normative additive Core Usability extension over alpha.3;
- eight non-atomic Workflow Macros;
- versioned Workflow Macro registry and profile;
- separate Claim kind and verification status;
- raw-response preservation;
- multidimensional Evidence;
- separate dissent state and human disposition;
- revision-bound Human Final Authority Decision;
- separate external-action authorization;
- non-destructive legacy `FACT` migration;
- positive and negative semantic validation.

### GitHub-first loading and Core distribution

- QUICK and VERIFIED loading profiles;
- `MADP-PROTOCOL-LOAD-REPORT-v3`;
- fail-closed source inventory, commit, provenance, and profile binding;
- optional complete-bundle access with exact manifest binding;
- deterministic thirteen-source Core distribution bundle;
- companion manifest with per-source SHA-256 and byte counts;
- canonical whole-artifact regeneration;
- two-pass reproducibility tests;
- GitHub Actions artifact upload;
- local checkout remains optional.

### Prerelease package and integrity audit

- deterministic `MADP-v0.3.0-alpha.4-prerelease-candidate.zip`;
- fixed ZIP timestamps, permissions, path order, and compression settings;
- embedded package manifest and integrity audit;
- internal `SHA256SUMS`;
- archive SHA-256 sidecar;
- package payload bound to repository and exact source commit;
- Core distribution regenerated inside the package;
- schema validation and canonical package regeneration;
- detection of payload, checksum, manifest, authority, path, and privacy tampering;
- two independent package generations required to be byte-identical.

### Release-candidate receipt and publication handoff

- deterministic release-candidate receipt;
- exact package, manifest, and release-notes SHA-256 binding;
- known-limitations and authority-boundary record;
- explicit `PULL_REQUEST_HEAD` and `MERGED_MAIN` classification;
- exact repository, source commit, target tag, receipt, package, release-note, and rollback binding;
- read-only retained publication-handoff validation.

## Published assets

- `MADP-v0.3.0-alpha.4-prerelease-candidate.zip`
- `MADP-v0.3.0-alpha.4-prerelease-candidate.manifest.yaml`
- `MADP-v0.3.0-alpha.4-prerelease-integrity-audit.yaml`
- `MADP-v0.3.0-alpha.4-prerelease-candidate.zip.sha256`
- `MADP-v0.3.0-alpha.4-release-candidate.receipt.yaml`

The successful publication workflow regenerated the exact-target artifacts, verified the authorized SHA-256 values, confirmed tag binding, compared GitHub's stored release-asset digests, published with `prerelease: true`, and preserved the rollback and latest-stable states.

The one-time write-capable publication workflows are retired after publication. A read-only published-state audit remains.

## Compatibility

- The alpha.3 canonical command namespace is unchanged.
- Alpha.3 protocol and schemas are unchanged.
- Legacy `FACT` records remain valid historical and migration inputs.
- Existing alpha.3 artifacts are not rewritten.
- New records, loaders, schemas, bundles, package metadata, receipts, and handoffs use versioned alpha.4 paths.

## Evidence and authority boundaries

- The terminated four-workflow experiment does not establish comparative superiority.
- The retained Core Candidate result is a DEGRADED single-case study.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- A Decision does not itself authorize an external action.
- A bundle or package does not prove that a model read every embedded source.
- A load report is self-reported unless independently verified.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Known limitations

- Dynamic role planning is not promoted into alpha.4.
- Skill adapters and broader installer-facing packages are not updated.
- Broader alpha.3-to-alpha.4 migration coverage remains incomplete.
- A load report remains a reported observation unless independently verified.
- A bundle or package cannot prove model ingestion or conformance.
- The four-workflow comparison was terminated after one completed workflow and does not establish comparative superiority.

## Rollback and previous version

```yaml
version: MADP-v0.3.0-alpha.2
tag: MADP-v0.3.0-alpha.2
status: published immutable prerelease rollback target
```

The published alpha.4 tag is immutable. Future corrections must use fix-forward development and a separately authorized superseding prerelease.
