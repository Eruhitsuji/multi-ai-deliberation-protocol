# CORE-ATTEMPT-002 run notes

## Phase 4D-B Human Final Authority decision record

- authorization_record:
  - cumulative_human_action_number: 32
  - attempt_local_human_action_number: 20
  - authorized_phase: `ATTEMPT_002_PHASE_4D_B_HUMAN_FINAL_AUTHORITY_DECISION_RECORDING`
- decided_by:
  - raw_input_value: `HFA-001`
  - human_clarified_formal_value: `Eruhitsuji`
- created:
  - `artifacts/structured-comparison/human-final-authority-input-public-redacted.md`
  - `artifacts/structured-comparison/human-decision-record.yaml`
- preserved:
  - `artifacts/structured-comparison/human-decision-record-draft.yaml`
  - raw participant evidence
  - `experiment.yaml`
- decision:
  - selected_option_id: `OPTION-A`
  - selected_path: `COMPARISON_FIRST`
  - selection_mode: `CONDITIONAL`
  - mandatory_pre_field_trial_gates: [`EG-001`, `EG-005`]
  - fallback_option: `OPTION-B`
  - automatic_switch_to_fallback_authorized: false
  - new_human_decision_required_for_fallback: true
  - alpha4_disposition: `CONSIDER_AFTER_COMPARISON`
  - alpha4_authorized: false
- dissent_dispositions:
  - DS-001: `ACCEPT_POSITION`; selected direction `COMPARISON_FIRST`; field-trial-first retained as conditional alternative.
  - DS-002: `REQUIRE_EVIDENCE`; blocking gap `EG-005`.
  - DS-003: `ACCEPT_POSITION`; alpha.4 disposition `CONSIDER_AFTER_COMPARISON`; alpha4 remains unauthorized.
  - DS-004: `ACCEPT_POSITION`; controlling priority `PRESERVE_PRE_IMPROVEMENT_COMPARISON_EVIDENCE`.
- task_completed_by_human_decision: true
- task_completed_scope:
  - bounded_decision_task_completed: true
  - selected_work_package_execution_completed: false
  - comparison_workflow_completed: false
  - repository_modification_completed: false
  - pr_created_or_merged: false
  - A3_REL_001_completed: false
  - A3_REL_005_completed: false
  - field_trial_completed: false
  - release_evidence_established: false
  - release_authorized: false
  - alpha4_authorized: false
- status: `HUMAN_FINAL_DECISION_RECORDED`
- ready_for_core_conformance_evaluation: true
- core_conformance: `NOT_EVALUATED`
- completion_time_seconds: null
- metrics_finalized: false
- validation:
  - custom_phase4d_b_validation: PASS
  - dynamic_role_plan_checker: PASS
  - pilot_validator: PASS
  - core_candidate_experiments_checker: PASS
  - draft_sha_unchanged: true
  - experiment_yaml_diff_empty: true
  - raw_participant_evidence_unchanged: true

## Phase 4D-A Human Final Authority review packet

- authorization_record:
  - cumulative_human_action_number: 31
  - attempt_local_human_action_number: 19
  - authorized_phase: `ATTEMPT_002_PHASE_4D_A_HUMAN_REVIEW_PACKET`
- status: `AWAITING_HUMAN_FINAL_AUTHORITY_INPUT`
- phase_type: read-only review packet presentation
- phase4c_completed: true
- human_final_decision_recorded: false
- ready_for_human_decision: true
- core_conformance: `NOT_EVALUATED`
- formal_release_evidence: false
- alpha4_authorized: false
- files_changed:
  - `attempt.yaml`
  - `logs/operator-actions.md`
  - `logs/commands.log`
  - `run-notes.md`
  - workflow-level `logs/operator-actions.md`
  - workflow-level `logs/commands.log`
  - workflow-level `run-notes.md`
- files_not_changed:
  - structured comparison analysis artifacts
  - human decision draft
  - raw evidence
  - `experiment.yaml`
