# Multi-AI Deliberation Protocol (MADP)

English | [日本語](README.ja.md)

> Current published prerelease: **MADP-v0.3.0-alpha.2**
>
> Release tag: `MADP-v0.3.0-alpha.2`
>
> Release commit: `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9`

MADP is a service-neutral protocol for structured deliberation with AI systems, role-separated instances, human validators, and execution agents. It supports research, design, review, software development, and everyday decisions while keeping the user as the sole final decision-maker.

## Start here

1. Read the [English documentation index](docs/en/README.md) or [Japanese documentation index](docs/ja/README.md).
2. Use [Basic usage and workflow selection](docs/en/basic-usage.md) to define the issue and choose a deliberation pattern.
3. Select a practical workflow from the [Practical guide index](docs/en/practical-guides.md).

For a first trial, use [one model in one chat](docs/en/single-model-single-chat.md). Use [one model across multiple chats](docs/en/single-model-multi-chat.md) for stronger role separation, or [multiple AI models](docs/en/multi-model-deliberation.md) when model diversity matters.

## Current release status

```yaml
current_published_prerelease: MADP-v0.3.0-alpha.2
release_tag: MADP-v0.3.0-alpha.2
release_commit: 207e24290e0a66bf0dd34e13f9b3525a42a5a6c9
release_preparation_workflow_run: 29135177099
release_preparation_workflow_result: success
tagged: true
published: true
published_at: UNKNOWN
previous_published_prerelease: MADP-v0.3.0-alpha.1
historical_compatibility_release_candidate: MADP-v0.2.5-rc.2
status: published unstable prerelease
```

The authoritative GitHub Release publication timestamp could not be retrieved through the available connector, so repository metadata records `published_at: UNKNOWN` rather than guessing. The release tag was independently verified to resolve exactly to the expected release commit.

## Status and canonical files

This section is retained for the repository's rc.2 compatibility checks. It does not override the current published alpha.2 status above.

```yaml
current_release_candidate: "MADP-v0.2.5-rc.2"
previous_release_candidate: "MADP-v0.2.5-rc.1"
previous_draft: "MADP-v0.2.5-draft"
```

Historical rc.2 canonical files retained for compatibility testing:

- [`protocol/MADP-v0.2.5-rc.2.md`](protocol/MADP-v0.2.5-rc.2.md)
- [`protocol/GLOSSARY-v0.2.5-rc.2.md`](protocol/GLOSSARY-v0.2.5-rc.2.md)
- [`schemas/session-state-v0.2.5-rc.2.schema.yaml`](schemas/session-state-v0.2.5-rc.2.schema.yaml)

Published historical tags are immutable. The rc.2 compatibility marker is not the current published prerelease.

## Core principles

- The user is the sole final decision-maker.
- A TODO is not a decision.
- A decision is not approval.
- Approval is not execution permission.
- A review is not merge approval.
- Agreement among AI systems is convergence, not evidence.
- Context transfer does not transfer authority.
- Unknown actions, empty scopes, stale states, and unsupported inputs fail closed.
- External or irreversible actions require explicit action-specific user authorization.

## Alpha.2 highlights

- registry-backed command layer with 20 commands;
- strict CLI and YAML parsing and normalization;
- schema validation, authority evaluation, and bounded internal-state application;
- trusted, scoped, single-use confirmation grants and replay protection;
- TODO lifecycle enforcement with immutable terminal items;
- context packages and receipts that transfer information without authority;
- structured review requests and responses under proposal-only boundaries;
- relay modes and conservative alpha.1-to-alpha.2 migration fixtures;
- AI-driven development boundaries for edit, test, review, commit, push, PR, merge, tag, and release;
- English and Japanese onboarding, practical guides, and translation-governance checks.

## Canonical alpha.2 sources

The canonical normative sources are English:

- [MADP-v0.3.0-alpha.2 protocol](protocol/MADP-v0.3.0-alpha.2.md)
- [MADP-v0.3.0-alpha.2 glossary](protocol/GLOSSARY-v0.3.0-alpha.2.md)
- [Alpha.2 schemas](schemas/v0.3.0-alpha.2/)
- [Alpha.2 command registry](registries/v0.3.0-alpha.2/commands.yaml)
- [AI-driven development profile](docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md)
- [Alpha.2 prerelease README](README-v0.3.0-alpha.2.md)
- [Alpha.2 release notes](docs/releases/MADP-v0.3.0-alpha.2.md)

