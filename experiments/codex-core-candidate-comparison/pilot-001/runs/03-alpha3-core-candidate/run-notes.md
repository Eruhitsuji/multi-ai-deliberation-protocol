# ALPHA3_CORE_CANDIDATE run notes

## Attempt-002 Phase 4D-B Human Final Authority decision

- authorization_record:
  - cumulative_human_action_number: 32
  - attempt_local_human_action_number: 20
  - authorized_phase: `ATTEMPT_002_PHASE_4D_B_HUMAN_FINAL_AUTHORITY_DECISION_RECORDING`
- attempt_status: `HUMAN_FINAL_DECISION_RECORDED`
- selected_option_id: `OPTION-A`
- selected_path: `COMPARISON_FIRST`
- selection_mode: `CONDITIONAL`
- mandatory_pre_field_trial_gates: [`EG-001`, `EG-005`]
- fallback_option: `OPTION-B`
- automatic_switch_authorized: false
- new_human_decision_required_for_fallback: true
- alpha4_disposition: `CONSIDER_AFTER_COMPARISON`
- task_completed_by_human_decision: true
- ready_for_core_conformance_evaluation: true
- core_conformance: `NOT_EVALUATED`
- formal_release_evidence: false
- alpha4_authorized: false
- completion_time_seconds: null
- metrics_finalized: false
- experiment_yaml_changed: false
- raw_participant_evidence_changed: false
- release_authorized: false

## Attempt-002 Phase 4D-A Human review packet

- authorization_record:
  - cumulative_human_action_number: 31
  - attempt_local_human_action_number: 19
  - authorized_phase: `ATTEMPT_002_PHASE_4D_A_HUMAN_REVIEW_PACKET`
- attempt_status: `AWAITING_HUMAN_FINAL_AUTHORITY_INPUT`
- phase_type: read-only review packet presentation
- decision_draft_updated: false
- experiment_yaml_changed: false
- raw_evidence_changed: false
- analysis_artifacts_changed: false
- human_final_decision_recorded: false
- core_conformance: `NOT_EVALUATED`
- formal_release_evidence: false
- alpha4_authorized: false
- metrics_finalized: false
- completion_timer_stopped: false

## Attempt-002 Phase 4C structured comparison

- authorization_record:
  - cumulative_human_action_number: 30
  - attempt_local_human_action_number: 18
  - authorized_phase: `ATTEMPT_002_PHASE_4C_STRUCTURED_COMPARISON_AND_HUMAN_DECISION_PREPARATION`
- attempt_status: `READY_FOR_HUMAN_DECISION`
- structured_comparison_artifact_dir: `attempts/attempt-002/artifacts/structured-comparison/`
- stage_a_hash_fixed_before_stage_b: true
- preliminary_blind_first_round_status: `VALID`
- preliminary_convergence_classification: `MIXED`
- blind_multi_group_convergence_cluster_count: 2
- common_source_mandated_cluster_count: 4
- material_dissent_count: 4
- unresolved_material_dissent_count: 3
- blocking_evidence_gap_count: 2
- candidate_options: `OPTION-A`, `OPTION-B`, `OPTION-C`
- best_supported_option_for_human_review: `OPTION-A`
- gemini_reconciliation_limitation:
  - canonical_cross_exposure_response: `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md`
  - noncanonical_duplicate_submission_preserved: `attempts/attempt-002/raw/cross-exposure-GEMINI-B.md`
  - noncanonical_submission_used_for_semantic_analysis: false
- validation:
  - custom_structured_comparison_validation: PASS
  - dynamic_role_plan_checker: PASS
  - pilot_validator: PASS
  - core_candidate_experiments_checker: PASS
  - source_reference_validation: PASS
  - raw_evidence_unchanged: true
  - experiment_yaml_diff_empty: true
- boundaries:
  - human_final_decision_recorded: false
  - core_conformance: `NOT_EVALUATED`
  - formal_release_evidence: false
  - alpha4_authorized: false
  - release_authorized: false
  - experiment_yaml_changed: false
  - attempt_001_evidence_changed: false
  - sibling_run_used: false
- metrics:
  - cumulative_human_actions: 30
  - attempt_local_human_actions: 18
  - completion_time_seconds: null
  - metrics_finalized: false

Run status: CROSS_EXPOSURE_RECONCILIATION_IN_PROGRESS for attempt-002 Phase 4B-R.

Latest attempt-002 reconciliation authorization:

```yaml
cumulative_human_action_number: 28
attempt_local_human_action_number: 16
authorized_phase: ATTEMPT_002_PHASE_4B_RECONCILIATION
codex_receipt_timestamp_utc: 2026-07-18T16:11:10Z
status: CROSS_EXPOSURE_RECONCILIATION_IN_PROGRESS
cross_exposure_authorized: true
cross_exposure_started: true
phase4c_authorized: false
comparison_performed: false
decision_created: false
awaiting_retrospective_send_attestation: true
awaiting_gemini_ui_inspection_attestation: true
```

Latest attempt-002 reconciliation attestation and disposition:

```yaml
cumulative_human_action_number: 29
attempt_local_human_action_number: 17
codex_receipt_timestamp_utc: 2026-07-18T16:15:21Z
retrospective_send_action_ids:
  - HA-RETRO-CROSS-SEND-CLAUDE-B
  - HA-RETRO-CROSS-SEND-GEMINI-B
retrospective_send_time_inferred: false
gemini_ui_inspection_result: DIFFERENT_RESPONSE_PRESENT
case: CASE_A
gemini_disposition: UI_RECAPTURE_CANONICALIZED
canonical_raw_response_ref: attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md
canonical_raw_response_sha256: 9251f0715198f992988392e78d2077d958e4f5875cff15e67277253500c2802e
canonical_raw_response_bytes: 31008
status: CROSS_EXPOSURE_RESPONSES_CAPTURED_WITH_RECONCILIATION
valid_cross_exposure_response_count: 3
ready_for_structured_comparison: true
phase4c_authorized: false
comparison_performed: false
decision_created: false
```

