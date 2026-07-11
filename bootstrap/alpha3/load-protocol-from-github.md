---
bootstrap_version: 0.6-draft
protocol_version: MADP-v0.3.0-alpha.3
bootstrap_role: PROTOCOL_LOADER
repository_template: "{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}"
commit_template: "{{MADP_COMMIT_SHA}}"
required_sources:
  - README-v0.3.0-alpha.2.md
  - protocol/MADP-v0.3.0-alpha.2.md
  - protocol/GLOSSARY-v0.3.0-alpha.2.md
  - schemas/v0.3.0-alpha.2/command.schema.yaml
  - schemas/v0.3.0-alpha.2/command-registry.schema.yaml
  - schemas/v0.3.0-alpha.2/todo.schema.yaml
  - schemas/v0.3.0-alpha.2/context-package.schema.yaml
  - schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml
  - schemas/v0.3.0-alpha.2/review.schema.yaml
  - schemas/v0.3.0-alpha.2/relay.schema.yaml
  - registries/v0.3.0-alpha.2/commands.yaml
  - docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md
  - README-v0.3.0-alpha.3.md
  - protocol/MADP-v0.3.0-alpha.3.md
  - protocol/GLOSSARY-v0.3.0-alpha.3.md
  - schemas/v0.3.0-alpha.3/deliberation.schema.yaml
  - schemas/v0.3.0-alpha.3/command.schema.yaml
  - schemas/v0.3.0-alpha.3/migration.schema.yaml
  - schemas/v0.3.0-alpha.3/session-portability.schema.yaml
  - registries/v0.3.0-alpha.3/commands.yaml
  - docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md
  - docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md
  - docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md
  - docs/profiles/MADP_HELP-v0.3.0-alpha.3.md
  - docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md
  - docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md
  - docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md
  - skills/README.md
  - skills/madp-start/SKILL.md
  - skills/madp-facilitator/SKILL.md
  - skills/madp-participant/SKILL.md
  - skills/madp-recorder/SKILL.md
  - skills/madp-help/SKILL.md
---

# Load MADP v0.3.0-alpha.3 From GitHub

Load the alpha.2 core and alpha.3 extension from one immutable GitHub commit before using any alpha.3 start profile. This loader is informative and cannot override normative sources or higher-priority authority.

The caller must provide all three values:

- `MADP_GITHUB_OWNER`;
- `MADP_GITHUB_REPOSITORY`;
- a 40-character hexadecimal `MADP_COMMIT_SHA`.

Do not substitute `main`, `master`, a tag, or another movable ref for the commit SHA.

## Retrieval procedure

For every path in frontmatter `required_sources`, attempt the exact commit-pinned Raw GitHub URL:

```text
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/<path>
```

Report each source as `READ`, `PARTIALLY_READ`, or `FAILED`. Do not infer, reconstruct, or silently replace unread content. Do not claim protocol conformance when any required source is incomplete.

Access through a GitHub connector, repository file API, user-provided exact text, or a generated complete protocol bundle is allowed only when provenance resolves to the same repository, commit, and path. Record the actual access method.

Do not begin substantive deliberation until exactly one `PROTOCOL_LOAD_REPORT` has been emitted and its status is `COMPLETE`.

## Required output

Return one YAML document before any start profile or deliberation:

```yaml
PROTOCOL_LOAD_REPORT:
  report_version: MADP-PROTOCOL-LOAD-REPORT-v1
  protocol_version: MADP-v0.3.0-alpha.3
  repository: "{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}"
  repository_commit: "{{MADP_COMMIT_SHA}}"
  status: COMPLETE | INCOMPLETE
  files:
    - path: README-v0.3.0-alpha.2.md
      status: READ | PARTIALLY_READ | FAILED
      access_method: RAW_URL | GITHUB_CONNECTOR | PROVIDED_TEXT | COMPLETE_BUNDLE | OTHER
      source_ref: "commit-pinned URL, connector reference, or bundle entry"
  all_required_files_read: true | false
  schema_validation_capability: EXECUTED | AVAILABLE_NOT_EXECUTED | UNAVAILABLE
  inferred_unread_content: false
  limitations: []
  next_action:
    command: APPLY_START_PROFILE | RECOVER_PROTOCOL_SOURCE
    accepted_input: bootstrap/alpha3/quick-start.md | bootstrap/alpha3/verified-start.md | corrected source access
```

The `files` array must contain exactly one entry for every frontmatter `required_sources` path, without omissions or additions.

Set `status: COMPLETE` only when:

- repository and commit are explicit and immutable;
- every required source is `READ`;
- `all_required_files_read` is `true`;
- `inferred_unread_content` is `false`.

If any requirement fails, set `status: INCOMPLETE`, use `RECOVER_PROTOCOL_SOURCE`, stop, and report `PROTOCOL_SOURCE_UNAVAILABLE`. Do not apply `quick-start.md`, `verified-start.md`, or begin a MADP session.