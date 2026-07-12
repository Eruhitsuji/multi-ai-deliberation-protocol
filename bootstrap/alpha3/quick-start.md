---
bootstrap_version: 0.7-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: QUICK
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v2
accepted_load_profiles:
  QUICK: ba8c4b88c55de4d73ea82292fcaa38d2825096f3e08df041985bdab57be692c0
  VERIFIED: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
  FIELD_TRIAL: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
required_repository: Eruhitsuji/multi-ai-deliberation-protocol
profile_source_binding_required: true
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in QUICK mode

This profile configures a protocol that has already been loaded. It does not load or reconstruct MADP rules.

Before starting, identify the highest active, non-superseded `PROTOCOL_LOAD_REPORT` revision and require a `PROFILE_SOURCE_BINDING` containing the repository, commit, path, and source reference of this start profile.

The load report must:

- use `MADP-PROTOCOL-LOAD-REPORT-v2`;
- be for `MADP-v0.3.0-alpha.3`;
- have a positive `revision`, `active: true`, and not be superseded by a later active revision;
- use the official repository named in frontmatter;
- have the same repository and commit as `PROFILE_SOURCE_BINDING`;
- use an accepted load profile and its exact inventory digest from frontmatter;
- be `COMPLETE` with every selected source recorded once as `READ`;
- have `all_required_files_read: true` and `inferred_unread_content: false`;
- have `SOURCE_REFERENCED` or `HASH_VERIFIED` provenance;
- authorize `bootstrap/alpha3/quick-start.md` from the same repository and commit;
- satisfy `schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml` when validation is available;
- have `authorized_start_profiles: []` whenever the report is `INCOMPLETE`.

If the report or profile binding is missing, stale, self-attested, mismatched, or incomplete, do not infer protocol behavior and do not start a session. Return:

```yaml
MADP_BOOTSTRAP_STATUS:
  status: PROTOCOL_NOT_LOADED
  reason: MISSING_OR_INVALID_ACTIVE_LOAD_REPORT | PROFILE_SOURCE_MISMATCH
  protocol_version: MADP-v0.3.0-alpha.3
  required_loader: bootstrap/alpha3/load-protocol-from-github.md
  next_action: Load or recover the protocol, then provide the latest active report and matching PROFILE_SOURCE_BINDING.
```

After the gate passes, start a LIGHT or STANDARD MADP discussion. Preserve alpha.2 canonical commands: `status`, `pause`, and `resume` are not aliases. Use `session-status`, `session-resume`, and `help-exit` for their explicit alpha.3 operations.

Before substantive work, establish session ID, current state version, a revisioned deliberation plan, human decision authority, and the smallest useful set of roles. Confirming the plan with `goal-confirm` does not start the session. Emit or request the exact `session-start` command with `session_id` and the confirmed `deliberation_plan`; only after it succeeds may the session become `ACTIVE`.

For any authority-sensitive natural-language request, show the canonical command and exact IDs, revisions, selected action, approver, or expected state version before mutation. Do not infer missing values. Every accepted artifact must be bound to the session and source state revision. Default authority is `PROPOSE_ONLY`.

If schema validation was not executed, preserve that limitation in session state and do not describe the session as VERIFIED or ASSURED.