## Timing

- run_start_utc: `2026-07-18T11:10:54Z`
- completion_time_seconds_start: immediately before first operator command after human Phase 1 approval
- completion_time_seconds_end: not reached
- intentional_interruptions: none recorded

## Commit binding

- operator_environment_commit: `43815810f988588a29ba2dcaea9d2641d6263606`
- tested_alpha3_baseline_commit: `2a29ddfebe4d9664d3a4043a01d8728fa525d049`
- current_operator_branch: `experiment/pilot-001-core`
- checkout_reset_rebase_or_branch_change_in_core_worktree: not performed

## Task binding

- task_file: `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md`
- task_sha256_registered: `34cb80469054d7da7cafed6f091f73d0c127d71b5e9c132b52f455a509d72c1c`
- task_sha256_actual: `34cb80469054d7da7cafed6f091f73d0c127d71b5e9c132b52f455a509d72c1c`

## Compact bundle artifacts

- output_directory: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/compact-bundle`
- bundle_file: `MADP-v0.3.0-alpha.3-core-compact.md`
- bundle_sha256: `303fd59a8e08a052bdef74a3545fd74a1ad5182e994c5970861428fe2b5b9c48`
- bundle_bytes: `62637`
- manifest_file: `MADP-v0.3.0-alpha.3-core-compact.manifest.yaml`
- manifest_sha256: `762ba8b6c60e0ec33d25e39b3c94116f138dc0feb1c143b35417ddce84e001c0`
- manifest_bytes: `1745`
- source_inventory_sha256: `9b63d53922c0f7475ba475419bb4a934f5aa48d912ff464a9bd8d527a58e2ee9`
- deterministic_regeneration_diff: `PASS`
- temporary_regeneration_directory: `/tmp/tmp.o5USricokv/compact-bundle`

## Profile hash from tested baseline worktree

- profile_file: `docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md`
- profile_sha256: `0f9e2007407e8c565b0c128bdcdaa678b4b5ed3a0aeb76f76bff35460a6ccfc1`
- profile_bytes: `7754`

## Validators

- `python scripts/check_alpha3_core_compact_bundle.py ...`: PASS
- `python scripts/check_alpha3_core_candidate.py`: PASS
- `python tests/v0.3.0-alpha.3/test_core_distribution_and_role_planning.py`: PASS
- `python experiments/codex-core-candidate-comparison/pilot-001/validate.py`: PASS
- `python scripts/check_alpha3_core_candidate_experiments.py`: PASS

## Temporary baseline worktree

- path: `/mnt/e/madp-codex-pilot-core-baseline`
- created: yes
- head_verified: `2a29ddfebe4d9664d3a4043a01d8728fa525d049`
- removed_after_success: yes

## Phase 1 scope

Allowed in this phase:

- source binding
- compact bundle generation from detached baseline worktree
- compact bundle validation
- command and operator-action logging

Not allowed in this phase:

- participant raw response creation
- cross-exposure record creation
- decision record creation
- dynamic role plan generation
- Blind First Round final records
- `experiment.yaml` modification
- external AI queries
- release state changes

## Human action count

- current_confirmed_human_actions: `1`
- action_1: human approved ALPHA3_CORE_CANDIDATE run start and Phase 1 source binding / compact bundle preparation.
- action_2: human approved Phase 2 participant registration, dynamic role planning, and Blind First Round packet preparation.
- action_3: human approved Phase 3A Blind First Round send preparation; authorized rendered participant prompts, capture register, raw directory creation, checklist update, manifest rendering metadata update, and validation without external AI sending.
- action_4: human approved Phase 3B Blind First Round send and raw capture; authorized human external-AI sending, Codex send recording, raw response preservation, SHA-256 calculation, capture register updates, and mechanical validation; did not authorize Cross Exposure, comparison, critique, integration, or decision creation.
- action_5: human submitted CHATGPT-A raw response.
- action_6: human submitted CLAUDE-A raw response.
- action_7: human submitted GEMINI-A raw response.
- action_HA-RETRO-SEND-CHATGPT-A: retrospective human attestation that CHATGPT-A external send occurred before the corresponding raw submission; exact send time unavailable.
- action_HA-RETRO-SEND-CLAUDE-A: retrospective human attestation that CLAUDE-A external send occurred before the corresponding raw submission; exact send time unavailable.
- action_HA-RETRO-SEND-GEMINI-A: retrospective human attestation that GEMINI-A external send occurred before the corresponding raw submission; exact send time unavailable.
- action_11: human approved Phase 3C Blind First Round send-record reconciliation.
- action_12: human approved Phase 4A Cross Exposure packet preparation and fixed the Cross Exposure attachment order and prompt template.

## Phase 2 dynamic role planning

- dynamic_role_input: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/dynamic-role-input.yaml`
- dynamic_role_input_sha256: `9fc808a5e085f57247294b35937e07a4331dfdd87fee43602334b76febfdf2e9`
- dynamic_role_plan: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/dynamic-role-plan.yaml`
- dynamic_role_plan_sha256: `396041ae9389da51ddab78413973e6a9a06e3cc101af5592a9be9b462be261cc`
- dynamic_role_plan_status: `READY`
- blind_first_round_plan_status: `PLAN_VALID`

## Phase 2 participant register and packet

- participant_register: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/participant-register.yaml`
- participant_register_sha256: `a154fcbb5db4623c5b06a406464236c5e40b05e316a00f5b9b2ced03283f37b9`
- participant_initial_prompt: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/blind-first-round/participant-initial-prompt.md`
- participant_initial_prompt_sha256: `b132c9b8dd17a4b61ea739cdc986cf82407b9b78fe66e222565d2f4d1b8bc39e`
- information_set_manifest: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/blind-first-round/information-set-manifest.yaml`
- information_set_manifest_sha256: `848fcdd7ec56e4ff22b1a7a0d9b2bf662518ebcc616125cf0d25f2371fb53b0e`
- operator_send_checklist: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/blind-first-round/operator-send-checklist.md`
- operator_send_checklist_sha256: `206fc5f9385ea112b52a17714e9f053ac5a8ae3b53146b3ce745562274d80a3f`
- information_set_hash: `a754c49463e74c2fe79ed039438da070ed3ea0259fd55c87c71195a901f26925`
- information_set_hash_method: exact bytes concatenated in order: task prompt, compact bundle Markdown, participant initial prompt, participant register, dynamic role plan; no separators, directory metadata, mtimes, filenames, or normalization.

## Phase 2 assignments

- `ASSIGN-PROPOSER-1`: CHATGPT-A / BLIND_INITIAL / PROPOSE_ONLY / independent_count_eligible=true
- `ASSIGN-PROPOSER-2`: CLAUDE-A / BLIND_INITIAL / PROPOSE_ONLY / independent_count_eligible=true
- `ASSIGN-PROPOSER-3`: GEMINI-A / BLIND_INITIAL / PROPOSE_ONLY / independent_count_eligible=true
- `ASSIGN-FACILITATOR-1`: CHATGPT-A / ALL / PROPOSE_ONLY
- `ASSIGN-CRITIC-1`: CLAUDE-A / CROSS_EXPOSURE / OPINION_ONLY
- `ASSIGN-EVIDENCE_REVIEWER-1`: GEMINI-A / CROSS_EXPOSURE / OPINION_ONLY
- `ASSIGN-RECORDER-1`: CHATGPT-A / ALL / RECORD_ONLY

## Phase 2 temporary directory

- checked_directory: `/tmp/tmp.o5USricokv`
- content_verified_as_phase1_second_bundle_only: yes
- deleted: yes

## Phase 2 boundaries

- external_ai_prompt_sent: no
- participant_response_generated_or_captured: no
- raw_response_directory_exists: no
- cross_exposure_performed: no
- decision_record_created: no

## Phase 3A rendered prompts

- common_information_set_hash_preserved: `a754c49463e74c2fe79ed039438da070ed3ea0259fd55c87c71195a901f26925`
- template_preserved: yes
- rendered_prompt_diff_check: PASS; only `participant_id` and `model_label` substitutions differ from `participant-initial-prompt.md`.
- `rendered-prompt-CHATGPT-A.md`: sha256=`60856cfacfd8e6e380aef8a84f2df11b5a4882b92c0deedaa35cdc3144dc77df`, bytes=`1603`
- `rendered-prompt-CLAUDE-A.md`: sha256=`27fd1033b90e467a9756221110c7627ab5bf04536dda85f794f8f520f8cafc72`, bytes=`1599`
- `rendered-prompt-GEMINI-A.md`: sha256=`2b9edd842e6f090f5566ae6bd58abec9d365580c47bca38f7e8eb01461ee2b3f`, bytes=`1598`

## Phase 3A capture preparation

- capture_register: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/blind-first-round/capture-register.yaml`
- capture_register_sha256: `cbe9882a680092d7be53394b4296bc3f72387fbf21a612a04f341be1d4b37e3b`
- updated_information_set_manifest_sha256: `f91fe38e0e1a6dc8b3b261ddffdae73986c4a8b2420e9767f772962cb4a4ae3f`
- raw_directory: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/`
- raw_directory_empty: yes
- cross_exposure_authorized: false
- cross_exposure_started: false

## Phase 3A boundaries

- external_ai_prompt_sent: no
- external_ai_chat_created: no
- participant_response_generated_or_captured: no
- raw_response_file_created: no
- cross_exposure_performed: no
- participant_outputs_shared: no
- decision_record_created: no

## Phase 3B boundaries

- send_order: `CHATGPT-A`, `CLAUDE-A`, `GEMINI-A`
- waiting_for_send_confirmed_reports: yes
- external_ai_prompt_sent_by_codex: no
- cross_exposure_authorized: false
- cross_exposure_started: false
- comparison_or_summary_authorized: no
- decision_record_authorized: no

## Phase 3B partial raw capture

### CHATGPT-A

- raw_response_submission_action: `5`
- raw_response_received_at_utc: `2026-07-18T13:12:53Z`
- raw_response_path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CHATGPT-A.md`
- raw_response_sha256: `b405cd9f321ba092ffa402ab501db44a6484d4308292fbd1e279e2d87ad77377`
- raw_response_bytes: `32709`
- model_label_confirmed_by_submission: `GPT-5.6 Sol`
- expected_model_label: `GPT-5.6 Sol`
- model_label_match_in_submission_metadata: yes
- model_label_in_raw_response_header: `GPT-5.6 Thinking`
- deviation: raw response header model_label differs from expected/submission-confirmed model label.
- send_confirmed_report_received: no
- sent_at_utc: `UNKNOWN`
- send_action_number: `UNKNOWN`
- external_web_research_observed_by_human: false
- other_participant_outputs_seen_before_response_capture: false
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: no
- action_taken_on_content: none; raw response preserved without correction, summary, comparison, or critique.

