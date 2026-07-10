# Claude Follow-up Review Prompt — MADP v0.3.0-alpha.2

Perform an independent follow-up adversarial review of the remediation for the prior Claude alpha.2 review.

Read first:

1. `reviews/v0.3.0-alpha.2/claude/alpha2-follow-up-review.context-package.yaml`
2. `reviews/v0.3.0-alpha.2/claude/alpha2-follow-up-review.review-request.yaml`
3. `reviews/v0.3.0-alpha.2/claude/alpha2-review-disposition.yaml`

Then inspect every accessible artifact listed in the review request. Explicitly list unread files. Do not rely only on the disposition or green CI.

## Authority boundary

This is a review-only task under `PROPOSE_ONLY` authority. Do not modify files, commit, push, alter PR state, merge, tag, release, or perform another external action.

## Required method

Re-run the original blocking counterexamples and try nearby variants. Confirm each result from actual execution when possible.

At minimum verify:

- omitted issuer does not obtain USER authority;
- non-USER actors cannot apply USER_COMMAND, including with a generic internal grant;
- grant assurance level, assurance origin, reference, action, scope, activity, and replay rules fail closed;
- bare, boolean, zero, negative, non-integer, and downgraded approval revisions are rejected;
- TODO runtime and lifecycle checker use one transition table and agree for all state pairs;
- terminal TODO completion evidence cannot be rewritten;
- duplicate YAML keys, anchors, aliases, and custom tags are rejected;
- the fixes did not cause regressions in all-command coverage or read-only behavior.

Run all commands listed in the review request. You may create temporary scratch files outside the repository or use an in-memory/read-only harness, but do not write repository files.

## Required response

Return one YAML report:

```yaml
CLAUDE_ALPHA2_FOLLOWUP_REVIEW:
  protocol_version: MADP-v0.3.0-alpha.2
  review_request: REVIEW-REQ-ALPHA2-CLAUDE-FOLLOWUP-001
  reviewer: CLAUDE
  coverage:
    files_read: []
    files_unread: []
    checks_or_commands_run: []
  remediation_verification:
    - finding_id: CLAUDE-A2-001
      status: VERIFIED_FIXED | PARTIALLY_FIXED | NOT_FIXED | NOT_VERIFIED
      evidence: []
      remaining_risk: ""
    - finding_id: CLAUDE-A2-002
      status: VERIFIED_FIXED | PARTIALLY_FIXED | NOT_FIXED | NOT_VERIFIED
      evidence: []
      remaining_risk: ""
    - finding_id: CLAUDE-A2-003
      status: VERIFIED_FIXED | PARTIALLY_FIXED | NOT_FIXED | NOT_VERIFIED
      evidence: []
      remaining_risk: ""
    - finding_id: CLAUDE-A2-004
      status: VERIFIED_FIXED | PARTIALLY_FIXED | NOT_FIXED | NOT_VERIFIED
      evidence: []
      remaining_risk: ""
    - finding_id: CLAUDE-A2-005
      status: VERIFIED_FIXED | PARTIALLY_FIXED | NOT_FIXED | NOT_VERIFIED
      evidence: []
      remaining_risk: ""
  overall_assessment:
    recommendation: BLOCK_READY_FOR_REVIEW | READY_WITH_REQUIRED_FIXES | READY_WITH_NONBLOCKING_NOTES
    rationale: ""
  new_findings:
    - finding_id: CLAUDE-A2-FOLLOWUP-001
      severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
      disposition: ALPHA2_BLOCKING | ALPHA2_NONBLOCKING | LATER_VERSION
      confidence: HIGH | MEDIUM | LOW
      title: ""
      affected_files: []
      evidence: []
      reproduction_or_counterexample: ""
      impact: ""
      recommended_change: ""
      recommended_tests: []
  remaining_nonblocking_findings: []
  documentation_inconsistencies: []
  questions_for_user: []
  external_actions_performed: false
  user_approval_claimed: false
```

A finding may be marked `VERIFIED_FIXED` only when the original counterexample and relevant nearby variants fail closed as intended. Separate confirmed defects from design preferences.
