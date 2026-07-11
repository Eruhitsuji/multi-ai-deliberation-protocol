---
bootstrap_version: 0.6-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: VERIFIED
requires_protocol_load: true
required_load_report: PROTOCOL_LOAD_REPORT
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v1
required_load_status: COMPLETE
required_loader: bootstrap/alpha3/load-protocol-from-github.md
---

# Start MADP alpha.3 in VERIFIED mode

This profile starts an already-loaded protocol in `ASSURED` mode. Loading and starting are separate phases.

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

After the load gate passes, do not begin substantive deliberation unless:

- schema validation capability is reported, including whether validation was actually executed;
- the `DELIBERATION_PLAN` exact revision is confirmed;
- participant capability and authority profiles are recorded;
- privacy and team decision policy are explicit;
- a claim ledger is initialized;
- external relays preserve state version and raw responses;
- all legitimate pauses have a Next Action Card.

Default authority is `PROPOSE_ONLY`. File, network, command, commit, push, send, approval, and external execution permissions remain separate.