## Phase 3B completion validation

- raw_response_file_count: `3`
- raw_response_files:
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CHATGPT-A.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CLAUDE-A.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-GEMINI-A.md`
- duplicate_or_overwrite_detected: no
- capture_register_raw_hash_match: PASS
- captured_before_cross_exposure_all: true
- exposed_response_refs_empty_all: true
- cross_exposure_authorized: false
- cross_exposure_started: false
- participant_register_raw_file_mapping: PASS
- rendered_prompt_hashes_unchanged: PASS
- common_information_set_hash_unchanged: `a754c49463e74c2fe79ed039438da070ed3ea0259fd55c87c71195a901f26925`
- experiment_yaml_changed_after_phase3b: no
- capture_register_sha256_final_phase3b: `ed5bb0f332090c87b7f8ebc00a4b570ee4ea02701a9ed2881674096f19c00cac`
- validators:
  - `python scripts/check_alpha3_dynamic_role_plan.py experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/dynamic-role-plan.yaml`: PASS
  - `python experiments/codex-core-candidate-comparison/pilot-001/validate.py`: PASS
  - `python scripts/check_alpha3_core_candidate_experiments.py`: PASS

## Phase 3B unresolved timing/action gaps

- `SEND_CONFIRMED` reports received in realtime: none
- retrospective send attestation received in Phase 3C: yes
- sent_at_utc values: `null` / `UNKNOWN` for CHATGPT-A, CLAUDE-A, GEMINI-A
- human external prompt-send action IDs: `HA-RETRO-SEND-CHATGPT-A`, `HA-RETRO-SEND-CLAUDE-A`, `HA-RETRO-SEND-GEMINI-A`
- confirmed human action count through Phase 3C: `11`
- remaining timing limitation: exact send times unavailable; no reverse inference from received_at_utc was performed

## Phase 3B mechanical participant-output observations

- CHATGPT-A: submission metadata model label was `GPT-5.6 Sol`; raw response header model label was `GPT-5.6 Thinking`.
- CLAUDE-A: submission metadata and raw response header model label both `Opus 4.8`.
- GEMINI-A: submission metadata and raw response header model label both `3.1 Pro`; raw response begins with the required header inside a fenced YAML block.
- All submissions reported `external_web_research_observed: false`.
- All submissions reported `other_participant_outputs_seen_before_response_capture: false`.
- All raw response headers state `authority: PROPOSE_ONLY`.
- No raw response was corrected, reformatted, translated, summarized, compared, or shared with another participant.

## Phase 3C send reconciliation

- send_reconciliation_file: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/blind-first-round/send-reconciliation.yaml`
- send_reconciliation_sha256: `4b6491770510c6359af8666428133f7b091f0334f9ca1545199b14a1b87dc057`
- reconciliation_basis: `RETROSPECTIVE_HUMAN_ATTESTATION`
- send_confirmed_in_realtime: false
- exact_send_times_available: false
- external_send_actions_added:
  - `HA-RETRO-SEND-CHATGPT-A`
  - `HA-RETRO-SEND-CLAUDE-A`
  - `HA-RETRO-SEND-GEMINI-A`
