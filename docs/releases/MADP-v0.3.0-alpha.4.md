# MADP v0.3.0-alpha.4 release notes

Status: **DRAFT — implementation kickoff only**

No tag, GitHub Release, Pages publication, or stable release is created by this document.

## Intended theme

**Practical Core Integration and Fix-Forward Delivery**

Alpha.4 begins a short-cycle prerelease line intended for a single primary user. It prioritizes practical use and rapid correction while retaining Human Final Authority, explicit action authorization, and honest evidence classification.

## Included in the kickoff increment

- alpha.4 implementation decision and scope;
- machine-readable implementation status;
- alpha.4 overview README;
- draft release notes with limitations and rollback information;
- a dedicated kickoff checker and GitHub Actions workflow.

## Planned for later increments

- versioned non-atomic Workflow Macros;
- additive Claim and Evidence semantics with preserved legacy `FACT` records;
- explicit Blind First Round, correlation, dissent, and human-disposition records;
- compatibility fixtures and migration checks;
- deterministic alpha.4 distribution artifacts;
- reproducibility and integrity validation.

## Compatibility

The kickoff increment does not change the alpha.3 canonical command namespace or existing schemas. It does not remove, reinterpret, or migrate legacy records.

## Evidence and authority boundaries

- The terminated four-workflow experiment does not establish comparative superiority.
- The retained Core Candidate result is a DEGRADED single-case study.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- AI systems do not gain merge, release, publication, or external-execution authority.
- Formal release evidence remains false.
- Stable release remains unauthorized.

## Known limitations

- The alpha.4 normative protocol is not implemented yet.
- Alpha.4 schemas, registries, bootstraps, migrations, Skills, and generated bundles are not available yet.
- No alpha.4 distribution artifact is produced by the kickoff increment.
- The repository's current published prerelease remains `MADP-v0.3.0-alpha.2`.
- Tagging and GitHub Release publication require a later explicit action.
- A local checkout is optional, but GitHub Actions must pass before later prerelease publication.

## Rollback and previous version

Published rollback target:

```yaml
version: MADP-v0.3.0-alpha.2
tag: MADP-v0.3.0-alpha.2
status: published immutable prerelease
```

The merged alpha.3 implementation remains available on repository history for development reference, but it is not the published rollback tag.
