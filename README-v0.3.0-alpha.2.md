# MADP v0.3.0-alpha.2 Draft README

> Draft prerelease planning version: `MADP-v0.3.0-alpha.2`
>
> Status: draft, not tagged, not published, and not release-ready.
>
> Published `MADP-v0.3.0-alpha.1` artifacts remain the current published alpha prerelease until a separate explicit release action occurs.

## Status

`MADP-v0.3.0-alpha.2` is a draft prerelease planning version for the Command and Context Relay Layer.

It extends the alpha.1 security and authority model with draft support for:

- structured MADP commands;
- command semantic-invalid fixtures for unsafe or ambiguous command input;
- a command registry for command-specific argument and authority rules;
- AI-to-AI or chat-to-chat context sharing;
- context package receipt validation;
- bounded review request and response validation;
- TODO tracking for future discussion and implementation planning;
- relay mode classification;
- command parse and missing-argument error artifacts;
- alpha.1 to alpha.2 draft migration fixtures;
- draft bootstrap prompts and alpha.2 bootstrap prompt generation.

This draft does not claim production readiness, stable command interoperability, release readiness, automatic external execution, or a complete permission-system redesign.

## Relationship to v0.3.0-alpha.1

`MADP-v0.3.0-alpha.1` remains the current published alpha prerelease.

alpha.2 is intended to be conservative:

- no automatic authority increase;
- no fabricated user approval;
- no external execution from command parsing alone;
- no TODO-to-decision promotion without explicit decision handling;
- no active-session auto-upgrade from alpha.1 to alpha.2.

The core safety rules continue to apply:

```text
A TODO is not a decision.
A decision is not approval.
Approval is not execution permission.
Raw command text is not authoritative by itself.
```

## Canonical draft sources

Draft normative sources:

- `protocol/MADP-v0.3.0-alpha.2.md`
- `protocol/GLOSSARY-v0.3.0-alpha.2.md`

Draft schemas:

- `schemas/v0.3.0-alpha.2/command.schema.yaml`
- `schemas/v0.3.0-alpha.2/command-registry.schema.yaml`
- `schemas/v0.3.0-alpha.2/todo.schema.yaml`
- `schemas/v0.3.0-alpha.2/context-package.schema.yaml`
- `schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml`
- `schemas/v0.3.0-alpha.2/review.schema.yaml`

Draft registries:

- `registries/v0.3.0-alpha.2/commands.yaml`

Draft planning and traceability:

- `docs/planning/MADP-v0.3.0-alpha.2-scope.md`
- `tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml`

Draft migration fixtures:

- `tests/migration-v0.3.0-alpha.2/README.md`
- `tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-001/`
- `tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-002/`

Draft bootstrap prompts:

- `bootstrap/use-madp-commands.md`
- `bootstrap/share-context-with-ai.md`
- `bootstrap/request-review.md`

Draft bootstrap generation:

- `scripts/generate_alpha2_bootstrap_prompts.py`
- `scripts/check_generated_alpha2_bootstrap.py`
- `scripts/test_generate_alpha2_bootstrap_prompts.py`

## New draft artifacts

### COMMAND_BLOCK

`COMMAND_BLOCK` is the canonical representation of a parsed MADP command.

Raw command input must be processed in this order:

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

Command classes introduced in the draft:

- `AI_COMMAND`
- `USER_COMMAND`
- `TODO_COMMAND`
- `EXTERNAL_ACTION_COMMAND`

A parseable or schema-valid command is not execution permission.

### Command registry

The command registry defines command-specific operational rules that are intentionally not encoded in the generic `COMMAND_BLOCK` schema.

Registry path:

```text
registries/v0.3.0-alpha.2/commands.yaml
```

Registry schema:

```text
schemas/v0.3.0-alpha.2/command-registry.schema.yaml
```

The registry records, for each command:

- command class;
- default authority boundary;
- required arguments;
- optional arguments;
- effect summary;
- safety notes;
- prohibited effects.

The registry checker verifies that command names match the `command.schema.yaml` enum, that required and optional arguments are not duplicated, and that sensitive commands keep conservative default authority.

Examples:

```yaml
approve:
  required_arguments: ["decision", "revision"]
  default_authority_boundary: "USER_CONFIRMED"

external-action:
  required_arguments: ["action", "scope"]
  default_authority_boundary: "REQUIRES_USER_CONFIRMATION"

todo-promote:
  default_authority_boundary: "REQUIRES_USER_CONFIRMATION"
```