- boundaries:
  - candidate_option_selected: false
  - dissent_disposition_decided: false
  - task_completed_decided: false
  - convergence_classification_finalized: false
  - blind_first_round_status_finalized: false
  - completion_timer_stopped: false
  - metrics_finalized: false
  - release_authorized: false
  - formal_release_evidence_recognized: false
  - alpha4_authorized: false

## Phase 4C structured comparison and Human Final Authority packet

- authorization_record:
  - cumulative_human_action_number: 30
  - attempt_local_human_action_number: 18
  - authorized_phase: `ATTEMPT_002_PHASE_4C_STRUCTURED_COMPARISON_AND_HUMAN_DECISION_PREPARATION`
- status: `READY_FOR_HUMAN_DECISION`
- phase4c_authorized: true
- phase4c_completed: true
- human_final_decision_recorded: false
- ready_for_human_decision: true
- core_conformance: `NOT_EVALUATED`
- formal_release_evidence: false
- alpha4_authorized: false
- Stage A:
  - started_at_utc: `2026-07-18T16:30:52Z`
  - completed_at_utc: `2026-07-18T16:33:46Z`
  - initial_claim_ledger_sha256: `2a0a19cc84552e034708b5eabdb33b05dd03c03e05276e78d66ee0f2e6b26556`
  - initial_convergence_assessment_sha256: `e1f8cb1a063f0b96002a94f708c9077520236452b801b2acfbee72c0f47f7b53`
  - cross_exposure_content_used: false
- Stage B:
  - canonical_cross_exposure_sources: 3
  - gemini_canonical_source: `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md`
  - noncanonical_gemini_submission_used_for_semantic_analysis: false
- preliminary_findings:
  - blind_first_round_status: `VALID`
  - convergence_classification: `MIXED`
  - blind_multi_group_convergence_cluster_count: 2
  - common_source_mandated_cluster_count: 4
  - material_dissent_count: 4
  - unresolved_material_dissent_count: 3
  - blocking_evidence_gap_count: 2
  - candidate_options: `OPTION-A`, `OPTION-B`, `OPTION-C`
  - best_supported_option_for_human_review: `OPTION-A`
- validation:
  - custom_structured_comparison_validation: PASS
  - dynamic_role_plan_checker: PASS
  - pilot_validator: PASS
  - core_candidate_experiments_checker: PASS
  - raw_evidence_unchanged: true
  - source_reference_validation: PASS
  - experiment_yaml_diff_empty: true
- metrics:
  - cumulative_human_actions: 30
  - attempt_local_human_actions: 18
  - completion_time_seconds: null
  - metrics_finalized: false
- boundaries:
  - participant_prompt_sent: false
  - external_web_research_used: false
  - final_decision_created: false
  - release_authorized: false
  - formal_release_evidence_recognized: false
  - A3_REL_001_completed: false
  - alpha4_authorized: false

## Attempt identity

- attempt_id: `CORE-ATTEMPT-002`
- workflow: `ALPHA3_CORE_CANDIDATE`
- tested_baseline_commit: `2a29ddfebe4d9664d3a4043a01d8728fa525d049`
- operator_environment_commit: `43815810f988588a29ba2dcaea9d2641d6263606`
- restart_scope: `BLIND_FIRST_ROUND_AND_LATER`
- prior_attempt_evidence_preserved: true
- prior_attempt_outputs_reused: false
- prior_attempt_outputs_visible_to_participants: false
- cross_exposure_authorized: false
- cross_exposure_started: false
- formal_release_evidence: false
- alpha4_authorized: false

## Human action metrics

```yaml
cumulative_workflow_human_actions:
  basis: ALL_ATTEMPTS_FROM_ORIGINAL_RUN_START
  reset_on_restart: false
  restart_authorization_action: 13

attempt_local_human_actions:
  attempt_id: CORE-ATTEMPT-002
  initial_count: 1
  first_action: THIS_RESTART_AUTHORIZATION
```

