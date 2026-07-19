# MADP v0.3.0-alpha.4 release notes

Status: **DRAFT — Core Distribution Slice**

No tag, GitHub Release, Pages publication, or stable release is created by this document.

## Theme

**Practical Core Integration and Fix-Forward Delivery**

Alpha.4 is a short-cycle prerelease line intended for a single primary user. It prioritizes practical use and rapid correction while retaining Human Final Authority, explicit action authorization, and honest evidence classification.

## Implemented

### Core Usability Slice 1

- normative additive Core Usability extension over alpha.3;
- eight non-atomic Workflow Macros;
- versioned Workflow Macro registry and profile;
- additive Claim and Evidence model;
- raw-response preservation;
- multidimensional evidence assessment;
- separate dissent state and human disposition;
- revision-bound Human Final Authority Decision;
- separate external-action authorization;
- non-destructive legacy `FACT` migration;
- positive and negative semantic validation.

### Core Distribution Slice

- GitHub-first QUICK and VERIFIED loading profiles;
- `MADP-PROTOCOL-LOAD-REPORT-v3`;
- fail-closed source inventory, commit, provenance, and profile binding;
- optional complete-bundle access with exact manifest binding;
- deterministic thirteen-source Core distribution bundle;
- companion manifest with per-source SHA-256 and byte counts;
- canonical whole-artifact regeneration;
- two-pass reproducibility tests;
- GitHub Actions artifact upload;
- local checkout remains optional.

## Compatibility

- The alpha.3 canonical command namespace is unchanged.
- Alpha.3 schemas are unchanged.
- Legacy `FACT` records remain valid historical and migration inputs.
- Existing alpha.3 artifacts are not rewritten.
- New records, loaders, schemas, and bundles use versioned alpha.4 paths.

## Evidence and authority boundaries

- The terminated four-workflow experiment does not establish comparative superiority.
- The retained Core Candidate result is a DEGRADED single-case study.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- A Decision does not itself authorize an external action.
- A bundle does not prove that a model read every embedded source.
- A load report is self-reported unless independently verified.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Validation

The implementation slice runs:

```bash
python scripts/check_alpha4_kickoff.py
python scripts/check_alpha4_core_usability.py
python tests/v0.3.0-alpha.4/test_core_distribution.py
python scripts/generate_alpha4_core_compact_bundle.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit>
python scripts/check_alpha4_core_compact_bundle.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit>
```

GitHub Actions generate the distribution twice, require byte-for-byte equality, validate both copies, and upload one candidate artifact.

## Known limitations

- The generated artifact is not yet a tagged or published prerelease.
- Dynamic role planning is deferred to a later alpha.4 slice.
- Skill adapters and installer-facing packages are not updated yet.
- Broader alpha.3-to-alpha.4 migration coverage remains incomplete.
- The repository's current published prerelease remains `MADP-v0.3.0-alpha.2`.
- Tagging and GitHub Release publication require a later explicit action.

## Rollback and previous version

Published rollback target:

```yaml
version: MADP-v0.3.0-alpha.2
tag: MADP-v0.3.0-alpha.2
status: published immutable prerelease
```

The merged alpha.3 and alpha.4 development commits remain available in repository history, but they are not the published rollback tag.
