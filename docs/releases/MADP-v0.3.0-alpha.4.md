# MADP v0.3.0-alpha.4 release notes

Status: **PRERELEASE CANDIDATE — READ-ONLY PUBLICATION HANDOFF IMPLEMENTED**

No tag, GitHub Release, Pages publication, stable release, or formal release evidence is created by this document or by the publication-handoff workflow.

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
- two independent package generations required to be byte-identical;
- GitHub Actions candidate artifact.

### Release-candidate receipt

- deterministic `MADP-v0.3.0-alpha.4-release-candidate.receipt.yaml`;
- exact package archive SHA-256;
- exact package manifest SHA-256;
- exact release-notes SHA-256;
- known-limitations count;
- retained validation results;
- authority-boundary record;
- explicit distinction between `PULL_REQUEST_HEAD` and `MERGED_MAIN` candidates;
- automatic validation and artifact upload on pushes to `main`.

### Publication handoff

- deterministic `MADP-v0.3.0-alpha.4-publication-handoff.yaml`;
- operator-facing `MADP-v0.3.0-alpha.4-publication-checklist.md`;
- exact repository, source commit, source classification, target tag, package hashes, receipt hash, release-notes hash, and rollback binding;
- every required Human Final Authority action recorded as incomplete;
- tag, GitHub Release, Pages, stable-release, and formal-evidence boundaries recorded as false;
- read-only GitHub Actions permissions;
- two-pass deterministic generation and canonical validation;
- 30-day workflow artifact retention.

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
- A PR-head receipt or handoff is not merged-main evidence.
- Candidate readiness and handoff readiness do not authorize merge, tagging, release, publication, or execution.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Validation

The complete candidate and handoff validation path runs:

```bash
python scripts/check_alpha4_kickoff.py
python scripts/check_alpha4_core_usability.py
python tests/v0.3.0-alpha.4/test_core_distribution.py \
  --repository owner/repository \
  --source-commit <40-character-commit>
python tests/v0.3.0-alpha.4/test_prerelease_package.py \
  --repository owner/repository \
  --source-commit <40-character-commit>
python tests/v0.3.0-alpha.4/test_release_candidate.py \
  --repository owner/repository \
  --source-commit <40-character-commit> \
  --branch-name feature/example
python tests/v0.3.0-alpha.4/test_publication_handoff.py \
  --repository owner/repository \
  --source-commit <40-character-commit> \
  --branch-name feature/example
python scripts/generate_alpha4_publication_handoff.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit> \
  --source-ref-kind PULL_REQUEST_HEAD \
  --branch-name feature/example \
  --target-tag MADP-v0.3.0-alpha.4
python scripts/check_alpha4_publication_handoff.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit> \
  --source-ref-kind PULL_REQUEST_HEAD \
  --branch-name feature/example \
  --target-tag MADP-v0.3.0-alpha.4
```

GitHub Actions generate the handoff twice, require byte-for-byte equality, validate both copies, and upload one read-only handoff artifact. After merge, the same workflow runs against the exact resulting `main` commit and classifies the handoff as `MERGED_MAIN`.

## Publication procedure

After the publication-handoff PR is merged:

1. confirm the handoff workflow passes on the exact merged `main` commit;
2. inspect the handoff manifest, release-candidate receipt, package manifest, integrity audit, archive digest, release notes, and known limitations;
3. confirm `source_ref_kind: MERGED_MAIN`, `branch_name: main`, the exact commit, and target tag `MADP-v0.3.0-alpha.4`;
4. explicitly authorize tag creation;
5. explicitly authorize GitHub Prerelease creation;
6. keep Pages publication separate unless explicitly authorized.

## Known limitations

- Dynamic role planning is not promoted into alpha.4.
- Skill adapters and broader installer-facing packages are not updated.
- Broader alpha.3-to-alpha.4 migration coverage remains incomplete.
- A load report remains a reported observation unless independently verified.
- A bundle or package cannot prove model ingestion or conformance.
- The repository's current published prerelease remains `MADP-v0.3.0-alpha.2`.
- Tagging and GitHub Release publication require later explicit Human Final Authority actions.

## Rollback and previous version

Published rollback target:

```yaml
version: MADP-v0.3.0-alpha.2
tag: MADP-v0.3.0-alpha.2
status: published immutable prerelease
```

The merged alpha.3 and alpha.4 development commits remain available in repository history, but they are not the published rollback tag.
