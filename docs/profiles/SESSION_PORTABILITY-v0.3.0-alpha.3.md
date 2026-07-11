# MADP Session Portability Profile v0.3.0-alpha.3

Status: normative implementation profile.

A user may request an export, backup, handoff, inspection, or resume file at any checkpoint. File capability must be reported honestly.

## Export

Profiles are `MINIMAL`, `STANDARD`, `COMPLETE`, and `HANDOFF`. Private content is excluded by default. Including private content requires a confirmation reference for that exact export.

The manifest binds the export to `session_id` and `source_state_version` and inventories every file with SHA-256.

## Import sequencing

`session-import` preserves the source and creates a report with its own positive `report_revision`. It cannot modify canonical state.

`session-import-confirm` must identify:

- the exact `import_id`;
- the exact `report_revision`;
- one selected action.

Allowed actions are `CREATE_NEW_SESSION`, `RESUME_EXISTING`, `MERGE_AS_PROPOSAL`, `QUARANTINE`, and `REJECT`.

Hash, schema, authority, or collision failures remain visible. Imported approval and identity assertions receive normal authority validation and are never trusted merely because they were in a file.
