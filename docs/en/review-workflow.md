---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Review workflow

English | [日本語](../ja/review-workflow.md)

> This guide is explanatory. A review is evidence, not approval to merge, tag, release, or execute external actions.

## Review stages

1. **Prepare context.** Pin the branch or commit and list the artifacts in scope.
2. **Define review questions.** Ask for concrete checks rather than general impressions.
3. **Set authority.** Prefer `PROPOSE_ONLY` and prohibit repository modification unless separately authorized.
4. **Run independent checks.** Reproduce failures and test nearby variants.
5. **Return structured findings.** Include severity, evidence, impact, recommended change, and tests.
6. **Disposition findings.** Classify each finding as accepted, rejected with reason, deferred, or remediated.
7. **Request follow-up review.** Re-run the original counterexamples after remediation.
8. **Decide the next governance action separately.** Ready-for-review, merge, tag, and release remain distinct.

## Useful severity model

- `CRITICAL`: immediate authority or safety failure with severe impact.
- `HIGH`: likely integrity, security, or interoperability failure.
- `MEDIUM`: meaningful defect with bounded impact.
- `LOW`: quality, documentation, or audit-hygiene issue.
- `INFO`: observation or future improvement.

Severity should reflect impact and exploitability, not reviewer confidence. Record confidence separately.

## Finding template

```yaml
finding_id: REVIEW-001
severity: HIGH
confidence: HIGH
title: Non-user actor can apply a USER_COMMAND
affected_files:
  - scripts/apply_command.py
evidence:
  - exact code location
  - executed counterexample
impact: Unauthorized state mutation is possible.
recommended_change: Require explicit user provenance before the grant path.
recommended_tests:
  - participant approve is denied
  - generic grant cannot escalate USER_COMMAND
```

## Follow-up status

Use explicit statuses:

- `VERIFIED_FIXED`
- `PARTIALLY_FIXED`
- `NOT_FIXED`
- `NOT_VERIFIED`

A test suite passing is useful but insufficient by itself. For important findings, independently re-run the original counterexample against the production path.

## Review completion checklist

- all requested files read or listed as unread;
- all requested checks executed or explained;
- original blocking counterexamples re-run;
- new findings classified;
- no external action performed;
- no user approval claimed;
- remaining risks and questions stated.