### CONTEXT_PACKAGE and CONTEXT_PACKAGE_RECEIPT

`CONTEXT_PACKAGE` is a lightweight artifact for sharing context with another AI system or chat session without requiring a full deliberation relay.

It is intended for:

- information transfer;
- bounded review setup;
- task handoff;
- evidence or context packaging.

A context package is not a permission grant and must not be treated as user approval.

`CONTEXT_PACKAGE_RECEIPT` records how a receiver interprets a context package. It must keep `external_actions_allowed: false` and `user_approval_inferred: false`.

### REVIEW_REQUEST and REVIEW_RESPONSE

`REVIEW_REQUEST` and `REVIEW_RESPONSE` support bounded review without granting execution authority.

Review artifacts must preserve these constraints:

- authority boundary is `PROPOSE_ONLY`;
- external actions are not performed;
- user approval is not claimed;
- evidence and recommendations remain distinguishable.

### TODO_ITEM and TODO_LIST

`TODO_ITEM` records future work or future discussion.

TODO records can help track:

- discussion topics;
- design work;
- schema work;
- implementation tasks;
- validation work;
- documentation work;
- release preparation;
- safety review.

A TODO item does not approve a decision and does not authorize execution.

### relay_mode

alpha.2 drafts optional relay mode classification:

- `DELIBERATION`
- `INFORMATION_TRANSFER`
- `REVIEW_REQUEST`
- `TASK_HANDOFF`
- `EVIDENCE_TRANSFER`
- `RECOVERY`

Migration default for alpha.1 material without `relay_mode` is `DELIBERATION`.

### alpha.1 to alpha.2 migration fixtures

alpha.2 draft migration fixtures live separately from the published alpha.1 migration corpus:

```text
tests/migration-v0.3.0-alpha.2/
```

The draft migration checker verifies conservative migration planning invariants:

- active alpha.1 sessions are not silently auto-upgraded to alpha.2;
- alpha.1 relay material without `relay_mode` is interpreted as `DELIBERATION` only as proposed migration metadata;
- historical alpha.1 text that resembles `/madp` syntax is not retroactively applied as an alpha.2 command;
- user confirmation remains required for migration interpretation.

Run:

```bash
python scripts/check_migration_v030_alpha2.py
```

### alpha.2 bootstrap prompt generation

alpha.2 draft bootstrap prompt generation is intentionally separate from the published alpha.1 generator.

Generate draft prompts locally:

```bash
python scripts/generate_alpha2_bootstrap_prompts.py \
  tmp/generated-alpha2-bootstrap \
  --repository ExampleOwner/madp-alpha2-fixture \
  --commit-sha 0123456789abcdef0123456789abcdef01234567 \
  --workflow-run-id ALPHA2_LOCAL_TEST \
  --generated-by LOCAL
```

Check generated output:

```bash
python scripts/check_generated_alpha2_bootstrap.py tmp/generated-alpha2-bootstrap
```

The alpha.2 draft generator emits only:

- `bootstrap/use-madp-commands.md`
- `bootstrap/share-context-with-ai.md`
- `bootstrap/request-review.md`
- `bootstrap/alpha2-manifest.yaml`
- `index.html`

It does not publish a release and does not emit the alpha.1 complete protocol bundle.

## Command syntax draft

CLI-style surface form:

```text
/madp <command> [--key value] [--key=value] [--flag]
```

YAML command form:

```yaml
MADP_COMMAND:
  command: "todo-add"
  arguments:
    type: "DISCUSSION"
    title: "Define command syntax"
    priority: "HIGH"
```

Malformed commands must not be partially applied.

Missing required arguments should produce `COMMAND_NEEDS_ARGUMENTS`.

Malformed syntax should produce `COMMAND_PARSE_ERROR`.

Approval, authority, and external-action commands must not be silently repaired by AI.

## Fixtures

Draft fixtures are under `fixtures/v0.3.0-alpha.2/`.

```text
fixtures/v0.3.0-alpha.2/command/
fixtures/v0.3.0-alpha.2/todo/
fixtures/v0.3.0-alpha.2/context-package/
fixtures/v0.3.0-alpha.2/context-package-receipt/
fixtures/v0.3.0-alpha.2/review/
```

