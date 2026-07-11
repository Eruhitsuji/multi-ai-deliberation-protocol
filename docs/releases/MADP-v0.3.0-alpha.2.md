# MADP-v0.3.0-alpha.2 Release Notes

## Status

`MADP-v0.3.0-alpha.2` is a published unstable prerelease.

```yaml
release_tag: MADP-v0.3.0-alpha.2
release_commit: 207e24290e0a66bf0dd34e13f9b3525a42a5a6c9
release_preparation_workflow_run: 29135177099
release_preparation_workflow_result: success
post_publication_tag_verification: identical
published_at: UNKNOWN
```

The user confirmed that the release operation completed. The tag was independently verified to resolve exactly to the expected release commit. The authoritative GitHub Release publication timestamp could not be retrieved through the available connector and is therefore recorded as `UNKNOWN` rather than guessed.

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

The published release candidate was covered by:

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

The complete release-preparation workflow succeeded as run `29135177099`. After publication, tag `MADP-v0.3.0-alpha.2` was compared with commit `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9` and reported `identical`, with no commits ahead or behind.

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
- The authoritative GitHub Release publication timestamp remains unrecorded in the repository.

## Publication verification

1. Release-preparation PR #5 was merged.
2. The release merge commit was verified as `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9`.
3. Tag `MADP-v0.3.0-alpha.2` was created.
4. The user confirmed that the GitHub release operation completed.
5. The tag and expected release commit were compared and found identical.
6. This maintenance change records the publication state in repository metadata.
