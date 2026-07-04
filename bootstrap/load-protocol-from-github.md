---
bootstrap_version: 0.1
protocol_version: MADP-v0.2.5-draft
status: informative implementation aid
---

# Load MADP Protocol From GitHub

You are being asked to load MADP v0.2.5-draft from commit-pinned Raw GitHub URLs. This bootstrap prompt is an informative implementation aid and does not override the protocol, glossary, schema, user instructions, platform safety rules, or any higher-priority authority.

Do not begin deliberation until you have attempted to read all required files and emitted `PROTOCOL_LOAD_REPORT`.

## Required Files

Read these exact files from the same immutable commit:

```text
README.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/README.md

protocol/MADP-v0.2.5-draft.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/protocol/MADP-v0.2.5-draft.md

protocol/GLOSSARY-v0.2.5-draft.md
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/protocol/GLOSSARY-v0.2.5-draft.md

schemas/session-state-v0.2.5-draft.schema.yaml
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/schemas/session-state-v0.2.5-draft.schema.yaml
```

Do not substitute a movable branch name such as `main` for `{{MADP_COMMIT_SHA}}`.

## Load Rules

- Report whether each file was read, partially read, or failed.
- Do not infer unread or partially read content.
- Do not claim full MADP conformance when any required file is unread or partially read.
- Do not treat model agreement as evidence.
- Do not claim, generate, or infer user approval.
- Treat default execution authority as `PROPOSE_ONLY` unless a valid permission grant is supplied.
- If the schema cannot be formally validated, say so in `limitations`.

## Required Output

Return exactly one load report before any deliberation:

```yaml
PROTOCOL_LOAD_REPORT:
  protocol_version: "MADP-v0.2.5-draft"
  repository_commit: "{{MADP_COMMIT_SHA}}"
  files:
    - path: "README.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "protocol/MADP-v0.2.5-draft.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "protocol/GLOSSARY-v0.2.5-draft.md"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
    - path: "schemas/session-state-v0.2.5-draft.schema.yaml"
      status: "READ | PARTIALLY_READ | FAILED"
      access_method: "RAW_URL | GITHUB_PAGE | PROVIDED_TEXT | OTHER"
  all_required_files_read: true | false
  limitations: []
```

If `all_required_files_read: false`, stop after the report and ask for recovery input. Do not continue as fully MADP conformant.