The original workflow completion timer is not reset. Final workflow metrics must include elapsed time, human actions, corrections, and rerun burden from prior attempt activity.

## Phase 4B-R reconciliation authorization

```yaml
phase_4b_reconciliation_authorization:
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
  existing_raw_response_modified: false
  awaiting_retrospective_send_attestation: true
  awaiting_gemini_ui_inspection_attestation: true
```

## Phase 4B-R reconciliation attestation and CASE A disposition

```yaml
phase_4b_reconciliation_attestation:
  cumulative_human_action_number: 29
  attempt_local_human_action_number: 17
  codex_receipt_timestamp_utc: 2026-07-18T16:15:21Z
  retrospective_send_action_ids:
    - HA-RETRO-CROSS-SEND-CLAUDE-B
    - HA-RETRO-CROSS-SEND-GEMINI-B
  retrospective_send_time_inferred: false
  participants:
    - participant_id: CLAUDE-B
      send_status: SENT
      sent_at_utc: null
      send_time_status: UNKNOWN
      send_confirmation_status: RETROSPECTIVE_HUMAN_ATTESTATION
      same_existing_chat_confirmed_by_human: true
      new_chat_created: false
      attachment_count: 5
      attachments_sent_in_one_message: true
      attachment_order_confirmed_by_human: true
      external_web_research_enabled: false
      additional_information_sent: false
    - participant_id: GEMINI-B
      send_status: SENT
      sent_at_utc: null
      send_time_status: UNKNOWN
      send_confirmation_status: RETROSPECTIVE_HUMAN_ATTESTATION
      same_existing_chat_confirmed_by_human: true
      new_chat_created: false
      attachment_count: 5
      attachments_sent_in_one_message: true
      attachment_order_confirmed_by_human: true
      external_web_research_enabled: false
      additional_information_sent: false
  gemini_ui_inspection:
    same_existing_chat_reopened: true
    new_message_sent_during_inspection: false
    response_after_cross_exposure_packet_present: true
    response_is_identical_to_initial_response: false
    different_cross_exposure_response_present: true
    response_regenerated: false
    case: CASE_A
    disposition: UI_RECAPTURE_CANONICALIZED
    canonical_raw_response_ref: attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md
    canonical_raw_response_sha256: 9251f0715198f992988392e78d2077d958e4f5875cff15e67277253500c2802e
    canonical_raw_response_bytes: 31008
    recaptured_at_utc: 2026-07-18T16:15:21Z
    recaptured_time_basis: OPERATOR_RECAPTURE_SUBMISSION_RECEIPT
  status: CROSS_EXPOSURE_RESPONSES_CAPTURED_WITH_RECONCILIATION
  valid_cross_exposure_response_count: 3
  ready_for_structured_comparison: true
  phase4c_authorized: false
  comparison_performed: false
  decision_created: false
  existing_raw_response_modified: false
```

## Preparation constraints

- No external AI prompts were sent by Codex.
- No external chat was created by Codex.
- No raw response files were created for attempt-002.
- Old attempt raw response content was not reused in the attempt-002 participant information set.
- Old attempt Cross Exposure packet content was not reused in the attempt-002 participant information set.
- Sibling workflow run outputs were not referenced.

## Preparation result

- attempt_status: `READY_FOR_BLIND_FIRST_ROUND`
- dynamic_role_plan_status: `READY`
- blind_first_round_plan_status: `PLAN_VALID`
- attempt_002_information_set_hash: `e08e2bb419f2b2b091f896165471e572f6d94fd4c54ee6c08da2c9ce02a3ed46`
- compact_bundle_copy_sha256: `303fd59a8e08a052bdef74a3545fd74a1ad5182e994c5970861428fe2b5b9c48`
- compact_bundle_copy_bytes: `62637`
- compact_bundle_manifest_copy_sha256: `762ba8b6c60e0ec33d25e39b3c94116f138dc0feb1c143b35417ddce84e001c0`
- compact_bundle_manifest_copy_bytes: `1745`
- rendered_prompt_diff_check: PASS; only participant_id and model_label differ from the copied template.
- attempt_002_raw_directory_empty: true
- continuity_confirmation_items_prepared: true
- cross_exposure_authorized: false
- cross_exposure_started: false
- external_ai_sent: false
- raw_response_created: false
- experiment_yaml_changed: false

