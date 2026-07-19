# Human decision brief

## 1. Authority notice

This brief is `PROPOSAL_ONLY`; Human Final Authority is required for option selection, dissent disposition, task completion, Core conformance, release, and alpha.4 decisions. No repository modification, merge, release, publication, deployment, formal release evidence, A3-REL-001 completion, or alpha.4 authorization is granted by this brief. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L202-L209`, `artifacts/structured-comparison/human-decision-record-draft.yaml#L1-L43`.

## 2. Task and required output

The task asks which MADP work package should be prioritized next and how three major work packages should proceed through evidence gates. Required output includes one first priority, alternative comparison, three-stage roadmap, PR proposal, alpha.4 disposition, uncertainty/dissent, and final summary. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L11-L30`, `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L98-L185`.

## 3. Canonical evidence inventory

Canonical evidence consists of three Blind initial raw responses and three Cross Exposure raw responses, with Gemini's canonical Cross Exposure response captured by UI recapture. Source: `artifacts/structured-comparison/source-inventory.yaml#L50-L91`.

The preserved noncanonical Gemini submission duplicates the initial response and is retained only for reconciliation provenance, not semantic analysis. Source: `artifacts/structured-comparison/source-inventory.yaml#L93-L101`, `attempts/attempt-002/artifacts/cross-exposure/cross-exposure-reconciliation.yaml#L47-L84`.

## 4. Reconciliation limitations

CLAUDE-B and GEMINI-B send confirmations were retrospective; both have `sent_at_utc: null` and `send_time_status: UNKNOWN`. Source: `attempts/attempt-002/artifacts/cross-exposure/cross-exposure-reconciliation.yaml#L16-L45`.

Gemini's original submitted Cross Exposure raw was a duplicate initial response; the canonical response is the UI recapture. Source: `attempts/attempt-002/artifacts/cross-exposure/cross-exposure-reconciliation.yaml#L47-L84`.

## 5. Preliminary Blind First Round procedure status

Preliminary status is `VALID`, subject to human confirmation. Three initial raw responses exist, were captured before Cross Exposure, are marked `UNEXPOSED`, have SHA-256/byte records, and have independence groups. Source: `artifacts/structured-comparison/initial-convergence-assessment.yaml#L6-L27`.

This is a procedure assessment only; it does not prove model-world independence or correctness. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L211-L220`.

## 6. Blind-stage convergence findings

Preliminary convergence classification is `MIXED`: comparison-first has Blind multi-group support from CHATGPT-B and GEMINI-B, while CLAUDE-B conflicts with field-trial-first. Source: `artifacts/structured-comparison/initial-convergence-assessment.yaml#L29-L55`, `artifacts/structured-comparison/initial-convergence-assessment.yaml#L126-L138`.

Blind multi-group convergence clusters: 2. Source: `artifacts/structured-comparison/initial-convergence-assessment.yaml#L29-L42`, `artifacts/structured-comparison/initial-convergence-assessment.yaml#L82-L94`.

Common-source-mandated clusters: 4. These include release/authority boundary and A3-REL-001/A3-REL-005 ordering items that come directly from task requirements. Source: `artifacts/structured-comparison/initial-convergence-assessment.yaml#L56-L80`, `artifacts/structured-comparison/initial-convergence-assessment.yaml#L95-L110`.

## 7. Cross Exposure changes by participant

CHATGPT-B retained comparison-first but narrowed field-trial dependency claims, separated A3-REL-001 and A3-REL-005 more clearly, and withdrew automatic field-trial profile selection. Source: `artifacts/structured-comparison/participant-change-ledger.yaml#L8-L58`.

CLAUDE-B retained field-trial-first but made it conditional on entry-readiness and downgraded audit-area minimization from a primary reason to a secondary consideration. Source: `artifacts/structured-comparison/participant-change-ledger.yaml#L61-L113`.

GEMINI-B retained comparison-first but added artifact isolation and withdrew the optimistic low-risk framing. Source: `artifacts/structured-comparison/participant-change-ledger.yaml#L116-L165`.

