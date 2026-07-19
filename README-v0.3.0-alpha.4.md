# MADP v0.3.0-alpha.4 — Practical Core Integration and Fix-Forward Delivery

Status: Core Usability Slice 1 implemented on a feature branch. This version is
not release-ready, tagged, published, or a stable release.

MADP v0.3.0-alpha.4 is a short-cycle prerelease line focused on reducing human
operating burden while preserving explicit authority, evidence, provenance, and
revision boundaries.

The implementation direction is authorized by:

- `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-001.yaml`
- `docs/planning/DEC-MADP-ALPHA4-002.yaml`

## Current implementation

The first Core Usability slice adds:

- a normative additive Core Usability extension over alpha.3;
- eight versioned, non-atomic Workflow Macros;
- a macro registry whose steps remain canonical alpha.3 commands;
- an additive Claim, Evidence, Dissent, Human Decision, and migration record;
- explicit raw-response preservation;
- separate dissent status and human disposition;
- separate decision and external-action authorization;
- executable schema-positive, schema-negative, and semantic-negative fixtures;
- a dedicated GitHub Actions validation path.

Normative and executable artifacts:

- [`protocol/MADP-v0.3.0-alpha.4-core-usability.md`](protocol/MADP-v0.3.0-alpha.4-core-usability.md)
- [`docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md`](docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md)
- [`registries/v0.3.0-alpha.4/workflow-macros.yaml`](registries/v0.3.0-alpha.4/workflow-macros.yaml)
- [`schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml`](schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml)
- [`tests/v0.3.0-alpha.4/core-usability-fixtures.yaml`](tests/v0.3.0-alpha.4/core-usability-fixtures.yaml)

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

Macros are guided workflows, not canonical commands, aliases, atomic
transactions, or authority grants. Accepted machine operations are still
recorded as canonical alpha.3 commands with exact identifiers, revisions, and
state versions.

## Claim, Evidence, Dissent, and Decision

Alpha.4 separates:

- `claim_kind` from `verification_status`;
- Evidence from the Claim it supports or challenges;
- dissent `status` from human `disposition`;
- a Human Final Authority Decision from external-action authorization.

Existing alpha.3 `FACT` records remain valid historical inputs. Migration must
preserve the original record and revision and must not silently upgrade
verification.

Agreement among AI systems is not evidence. AI agreement, vote count, or
convergence cannot replace the human decision.

## Compatibility

This slice:

- preserves the alpha.3 canonical command namespace;
- does not modify alpha.3 schemas;
- preserves legacy `FACT` records;
- leaves alpha.3 artifacts historical and unchanged;
- adds only versioned alpha.4 artifacts.

## GitHub-first development

Alpha.4 development treats GitHub branches, pull requests, Actions, and
generated artifacts as first-class. A local checkout is optional.

## Release model

Alpha.4 follows `RELEASE_EARLY_FIX_FORWARD` for a single-primary-user phase.
Short prerelease increments may proceed without completing the terminated
four-workflow comparison or the alpha.3 stable-release gates.

Tagging, GitHub Release creation, Pages publication, and stable-release
authorization remain separate actions.

## Known limitations

- The alpha.4 bootstrap, load profile, generated distribution, and release
  package are not implemented yet.
- The Core Usability record is not yet included in a deterministic alpha.4
  bundle.
- No new canonical command namespace is introduced in this slice.
- The four-workflow comparison was terminated after one completed workflow; no
  comparative superiority is claimed.
- The retained Core Candidate result is a DEGRADED single-case study.
- Formal release evidence and stable-release authorization are absent.
- The current published prerelease remains `MADP-v0.3.0-alpha.2`.

## Rollback

The immutable published rollback target is `MADP-v0.3.0-alpha.2` at tag
`MADP-v0.3.0-alpha.2`.
