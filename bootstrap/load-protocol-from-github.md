---
bootstrap_version: 0.3
protocol_version: MADP-v0.3.0-alpha.2
status: informative implementation aid
---

# Load MADP Protocol From GitHub

Load the published prerelease `MADP-v0.3.0-alpha.2` from commit-pinned Raw GitHub URLs. This prompt is informative and does not override normative sources or higher-priority authority.

Do not begin deliberation until all required files have been attempted and one `PROTOCOL_LOAD_REPORT` has been emitted.

## Required files

Read these exact files from the same immutable commit:

```text
README-v0.3.0-alpha.2.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/README-v0.3.0-alpha.2.md

protocol/MADP-v0.3.0-alpha.2.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/protocol/MADP-v0.3.0-alpha.2.md

protocol/GLOSSARY-v0.3.0-alpha.2.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/protocol/GLOSSARY-v0.3.0-alpha.2.md

schemas/v0.3.0-alpha.2/command.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/command.schema.yaml

schemas/v0.3.0-alpha.2/command-registry.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/command-registry.schema.yaml

schemas/v0.3.0-alpha.2/todo.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/todo.schema.yaml

schemas/v0.3.0-alpha.2/context-package.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/context-package.schema.yaml

schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml

schemas/v0.3.0-alpha.2/review.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/review.schema.yaml

schemas/v0.3.0-alpha.2/relay.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/v0.3.0-alpha.2/relay.schema.yaml

registries/v0.3.0-alpha.2/commands.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/registries/v0.3.0-alpha.2/commands.yaml

docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md
```

Do not substitute `main`, `master`, or another movable ref for `{{MADP_COMMIT_SHA}}`.

## Load rules

- Report `READ`, `PARTIALLY_READ`, or `FAILED` for every file.
- Do not infer unread content.
- Do not claim full conformance when any required file is incomplete.
- Do not claim user approval or execution permission.
- Default authority is `PROPOSE_ONLY` unless a valid trusted grant applies.
- If no schema validator was actually executed, state that limitation.

## Required output

Return exactly one YAML document before deliberation:

```yaml
PROTOCOL_LOAD_REPORT:
  protocol_version: "MADP-v0.3.0-alpha.2"
  repository_commit: "{{MADP_COMMIT_SHA}}"
  files:
    - path: "README-v0.3.0-alpha.2.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "protocol/MADP-v0.3.0-alpha.2.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "protocol/GLOSSARY-v0.3.0-alpha.2.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/command.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/command-registry.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/todo.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/context-package.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/review.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/v0.3.0-alpha.2/relay.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "registries/v0.3.0-alpha.2/commands.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
  all_required_files_read: true | false
  limitations: []
```

If `all_required_files_read: false`, stop and request recovery input.