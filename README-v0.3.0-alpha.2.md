# MADP v0.3.0-alpha.2 Draft README

> Draft prerelease planning version: `MADP-v0.3.0-alpha.2`
>
> Status: draft, not tagged, not published, and not release-ready.
>
> Published `MADP-v0.3.0-alpha.1` remains the current published alpha prerelease until a separate explicit release action occurs.

## Status

`MADP-v0.3.0-alpha.2` is the draft Command, Context Relay, TODO, Review, and AI-Driven Development layer.

The draft currently includes:

- structured `COMMAND_BLOCK` processing;
- command registry and semantic-invalid command fixtures;
- `CONTEXT_PACKAGE` and `CONTEXT_PACKAGE_RECEIPT`;
- `REVIEW_REQUEST` and `REVIEW_RESPONSE`;
- TODO lifecycle artifacts;
- relay mode classification;
- conservative alpha.1-to-alpha.2 migration fixtures;
- generated alpha.2 bootstrap prompts;
- an AI-driven development profile for coding agents such as Codex and Claude Code.

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

Draft registry:

- `registries/v0.3.0-alpha.2/commands.yaml`

Planning and traceability:

- `docs/planning/MADP-v0.3.0-alpha.2-scope.md`
- `tests/traceability/traceability-matrix-v0.3.0-alpha.2.yaml`

## Command and authority model

Raw command text is never authoritative by itself.

```text
Parse first.
Normalize second.
Validate third.
Authorize fourth.
Apply last.
```

Recognized command classes are:

- `AI_COMMAND`
- `USER_COMMAND`
- `TODO_COMMAND`
- `EXTERNAL_ACTION_COMMAND`

The command registry defines per-command arguments, default authority boundaries, safety notes, and prohibited effects.

Sensitive examples:

```yaml
approve:
  required_arguments: ["decision", "revision"]

external-action:
  required_arguments: ["action", "scope"]
  default_authority_boundary: "REQUIRES_USER_CONFIRMATION"

todo-promote:
  default_authority_boundary: "REQUIRES_USER_CONFIRMATION"
```

A parseable or schema-valid command is not execution permission.

## Context sharing and review

`CONTEXT_PACKAGE` transfers bounded context without granting authority.

`CONTEXT_PACKAGE_RECEIPT` records what the receiving AI understood, what remains limited, and the authority boundary applied. It must not infer user approval or permit external actions by itself.

`REVIEW_REQUEST` and `REVIEW_RESPONSE` support bounded review under `PROPOSE_ONLY` authority. Review findings may inform a user decision, but they are not user approval and are not merge authorization.

## AI-driven development profile

The AI-driven development profile supports coding agents such as Codex, Claude Code, and similar tools.

Profile files:

- `docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md`
- `bootstrap/use-madp-for-ai-driven-development.md`
- `scripts/check_ai_development_profile_v030_alpha2.py`

Profile fixtures:

- `fixtures/v0.3.0-alpha.2/ai-development/valid/coding-task-handoff.context-package.yaml`
- `fixtures/v0.3.0-alpha.2/ai-development/valid/review-before-commit.review.yaml`
- `fixtures/v0.3.0-alpha.2/ai-development/invalid/auto-commit-without-approval.command.yaml`

The profile separates these stages:

```text
analysis -> proposal -> edit -> test -> review -> commit -> push -> PR -> merge -> tag -> release
```

Later stages do not inherit authority from earlier stages. In particular:

- a patch is not edit permission;
- an edit is not commit permission;
- a commit is not push permission;
- a review is not merge permission;
- a passing CI run is not release permission.

Coding agents should return `AI_DEVELOPMENT_STATUS` with files read, files changed, tests run, skipped checks, assumptions, limitations, external-action state, and the next required user decision.

## Fixtures

Draft fixtures are under `fixtures/v0.3.0-alpha.2/`:

- `command/`
- `todo/`
- `context-package/`
- `context-package-receipt/`
- `review/`
- `ai-development/`

The fixture corpus covers schema-valid, schema-invalid, and semantic-invalid cases, including:

- missing approval revision;
- repeated or unknown command options;
- ambiguous quoted command input;
- unconfirmed external actions;
- silent AI repair of an approval command;
- context packages that attempt external execution;
- receipts that infer approval;
- review responses that claim execution;
- coding-agent commit requests without a confirmation reference.

## Migration

alpha.2 migration fixtures are separate from the published alpha.1 fixture corpus:

- `tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-001/`
- `tests/migration-v0.3.0-alpha.2/A2-MIG-FIX-002/`

The migration checker verifies that:

- active alpha.1 sessions are not silently upgraded;
- absent alpha.1 `relay_mode` is interpreted conservatively as `DELIBERATION`;
- historical `/madp`-like text is not replayed as an alpha.2 command;
- published alpha.1 tags remain immutable.

## Bootstrap generation

alpha.2 bootstrap generation is intentionally separate from the published alpha.1 generator.

Templates generated by `scripts/generate_alpha2_bootstrap_prompts.py`:

- `bootstrap/use-madp-commands.md`
- `bootstrap/share-context-with-ai.md`
- `bootstrap/request-review.md`
- `bootstrap/use-madp-for-ai-driven-development.md`

Generated output also contains `bootstrap/alpha2-manifest.yaml` and `index.html`.

Example:

```bash
python scripts/generate_alpha2_bootstrap_prompts.py \
  tmp/generated-alpha2-bootstrap \
  --repository ExampleOwner/madp-alpha2-fixture \
  --commit-sha 0123456789abcdef0123456789abcdef01234567 \
  --workflow-run-id ALPHA2_LOCAL_TEST \
  --generated-by LOCAL

python scripts/check_generated_alpha2_bootstrap.py \
  tmp/generated-alpha2-bootstrap
```

The generator creates draft implementation aids only. It does not publish a release and does not emit the alpha.1 complete protocol bundle.

## Validation

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the main alpha.2 checks:

```bash
python scripts/test_generate_alpha2_bootstrap_prompts.py
python scripts/check_generated_alpha2_bootstrap.py tmp/generated-alpha2-bootstrap
python scripts/check_traceability_v030_alpha2.py
python scripts/validate_alpha2_command_context_todo_fixtures.py
python scripts/check_command_semantic_invalid_fixtures_v030_alpha2.py
python scripts/check_command_registry_v030_alpha2.py
python scripts/check_ai_development_profile_v030_alpha2.py
python scripts/check_migration_v030_alpha2.py
python scripts/check_release_readiness_v030_alpha2.py
```

The existing rc.2 and alpha.1 validation paths remain in CI and must continue to pass.

## Draft readiness audit

The alpha.2 draft readiness audit checks required files, schema IDs, protocol phrases, glossary terms, traceability coverage, fixtures, command registry, migration artifacts, bootstrap prompts, bootstrap generation support, and the AI-driven development profile.

The audit intentionally reports:

```yaml
release_ready: false
draft_ready_for_review: true | false
```

A passing draft audit means the draft is internally reviewable. It does not authorize merge, tagging, release publication, or external execution.

## Release and authority boundaries

`MADP-v0.3.0-alpha.2` is not published by this file.

Implementation completion, review, merge, tagging, and release publication are separate actions. Each requires its own applicable user authorization.

No draft artifact authorizes modifying or moving the published `MADP-v0.3.0-alpha.1` tag.

The user remains the sole final decision-maker for promotion, supersession, tagging, and publication.

## Known remaining work

- Decide whether generated alpha.2 bundle schemas are needed before tagging.
- Decide whether the AI-driven development profile should become a normative protocol section in a later prerelease.
