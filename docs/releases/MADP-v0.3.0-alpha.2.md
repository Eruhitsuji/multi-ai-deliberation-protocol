# MADP-v0.3.0-alpha.2 Release Notes

## Status

`MADP-v0.3.0-alpha.2` is an unstable prerelease. The repository contents are prepared for tagging after the release-preparation PR is merged and the exact main commit is verified.

## Highlights

- Adds a registry-backed command layer with 20 commands.
- Implements strict CLI and YAML parsing, normalization, schema validation, authority evaluation, and bounded internal-state application.
- Requires explicit issuer handling for user commands.
- Adds trusted, scoped, single-use confirmation grants and replay protection.
- Adds TODO lifecycle enforcement with immutable terminal items.
- Adds context packages and receipts that transfer information without transferring authority.
- Adds structured review requests and responses under proposal-only boundaries.
- Adds relay modes and conservative alpha.1-to-alpha.2 migration fixtures.
- Adds an AI-driven development profile that separates edit, test, review, commit, push, PR, merge, tag, and release permissions.
- Adds English and Japanese explanatory documentation, onboarding, practical guides, and translation-governance checks.

## Safety and authority changes

The following distinctions are explicit throughout alpha.2:

```text
A TODO is not a decision.
A decision is not approval.
Approval is not execution permission.
A review is not merge approval.
A context package does not grant authority.
```

Malformed, unknown, stale, unsupported, or unauthorized inputs fail closed. The internal runtime never performs external actions.

## Validation

The release candidate is covered by:

- schema and semantic fixture validation;
- strict parser and all-command coverage tests;
- command authority and state-application tests;
- TODO lifecycle tests;
- AI-development profile checks;
- migration and traceability checks;
- reproducible standalone schema bundle generation;
- Markdown-link and document-consistency checks;
- English/Japanese translation-pair and metadata checks;
- release-readiness audit.

The exact workflow run and final release commit will be recorded when the release-preparation PR is merged and verified.

## Documentation

- `README-v0.3.0-alpha.2.md`
- `protocol/MADP-v0.3.0-alpha.2.md`
- `protocol/GLOSSARY-v0.3.0-alpha.2.md`
- `docs/en/`
- `docs/ja/`
- `README.ja.md`

## Compatibility

Published historical tags remain immutable. Active sessions must not auto-upgrade. Migration from alpha.1 must be explicit and fail closed where authority cannot be verified.

## Known limitations

- This is an alpha prerelease and may change incompatibly.
- Cryptographic issuer provenance is not implemented.
- Full stale-parent and state-lineage enforcement remain future hardening work.
- The apply runtime operates only on its explicit internal runtime state and does not execute external operations.
- Formal universal interoperability is not claimed.

## Publication procedure

1. Merge the release-preparation PR after all checks pass.
2. Verify the resulting main commit and its CI evidence.
3. Create tag `MADP-v0.3.0-alpha.2` at that exact commit.
4. Create a GitHub prerelease using these notes.
5. Verify the tag, release page, downloadable source archives, and canonical file links.
6. Record the final release commit and publication timestamp in repository metadata in a follow-up maintenance change.
