# Changelog

## Unreleased

### Added

- A generated complete-protocol text bundle for environments without external URL retrieval.
- Manual-paste recovery instructions for protocol load failures.

### Changed

- Load-failure recovery now directs users to paste the complete generated bundle before normal MADP processing resumes.

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
