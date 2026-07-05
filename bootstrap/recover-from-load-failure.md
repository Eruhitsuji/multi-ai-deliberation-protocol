---
bootstrap_version: 0.2
protocol_version: MADP-v0.3.0-alpha.1
status: informative implementation aid
---

# Recover From Protocol Load Failure

Use this when a new AI chat could not read all required MADP v0.3.0-alpha.1 files. This bootstrap prompt is an informative implementation aid and does not override the protocol, glossary, schemas, user instructions, platform safety rules, or any higher-priority authority.

Do not reconstruct protocol content from general knowledge. Do not proceed as fully MADP conformant until required files are read or provided.

## Preferred Manual Paste Recovery

When `all_required_files_read: false`, use this recovery path first:

1. Ask the user to open this bundle URL in a browser:

```text
https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt
```

2. Ask the user to copy the entire page from `BEGIN_MADP_BUNDLE_METADATA` through the final `END_FILE` line.
3. Ask the user to paste the entire copied text into this same chat.
4. Use `BEGIN_MADP_BUNDLE_METADATA` for provenance and the `BEGIN_FILE` and `END_FILE` boundaries to identify the seven required files.
5. Return a new `PROTOCOL_LOAD_REPORT`.
6. Continue normal MADP processing only if all seven files were completely read.

Do not begin normal MADP deliberation until all seven required files have been completely read. If `JOIN_INPUT`, `RELAY_BLOCK`, or other session material is provided before complete protocol loading, do not treat it as MADP-conformant processing. If only part of the bundle is pasted, keep `all_required_files_read: false`. Do not fill missing content from general knowledge or inference. Do not claim URL access unless the URL was actually retrieved. Take `repository_commit` only from `BEGIN_MADP_BUNDLE_METADATA.source_commit`; if metadata is missing, use `repository_commit: "UNKNOWN"` and do not guess. When the user pasted the bundle, report `access_method: "PASTED_TEXT"`. When the user uploaded the bundle file, report `access_method: "UPLOADED_FILE"`. Do not claim formal JSON Schema validation unless an actual validator was executed.

## Failure Inputs

```yaml
failed_paths: "{{FAILED_PATHS}}"
access_method: "{{ACCESS_METHOD}}"
partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
```

## Required Failure Report

```yaml
PROTOCOL_LOAD_RECOVERY_REQUEST:
  protocol_version: "MADP-v0.3.0-alpha.1"
  all_required_files_read: false
  failed_paths: "{{FAILED_PATHS}}"
  access_method: "{{ACCESS_METHOD}}"
  partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
  can_claim_full_madp_conformance: false
  preferred_recovery:
    method: "MANUAL_PASTE_COMPLETE_BUNDLE"
    bundle_url: "https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt"
    user_instructions:
      - "Open the bundle URL in a browser."
      - "Copy the entire page from BEGIN_MADP_BUNDLE_METADATA through the final END_FILE line."
      - "Paste the entire copied text into this same chat."
  accepted_alternatives:
    - "uploaded complete bundle file"
    - "individually pasted complete canonical files"
    - "accessible commit-pinned Raw URLs"
```

## Report After Pasted Bundle

After receiving recovery input, retry loading the exact missing files and emit a new `PROTOCOL_LOAD_REPORT`. If any required file remains unread or partially read, keep `all_required_files_read: false` and do not continue by inference.

```yaml
PROTOCOL_LOAD_REPORT:
  protocol_version: "MADP-v0.3.0-alpha.1"
  repository_commit: "<BEGIN_MADP_BUNDLE_METADATA.source_commit, or UNKNOWN>"
  files:
    - path: "README-v0.3.0-alpha.1.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "protocol/MADP-v0.3.0-alpha.1.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "protocol/GLOSSARY-v0.3.0-alpha.1.md"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
    - path: "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml"
      status: "READ"
      access_method: "PASTED_TEXT | UPLOADED_FILE"
  all_required_files_read: true
  limitations:
    - "The canonical files were supplied as pasted text because external URL retrieval was unavailable."
    - "No formal JSON Schema validator was executed unless explicitly stated otherwise."
```
