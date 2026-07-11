# MADP v0.3.0-alpha.2 Prerelease README

> Published prerelease status for `MADP-v0.3.0-alpha.2`.
>
> Tag `MADP-v0.3.0-alpha.2` points to release commit `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9`.

## Status

```yaml
protocol_version: MADP-v0.3.0-alpha.2
implementation_status: PUBLISHED_PRERELEASE
integration_status: MERGED_TO_MAIN
release_ready: true
tagged: true
published: true
release_tag: MADP-v0.3.0-alpha.2
release_commit: 207e24290e0a66bf0dd34e13f9b3525a42a5a6c9
published_at: UNKNOWN
```

The publication timestamp remains `UNKNOWN` in repository metadata because the available connector could not independently retrieve the authoritative GitHub Release timestamp. The user confirmed that the release operation completed, and the tag target was independently verified against the expected release commit.

## What alpha.2 adds

- structured `COMMAND_BLOCK` parsing, normalization, validation, authorization, and bounded internal-state application;
- registry-backed coverage for all 20 commands;
- strict YAML handling, including duplicate-key, anchor, alias, and custom-tag rejection;
- explicit issuer handling and trusted, single-use confirmation grants;
- TODO schema and lifecycle enforcement, including immutable terminal items;
- context packages and receipts that transfer information without authority;
- review request and response artifacts under `PROPOSE_ONLY` boundaries;
- relay modes and alpha.1-to-alpha.2 migration fixtures;
- an AI-driven development profile with separate edit, test, review, commit, push, merge, tag, and release boundaries;
- bilingual English/Japanese explanatory documentation and practical usage guides;
- reproducible standalone schema bundles generated in CI.

## Core safety rules

```text
A TODO is not a decision.
A decision is not approval.
Approval is not execution permission.
A review is not merge approval.
A patch proposal is not repository modification permission.
```

Raw command text is never authoritative by itself.

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

## Canonical sources

- `protocol/MADP-v0.3.0-alpha.2.md`
- `protocol/GLOSSARY-v0.3.0-alpha.2.md`
- `schemas/v0.3.0-alpha.2/`
- `registries/v0.3.0-alpha.2/commands.yaml`
- `docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md`

## Explanatory documentation

- `docs/en/`
- `docs/ja/`
- `README.ja.md`

The English protocol, schemas, and registries remain normative. Japanese documents are non-normative explanatory translations.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/check_markdown_links.py
python scripts/check_document_consistency.py
python scripts/check_translation_docs.py
python scripts/test_generate_alpha2_bootstrap_prompts.py
python scripts/check_traceability_v030_alpha2.py
python scripts/validate_alpha2_command_context_todo_fixtures.py
python scripts/check_command_semantic_invalid_fixtures_v030_alpha2.py
python scripts/check_command_registry_v030_alpha2.py
python scripts/test_command_parser_v030_alpha2.py
python scripts/check_all_commands_v030_alpha2.py
python scripts/test_command_runtime_v030_alpha2.py
python scripts/check_todo_lifecycle_v030_alpha2.py
python scripts/check_ai_development_profile_v030_alpha2.py
python scripts/check_alpha2_implementation_status.py
python scripts/check_migration_v030_alpha2.py
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas --check
python scripts/check_release_readiness_v030_alpha2.py
```

The release-preparation PR head passed the complete repository validation workflow before merge. The published tag was then verified to resolve exactly to the release merge commit.

## Release notes

See `docs/releases/MADP-v0.3.0-alpha.2.md`.

## Known limitations

- alpha.2 is an unstable prerelease and may change incompatibly;
- the apply runtime updates only its explicit internal state model and never performs external actions;
- cryptographic issuer provenance is not implemented;
- stale-parent and full state-lineage enforcement remain future hardening work;
- universal interoperability is not claimed.

## Publication record

```yaml
release_tag: MADP-v0.3.0-alpha.2
release_commit: 207e24290e0a66bf0dd34e13f9b3525a42a5a6c9
release_preparation_workflow_run: 29135177099
release_preparation_workflow_result: success
post_publication_tag_verification: identical
published_at: UNKNOWN
```
