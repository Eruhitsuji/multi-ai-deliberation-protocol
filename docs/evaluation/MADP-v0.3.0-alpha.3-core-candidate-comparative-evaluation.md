# MADP v0.3.0-alpha.3 Core Candidate Comparative Evaluation

Status: experimental evaluation procedure. It is not formal release evidence.

## Purpose

Compare one bounded decision task across four workflows:

1. `MANUAL_MULTI_AI`
2. `STANDARD_ALPHA3`
3. `ALPHA3_CORE_CANDIDATE`
4. `MARKDOWN_VALIDATOR`

The experiment asks whether the Core Candidate reduces human burden and unclear
next actions without increasing authority errors, stale-revision errors, loss of
raw records, or loss of material dissent.

This experiment does not complete `A3-REL-001`, sign off usability evidence,
authorize a release, or authorize alpha.4. alpha.4 remains deferred until a human
reviews comparative evidence.

## Evidence boundary

Use the experimental schema:

```text
schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml
```

Start from:

```text
docs/evaluation/MADP-v0.3.0-alpha.3-core-candidate-comparison-template.yaml
```

The artifact always records:

```yaml
formal_release_evidence: false
conclusion:
  alpha4_authorized: false
```

A formal FIELD_TRIAL remains a separate receipt-bound process.

## Experimental control

Use the same task statement and acceptance criteria for all four workflows.

Before the first run:

1. freeze the task text;
2. calculate `task.prompt_sha256`;
3. record the human authority boundary;
4. select participants and record service, model label, chat context, correlation,
   and independence group;
5. choose a run order.

To reduce learning effects, randomize or rotate the workflow order when practical.
Use a new chat context for each run. Do not silently transfer conclusions between
runs. When a common source, model family, prompt lineage, or retrieval origin is
known, record the correlation rather than claiming independence.

## Workflow definitions

### MANUAL_MULTI_AI

Ordinary copy-and-paste comparison without the alpha.3 runtime. Manual relay is a
first-class baseline, not a failure mode.

### STANDARD_ALPHA3

Use the current alpha.3 protocol and canonical commands without the Core Candidate
Workflow Macro layer.

### ALPHA3_CORE_CANDIDATE

Use the Core Candidate Profile and Workflow Macros. This workflow requires a
Blind First Round for a conforming multi-participant run.

### MARKDOWN_VALIDATOR

Use typed Markdown or YAML records plus a local validator, without the full
alpha.3 runtime. Preserve authority, raw records, evidence, dissent, and decision
boundaries explicitly.

## Blind First Round fields

For each run, record whether Blind First Round was required and what actually
happened. `VALID` is not inferred from a clean-looking answer. It requires at
least two raw initial responses fixed before direct cross-participant exposure.

Use:

- `VALID`
- `PARTIALLY_COMPROMISED`
- `ANCHORING_EXPOSED`
- `NOT_PERFORMED`
- `NOT_APPLICABLE`

A non-valid status may still produce useful ordinary review evidence. It cannot
be represented as conforming blind-round evidence.

`INDEPENDENT_CONVERGENCE` requires at least two recorded independence groups.
Agreement after exposure or within one correlated group must use
`CORRELATED_CONVERGENCE`, `MIXED`, or another accurate classification.

## Metrics

Record these without post-hoc rewriting:

- `completion_time_seconds`: elapsed task time;
- `human_actions`: messages, confirmations, copy operations, and manual edits;
- `canonical_commands`: accepted canonical command invocations;
- `corrections`: explicit repairs caused by system or user misunderstanding;
- `unclear_next_actions`: pauses where the user could not identify the next step;
- `authority_errors`: unauthorized or falsely authorized state/action attempts;
- `stale_revision_errors`: rejected or incorrectly accepted stale bindings;
- `user_burden`: human rating from 1 to 5.

Also record:

- task completion;
- raw-record preservation;
- authority-boundary recording;
- material dissent count and preserved count;
- decision reconstruction result;
- Core conformance;
- the decision record reference.

## Completion states

`DRAFT` permits null metrics and incomplete participant records.

`READY_FOR_REVIEW` requires all four workflows, a fixed prompt hash, recorded
participants, complete metrics and results, and commit-bound alpha.3 runs.

`HUMAN_REVIEWED` additionally requires a named human reviewer and rationale.

The checker does not choose the best workflow. It only rejects inconsistent or
overclaimed evidence.

## Human conclusion

The reviewer may recommend:

- `KEEP_DEFERRED`
- `CONSIDER_ALPHA4`
- `REVISE_CORE_CANDIDATE`
- `ABANDON_CORE_CANDIDATE`

The artifact cannot set `alpha4_authorized: true`. Starting alpha.4 requires a
separate human decision record.

## Validation

Run:

```bash
python scripts/check_alpha3_core_candidate_experiments.py
```
