# Claude Review Prompt — MADP v0.3.0-alpha.2

Please perform an independent, adversarial final review of `MADP-v0.3.0-alpha.2` before Draft PR #2 is marked ready for review.

Start by reading:

1. `reviews/v0.3.0-alpha.2/claude/alpha2-final-review.context-package.yaml`
2. `reviews/v0.3.0-alpha.2/claude/alpha2-final-review.review-request.yaml`

Then inspect every accessible artifact listed in the review request. Explicitly list any artifact you could not read. Do not claim complete review coverage for unread files.

## Authority boundary

This is a review-only task under `PROPOSE_ONLY` authority.

Do not modify repository files, create commits, push, open or merge pull requests, create tags, publish releases, or perform any other external action. Do not infer user approval. Passing CI is evidence only that registered checks passed.

## Required review approach

Review the implementation independently rather than accepting its `COMPLETE_FOR_DRAFT_REVIEW` status as proof.

Check at least:

- protocol, glossary, schema, registry, parser, runtime, tests, and README consistency;
- parser ambiguity and repeated `LIST` versus `SCALAR` options;
- malformed YAML and CLI input handling;
- authority classification and trusted-grant validation;
- grant action, scope, issuer, activity, reference, and replay handling;
- non-user issuance of `USER_COMMAND`;
- approval binding to decision id and revision;
- stale state, state version, parent version, and command-history behavior;
- TODO state transitions and promotion semantics;
- whether every registered command has an implemented and appropriately bounded effect;
- whether read-only commands can accidentally mutate state;
- whether context, receipt, review, relay, TODO, patch, or CI artifacts can be confused with permission;
- external-action fail-closed behavior;
- migration invariants and bundle generation;
- missing negative, property-based, fuzz, concurrency, and cross-model interoperability tests.

Try to construct concrete counterexamples for every safety claim.

## Required response structure

Return a single `REVIEW_RESPONSE`-style report with these sections:

```yaml
CLAUDE_ALPHA2_REVIEW:
  protocol_version: MADP-v0.3.0-alpha.2
  review_request: REVIEW-REQ-ALPHA2-CLAUDE-001
  reviewer: CLAUDE
  coverage:
    files_read: []
    files_unread: []
    checks_or_commands_run: []
  overall_assessment:
    recommendation: BLOCK_READY_FOR_REVIEW | READY_WITH_REQUIRED_FIXES | READY_WITH_NONBLOCKING_NOTES
    rationale: ""
  findings:
    - finding_id: CLAUDE-A2-001
      severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
      disposition: ALPHA2_BLOCKING | ALPHA2_NONBLOCKING | LATER_VERSION
      confidence: HIGH | MEDIUM | LOW
      title: ""
      affected_files: []
      evidence:
        - "Exact path, function, field, clause, or reproducible input"
      impact: ""
      reproduction_or_counterexample: ""
      recommended_change: ""
      recommended_tests: []
  missing_tests: []
  interoperability_risks: []
  documentation_inconsistencies: []
  later_version_ideas: []
  questions_for_user: []
  external_actions_performed: false
  user_approval_claimed: false
```

## Quality requirements

- Separate confirmed defects from design preferences.
- Avoid generic advice; point to exact files and behavior.
- Include proposed test cases for every blocking or high-severity finding.
- State when a finding is based on inference rather than direct execution.
- Do not recommend weakening fail-closed behavior merely for convenience.
- Do not mark the implementation ready solely because CI is green.