- current_human_action_total: `11`
- capture_register_sha256_after_phase3c: `e06a865e1e2047480f26c4bc12ea5ae4674bad3bf20b6708669aa97f31d8c0c6`
- raw_response_hashes_recomputed_after_phase3c:
  - CHATGPT-A: `b405cd9f321ba092ffa402ab501db44a6484d4308292fbd1e279e2d87ad77377`, bytes=`32709`
  - CLAUDE-A: `23d3bfb31da0fb29e93a524e0487c9703bd6a98c4e3cb3e1f94e1c37d6379ca3`, bytes=`26120`
  - GEMINI-A: `0281d4d113c5aa277b2e207209963a026b7a3a751559c2b2164d0498dd1726b5`, bytes=`22893`
- raw_responses_changed_in_phase3c: no
- cross_exposure_authorized: false
- cross_exposure_started: false
- blind_first_round_mechanical_state:
  - raw_initial_responses_present: 3
  - all_saved_before_cross_exposure: true
  - all_exposure_state: `UNEXPOSED`
  - all_sha256_recorded: true
  - independence_group_count_recorded: 3
  - chatgpt_model_label_conflict_recorded: true
- not_evaluated_in_phase3c:
  - convergence classification
  - participant response quality
  - Core conformance final status
  - best proposal
  - material dissent
  - decision result
- phase3c_validators:
  - `python scripts/check_alpha3_dynamic_role_plan.py experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/dynamic-role-plan.yaml`: PASS
  - `python experiments/codex-core-candidate-comparison/pilot-001/validate.py`: PASS
  - `python scripts/check_alpha3_core_candidate_experiments.py`: PASS
- experiment_yaml_changed_after_phase3c: no
- sibling_run_directories_read_in_phase3c: none
- release_state_changed_in_phase3c: no
- formal_release_evidence_changed_in_phase3c: no
- alpha4_authorized_changed_in_phase3c: no

## Phase 4A Cross Exposure packet preparation

- human_action_total_after_phase4a_approval: `12`
- cross_exposure_directory: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/`
- cross_exposure_prompt_template: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/cross-exposure-prompt-template.md`
- cross_exposure_prompt_template_sha256: `c706d32a63528e86a3edf573b5d27f7c514a848e36b8f432e211b3b12f6b1559`
- cross_exposure_prompt_template_bytes: `3909`
- rendered_prompts:
  - participant_id: CHATGPT-A
    path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/rendered-prompt-CHATGPT-A.md`
    sha256: `3f94b426a8e14be0cc06628294a326d4df0f7129162cb2aac29c5b0efc9ce3a6`
    bytes: `3907`
  - participant_id: CLAUDE-A
    path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/rendered-prompt-CLAUDE-A.md`
    sha256: `7ad07e2c47d816792b59a4acb949caef787ab42415bb602b3045da97126020d0`
    bytes: `3902`
  - participant_id: GEMINI-A
    path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/rendered-prompt-GEMINI-A.md`
    sha256: `cdc7be82e2e72546084cce7e1ff35ac21379c35faa168fb8a02a29586b001dd2`
    bytes: `3901`
- rendered_prompt_diff_check: PASS; only `PARTICIPANT_ID`, `MODEL_LABEL`, and `OWN_INITIAL_RESPONSE_REF` replacements differ from template.
- cross_exposure_common_information_set_hash: `7c7a642de7f16640b17a35bf78b8c7fd9ede199fb30ec963032971c62fb5fbf7`
- cross_exposure_information_set_manifest: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/cross-exposure-information-set-manifest.yaml`
- cross_exposure_information_set_manifest_sha256: `f1d9cdc322ee5420590315ada0e8315e75ca0b7a32d279bd7fee392fb9450b35`
- cross_exposure_capture_register: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/cross-exposure-capture-register.yaml`
- cross_exposure_capture_register_sha256: `8af2849f83ac2fcdceed5124a8efe1671c23c2b825f68d1d927530ec2f9a410d`
- cross_exposure_operator_checklist: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/cross-exposure/operator-cross-exposure-checklist.md`
- attachment_order_identical_for_all_participants: true
- attachment_order:
  - `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/compact-bundle/MADP-v0.3.0-alpha.3-core-compact.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CHATGPT-A.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CLAUDE-A.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-GEMINI-A.md`
