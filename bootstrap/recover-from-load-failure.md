---
bootstrap_version: 0.1
protocol_version: MADP-v0.2.5-rc.1
status: informative implementation aid
---

# Recover From Protocol Load Failure

Use this when a new AI chat could not read all required MADP v0.2.5-rc.1 files. This bootstrap prompt is an informative implementation aid and does not override the protocol, glossary, schema, user instructions, platform safety rules, or any higher-priority authority.

Do not reconstruct protocol content from general knowledge. Do not proceed as fully MADP conformant until required files are read or provided.

## Failure Inputs

```yaml
failed_paths: "{{FAILED_PATHS}}"
access_method: "{{ACCESS_METHOD}}"
partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
```

## Required Failure Report

```yaml
PROTOCOL_LOAD_RECOVERY_REQUEST:
  protocol_version: "MADP-v0.2.5-rc.1"
  failed_paths: "{{FAILED_PATHS}}"
  access_method: "{{ACCESS_METHOD}}"
  partial_content_limitations: "{{PARTIAL_CONTENT_LIMITATIONS}}"
  can_claim_full_madp_conformance: false
  requested_recovery_input:
    - "commit-pinned Raw URL"
    - "uploaded file"
    - "pasted text"
    - "commit-pinned repository digest"
```

After receiving recovery input, retry loading the exact missing files and emit a new `PROTOCOL_LOAD_REPORT`. If any required file remains unread or partially read, keep `all_required_files_read: false` and do not continue by inference.
