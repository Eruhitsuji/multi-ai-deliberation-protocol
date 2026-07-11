# MADP Session Portability Profile v0.3.0-alpha.3

Status: normative implementation profile for alpha.3 session file input and output.

## Purpose

A user may request a file at any time to record, back up, review, transfer, or resume a MADP session. A user may also supply a previously exported file for inspection or recovery. File support is capability-dependent: an AI must not claim that it created, opened, read, validated, or stored a file unless the current environment actually provided that capability.

## Export profiles

- `MINIMAL`: current goal, canonical state reference, decisions, unresolved items, and next action.
- `STANDARD`: MINIMAL plus participant profiles, claim ledger, action items, and selected minutes.
- `COMPLETE`: STANDARD plus raw responses, normalization records, and permitted attachments.
- `HANDOFF`: a redacted STANDARD export optimized for another AI or another chat.

Supported container preferences are `DIRECTORY`, `ZIP`, `SINGLE_FILE_YAML`, `SINGLE_FILE_JSON`, and `MARKDOWN_BUNDLE`. The implementation may use another requested format only when it preserves the same manifest, provenance, and authority information.

## Export rules

1. Preserve the source session and state version.
2. Create a `PORTABLE_SESSION_MANIFEST` with a SHA-256 inventory.
3. Record the export profile, included artifact types, redactions, sensitivity, and destination.
4. Exclude private content by default. Private content requires explicit user confirmation for that export.
5. Do not change approval, verification, or authority status while serializing.
6. When file creation is unavailable, provide a complete copyable representation and state that no file was created.
7. A generated export is a record or handoff artifact; it is not a new approval or execution grant.

## Import rules

1. Preserve the uploaded or pasted source unchanged.
2. Detect the container and protocol versions without guessing unread content.
3. Validate the manifest, hashes, schemas, authority boundaries, and session/version collision when possible.
4. Produce a `SESSION_IMPORT_REPORT` before any canonical change.
5. Never silently replace or merge canonical state.
6. Import confirmation must identify the exact import report and selected action.
7. Permitted actions are `CREATE_NEW_SESSION`, `RESUME_EXISTING`, `MERGE_AS_PROPOSAL`, `QUARANTINE`, or `REJECT`.
8. Imported approvals, grants, and identity claims remain subject to normal MADP authority validation.
9. Failed or unavailable validation must remain explicit in warnings and limitations.

## Checkpoints

A `SESSION_CHECKPOINT` records a label, session ID, state version, artifact references, and export readiness. A checkpoint does not duplicate, replace, or approve canonical state.

## Portability commands

- `session-checkpoint-create`
- `session-export`
- `session-import`
- `session-import-confirm`
- `minutes-export`

Aliases such as `save`, `backup`, `load`, and `restore` are convenience inputs only. Canonical command names and original user input must be recorded.
