---
bootstrap_version: 0.8-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: VERIFIED
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v2
accepted_load_profiles:
  VERIFIED: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
  FIELD_TRIAL: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
required_repository: Eruhitsuji/multi-ai-deliberation-protocol
profile_source_binding_required: true
required_schema_validation: EXECUTED
required_provenance: HASH_VERIFIED
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in VERIFIED mode

This profile starts an already-loaded protocol in `ASSURED` mode. Loading and starting are separate phases.

Before starting, identify the highest active, non-superseded `PROTOCOL_LOAD_REPORT` revision and require a `PROFILE_SOURCE_BINDING` containing repository, commit, path, source reference, exact profile SHA-256, and source inventory digest.

The load report must:

- use `MADP-PROTOCOL-LOAD-REPORT-v2`;
- be for `MADP-v0.3.0-alpha.3`;
- have a positive revision, `active: true`, and not be superseded by a later active revision;
- use the official repository named in frontmatter;
- have the same repository and commit as `PROFILE_SOURCE_BINDING`;
- use VERIFIED or FIELD_TRIAL with the exact inventory digest from frontmatter;
- be `COMPLETE`, with every selected source recorded once as `READ`;
- have `all_required_files_read: true` and `inferred_unread_content: false`;
- have `schema_validation_capability: EXECUTED` and `schema_validation_executed: true`;
- contain PASS `schema_validation_records` for both inherited and alpha.3 command registries;
- have matching `schemas_applicable`, `schemas_executed`, and no `unvalidated_structured_sources`;
- resolve every `validation_receipt_refs` entry to an actual schema-valid receipt;
- have `provenance_level: HASH_VERIFIED` and one valid SHA-256 per selected source;
- authorize `bootstrap/alpha3/verified-start.md` from the same repository and commit with its exact content SHA-256.

If any condition fails, do not infer protocol behavior and do not start a session. Return `PROTOCOL_NOT_LOADED` with reason `MISSING_OR_INVALID_ACTIVE_LOAD_REPORT`, `PROFILE_SOURCE_MISMATCH`, `SCHEMA_VALIDATION_REQUIRED`, `VALIDATION_RECEIPT_REQUIRED`, or `HASH_VERIFICATION_REQUIRED`.

After the gate passes:

1. record the revisioned deliberation plan, participant capabilities, authority profiles, privacy policy, team decision policy, claim ledger, and legitimate-pause behavior;
2. use `goal-confirm` only to confirm the exact plan revision;
3. request a separate exact `session-start`;
4. begin substantive deliberation only after `session-start` succeeds.

External relays preserve state version and raw responses. Every legitimate pause has a Next Action Card. Default authority is `PROPOSE_ONLY`. File, network, command, commit, push, send, approval, and external execution permissions remain separate.
