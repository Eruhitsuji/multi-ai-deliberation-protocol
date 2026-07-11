# MADP v0.3.0-alpha.2 Prerelease README

> Release candidate status for `MADP-v0.3.0-alpha.2`.
>
> This repository state is release-ready, but the tag and GitHub Release have not yet been created.

## Status

```yaml
protocol_version: MADP-v0.3.0-alpha.2
implementation_status: RELEASE_CANDIDATE_READY
integration_status: MERGED_TO_MAIN
release_ready: true
tagged: false
published: false
```

`MADP-v0.3.0-alpha.1` remains the currently published alpha until the separately authorized tag and GitHub Release actions complete.

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

A passing audit means the repository contents are ready to be tagged from the exact verified main commit. It does not itself create the tag or publish the GitHub Release.

## Release notes

See `docs/releases/MADP-v0.3.0-alpha.2.md`.

## Known limitations

- alpha.2 is an unstable prerelease and may change incompatibly;
- the apply runtime updates only its explicit internal state model and never performs external actions;
- cryptographic issuer provenance is not implemented;
- stale-parent and full state-lineage enforcement remain future hardening work;
- universal interoperability is not claimed.

## Publication boundary

Tagging and GitHub Release publication remain separate user-authorized actions. After publication, repository metadata should record the final release commit, tag, publication timestamp, and successful post-publication verification.
