# MADP v0.3.0-alpha.4 — Practical Core Integration and Fix-Forward Delivery

Status: implementation kickoff baseline on a feature branch. This version is not release-ready, tagged, published, or a stable release.

MADP v0.3.0-alpha.4 starts a short-cycle prerelease line focused on reducing human operating burden while preserving explicit authority, evidence, and provenance boundaries. The direction is authorized by `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml` and specified for implementation by `docs/planning/DEC-MADP-ALPHA4-001.yaml`.

## Kickoff scope

This first increment establishes:

- a versioned alpha.4 implementation decision;
- a machine-readable implementation status;
- draft release notes and known limitations;
- a GitHub Actions validation path that does not require a local checkout;
- explicit compatibility and authority boundaries for subsequent implementation PRs.

It does not yet implement the alpha.4 protocol, schemas, registries, bootstraps, migration fixtures, or generated distribution package.

## Planned alpha.4 direction

### Human-facing workflow layer

The eight Workflow Macros—`init`, `register`, `capture`, `structure`, `review`, `decide`, `authorize`, and `status`—are planned as a versioned, non-atomic interaction layer. They must expand into recorded canonical operations and may stop at human or validation gates.

### Claim and Evidence semantics

Alpha.4 is planned to distinguish claim kind from verification status as additive concepts. Existing `FACT` records remain valid historical and compatibility inputs until explicit migration schemas, fixtures, and safety tests exist.

### Blind review, correlation, and dissent

Blind First Round procedure status, known participant correlation, material dissent, and human disposition remain explicit. Agreement among AI systems is not evidence, and degraded runs must not be relabeled as conforming.

### Distribution and role planning

The compact bundle and dynamic role planner may become alpha.4 distribution inputs. They remain deterministic advisory tools: a bundle does not prove that a model read it, and a role plan does not grant approval or execution authority.

### GitHub-first development

Alpha.4 development supports branch creation, repository editing, validation, artifact generation, and pull-request review through GitHub-hosted workflows. A local checkout is optional rather than required.

## Compatibility policy

During the kickoff increment:

- the alpha.3 command namespace remains unchanged;
- no breaking schema change is introduced;
- legacy `FACT` records are preserved;
- alpha.3 artifacts remain historical and unchanged;
- external actions still require separate, action-specific human authorization.

## Release model

Alpha.4 follows the `RELEASE_EARLY_FIX_FORWARD` policy for a single-primary-user phase. Short prerelease increments may proceed without completing the terminated four-workflow comparison or the alpha.3 stable-release gates.

Tagging, GitHub Release creation, Pages publication, and stable-release authorization remain separate actions.

## Known limitations

- Alpha.4 normative protocol and schema content is not implemented in this kickoff increment.
- No alpha.4 distribution artifact exists yet.
- The four-workflow comparison was terminated after one completed workflow; no comparative superiority is claimed.
- The retained Core Candidate result is a DEGRADED single-case study.
- Formal release evidence and stable-release authorization are absent.
- The current published prerelease remains `MADP-v0.3.0-alpha.2` until a later publication action is completed.

## Rollback

The immutable published rollback target is `MADP-v0.3.0-alpha.2` at tag `MADP-v0.3.0-alpha.2`.