- newly_exposed_response_refs:
  - participant_id: CHATGPT-A
    refs:
      - `raw/initial-response-CLAUDE-A.md`
      - `raw/initial-response-GEMINI-A.md`
  - participant_id: CLAUDE-A
    refs:
      - `raw/initial-response-CHATGPT-A.md`
      - `raw/initial-response-GEMINI-A.md`
  - participant_id: GEMINI-A
    refs:
      - `raw/initial-response-CHATGPT-A.md`
      - `raw/initial-response-CLAUDE-A.md`
- raw_initial_response_hash_check_phase4a:
  - CHATGPT-A: `b405cd9f321ba092ffa402ab501db44a6484d4308292fbd1e279e2d87ad77377`, bytes=`32709`
  - CLAUDE-A: `23d3bfb31da0fb29e93a524e0487c9703bd6a98c4e3cb3e1f94e1c37d6379ca3`, bytes=`26120`
  - GEMINI-A: `0281d4d113c5aa277b2e207209963a026b7a3a751559c2b2164d0498dd1726b5`, bytes=`22893`
- cross_exposure_raw_response_files_exist: false
- cross_exposure_authorized: false
- cross_exposure_started: false
- validators_phase4a:
  - `python scripts/check_alpha3_dynamic_role_plan.py experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/artifacts/dynamic-role-plan.yaml`: PASS
  - `python experiments/codex-core-candidate-comparison/pilot-001/validate.py`: PASS
  - `python scripts/check_alpha3_core_candidate_experiments.py`: PASS
- external_ai_sent_in_phase4a: no
- chat_created_in_phase4a: no
- participant_response_semantic_analysis_performed: no
- initial_response_comparison_or_summary_performed: no
- convergence_classification_performed: no
- core_conformance_judgment_performed: no
- decision_record_created: no
- experiment_yaml_changed_after_phase4a: no
- sibling_run_directories_read_in_phase4a: none
- release_state_changed_in_phase4a: no
- formal_release_evidence_changed_in_phase4a: no
- alpha4_authorized_changed_in_phase4a: no

## Cross Exposure blocker

```yaml
cross_exposure_blocker:
  status: BLOCKED
  reason: ORIGINAL_PARTICIPANT_CHATS_UNAVAILABLE
  discovered_before_cross_exposure_send: true
  blind_initial_responses_preserved: true
  cross_exposure_authorized: false
  cross_exposure_started: false
  new_chat_substitution_performed: false
  raw_cross_exposure_responses_created: false
  human_decision_required: true
```

Phase 4A packet, manifest, rendered prompts, Blind First Round raw responses, raw SHA-256 values, and Blind First Round capture register were not changed while recording this blocker.

Required human choice before continuing:

1. create a new run revision that repeats Blind First Round with chat contexts that will remain available for Cross Exposure; or
2. continue only as degraded/nonconforming review with explicit metadata changes that preserve the fact that same-chat Cross Exposure was not possible.
- capture_register_sha256_after_claude_a_capture: `a1883cc1c62f38151c36b67c2787e2d2df2b5bebcfaf9e9de0d9619209aecb93`
- partial_capture_validation_after_claude_a: PASS
- raw_files_present_after_claude_a_capture:
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CHATGPT-A.md`
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CLAUDE-A.md`
- experiment_yaml_changed_after_claude_a_capture: no

### GEMINI-A

- raw_response_submission_action: `7`
- raw_response_received_at_utc: `2026-07-18T13:22:25Z`
- raw_response_path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-GEMINI-A.md`
- raw_response_sha256: `0281d4d113c5aa277b2e207209963a026b7a3a751559c2b2164d0498dd1726b5`
- raw_response_bytes: `22893`
- model_label_confirmed_by_submission: `3.1 Pro`
- expected_model_label: `3.1 Pro`
- model_label_match_in_submission_metadata: yes
- model_label_in_raw_response_header: `3.1 Pro`
- send_confirmed_report_received: no
- sent_at_utc: `UNKNOWN`
- send_action_number: `UNKNOWN`
- external_web_research_observed_by_human: false
- other_participant_outputs_seen_before_response_capture: false
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: no
- action_taken_on_content: none; raw response preserved without correction, summary, comparison, or critique.
- capture_register_sha256_after_chatgpt_a_capture: `36adb1de44e5f50c519763429e6c83bb16a4a6044b63528f3ae1c38fa8f66810`
- partial_capture_validation: PASS
- raw_files_present_after_capture:
  - `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CHATGPT-A.md`
- experiment_yaml_changed_after_capture: no

### CLAUDE-A

- raw_response_submission_action: `6`
- raw_response_received_at_utc: `2026-07-18T13:18:07Z`
- raw_response_path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/raw/initial-response-CLAUDE-A.md`
- raw_response_sha256: `23d3bfb31da0fb29e93a524e0487c9703bd6a98c4e3cb3e1f94e1c37d6379ca3`
- raw_response_bytes: `26120`
- model_label_confirmed_by_submission: `Opus 4.8`
- expected_model_label: `Opus 4.8`
- model_label_match_in_submission_metadata: yes
- model_label_in_raw_response_header: `Opus 4.8`
- send_confirmed_report_received: no
- sent_at_utc: `UNKNOWN`
- send_action_number: `UNKNOWN`
- external_web_research_observed_by_human: false
- other_participant_outputs_seen_before_response_capture: false
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: no
- action_taken_on_content: none; raw response preserved without correction, summary, comparison, or critique.

## Isolation

