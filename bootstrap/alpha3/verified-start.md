---
bootstrap_version: 0.7-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: VERIFIED
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v2
accepted_load_profiles:
  VERIFIED: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
  FIELD_TRIAL: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
required_repository: Eruhitsuji/multi-ai-deliberation-protocol
profile_source_binding_required: true
required_schema_validation: EXECUTED
required_provenance: HASH_VERIFIED
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in VERIFIED mode

This profile starts an already-loaded protocol in `ASSURED` mode. Loading and starting are separate phases.

Before starting, identify the highest active, non-superseded `PROTOCOL_LOAD_REPORT` revision and require a `PROFILE_SOURCE_BINDING` containing the repository, commit, path, source reference, and content SHA-256 of this profile.

The load report must:

- use `MADP-PROTOCOL-LOAD-REPORT-v2`;
- be for `MADP-v0.3.0-alpha.3`;
- have a positive `revision`, `active: true`, and not be superseded by a later active revision;
- use the official repository named in frontmatter;
- have the same repository and commit as `PROFILE_SOURCE_BINDING`;
- use `VERIFIED` or `FIELD_TRIAL` with the exact inventory digest from frontmatter;
- be `COMPLETE` with every selected source recorded once as `READ`;
- have `all_required_files_read: true` and `inferred_unread_content: false`;
- have `schema_validation_capability: EXECUTED` and `schema_validation_executed: true`;
- list every applicable schema in `schemas_executed`, have no `unvalidated_structured_sources`, and reference machine-generated validation receipts;
- have `provenance_level: HASH_VERIFIED` and one valid `content_sha256` per selected source;
- authorize `bootstrap/alpha3/verified-start.md` from the same repository and commit.

If any condition fails, do not infer protocol behavior and do not start a session. Return `PROTOCOL_NOT_LOADED` with reason `MISSING_OR_INVALID_ACTIVE_LOAD_REPORT`, `PROFILE_SOURCE_MISMATCH`, `SCHEMA_VALIDATION_REQUIRED`, or `HASH_VERIFICATION_REQUIRED`.

After the gate passes, do not begin substantive deliberation unless:

- the `DELIBERATION_PLAN` exact revision is confirmed;
- a separate exact `session-start` command binds the session ID to that confirmed plan and succeeds;
- participant capability and authority profiles are recorded;
- privacy and team decision policy are explicit;
- a claim ledger is initialized;
- external relays preserve state version and raw responses;
- all legitimate pauses have a Next Action Card.

Goal confirmation alone must leave the session in planning state. Authority-sensitive natural language is converted only into a canonical-command preview; missing IDs, revisions, approvers, selected actions, and expected state versions are never inferred.

Default authority is `PROPOSE_ONLY`. File, network, command, commit, push, send, approval, and external execution permissions remain separate. Any schema-validity claim must be backed by a `VALIDATION_RECEIPT`; model self-assessment is not evidence.
