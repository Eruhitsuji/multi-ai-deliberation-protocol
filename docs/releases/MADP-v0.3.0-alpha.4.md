# MADP v0.3.0-alpha.4 release notes

Status: **PRERELEASE CANDIDATE — PUBLICATION NOT AUTHORIZED**

No tag, GitHub Release, Pages publication, stable release, or formal release evidence is created by this document.

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
- 14-day GitHub Actions candidate artifact.

## Compatibility

- The alpha.3 canonical command namespace is unchanged.
- Alpha.3 protocol and schemas are unchanged.
- Legacy `FACT` records remain valid historical and migration inputs.
- Existing alpha.3 artifacts are not rewritten.
- New records, loaders, schemas, bundles, and package metadata use versioned alpha.4 paths.

## Evidence and authority boundaries

- The terminated four-workflow experiment does not establish comparative superiority.
- The retained Core Candidate result is a DEGRADED single-case study.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- A Decision does not itself authorize an external action.
- A bundle or package does not prove that a model read every embedded source.
- A load report is self-reported unless independently verified.
- Candidate readiness does not authorize merge, tagging, release, publication, or execution.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Validation

The candidate validation path runs:

```bash
python scripts/check_alpha4_kickoff.py
python scripts/check_alpha4_core_usability.py
python tests/v0.3.0-alpha.4/test_core_distribution.py \
  --repository owner/repository \
  --source-commit <40-character-commit>
python tests/v0.3.0-alpha.4/test_prerelease_package.py \
  --repository owner/repository \
  --source-commit <40-character-commit>
python scripts/generate_alpha4_prerelease_package.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit>
python scripts/check_alpha4_prerelease_package.py <output> \
  --repository owner/repository \
  --source-commit <40-character-commit>
```

GitHub Actions generate the package twice, require byte-for-byte equality, validate both copies, and upload one candidate artifact.

## Publication procedure

After this candidate PR is merged:

1. regenerate the package against the exact merged `main` commit;
2. confirm all required GitHub Actions pass on that commit;
3. inspect the generated manifest, audit, archive digest, and known limitations;
4. obtain explicit Human Final Authority authorization for the tag;
5. obtain explicit Human Final Authority authorization for the GitHub Release;
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