## Blind First Round raw capture progress

```yaml
capture_progress:
  participant_id: CHATGPT-B
  status: CAPTURED
  raw_response_path: raw/initial-response-CHATGPT-B.md
  raw_response_sha256: 0e435699e6ab9a004b5bb14f523a249e459524c3b784b7e3f00e1127fadea4f7
  raw_response_bytes: 30392
  codex_capture_timestamp_utc: 2026-07-18T14:38:20Z
  model_label_confirmed_by_human: GPT-5.6 Sol
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  captured_before_cross_exposure: true
  exposure_state: UNEXPOSED
  sent_at_utc: null
  send_time_status: UNKNOWN
  continuity_status: NOT_CONFIRMED
  raw_response_edited_or_overwritten: false
```

```yaml
capture_progress:
  participant_id: GEMINI-B
  status: CAPTURED
  raw_response_path: raw/initial-response-GEMINI-B.md
  raw_response_sha256: cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482
  raw_response_bytes: 24741
  codex_capture_timestamp_utc: 2026-07-18T14:49:54Z
  model_label_confirmed_by_human: 3.1 Pro
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  captured_before_cross_exposure: true
  exposure_state: UNEXPOSED
  sent_at_utc: null
  send_time_status: UNKNOWN
  continuity_status: NOT_CONFIRMED
  raw_response_edited_or_overwritten: false
```

```yaml
capture_progress:
  participant_id: CLAUDE-B
  status: CAPTURED
  raw_response_path: raw/initial-response-CLAUDE-B.md
  raw_response_sha256: 737c74a1a247eb861767fbb7cc25c7c365605c5182c0ebd7dc249eb32c8af1a9
  raw_response_bytes: 25688
  codex_capture_timestamp_utc: 2026-07-18T14:44:25Z
  model_label_confirmed_by_human: Opus 4.8
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  captured_before_cross_exposure: true
  exposure_state: UNEXPOSED
  sent_at_utc: null
  send_time_status: UNKNOWN
  continuity_status: NOT_CONFIRMED
  raw_response_edited_or_overwritten: false
```

```yaml
human_action_metrics:
  cumulative_workflow_human_actions:
    current_total: 18
    includes:
      - 14: rejected CHATGPT-A legacy participant raw submission
      - 15: CHATGPT-B raw submission received before capture authorization
      - 16: attempt-002 Blind First Round raw capture authorization
      - 17: CLAUDE-B raw submission and capture
      - 18: GEMINI-B raw submission and capture
  attempt_local_human_actions:
    current_total: 7
    includes:
      - 2: rejected CHATGPT-A legacy participant raw submission
      - 3: CHATGPT-B raw submission received before capture authorization
      - 4: attempt-002 Blind First Round raw capture authorization
      - 5: CLAUDE-B raw submission and capture
      - 6: GEMINI-B raw submission and capture
      - 7: chat continuity reconciliation authorization
```

## Chat continuity reconciliation status

```yaml
chat_continuity_reconciliation:
  authorization_received: true
  authorization_action:
    cumulative_workflow_human_action: 19
    attempt_local_human_action: 7
  attestation_received: false
  continuity_reconciliation_created: false
  capture_register_updated_for_continuity: false
  attempt_status_updated_for_continuity: false
  cross_exposure_packet_created: false
  cross_exposure_authorized: false
  cross_exposure_started: false
```

