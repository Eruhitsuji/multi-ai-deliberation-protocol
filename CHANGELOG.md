# Changelog

## Unreleased

## MADP-v0.2.5-rc.2

Status: Release candidate. Not final.

### Added

- A generated complete-protocol text bundle for environments without external URL retrieval.
- Manual-paste and uploaded-file recovery instructions.
- Explicit bundle provenance metadata.
- A companion bundle manifest with hashes.
- Operational evidence for Gemini uploaded-file recovery.
- Runtime load smoke-test evidence for Claude using commit-pinned Raw URLs.
- Runtime load smoke-test evidence for Gemini using the uploaded complete-protocol bundle.

### Changed

- Load-failure recovery now requires complete protocol loading before normal MADP processing resumes.
- Repository commit provenance is taken only from bundle metadata.
- Pages publishing now begins after validation succeeds.
- Pages deployment waits briefly for backend readiness.

### Fixed

- Prevented fixture SHA values in canonical content from being mistaken for the bundle source commit.

### Validation

- Claude loaded all four rc.2 canonical files through commit-pinned Raw URLs.
- Gemini loaded all four rc.2 canonical files through the uploaded complete bundle.
- Both reported the expected source commit.
- Formal JSON Schema execution was outside the scope of these runtime load tests.

## MADP-v0.2.5-rc.1

Status: Release candidate. Not final.

### Added

- Generated bootstrap prompts published through GitHub Pages.
- Participant-response serialization validation.
- Operational records for normal relay and malformed relay rejection.

### Validated

- Static schema and semantic checks.
- ChatGPT normal cross-chat relay.
- Single-YAML participant response.
- Fail-closed rejection of source-state/snapshot version mismatch.

### Remaining validation

- Additional AI model families.
- Additional malformed and stale relay cases.
- Broader facilitator recovery and concurrent-state tests.

### Previous version

- MADP-v0.2.5-draft