## 8. Acceptance criteria matrix summary

Initial and Cross Exposure proposals mostly satisfy the task acceptance criteria. Remaining partials are evidence-path/profile coupling risk, A3-REL-001/A3-REL-005 grouping in CHATGPT-B's initial proposal, and unsupported absolute-risk framing in GEMINI-B's initial proposal. Source: `artifacts/structured-comparison/acceptance-criteria-matrix.md#L34-L41`.

## 9. Candidate work-package options

Option A is comparison-first with isolated artifact layout. It is the best-supported option for human review, not a final decision. Source: `artifacts/structured-comparison/candidate-work-package-options.md#L8-L62`.

Option B is conditional field-trial-first, preserving CLAUDE-B's material dissent. Source: `artifacts/structured-comparison/candidate-work-package-options.md#L64-L104`.

Option C is a readiness-gated staged policy that records facts required to choose A or B without deciding final roadmap order. Source: `artifacts/structured-comparison/candidate-work-package-options.md#L106-L136`.

## 10. Material dissent

Material dissent remains unresolved on first work package ordering, formal field trial execution profile, alpha.4 disposition label, and evidence-readiness versus release-progress priority. Source: `artifacts/structured-comparison/dissent-register.yaml#L5-L86`.

## 11. Evidence gaps

Blocking gaps: field-trial readiness/acceptance/profile facts and whether a comparison-selected experimental profile may be used for A3-REL-001. Source: `artifacts/structured-comparison/evidence-gap-register.yaml#L5-L14`, `artifacts/structured-comparison/evidence-gap-register.yaml#L51-L62`.

Material gaps: artifact isolation from release audit scope, comparison independence/operator control, actual four-method metrics, and bound-commit/current-repository changes. Source: `artifacts/structured-comparison/evidence-gap-register.yaml#L15-L50`, `artifacts/structured-comparison/evidence-gap-register.yaml#L63-L74`.

## 12. Unresolved risks and stop conditions

Stop or defer if field-trial readiness cannot be confirmed, artifact isolation is infeasible, comparison independence/operator control cannot be established, or resolving readiness requires unapproved repository modification. Source: `artifacts/structured-comparison/candidate-work-package-options.md#L51-L57`, `artifacts/structured-comparison/candidate-work-package-options.md#L95-L101`, `artifacts/structured-comparison/candidate-work-package-options.md#L133-L136`.

## 13. Decisions required from Human Final Authority

Human Final Authority must decide selected option, modifications, each material dissent disposition, whether additional evidence is required, final Blind First Round status, final convergence classification, task completion, and whether Core conformance can be evaluated in a later phase. Source: `artifacts/structured-comparison/human-decision-record-draft.yaml#L26-L43`.

Minimum decision items:

- Adopt `OPTION-A`, `OPTION-B`, `OPTION-C`, or request modification. Source: `artifacts/structured-comparison/candidate-work-package-options.md#L8-L136`.
- Resolve DS-001 through DS-004 or retain them as alternatives. Source: `artifacts/structured-comparison/dissent-register.yaml#L5-L86`.
- Decide whether EG-001 and EG-005 block task completion. Source: `artifacts/structured-comparison/evidence-gap-register.yaml#L5-L14`, `artifacts/structured-comparison/evidence-gap-register.yaml#L51-L62`.
- Confirm or revise preliminary Blind status and convergence classification. Source: `artifacts/structured-comparison/initial-convergence-assessment.yaml#L6-L138`.
- Decide whether `task_completed` is true, false, or requires another phase. Source: `artifacts/structured-comparison/human-decision-record-draft.yaml#L26-L43`.

## 14. Explicit non-authorizations

No repository modification, merge, release, publication, deployment, formal release evidence, A3-REL-001 completion, or alpha.4 authorization is granted by this brief. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L202-L209`, `artifacts/structured-comparison/human-decision-record-draft.yaml#L45-L46`.

Core conformance remains `NOT_EVALUATED`. Source: `artifacts/structured-comparison/human-decision-record-draft.yaml#L38-L38`.