```yaml
chat_continuity_reconciliation_result:
  attestation_received: true
  attestation_action:
    cumulative_workflow_human_action: 20
    attempt_local_human_action: 8
  verified_at_utc: 2026-07-18T15:00:24Z
  verified_time_basis: OPERATOR_ATTESTATION_RECEIPT
  actual_chat_urls_recorded: false
  prior_attempt_outputs_seen: false
  participants:
    - participant_id: CHATGPT-B
      ui_model_label_confirmed: GPT-5.6 Sol
      continuity_result: PASS
    - participant_id: CLAUDE-B
      ui_model_label_confirmed: Opus 4.8
      continuity_result: PASS
    - participant_id: GEMINI-B
      ui_model_label_confirmed: 3.1 Pro
      continuity_result: PASS
  chat_continuity_status: CONFIRMED
  ready_for_cross_exposure_packet_preparation: true
  cross_exposure_packet_created: false
  cross_exposure_authorized: false
  cross_exposure_started: false
```

```yaml
human_action_metrics:
  cumulative_workflow_human_actions:
    current_total: 21
    latest_action: Cross Exposure packet preparation authorization
  attempt_local_human_actions:
    current_total: 9
    latest_action: Cross Exposure packet preparation authorization
```

## Cross Exposure packet preparation

```yaml
cross_exposure_packet:
  authorization_action:
    cumulative_workflow_human_action: 21
    attempt_local_human_action: 9
  status: READY_FOR_CROSS_EXPOSURE
  cross_exposure_common_information_set_hash: 3e9978ad568c4a16032b9353293a3887b935bc9117e6c18ae6adee30580d537e
  prompt_template_sha256: 1bc9145bec4ae0f5fa05ec2aeeefef4592464f851656518776687199b127ae84
  prompt_template_bytes: 3909
  rendered_prompts:
    - participant_id: CHATGPT-B
      sha256: b36f8c189151b286157dd268f8e25826582a94e02ee5dce4e28ad2e3b0e94539
      bytes: 3928
    - participant_id: CLAUDE-B
      sha256: b747c673d31b22795725f86c4c9c329f01e5dfae0269b61e2c8aa56a720c3845
      bytes: 3923
    - participant_id: GEMINI-B
      sha256: b8e5311ff199b1960e5dbd586505d56af2bf7f1447b92126e6578ad087b97392
      bytes: 3922
  manifest_sha256: 3e3266da9093da1cb32e81925d3f623658136fdbed716af511ba9a8e09082b03
  capture_register_sha256: 1b35ff9031397a84363ed53b84c0a890d61a9c1ec3e92603842ade0005aa5fc7
  rendered_prompt_diff_check: PASS
  raw_response_hash_recheck: PASS
  continuity_reconciliation_all_pass: true
  cross_exposure_authorized: false
  cross_exposure_started: false
  cross_exposure_raw_response_created: false
  external_ai_sent: false
  response_content_compared_or_evaluated: false
```

## Cross Exposure send/raw capture authorization

```yaml
phase_4b_authorization:
  cumulative_human_action_number: 22
  attempt_local_human_action_number: 10
  authorized_phase: ATTEMPT_002_PHASE_4B_CROSS_EXPOSURE_SEND_AND_RAW_CAPTURE
  status: CROSS_EXPOSURE_AUTHORIZED
  cross_exposure_authorized: true
  cross_exposure_started: false
  cross_exposure_started_at_utc: null
  first_send_confirmation_received: false
  external_ai_operated_by_codex: false
  cross_exposure_raw_response_created: false
  response_content_compared_or_evaluated: false
  decision_record_created: false
```

## Cross Exposure raw capture reconciliation issue

