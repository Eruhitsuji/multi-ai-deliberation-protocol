---
bootstrap_version: 0.3
protocol_version: MADP-v0.3.0-alpha.2
status: informative implementation aid
---

# Recover From Protocol Load Failure

Use this when a new AI chat could not read all required MADP v0.3.0-alpha.2 files. Do not reconstruct protocol content from general knowledge or proceed as fully conformant until all required files are available.

## Preferred Manual Paste Recovery

When `all_required_files_read: false`:

1. Ask the user to open:

```text
https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt
```

2. Ask the user to copy the entire page from `BEGIN_MADP_BUNDLE_METADATA` through the final `END_FILE` line.
3. Ask the user to paste it into the same chat, or upload the complete bundle file.
4. Use metadata and file boundaries to identify all 12 required files.
5. Emit a new `PROTOCOL_LOAD_REPORT`.
6. Continue only when all 12 files were completely read.

Do not begin normal MADP deliberation until all 12 required files have been completely read. If only part of the bundle is pasted, keep `all_required_files_read: false`. Do not fill missing content from general knowledge or inference. Take `repository_commit` only from `BEGIN_MADP_BUNDLE_METADATA.source_commit`; otherwise use `UNKNOWN`. Report `PASTED_TEXT` or `UPLOADED_FILE` accurately. Do not claim formal validation unless a validator actually ran.

## Failure Inputs

```yaml
failed_paths: "{{FAILED_PATHS}}"
access_method: "{{ACCESS_METHOD}}"
partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
```

## Required Failure Report

```yaml
PROTOCOL_LOAD_RECOVERY_REQUEST:
  protocol_version: "MADP-v0.3.0-alpha.2"
  all_required_files_read: false
  failed_paths: "{{FAILED_PATHS}}"
  access_method: "{{ACCESS_METHOD}}"
  partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
  can_claim_full_madp_conformance: false
  preferred_recovery:
    method: "MANUAL_PASTE_COMPLETE_BUNDLE"
    bundle_url: "https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt"
  accepted_alternatives:
    - "uploaded complete bundle file"
    - "individually pasted complete canonical files"
    - "accessible commit-pinned Raw URLs"
```

After recovery, retry the missing files and emit a new report. Keep `all_required_files_read: false` if any file remains incomplete.

```yaml
PROTOCOL_LOAD_REPORT:
  protocol_version: "MADP-v0.3.0-alpha.2"
  repository_commit: "<BEGIN_MADP_BUNDLE_METADATA.source_commit, or UNKNOWN>"
  files:
    - path: "README-v0.3.0-alpha.2.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "protocol/MADP-v0.3.0-alpha.2.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "protocol/GLOSSARY-v0.3.0-alpha.2.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/command.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/command-registry.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/todo.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/context-package.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/review.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.2/relay.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "registries/v0.3.0-alpha.2/commands.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
  all_required_files_read: true
  limitations: []
```