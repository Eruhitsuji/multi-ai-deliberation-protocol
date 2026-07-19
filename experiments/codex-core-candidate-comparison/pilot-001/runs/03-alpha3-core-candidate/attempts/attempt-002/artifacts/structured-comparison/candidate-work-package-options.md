# Candidate work-package options

Authority: `PROPOSAL_ONLY`
Human Final Authority required: `true`

These options are derived from participant evidence only. They are not a final decision and do not authorize repository modification, release, publication, deployment, formal release evidence, A3-REL-001 completion, or alpha.4 authorization.

## Option A: Comparison-first with isolated artifact layout

- option_id: `OPTION-A`
- status: `PROPOSAL_ONLY`
- label: Best-supported option for human review; not a final decision.
- source participants: CHATGPT-B, GEMINI-B; CLAUDE-B recognizes comparison-first as a strong alternative.
- Blind-stage support: two independence groups supported comparison-first: CHATGPT-B and GEMINI-B. Source: `attempts/attempt-002/raw/initial-response-CHATGPT-B.md#L9-L18`, `attempts/attempt-002/raw/initial-response-GEMINI-B.md#L15-L30`.
- Cross Exposure changes: CHATGPT-B retained comparison-first but added stricter separation of formal field-trial authorization; GEMINI-B retained comparison-first and added artifact isolation; CLAUDE-B retained field-trial-first as conditional dissent. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L477-L489`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L315-L320`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L343-L356`.

### Work packages and ordering

1. Four-method Core Candidate comparison experiment with frozen evidence contract and isolated artifact layout. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L610-L691`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L322-L357`.
2. Alpha.3 formal field trial/A3-REL-001, with formal profile/binding confirmed separately and not automatically selected by comparison. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L693-L767`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L249-L257`.
3. A3-REL-005 final-main audit and evidence-directed disposition of bounded fixes/alpha.4 decision-record preparation. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L769-L841`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L400-L432`.

### Scope

The scope is comparison evidence collection first, not release evidence. Experiment artifacts remain `formal_release_evidence: false` and structurally isolated from normative release scope. Source: `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L183-L189`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L436-L468`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L996-L1012`.

### Deliverables

- Frozen information set, metric dictionary/evidence contract, participant/correlation register, raw prompts/responses, operator intervention log, exposure records, failure/aborted run recording, comparison report, and limitations/dissent. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L610-L627`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L322-L337`.
- Immediate PR: evidence contract, independence register, isolated logging layout, with no release-gate effect. Source: `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L436-L468`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L843-L908`.

### Evidence gate

Proceed only after human review of decision-useful comparison evidence, preservation of release/comparison separation, and confirmation of no blocking defect or bounded remediation. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L681-L691`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L357-L357`.

### Acceptance test

Accept if all four methods are recorded under the same criteria, raw artifacts are preserved, missing/failed/aborted runs are recorded, participant correlation/exposure is documented, and no release or alpha.4 authorization is inferred. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L641-L680`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L343-L357`.

### Stop condition

Stop or switch if field-trial readiness/time constraints override, artifact isolation is infeasible, independence/assistance control cannot be maintained, or comparison scaffold repair would require major implementation work. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L420-L429`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L972-L980`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L495-L499`.

### Unresolved dissent and evidence gaps

- Dissent: field-trial-first remains material. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L258-L265`.
- Evidence gaps: EG-002 artifact isolation, EG-003 independence/operator control, EG-004 actual metrics, EG-005 field-trial profile authorization. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L304-L312`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L431-L460`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L289-L305`.

### Authority boundary

No release, tag, publication, deployment, A3-REL-001 completion, formal release evidence, or alpha.4 authorization is granted. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L996-L1012`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L521-L530`.

## Option B: Conditional field-trial-first

- option_id: `OPTION-B`
- status: `PROPOSAL_ONLY`
- source participants: CLAUDE-B; CHATGPT-B records this as strongest dissent and gives switch conditions; GEMINI-B accepts a switch if human priority and artifact-isolation failure are confirmed.
- Blind-stage support: one independence group supported field-trial-first; two groups conflicted. Source: `attempts/attempt-002/raw/initial-response-CLAUDE-B.md#L19-L28`, `attempts/attempt-002/raw/initial-response-CHATGPT-B.md#L9-L18`, `attempts/attempt-002/raw/initial-response-GEMINI-B.md#L15-L30`.
- Cross Exposure changes: CLAUDE-B made field-trial-first conditional on G1-G3 readiness; CHATGPT-B and GEMINI-B retained comparison-first but accepted field-trial-first under specified conditions. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L343-L356`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L972-L980`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L495-L499`.

### Work packages and ordering

1. Alpha.3 formal field trial/A3-REL-001, conditional on confirmed entry readiness and release-target configuration. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L343-L391`.
2. Four-method Core Candidate comparison experiment as non-release evidence. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L394-L404`.
3. Evidence-based Core refinement and alpha.4 decision preparation. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L405-L416`.

