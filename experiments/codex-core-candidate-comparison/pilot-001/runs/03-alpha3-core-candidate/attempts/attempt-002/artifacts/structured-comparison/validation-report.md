# Structured comparison validation report

Authority: `PROPOSAL_ONLY`; Human Final Authority required.

## Validation summary

- validation_status: `PASS`
- custom_structured_comparison_validation: `PASS`
- core_conformance: `NOT_EVALUATED`
- formal_release_evidence: `false`
- alpha4_authorized: `false`
- phase4c_authorized: `true`
- human_final_decision_recorded: `false`

## Required checks

1. Canonical raw 6 SHA-256 and byte counts: `PASS`.

   | source | sha256 | bytes |
   |---|---:|---:|
   | `attempts/attempt-002/raw/initial-response-CHATGPT-B.md` | `0e435699e6ab9a004b5bb14f523a249e459524c3b784b7e3f00e1127fadea4f7` | 30392 |
   | `attempts/attempt-002/raw/initial-response-CLAUDE-B.md` | `737c74a1a247eb861767fbb7cc25c7c365605c5182c0ebd7dc249eb32c8af1a9` | 25688 |
   | `attempts/attempt-002/raw/initial-response-GEMINI-B.md` | `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482` | 24741 |
   | `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md` | `21600ecebc974cd8e9c1d561e3b6f9c4c2f046e850edb81dd0febb8f821c0ae5` | 48180 |
   | `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md` | `0de4538cc3e4810a50ee8324cb639fb6dc0053d6a26758a7cb4c4039430a5fa1` | 62298 |
   | `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md` | `9251f0715198f992988392e78d2077d958e4f5875cff15e67277253500c2802e` | 31008 |

2. Noncanonical Gemini raw unchanged: `PASS`, `attempts/attempt-002/raw/cross-exposure-GEMINI-B.md`, SHA-256 `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482`, bytes `24741`.
3. Stage A artifact was created and hash-fixed before Cross Exposure semantic analysis: `PASS`; initial claim ledger SHA-256 `2a0a19cc84552e034708b5eabdb33b05dd03c03e05276e78d66ee0f2e6b26556`, initial convergence assessment SHA-256 `e1f8cb1a063f0b96002a94f708c9077520236452b801b2acfbee72c0f47f7b53`.
4. Stage A artifacts were not changed during Stage B: `PASS`.
5. All claims have source references: `PASS`.
6. All dissents have source references: `PASS`.
7. All candidate work packages have source references: `PASS`.
8. Source line ranges exist: `PASS`.
9. Initial convergence artifact does not include Cross Exposure claims: `PASS`.
10. Post-exposure agreement is not counted as independent convergence: `PASS`.
11. Common-source mandated authority/release boundaries are not counted as task-outcome independent convergence: `PASS`.
12. Gemini canonical response is UI recapture: `PASS`.
13. Noncanonical Gemini raw is excluded from semantic analysis: `PASS`.
14. Human decision fields remain null: `PASS`.
15. `core_conformance: NOT_EVALUATED`: `PASS`.
16. `formal_release_evidence: false`: `PASS`.
17. `alpha4_authorized: false`: `PASS`.
18. `experiment.yaml` has no diff: `PASS`.
19. Sibling run references not present in structured-comparison artifacts: `PASS`.
20. attempt-001 evidence not referenced or changed: `PASS`.
21. Raw evidence unchanged: `PASS`.

## Preliminary findings checked

- preliminary_blind_first_round_status: `VALID`
- preliminary_convergence_classification: `MIXED`
- blind_multi_group_convergence_cluster_count: `2`
- common_source_mandated_cluster_count: `4`
- material_dissent_count: `4`
- unresolved_material_dissent_count: `3`
- blocking_evidence_gap_count: `2`
- candidate_options: `OPTION-A`, `OPTION-B`, `OPTION-C`
- best_supported_option_present: `OPTION-A`
- metrics_finalized: `false`
- completion_time_seconds: `null`

## Existing validator results

- `python scripts/check_alpha3_dynamic_role_plan.py experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/artifacts/dynamic-role-plan.yaml`: `PASS`
- `python experiments/codex-core-candidate-comparison/pilot-001/validate.py`: `PASS`
- `python scripts/check_alpha3_core_candidate_experiments.py`: `PASS`

stdout:

```text
alpha.3 dynamic role plan: PASS
Codex Core Candidate comparison pilot: PASS
task_sha256=34cb80469054d7da7cafed6f091f73d0c127d71b5e9c132b52f455a509d72c1c
experiment_status=DRAFT
alpha.3 Core Candidate operational experiments: PASS (2 experimental schemas, Blind First Round semantics, 4-workflow comparison, Claim/Evidence migration invariants)
```

stderr:

```text
```