- sibling_run_directories_read: none
- `experiment.yaml` changed in Phase 1: no
- `experiment.yaml` changed in Phase 2: no
- `experiment.yaml` changed in Phase 3A: no
- release_state_changed: no
- formal_release_evidence_changed: no
- alpha4_authorized_changed: no

## Attempt 002 restart

```yaml
attempt_restart:
  attempt_id: CORE-ATTEMPT-002
  workflow: ALPHA3_CORE_CANDIDATE
  restart_scope: BLIND_FIRST_ROUND_AND_LATER
  tested_baseline_commit: 2a29ddfebe4d9664d3a4043a01d8728fa525d049
  operator_environment_commit: 43815810f988588a29ba2dcaea9d2641d6263606
  prior_attempt_status: ABORTED_BEFORE_CROSS_EXPOSURE
  prior_attempt_reason: ORIGINAL_PARTICIPANT_CHATS_UNAVAILABLE
  prior_attempt_evidence_preserved: true
  prior_attempt_outputs_reused: false
  prior_attempt_outputs_visible_to_participants: false
  cross_exposure_authorized: false
  cross_exposure_started: false
  formal_release_evidence: false
  alpha4_authorized: false
```

```yaml
human_action_metrics:
  cumulative_workflow_human_actions:
    basis: ALL_ATTEMPTS_FROM_ORIGINAL_RUN_START
    reset_on_restart: false
    current_total: 13
    latest_action: THIS_RESTART_AUTHORIZATION
  attempt_local_human_actions:
    attempt_id: CORE-ATTEMPT-002
    current_total: 1
    first_action: THIS_RESTART_AUTHORIZATION
```

The original workflow completion timer is not reset. Final workflow metrics must include old attempt time, operations, corrections, restart burden, and attempt-002 activity.

Attempt-002 Blind First Round packet preparation status:

- attempt_status: `READY_FOR_BLIND_FIRST_ROUND`
- attempt_002_information_set_hash: `e08e2bb419f2b2b091f896165471e572f6d94fd4c54ee6c08da2c9ce02a3ed46`
- compact_bundle_sha256: `303fd59a8e08a052bdef74a3545fd74a1ad5182e994c5970861428fe2b5b9c48`
- compact_bundle_bytes: `62637`
- compact_bundle_manifest_sha256: `762ba8b6c60e0ec33d25e39b3c94116f138dc0feb1c143b35417ddce84e001c0`
- compact_bundle_manifest_bytes: `1745`
- dynamic_role_plan_status: `READY`
- blind_first_round_plan_status: `PLAN_VALID`
- attempt_002_raw_directory_empty: true
- external_ai_sent: false
- chat_created_by_codex: false
- raw_response_created: false
- decision_record_created: false
- experiment_yaml_changed: false
- sibling_run_referenced: false

Attempt-002 Blind First Round raw capture status:

- captured_participant: `CHATGPT-B`
- raw_response_path: `attempts/attempt-002/raw/initial-response-CHATGPT-B.md`
- raw_response_sha256: `0e435699e6ab9a004b5bb14f523a249e459524c3b784b7e3f00e1127fadea4f7`
- raw_response_bytes: `30392`
- codex_capture_timestamp_utc: `2026-07-18T14:38:20Z`
- sent_at_utc: `UNKNOWN`
- send_time_status: `UNKNOWN`
- chat_continuity_status: `NOT_CONFIRMED`
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: false
- response_content_evaluated: false
- cumulative_human_action_total: 16
- attempt_local_human_action_total: 4

Attempt-002 CLAUDE-B raw capture status:

- captured_participant: `CLAUDE-B`
- raw_response_path: `attempts/attempt-002/raw/initial-response-CLAUDE-B.md`
- raw_response_sha256: `737c74a1a247eb861767fbb7cc25c7c365605c5182c0ebd7dc249eb32c8af1a9`
- raw_response_bytes: `25688`
- codex_capture_timestamp_utc: `2026-07-18T14:44:25Z`
- sent_at_utc: `UNKNOWN`
- send_time_status: `UNKNOWN`
- chat_continuity_status: `NOT_CONFIRMED`
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: false
- response_content_evaluated: false
- cumulative_human_action_total: 17
- attempt_local_human_action_total: 5

Attempt-002 GEMINI-B raw capture status:

- captured_participant: `GEMINI-B`
- raw_response_path: `attempts/attempt-002/raw/initial-response-GEMINI-B.md`
- raw_response_sha256: `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482`
- raw_response_bytes: `24741`
- codex_capture_timestamp_utc: `2026-07-18T14:49:54Z`
- sent_at_utc: `UNKNOWN`
- send_time_status: `UNKNOWN`
- chat_continuity_status: `NOT_CONFIRMED`
- captured_before_cross_exposure: true
- exposure_state: `UNEXPOSED`
- raw_response_edited_or_overwritten: false
- response_content_evaluated: false
- cumulative_human_action_total: 18
- attempt_local_human_action_total: 6

Attempt-002 Blind First Round raw capture completion:

- all_initial_responses_captured: true
- captured_participants:
  - `CHATGPT-B`
  - `CLAUDE-B`
  - `GEMINI-B`
- cross_exposure_authorized: false
- cross_exposure_started: false
- participant_outputs_shared: false
- response_content_compared_or_integrated: false

Attempt-002 chat continuity reconciliation authorization:

- authorization_received: true
- cumulative_human_action_total: 19
- attempt_local_human_action_total: 7
- attestation_received: false
- continuity_reconciliation_created: false
- capture_register_updated_for_continuity: false
- attempt_status_updated_for_continuity: false
- cross_exposure_packet_created: false
- cross_exposure_authorized: false
- cross_exposure_started: false

Attempt-002 chat continuity reconciliation result:

- continuity_reconciliation_path: `attempts/attempt-002/artifacts/blind-first-round/continuity-reconciliation.yaml`
- continuity_reconciliation_sha256: `e792c1a0b393e232a71a618201ab6aacecd9f32199b245bb168b6a8d4c644d25`
- verified_at_utc: `2026-07-18T15:00:24Z`
- verified_time_basis: `OPERATOR_ATTESTATION_RECEIPT`
- CHATGPT-B continuity_result: `PASS`
- CLAUDE-B continuity_result: `PASS`
- GEMINI-B continuity_result: `PASS`
- chat_continuity_status: `CONFIRMED`
- attempt_status: `READY_FOR_CROSS_EXPOSURE_PACKET_PREPARATION`
- ready_for_cross_exposure_packet_preparation: true
- actual_chat_urls_recorded: false
- prior_attempt_outputs_seen: false
- raw_response_changed: false
- cross_exposure_packet_created: false
- cross_exposure_authorized: false
- cross_exposure_started: false
- cumulative_human_action_total: 20
- attempt_local_human_action_total: 8

Attempt-002 Cross Exposure packet preparation:

- authorization_action:
  - cumulative_human_action: 21
  - attempt_local_human_action: 9
- prompt_template_sha256: `1bc9145bec4ae0f5fa05ec2aeeefef4592464f851656518776687199b127ae84`
- prompt_template_bytes: `3909`
- rendered_prompt_CHATGPT_B_sha256: `b36f8c189151b286157dd268f8e25826582a94e02ee5dce4e28ad2e3b0e94539`
- rendered_prompt_CLAUDE_B_sha256: `b747c673d31b22795725f86c4c9c329f01e5dfae0269b61e2c8aa56a720c3845`
- rendered_prompt_GEMINI_B_sha256: `b8e5311ff199b1960e5dbd586505d56af2bf7f1447b92126e6578ad087b97392`
- cross_exposure_common_information_set_hash: `3e9978ad568c4a16032b9353293a3887b935bc9117e6c18ae6adee30580d537e`
- manifest_sha256: `3e3266da9093da1cb32e81925d3f623658136fdbed716af511ba9a8e09082b03`
- capture_register_sha256: `1b35ff9031397a84363ed53b84c0a890d61a9c1ec3e92603842ade0005aa5fc7`
- attempt_status: `READY_FOR_CROSS_EXPOSURE`
- cross_exposure_authorized: false
- cross_exposure_started: false
- cross_exposure_raw_response_created: false
- external_ai_sent: false
- response_content_compared_or_evaluated: false
- experiment_yaml_changed: false
- cumulative_human_action_total: 21
- attempt_local_human_action_total: 9

Attempt-002 Cross Exposure Phase 4B authorization:

- cumulative_human_action_total: 22
- attempt_local_human_action_total: 10
- authorized_phase: `ATTEMPT_002_PHASE_4B_CROSS_EXPOSURE_SEND_AND_RAW_CAPTURE`
- status: `CROSS_EXPOSURE_AUTHORIZED`
- cross_exposure_authorized: true
- cross_exposure_started: false
- cross_exposure_started_at_utc: null
- first_send_confirmation_received: false
- external_ai_operated_by_codex: false
- cross_exposure_raw_response_created: false
- response_content_compared_or_evaluated: false
- decision_record_created: false

Attempt-002 Cross Exposure send progress:

- first_send_confirmation_received: true
- cross_exposure_started: true
- cross_exposure_started_at_utc: `2026-07-18T15:32:41Z`
- attempt_status: `CROSS_EXPOSURE_IN_PROGRESS`
- CHATGPT-B_send_status: `SENT`
- CHATGPT-B_sent_at_utc: `2026-07-18T15:32:41Z`
- CHATGPT-B_send_time_basis: `OPERATOR_SEND_CONFIRMATION_RECEIPT`
- CHATGPT-B_external_send_action:
  - cumulative_human_action: 23
  - attempt_local_human_action: 11
- CHATGPT-B_send_confirmation_action:
  - cumulative_human_action: 24
  - attempt_local_human_action: 12
- cumulative_human_action_total: 24
- attempt_local_human_action_total: 12
- cross_exposure_raw_response_created: false
- response_content_compared_or_evaluated: false

Attempt-002 Cross Exposure raw capture progress:

- participant_id: `CHATGPT-B`
- raw_submission_action:
  - cumulative_human_action: 25
  - attempt_local_human_action: 13
- received_at_utc: `2026-07-18T15:40:41Z`
- receive_time_basis: `OPERATOR_RAW_SUBMISSION_RECEIPT`
- response_status: `CAPTURED`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md`
- raw_response_sha256: `21600ecebc974cd8e9c1d561e3b6f9c4c2f046e850edb81dd0febb8f821c0ae5`
- raw_response_bytes: 48180
- model_label_confirmed_by_human_at_capture: `GPT-5.6 Sol`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- cross_exposure_authorized: true
- cross_exposure_started: true
- cross_exposure_started_at_utc: `2026-07-18T15:32:41Z`
- CLAUDE-B_response_status: `NOT_RECEIVED`
- GEMINI-B_response_status: `NOT_RECEIVED`
- response_content_compared_or_evaluated: false
- decision_record_created: false

Attempt-002 Cross Exposure raw capture reconciliation issue:

- participant_id: `GEMINI-B`
- raw_submission_action:
  - cumulative_human_action: 27
  - attempt_local_human_action: 15
- received_at_utc: `2026-07-18T15:57:43Z`
- receive_time_basis: `OPERATOR_RAW_SUBMISSION_RECEIPT`
- send_confirmation_status: `MISSING_BEFORE_RAW_CAPTURE`
- send_status: `UNCONFIRMED`
- sent_at_utc: null
- send_time_status: `UNKNOWN`
- response_status: `CAPTURED`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-GEMINI-B.md`
- raw_response_sha256: `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482`
- raw_response_bytes: 24741
- raw_response_hash_duplicate_of: `attempts/attempt-002/raw/initial-response-GEMINI-B.md`
- expected_prior_participant_outputs_seen: true
- response_self_reported_prior_participant_outputs_seen: false
- cross_exposure_metadata_status: `CONFLICT_RECORDED`
- model_label_confirmed_by_human_at_capture: `3.1 Pro`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- response_content_compared_or_evaluated: false
- decision_record_created: false
- attempt_status: `CROSS_EXPOSURE_RECONCILIATION_REQUIRED`