### Scope

The scope is release critical path first: manual usability evidence, load report, profile binding, validation receipts, raw observation inventory, and named human sign-off for A3-REL-001. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L383-L391`.

### Deliverables

Field-trial entry-readiness assessment, evidence contract, FIELD_TRIAL load report, PROFILE_SOURCE_BINDING, VALIDATION_RECEIPTs, raw observation inventory, validation evidence manifest, and human sign-off record. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L383-L391`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L416-L445`.

### Evidence gate

Proceed to comparison only if A3-REL-001 exits successfully and the human records whether A3-REL-005 may proceed; if readiness is not short-term satisfiable, swap to comparison-first. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L392-L393`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L353-L356`.

### Acceptance test

Accept if field-trial evidence is receipt-bound, independently recomputable, tied to the exact revision, and explicitly signed off by a named human; checker PASS alone is insufficient. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L383-L391`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L515-L519`.

### Stop condition

Stop or switch if evidence runner, A3-REL-001 acceptance criteria, or release-target configuration cannot be confirmed. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L304-L312`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L353-L356`.

### Unresolved dissent and evidence gaps

- Dissent: comparison-first has stronger Blind multi-group support. Source: `attempts/attempt-002/raw/initial-response-CHATGPT-B.md#L9-L18`, `attempts/attempt-002/raw/initial-response-GEMINI-B.md#L15-L30`.
- Evidence gaps: EG-001 field-trial readiness and EG-005 field-trial execution profile. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L304-L312`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L272-L278`.

### Authority boundary

This option does not authorize sign-off, release, tag, publication, deployment, external action, or alpha.4. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L512-L519`.

## Option C: Readiness-gated staged policy

- option_id: `OPTION-C`
- status: `PROPOSAL_ONLY`
- source participants: primarily CLAUDE-B's G1-G3 readiness assessment and CHATGPT-B/GEMINI-B switch conditions.
- Blind-stage support: mixed; comparison-first has two-group support, field-trial-first has one-group support. Source: `attempts/attempt-002/raw/initial-response-CHATGPT-B.md#L9-L18`, `attempts/attempt-002/raw/initial-response-CLAUDE-B.md#L19-L28`, `attempts/attempt-002/raw/initial-response-GEMINI-B.md#L15-L30`.
- Cross Exposure changes: participants converged on needing readiness/artifact isolation facts, but this post-exposure agreement is not independent convergence. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L327-L337`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L212-L219`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L237-L247`.

### Work packages and ordering

1. Evidence contract/readiness gate to choose between Option A and Option B without changing release state. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L304-L312`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L416-L445`.
2. Execute the chosen path: either isolated four-method comparison or field-trial-first, according to human disposition of EG-001/EG-002/EG-005. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L972-L980`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L495-L499`.
3. A3-REL-005/evidence-directed disposition after A3-REL-001 when applicable. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L769-L841`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L405-L416`.

### Scope

This option is a narrow evidence-first gate, not a new final roadmap decision: it records readiness, isolation, and field-trial target facts so the human can choose Option A or B. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L181-L188`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L304-L312`.

### Deliverables

Entry-readiness assessment, evidence contract, artifact-isolation check, field-trial target/profile check, and human branching decision form. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L416-L445`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L436-L468`.

### Evidence gate

Human chooses A if artifact isolation and comparison feasibility are acceptable; chooses B if field-trial readiness is high and release timing dominates; requests more evidence if both are unready. Source: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L972-L980`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md#L495-L499`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L353-L356`.

### Acceptance test

Accept if the gate records facts without inferring missing timings, IDs, approvals, evidence status, or release authorization. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L211-L220`, `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L512-L519`.

### Stop condition

Stop if readiness/isolation facts cannot be established without expanding authority or performing unapproved repository modification. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L202-L209`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L996-L1012`.

### Unresolved dissent and evidence gaps

This option does not resolve DS-001 or DS-002; it defers them to Human Final Authority after targeted evidence review. Source: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md#L258-L278`, `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md#L381-L403`.

### Authority boundary

No human decision fields are prefilled and no external action is authorized. Source: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md#L202-L209`.
