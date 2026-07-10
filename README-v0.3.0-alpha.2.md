# MADP v0.3.0-alpha.2 Draft README

> Draft prerelease planning version: `MADP-v0.3.0-alpha.2`
>
> Status: draft, not tagged, not published, and not release-ready.
>
> Published `MADP-v0.3.0-alpha.1` remains the current published alpha prerelease until a separate explicit release action occurs.

## Status

`MADP-v0.3.0-alpha.2` is the draft Command, Context Relay, TODO, Review, Relay Mode, and AI-Driven Development layer.

The implemented draft includes:

- structured `COMMAND_BLOCK` processing;
- an executable CLI/YAML command parser and normalizer;
- an authority evaluator and bounded internal-state apply runtime;
- registry-driven coverage for all 20 commands;
- semantic-invalid command fixtures;
- `CONTEXT_PACKAGE` and `CONTEXT_PACKAGE_RECEIPT`;
- `REVIEW_REQUEST` and `REVIEW_RESPONSE`;
- TODO schema and lifecycle transition checks;
- a schema-validated `relay_mode` extension;
- conservative alpha.1-to-alpha.2 migration fixtures;
- generated alpha.2 bootstrap prompts;
- an AI-driven development profile for Codex, Claude Code, and similar coding agents;
- seven reproducible standalone schema bundles generated in CI.

The core safety rules remain:

```text
A TODO is not a decision.
A decision is not approval.
Approval is not execution permission.
A review is not merge approval.
A patch proposal is not repository modification permission.
```

## Canonical draft sources

Normative draft sources:

- `protocol/MADP-v0.3.0-alpha.2.md`
- `protocol/GLOSSARY-v0.3.0-alpha.2.md`

Application profile:

- `docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md`

Draft schemas:

- `schemas/v0.3.0-alpha.2/command.schema.yaml`
- `schemas/v0.3.0-alpha.2/command-registry.schema.yaml`
- `schemas/v0.3.0-alpha.2/todo.schema.yaml`
- `schemas/v0.3.0-alpha.2/context-package.schema.yaml`
- `schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml`
- `schemas/v0.3.0-alpha.2/review.schema.yaml`
- `schemas/v0.3.0-alpha.2/relay.schema.yaml`

Registry and traceability:

- `registries/v0.3.0-alpha.2/commands.yaml`
- `tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml`

## Command implementation

Raw command text is never authoritative by itself.

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

The parser supports:

```text
/madp <command> [--key value] [--key=value] [--flag]
```

and:

```yaml
MADP_COMMAND:
  command: "todo-add"
  arguments:
    title: "Write tests"
```

Implementation files:

- `scripts/parse_command_v030_alpha2.py`
- `scripts/apply_command_v030_alpha2.py`
- `scripts/test_command_parser_v030_alpha2.py`
- `scripts/test_command_runtime_v030_alpha2.py`
- `scripts/check_all_commands_v030_alpha2.py`

The parser rejects unknown commands, unknown options, repeated `SCALAR` options, unbound tokens, malformed quoting, duplicate YAML keys, YAML anchors or aliases, invalid semantic values, and missing required arguments. Repeated `LIST` options accumulate in input order when the registry declares list cardinality. All 20 registry commands are exercised with minimum valid arguments and missing-argument cases.

A parseable or schema-valid command is not execution permission. `USER_COMMAND` execution requires an explicit trusted `issued_by: USER` assertion from the invoking environment. Confirmation grants are assurance-checked and single-use by default. External-action commands remain non-executable in alpha.2.

Authorized read-only commands may append command history and advance `state_version`, but they do not report `effect_applied: true`. Commands that fail parsing, validation, or authorization do not append history, do not increment `state_version`, and return `state_changed: false`.

## TODO lifecycle

TODO lifecycle semantics are tested separately from schema enums.

- shared transition table: `scripts/todo_transitions_v030_alpha2.py`
- lifecycle cases: `tests/todo-lifecycle-v0.3.0-alpha.2/cases.yaml`
- checker: `scripts/check_todo_lifecycle_v030_alpha2.py`

Covered transitions include:

- `OPEN -> IN_PROGRESS`;
- `OPEN -> BLOCKED`;
- `IN_PROGRESS -> BLOCKED`;
- `BLOCKED -> IN_PROGRESS`;
- `IN_PROGRESS -> DONE` with `todo-done` and a completion basis;
- `OPEN -> DEFERRED`;
- `DEFERRED -> OPEN`;
- denial of terminal-state reopening;
- denial of terminal-item metadata updates;
- denial of `DONE` without a completion basis;
- confirmation requirements for `todo-promote`.

`DONE` and `CANCELLED` TODO items are immutable in the alpha.2 runtime. Their status, title, priority, owner, blocking reason, and completion evidence cannot be changed through `todo-update`.

## Context sharing, review, and relay mode

`CONTEXT_PACKAGE` transfers bounded context without granting authority.

`CONTEXT_PACKAGE_RECEIPT` records what the receiving AI understood and must not infer user approval or permit external actions by itself.

`REVIEW_REQUEST` and `REVIEW_RESPONSE` support bounded review under `PROPOSE_ONLY` authority.

`schemas/v0.3.0-alpha.2/relay.schema.yaml` validates these relay modes:

- `DELIBERATION`
- `INFORMATION_TRANSFER`
- `REVIEW_REQUEST`
- `TASK_HANDOFF`
- `EVIDENCE_TRANSFER`
- `RECOVERY`

Relay fixtures verify that relay metadata does not grant external-action authority or infer user approval.

## AI-driven development profile

The profile supports coding agents such as Codex and Claude Code.

- `docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md`
- `bootstrap/use-madp-for-ai-driven-development.md`
- `scripts/check_ai_development_profile_v030_alpha2.py`

The profile separates:

```text
analysis -> proposal -> edit -> test -> review -> commit -> push -> PR -> merge -> tag -> release
```

Later stages do not inherit authority from earlier stages.

## Fixtures

Draft fixtures are under `fixtures/v0.3.0-alpha.2/`:

- `command/`
- `todo/`
- `context-package/`
- `context-package-receipt/`
- `review/`
- `relay/`
- `ai-development/`

## Bootstrap generation

Templates generated by `scripts/generate_alpha2_bootstrap_prompts.py`:

- `bootstrap/use-madp-commands.md`
- `bootstrap/share-context-with-ai.md`
- `bootstrap/request-review.md`
- `bootstrap/use-madp-for-ai-driven-development.md`

Generated output also contains `bootstrap/alpha2-manifest.yaml` and `index.html`.

## Standalone schema bundles

`scripts/generate_alpha2_schema_bundles.py` produces deterministic standalone JSON schema bundles for:

- command;
- command registry;
- TODO;
- context package;
- context package receipt;
- review;
- relay.

Generate and check them with:

```bash
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas --check
```

The CI policy is to generate these distributions into a temporary directory and upload them as a GitHub Actions artifact. They are not committed under `schemas/generated/` in this draft.

## Validation

```bash
python -m pip install -r requirements-dev.txt
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
python scripts/check_migration_v030_alpha2.py
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas
python scripts/generate_alpha2_schema_bundles.py --output-dir tmp/generated-alpha2-schemas --check
python scripts/check_release_readiness_v030_alpha2.py
```

## Draft readiness audit

The audit verifies required files, all seven schema IDs, parser and all-command coverage, command authority/apply runtime tests, TODO lifecycle checks, relay fixtures, migration artifacts, bootstrap generation, AI-driven development support, traceability, and schema bundle configuration.

It intentionally reports:

```yaml
release_ready: false
draft_ready_for_review: true | false
```

A passing draft audit does not authorize merge, tagging, release publication, or external execution.

## Release and authority boundaries

`MADP-v0.3.0-alpha.2` is not published by this file.

Implementation completion, review, merge, tagging, and release publication are separate actions. Each requires its own applicable user authorization.

No draft artifact authorizes modifying or moving the published `MADP-v0.3.0-alpha.1` tag.

The user remains the sole final decision-maker for promotion, supersession, tagging, and publication.

## Known remaining work

No planned alpha.2 implementation item is currently marked as unimplemented. Remaining work is release governance: final review, merge authorization, tag authorization, release publication authorization, and post-publication verification. Later-version hardening may include cryptographic issuer provenance, state-lineage and stale-parent checks, and registry-derived argument type metadata.