Japanese documents are non-normative explanatory translations. If a translation conflicts with the English protocol, schemas, or registries, the English normative source takes precedence.

## Practical documentation

### Deliberation patterns

- [Multiple AI models](docs/en/multi-model-deliberation.md)
- [One model across multiple chats](docs/en/single-model-multi-chat.md)
- [One model in one chat](docs/en/single-model-single-chat.md)

### Applied workflows

- [AI-driven development](docs/en/ai-development.md)
- [Context sharing and relay](docs/en/context-relay.md)
- [TODO lifecycle](docs/en/todo-lifecycle.md)
- [Review workflow](docs/en/review-workflow.md)
- [Authority model](docs/en/authority-model.md)
- [Commands](docs/en/commands.md)

## Command safety pipeline

Raw command text is never authoritative by itself.

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

The alpha.2 apply runtime operates only on its explicit internal runtime state model. It does not execute external actions.

## Legacy compatibility example

The following minimal `SESSION_STATE` remains in the root README so the retained rc.2 compatibility validator continues to exercise a schema-valid example. New alpha.2 work should use the versioned alpha.2 protocol, schemas, commands, and practical guides instead.

```yaml
session_state:
  meta:
    protocol: "MADP"
    protocol_version: "0.2.5-rc.2"
    schema_version: "0.2.5-rc.2"
    session_id: "MADP-EXAMPLE-001"
    state_version: 1
    parent_version: 0
    updated_at: "UNKNOWN"
    updated_by: "facilitator"

  goal: "Select a minimum release structure"

  current_issue:
    id: "ISSUE-001"
    status: "IN_PROGRESS"
    question: "Which files are required?"

  participants:
    - actor_id: "facilitator"
      type: "FACILITATOR"
      role: "FACILITATOR"
      status: "ACTIVE"

  decisions:
    - id: "DEC-001"
      revision: 1
      deliberation_outcome: "USER_DECISION_REQUIRED"
      approval_status: "PENDING"
      summary: "No release structure has been approved yet."

  next_step:
    internal:
      actor: "FACILITATOR"
      task: "Evaluate the minimum structure"
      blocking_input: null
    user:
      action_required: false
      prompt_action: "NO_ACTION_REQUIRED"
      task: null
      response_format: null
```

## Validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/check_markdown_links.py
python scripts/check_document_consistency.py
python scripts/check_translation_docs.py
python scripts/check_traceability_v030_alpha2.py
python scripts/validate_alpha2_command_context_todo_fixtures.py
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

The release-preparation workflow passed as run `29135177099`. Post-publication verification confirmed that tag `MADP-v0.3.0-alpha.2` and commit `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9` are identical.

## Historical versions

Published historical tags are immutable. Active sessions must not auto-upgrade.

- [MADP-v0.3.0-alpha.1 prerelease README](README-v0.3.0-alpha.1.md)
- [MADP-v0.3.0-alpha.1 protocol](protocol/MADP-v0.3.0-alpha.1.md)
- [MADP-v0.3.0-alpha.1 glossary](protocol/GLOSSARY-v0.3.0-alpha.1.md)
- [MADP-v0.2.5-rc.2 protocol](protocol/MADP-v0.2.5-rc.2.md)
- [MADP-v0.2.5-rc.2 glossary](protocol/GLOSSARY-v0.2.5-rc.2.md)
- [MADP-v0.2.5-rc.2 schema](schemas/session-state-v0.2.5-rc.2.schema.yaml)

Migration from alpha.1 must be explicit and fail closed where authority cannot be verified.

## Known limitations

- alpha.2 is an unstable prerelease and may change incompatibly;
- cryptographic issuer provenance is not implemented;
- complete stale-parent and state-lineage enforcement remain future hardening work;
- the runtime does not execute external operations;
- formal universal interoperability is not claimed.

## License

Licensed under the [MIT License](LICENSE).