Attempt-002 Cross Exposure raw capture progress:

- participant_id: `CLAUDE-B`
- raw_submission_action:
  - cumulative_human_action: 26
  - attempt_local_human_action: 14
- received_at_utc: `2026-07-18T15:49:39Z`
- receive_time_basis: `OPERATOR_RAW_SUBMISSION_RECEIPT`
- send_confirmation_status: `MISSING_BEFORE_RAW_CAPTURE`
- send_status: `UNCONFIRMED`
- sent_at_utc: null
- send_time_status: `UNKNOWN`
- response_status: `CAPTURED`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md`
- raw_response_sha256: `0de4538cc3e4810a50ee8324cb639fb6dc0053d6a26758a7cb4c4039430a5fa1`
- raw_response_bytes: 62298
- model_label_confirmed_by_human_at_capture: `Opus 4.8`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- GEMINI-B_response_status: `NOT_RECEIVED`
- response_content_compared_or_evaluated: false
- decision_record_created: false


## Phase 4E-A / Phase 4E finalization

- Human action recorded: cumulative `33`, attempt-local `21`, authorized phase `ATTEMPT_002_PHASE_4E_IDENTIFIER_RECONCILIATION_AND_RESUME`.
- Previous stopped Phase 4E / Phase 4E-A approvals were not present in the operator action log and were not recounted.
- Preserved public-redacted Human Final Authority input records `decided_by: HFA-001`; final decision record records `decided_by: Eruhitsuji`.
- Human Final Authority explicitly clarified that both identifiers refer to the same human and that `Eruhitsuji` is the official record identifier. Existing decision evidence files were not modified.
- Created identifier reconciliation evidence and included DEV-004 in Core conformance evaluation.
- Final Core conformance classification: `DEGRADED` due to protocol-significant reconciliation limitations DEV-002, DEV-003, and DEV-004, while required Core sequence and decision reconstruction remain usable.
- Completion timer stopped at `2026-07-18T18:07:34Z` after primary validation passed. Completion time from `2026-07-18T11:10:54Z` is `25000` seconds.
- Metrics finalized with explicit nulls for unobserved values; cumulative human actions `33`, attempt-local `21`.
- `experiment.yaml` reflects only the `ALPHA3_CORE_CANDIDATE` run; experiment status and conclusion are not finalized.
- `task_completed_by_human_decision: true` means only the bounded decision task is complete, not selected work package execution, field trial, release, A3-REL-001/A3-REL-005 completion, or alpha.4 authorization.
- Formal release evidence remains false; alpha4_authorized remains false; pilot_completed remains false.
- Next preregistered workflow: `MARKDOWN_VALIDATOR`; not authorized.


## PRIVACY-1 public identifier redaction

- Human action recorded: cumulative `34`, attempt-local `22`, authorized phase `CORE_ATTEMPT_002_PRIVACY_1_PUBLIC_IDENTIFIER_REDACTION`.
- Public replacement identifier: `HFA-001`.
- The private original Human Final Authority input was backed up outside the repository before redaction. The private backup path and private original hash are not recorded in public artifacts.
- The public repository now uses `artifacts/structured-comparison/human-final-authority-input-public-redacted.md` as the decision source copy.
- The unredacted raw Human Final Authority input was removed from the public repository tree after backup.
- DEV-004 and the identifier provenance limitation are preserved with public pseudonymous wording.
- Human Final Authority decision content is unchanged: OPTION-A / COMPARISON_FIRST / CONDITIONAL, Blind status VALID, convergence MIXED, task_completed true, Core conformance DEGRADED.
- No commit, push, PR, merge, release, formal release evidence recognition, A3-REL-001/A3-REL-005 completion, or alpha.4 authorization was performed.
- Git commit identity check found a public-before-commit blocker: local email is not in the required GitHub noreply format. The email value is not recorded here.


## Human Final Authority termination and Rapid Prerelease transition

- decision_time_recorded_utc: `2026-07-19T03:52:18Z`
- experiment_id: `EXP-CODEX-PILOT-001`
- experiment_status: `TERMINATED_BY_HUMAN_FINAL_AUTHORITY`
- termination_class: `RESOURCE_CONSTRAINT_AND_PRIORITY_CHANGE`
- termination_reason_primary: `RESOURCE_AND_WORKFLOW_COST`
- factors: generated AI usage cost, human operating time, long waiting time, interference with other work, low incremental value for current single-user operation.
- completed_workflows: `ALPHA3_CORE_CANDIDATE`
- cancelled_workflows: `MARKDOWN_VALIDATOR`, `MANUAL_MULTI_AI`, `STANDARD_ALPHA3`
- full_comparison_completed: false
- comparative_conclusion_authorized: false
- pilot_completed: false
- core_candidate_evidence_preserved: true
- unsupported_claims: superiority between four workflows, relative human burden, relative completion time, comparative authority/stale-revision error rates, and four-workflow-based alpha.4 recommendation.
- rapid_prerelease_policy: `MADP-RAPID-PRERELEASE-v1`
- next_prerelease_line: `v0.3.0-alpha.4`
- alpha4_implementation_authorized_by_separate_human_development_decision: true
- alpha4_prerelease_authorized_by_separate_human_development_decision: true
- authorization_derived_from_comparison_experiment: false
- stable_release_authorized: false
- formal_release_evidence: false
- A3-REL-001_and_A3-REL-005_retained_as_stable_release_gates: true
- local_validator_resolver_issue: `JSONSCHEMA_REF_RESOLUTION_ERROR`, deferred and nonblocking for experiment termination/local record preservation/prerelease if required GitHub Actions pass.
- no commit, push, PR, merge, tag, GitHub Release, or Pages publication performed.
