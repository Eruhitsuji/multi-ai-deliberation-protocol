---
bootstrap_version: 0.6-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: QUICK
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v1
required_load_status: COMPLETE
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in QUICK mode

This profile configures a protocol that has already been loaded. It does not load or reconstruct MADP rules.

Before starting, verify that the current chat contains a `PROTOCOL_LOAD_REPORT` with:

- `protocol_version: MADP-v0.3.0-alpha.3`;
- `report_version: MADP-PROTOCOL-LOAD-REPORT-v1`;
- a 40-character hexadecimal `repository_commit`;
- `status: COMPLETE`;
- `all_required_files_read: true`;
- every required file recorded as `READ`;
- `inferred_unread_content: false`.

If the report is missing, incomplete, stale, or belongs to another protocol version or commit, do not infer protocol behavior and do not start a session. Return:

```yaml
MADP_BOOTSTRAP_STATUS:
  status: PROTOCOL_NOT_LOADED
  protocol_version: MADP-v0.3.0-alpha.3
  required_loader: bootstrap/alpha3/load-protocol-from-github.md
  next_action: Load the protocol and provide a COMPLETE PROTOCOL_LOAD_REPORT.
```

After the load gate passes, start a LIGHT or STANDARD MADP discussion. Preserve alpha.2 canonical commands: `status`, `pause`, and `resume` are not aliases. Use `session-status`, `session-resume`, and `help-exit` for their explicit alpha.3 operations.

Before substantive work, establish session ID, current state version, a revisioned deliberation plan, human decision authority, and the smallest useful set of roles. Every accepted artifact must be bound to the session and source state revision. Default authority is `PROPOSE_ONLY`.