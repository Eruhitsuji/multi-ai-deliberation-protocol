# MADP v0.3.0-alpha.4 release notes

Status: **DRAFT — Core Usability Slice 1**

No tag, GitHub Release, Pages publication, or stable release is created by this
document.

## Theme

**Practical Core Integration and Fix-Forward Delivery**

Alpha.4 is a short-cycle prerelease line intended for a single primary user. It
prioritizes practical use and rapid correction while retaining Human Final
Authority, explicit action authorization, and honest evidence classification.

## Implemented in Core Usability Slice 1

- normative additive Core Usability extension over alpha.3;
- eight non-atomic Workflow Macros;
- versioned Workflow Macro registry and profile;
- additive Claim and Evidence model;
- raw-response preservation requirement;
- multidimensional evidence assessment;
- separate dissent state and human disposition;
- revision-bound Human Final Authority Decision;
- separate external-action authorization reference;
- non-destructive legacy `FACT` migration records;
- positive, schema-negative, and semantic-negative fixtures;
- automated macro, reference, migration, privacy, and authority checks.

## Compatibility

- The alpha.3 canonical command namespace is unchanged.
- Alpha.3 schemas are unchanged.
- Legacy `FACT` records remain valid historical and migration inputs.
- Existing alpha.3 artifacts are not rewritten.
- New records use versioned alpha.4 paths.

## Evidence and authority boundaries

- The terminated four-workflow experiment does not establish comparative
  superiority.
- The retained Core Candidate result is a DEGRADED single-case study.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- AI systems do not gain merge, release, publication, or external-execution
  authority.
- A Decision does not itself authorize an external action.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Validation

The implementation slice is designed to run:

```bash
python scripts/check_alpha4_kickoff.py
python scripts/check_alpha4_core_usability.py
```

GitHub Actions are the required validation environment. A local checkout is
optional.

## Known limitations

- The alpha.4 bootstrap and load profile do not yet include the new extension.
- No deterministic alpha.4 distribution artifact is generated yet.
- Broader alpha.3-to-alpha.4 migration coverage is still pending.
- Skills and user-facing bootstraps are not updated in this slice.
- The repository's current published prerelease remains
  `MADP-v0.3.0-alpha.2`.
- Tagging and GitHub Release publication require a later explicit action.

## Rollback and previous version

Published rollback target:

```yaml
version: MADP-v0.3.0-alpha.2
tag: MADP-v0.3.0-alpha.2
status: published immutable prerelease
```

The merged alpha.3 and alpha.4 development commits remain available in
repository history, but they are not the published rollback tag.