```yaml
cross_exposure_raw_capture_progress:
  participant_id: GEMINI-B
  raw_submission_action:
    cumulative: 27
    attempt_local: 15
  received_at_utc: 2026-07-18T15:57:43Z
  receive_time_basis: OPERATOR_RAW_SUBMISSION_RECEIPT
  send_confirmation_status: MISSING_BEFORE_RAW_CAPTURE
  send_status: UNCONFIRMED
  sent_at_utc: null
  send_time_status: UNKNOWN
  response_status: CAPTURED
  raw_response_ref: attempts/attempt-002/raw/cross-exposure-GEMINI-B.md
  raw_response_sha256: cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482
  raw_response_bytes: 24741
  raw_response_hash_duplicate_of: attempts/attempt-002/raw/initial-response-GEMINI-B.md
  expected_prior_participant_outputs_seen: true
  response_self_reported_prior_participant_outputs_seen: false
  cross_exposure_metadata_status: CONFLICT_RECORDED
  model_label_confirmed_by_human_at_capture: 3.1 Pro
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  raw_response_preserved_unedited: true
  response_content_compared_or_evaluated: false
  decision_record_created: false
  attempt_status: CROSS_EXPOSURE_RECONCILIATION_REQUIRED
```

```yaml
cross_exposure_raw_capture_progress:
  participant_id: CLAUDE-B
  raw_submission_action:
    cumulative: 26
    attempt_local: 14
  received_at_utc: 2026-07-18T15:49:39Z
  receive_time_basis: OPERATOR_RAW_SUBMISSION_RECEIPT
  send_confirmation_status: MISSING_BEFORE_RAW_CAPTURE
  send_status: UNCONFIRMED
  sent_at_utc: null
  send_time_status: UNKNOWN
  response_status: CAPTURED
  raw_response_ref: attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md
  raw_response_sha256: 0de4538cc3e4810a50ee8324cb639fb6dc0053d6a26758a7cb4c4039430a5fa1
  raw_response_bytes: 62298
  model_label_confirmed_by_human_at_capture: Opus 4.8
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  raw_response_preserved_unedited: true
  remaining_cross_exposure_responses:
    - GEMINI-B
  response_content_compared_or_evaluated: false
  decision_record_created: false
```

## Cross Exposure send progress

```yaml
cross_exposure_send_progress:
  first_send_confirmation_received: true
  cross_exposure_started: true
  cross_exposure_started_at_utc: 2026-07-18T15:32:41Z
  attempt_status: CROSS_EXPOSURE_IN_PROGRESS
  participants:
    - participant_id: CHATGPT-B
      send_status: SENT
      sent_at_utc: 2026-07-18T15:32:41Z
      send_time_basis: OPERATOR_SEND_CONFIRMATION_RECEIPT
      external_send_action:
        cumulative: 23
        attempt_local: 11
      send_confirmation_action:
        cumulative: 24
        attempt_local: 12
      response_status: NOT_RECEIVED
    - participant_id: CLAUDE-B
      send_status: NOT_SENT
      response_status: NOT_RECEIVED
    - participant_id: GEMINI-B
      send_status: NOT_SENT
      response_status: NOT_RECEIVED
  cross_exposure_raw_response_created: false
  response_content_compared_or_evaluated: false
```

## Cross Exposure raw capture progress

```yaml
cross_exposure_raw_capture_progress:
  participant_id: CHATGPT-B
  raw_submission_action:
    cumulative: 25
    attempt_local: 13
  received_at_utc: 2026-07-18T15:40:41Z
  receive_time_basis: OPERATOR_RAW_SUBMISSION_RECEIPT
  response_status: CAPTURED
  raw_response_ref: attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md
  raw_response_sha256: 21600ecebc974cd8e9c1d561e3b6f9c4c2f046e850edb81dd0febb8f821c0ae5
  raw_response_bytes: 48180
  model_label_confirmed_by_human_at_capture: GPT-5.6 Sol
  other_participant_outputs_seen_before_response_capture: false
  external_web_research_observed: false
  raw_response_preserved_unedited: true
  cross_exposure_authorized: true
  cross_exposure_started: true
  cross_exposure_started_at_utc: 2026-07-18T15:32:41Z
  remaining_cross_exposure_responses:
    - CLAUDE-B
    - GEMINI-B
  response_content_compared_or_evaluated: false
  decision_record_created: false
```


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