They contain `valid/`, schema-level `invalid/`, and command `semantic-invalid/` cases.

The current fixture set covers:

- valid TODO command normalization;
- valid approval command binding;
- command parse error shape;
- invalid unknown command;
- invalid applied parse error;
- semantic-invalid approval missing revision;
- semantic-invalid repeated option;
- semantic-invalid unknown option;
- semantic-invalid unconfirmed external action;
- semantic-invalid silent AI repair of an approval command;
- semantic-invalid quoted argument ambiguity;
- valid TODO list;
- invalid TODO status;
- valid context package;
- invalid context package attempting external execution;
- valid context package receipt;
- invalid context package receipt attempting external actions and approval inference;
- valid review request;
- valid review response;
- invalid review response claiming execution and user approval.

Semantic-invalid command fixtures are schema-valid `COMMAND_BLOCK` documents that should still be rejected by command semantics and authority checks.

## Validation

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run alpha.2 draft checks:

```bash
python scripts/check_traceability_v030_alpha2.py
python scripts/validate_alpha2_command_context_todo_fixtures.py
python scripts/check_command_semantic_invalid_fixtures_v030_alpha2.py
python scripts/check_command_registry_v030_alpha2.py
python scripts/check_migration_v030_alpha2.py
python scripts/check_release_readiness_v030_alpha2.py
```

The existing alpha.1 and rc.2 checks remain part of CI and must continue to pass.

Run the full validation workflow locally where practical:

```bash
python scripts/validate_schema.py
python scripts/validate_examples.py
python scripts/validate_semantics.py
python scripts/validate_participant_response.py
python scripts/check_markdown_links.py
python scripts/check_document_consistency.py
python scripts/check_bootstrap_prompts.py
python scripts/test_generate_bootstrap_prompts.py
python scripts/test_generate_alpha2_bootstrap_prompts.py
python scripts/check_traceability_v030.py
python scripts/check_traceability_v030_alpha2.py
python scripts/run_schema_fixture_checks.py all --json
python scripts/validate_alpha2_command_context_todo_fixtures.py
python scripts/check_command_semantic_invalid_fixtures_v030_alpha2.py
python scripts/check_command_registry_v030_alpha2.py
python scripts/check_migration_v030_alpha2.py
python scripts/check_migration_invariants_v030.py
python scripts/generate_artifacts.py --check
python scripts/check_schema_bundle_equivalence.py
python scripts/verify_jcs_vectors.py all --json
python scripts/check_release_readiness_v030.py
python scripts/check_release_readiness_v030_alpha2.py
```

## Bootstrap prompts

alpha.2 adds draft bootstrap aids:

- `bootstrap/use-madp-commands.md`
- `bootstrap/share-context-with-ai.md`
- `bootstrap/request-review.md`

These prompts are informative implementation aids. They do not override the protocol, glossary, schemas, user instructions, platform safety rules, or higher-priority authority.

They also do not authorize:

- external execution;
- file writes;
- commits;
- releases;
- user approval claims;
- treating model convergence as evidence.

## Draft readiness audit

The alpha.2 draft readiness audit checks that the draft has the expected minimum artifacts, schema IDs, required protocol phrases, glossary terms, traceability coverage, fixtures, semantic-invalid command fixtures, context package receipt fixtures, review fixtures, command registry, migration fixtures, bootstrap prompts, and alpha.2 bootstrap generation support.

Run:

```bash
python scripts/check_release_readiness_v030_alpha2.py
```

The audit intentionally reports:

```yaml
release_ready: false
draft_ready_for_review: true | false
```

A passing draft audit means the draft is internally reviewable. It does not authorize merge, tagging, release publication, or external execution.

## Release and authority boundaries

`MADP-v0.3.0-alpha.2` is not published by this file.

Publishing alpha.2 would require a separate explicit user-authorized sequence, including at minimum:

1. complete implementation and validation;
2. user approval to merge;
3. user approval to tag;
4. user approval to publish a release;
5. post-publication verification.

No draft artifact authorizes modifying or moving the published `MADP-v0.3.0-alpha.1` tag.

The user remains the sole final decision-maker for promotion, supersession, tagging, and publication.

## Known remaining work

- Decide whether generated alpha.2 bundle schemas are needed before tagging.
