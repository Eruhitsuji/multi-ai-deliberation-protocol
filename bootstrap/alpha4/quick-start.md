---
profile_version: MADP-START-PROFILE-v0.3.0-alpha.4-quick
protocol_version: MADP-v0.3.0-alpha.4
profile_role: START_PROFILE
load_profile: QUICK
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v3
required_load_status: COMPLETE
minimum_provenance: SOURCE_REFERENCED
schema_validation_requirement: REPORT_ONLY
authority_boundary: REQUIRES_HUMAN_FINAL_AUTHORITY
---

# Start MADP v0.3.0-alpha.4 — QUICK

Apply this profile only after receiving an active, highest-revision `PROTOCOL_LOAD_REPORT` for the same repository and immutable commit.

Require an exact `PROFILE_SOURCE_BINDING`:

```yaml
PROFILE_SOURCE_BINDING:
  repository: owner/repository
  repository_commit: 40-lowercase-hex-commit
  path: bootstrap/alpha4/quick-start.md
  source_ref: commit-pinned source reference
  content_sha256: 64-lowercase-hex-or-null
```

The active load report must satisfy:

- `report_version: MADP-PROTOCOL-LOAD-REPORT-v3`;
- `protocol_version: MADP-v0.3.0-alpha.4`;
- `load_profile: QUICK`;
- `status: COMPLETE`;
- all seven QUICK sources are present exactly once in inventory order and marked `READ`;
- `provenance_level` is `SOURCE_REFERENCED` or `HASH_VERIFIED`;
- unread content is not inferred;
- the profile binding matches an authorized start profile entry.

Schema validation may be unavailable or not executed in QUICK mode, but that limitation must remain visible.

After validation:

1. use Workflow Macro `init`;
2. show the proposed plan and exact revision;
3. wait for Human Final Authority confirmation;
4. record canonical alpha.3 commands and the alpha.4 macro trace;
5. never infer approval, execution permission, independence, verification, or exposure state.

At every legitimate pause, show:

```yaml
CURRENT_STATE: "..."
CURRENT_QUESTION: "..."
FACILITATOR_ACTION: "..."
HUMAN_DECISION_REQUIRED: "... or NONE"
NEXT_ACTION: "..."
CANONICAL_EXPANSION: []
```

Agreement among AI systems is not evidence. A decision is not external-action authorization.
