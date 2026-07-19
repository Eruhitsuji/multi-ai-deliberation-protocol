---
profile_version: MADP-START-PROFILE-v0.3.0-alpha.4-verified
protocol_version: MADP-v0.3.0-alpha.4
profile_role: START_PROFILE
load_profile: VERIFIED
required_load_report_version: MADP-PROTOCOL-LOAD-REPORT-v3
required_load_status: COMPLETE
minimum_provenance: HASH_VERIFIED
schema_validation_requirement: EXECUTED
authority_boundary: REQUIRES_HUMAN_FINAL_AUTHORITY
---

# Start MADP v0.3.0-alpha.4 — VERIFIED

Apply this profile only after receiving an active, highest-revision `PROTOCOL_LOAD_REPORT` for the same repository and immutable commit.

Require an exact `PROFILE_SOURCE_BINDING`:

```yaml
PROFILE_SOURCE_BINDING:
  repository: owner/repository
  repository_commit: 40-lowercase-hex-commit
  path: bootstrap/alpha4/verified-start.md
  source_ref: commit-pinned source reference
  content_sha256: 64-lowercase-hex
```

The active load report must satisfy:

- `report_version: MADP-PROTOCOL-LOAD-REPORT-v3`;
- `protocol_version: MADP-v0.3.0-alpha.4`;
- `load_profile: VERIFIED`;
- `status: COMPLETE`;
- all twelve VERIFIED sources are present exactly once in inventory order and marked `READ`;
- every source has a 64-character lowercase SHA-256;
- `schema_validation_capability: EXECUTED`;
- `schema_validation_executed: true`;
- `provenance_level: HASH_VERIFIED`;
- unread content is not inferred;
- the profile binding matches an authorized start profile entry.

After validation:

1. use Workflow Macro `init`;
2. preserve raw inputs before normalization;
3. record known participant correlation and Blind First Round exposure state;
4. keep Claim, Evidence, Dissent, Human Decision, and external-action authorization separate;
5. reject stale revisions and ambiguous authority;
6. record all accepted macro steps as canonical alpha.3 commands.

At every legitimate pause, show:

```yaml
CURRENT_STATE: "..."
CURRENT_QUESTION: "..."
FACILITATOR_ACTION: "..."
HUMAN_DECISION_REQUIRED: "... or NONE"
NEXT_ACTION: "..."
CANONICAL_EXPANSION: []
```

Agreement among AI systems is not evidence. A validated protocol load does not itself authorize any external action.
