# Operator actions

## Counting rule

Preflight actions are excluded from run metrics. Human actions are counted from the explicit run-start approval onward.

## Human actions

32. `2026-07-19`: Human explicitly approved attempt-002 Phase 4D-B `ATTEMPT_002_PHASE_4D_B_HUMAN_FINAL_AUTHORITY_DECISION_RECORDING`; authorized preserving the prior `HUMAN_FINAL_AUTHORITY_INPUT` as raw decision input and creating the final attempt-local Human Final Authority decision record. Human clarified that `Eruhitsuji` replaces the prior `decided_by: HFA-001` as the formal value. Human did not authorize Core conformance evaluation, metrics finalization, completion timer stop, `experiment.yaml` update, repository modification, PR creation, field trial execution, release, formal release evidence recognition, A3-REL-001/A3-REL-005 completion, or alpha.4 authorization.

31. `2026-07-19`: Human explicitly approved attempt-002 Phase 4D-A `ATTEMPT_002_PHASE_4D_A_HUMAN_REVIEW_PACKET`; authorized read-only presentation of Human Final Authority review information and an unfilled input form. Human did not authorize option adoption, dissent disposition, task completion, final convergence classification, final Blind First Round status, Core conformance, release, formal release evidence, or alpha.4 authorization.

30. `2026-07-18`: Human explicitly approved attempt-002 Phase 4C `ATTEMPT_002_PHASE_4C_STRUCTURED_COMPARISON_AND_HUMAN_DECISION_PREPARATION`; authorized evidence structuring, Blind First Round convergence analysis, Cross Exposure change tracking, dissent/evidence-gap organization, and Human Final Authority decision packet preparation. Human did not authorize final decision, `experiment.yaml` update, release judgment, formal release evidence recognition, `A3-REL-001` completion, or alpha.4 judgment.

28. `2026-07-18`: Human explicitly approved attempt-002 Phase 4B-R `ATTEMPT_002_PHASE_4B_RECONCILIATION`; authorized retrospective send reconciliation for CLAUDE-B/GEMINI-B and Gemini UI response inspection only; did not authorize Phase 4C, comparison, evaluation, integration, convergence classification, decision creation, experiment.yaml update, release state change, `formal_release_evidence` change, or `alpha4_authorized` change. Codex receipt timestamp: `2026-07-18T16:11:10Z`.
29. `2026-07-18`: Human submitted attempt-002 `CROSS_EXPOSURE_RECONCILIATION_ATTESTATION`, including retrospective send attestations for CLAUDE-B/GEMINI-B and Gemini UI response recapture. Codex receipt timestamp: `2026-07-18T16:15:21Z`.
HA-RETRO-CROSS-SEND-CLAUDE-B. Retrospective human attestation: human sent the fixed Cross Exposure packet to CLAUDE-B in the same existing chat before raw response submission; exact send time unavailable and not inferred.
HA-RETRO-CROSS-SEND-GEMINI-B. Retrospective human attestation: human sent the fixed Cross Exposure packet to GEMINI-B in the same existing chat before raw response submission; exact send time unavailable and not inferred.

1. `2026-07-18`: Human approved ALPHA3_CORE_CANDIDATE run start and Phase 1 "source binding・compact bundle準備"; defined timing and action-count rules; authorized only the listed Phase 1 reads, generated compact bundle artifacts, and logs/run notes.
2. `2026-07-18`: Human approved Phase 2 "participant登録・dynamic role planning・Blind First Round packet固定"; supplied the exact participant service records and authorized dynamic role input, dynamic role plan, participant register, Blind First Round packet files, temporary directory cleanup, and validators.
3. `2026-07-18`: Human approved Phase 3A "Blind First Round送信準備"; authorized participant-specific rendered prompts, capture register, raw directory creation, checklist updates, manifest rendering metadata updates, and validators; did not authorize external AI sending or raw response capture.
4. `2026-07-18`: Human approved Phase 3B "Blind First Round送信・raw capture"; authorized human-operated external-AI sends in fixed order, Codex send recording, raw response preservation, SHA-256 calculation, capture register updates, and mechanical validation; did not authorize Cross Exposure, comparison, critique, integration, or decision creation.
5. `2026-07-18`: Human submitted CHATGPT-A raw response.
6. `2026-07-18`: Human submitted CLAUDE-A raw response.
7. `2026-07-18`: Human submitted GEMINI-A raw response.
HA-RETRO-SEND-CHATGPT-A. Retrospective human attestation: human sent the fixed information set and rendered prompt to CHATGPT-A before the corresponding raw response submission; exact send time unavailable.
HA-RETRO-SEND-CLAUDE-A. Retrospective human attestation: human sent the fixed information set and rendered prompt to CLAUDE-A before the corresponding raw response submission; exact send time unavailable.
HA-RETRO-SEND-GEMINI-A. Retrospective human attestation: human sent the fixed information set and rendered prompt to GEMINI-A before the corresponding raw response submission; exact send time unavailable.
11. `2026-07-18`: Human approved Phase 3C "Blind First Round送信記録の事後照合"; supplied retrospective human attestation for the three external send events.
12. `2026-07-18`: Human approved Phase 4A "Cross Exposure packet準備・固定"; authorized creation and hashing of Cross Exposure packet files, manifest, capture register, and checklist only.

## Operator actions

- Attempt-002 Phase 4D-B: preserved public-redacted Human Final Authority input, created final human decision record, and kept the draft decision record unchanged.
- Attempt-002 Phase 4D-B: applied the human clarification that `decided_by` is formally `Eruhitsuji`.
- Attempt-002 Phase 4D-B: recorded selected option `OPTION-A`, conditional comparison-first path, mandatory EG-001/EG-005 pre-field-trial gates, DS-001 through DS-004 dispositions, additional evidence requirement, `CONFIRM_VALID`, `CONFIRM_MIXED`, bounded `task_completed: true`, and readiness for later Core conformance evaluation.
- Attempt-002 Phase 4D-B: updated attempt status to `HUMAN_FINAL_DECISION_RECORDED`.
- Attempt-002 Phase 4D-B: kept `core_conformance: NOT_EVALUATED`, `formal_release_evidence: false`, `alpha4_authorized: false`, completion timer running, and metrics unfinalized.
- Attempt-002 Phase 4D-B: custom validation and existing validators passed; raw participant evidence and `experiment.yaml` were unchanged.

- Attempt-002 Phase 4D-A: read only the authorized structured-comparison review artifacts and local task prompt for review packet display.
- Attempt-002 Phase 4D-A: updated attempt status to `AWAITING_HUMAN_FINAL_AUTHORITY_INPUT`.
- Attempt-002 Phase 4D-A: did not update the decision draft, metrics, `experiment.yaml`, raw evidence, or analysis artifacts.
- Attempt-002 Phase 4D-A: did not select a candidate option, dispose dissent, finalize Blind First Round status, finalize convergence classification, evaluate Core conformance, authorize release, recognize formal release evidence, or authorize alpha.4.

- Attempt-002 Phase 4C: created structured-comparison artifacts under `attempts/attempt-002/artifacts/structured-comparison/`.
- Attempt-002 Phase 4C: performed Stage A with initial responses only, fixed Stage A artifact hashes, then performed Stage B with canonical Cross Exposure responses.
- Attempt-002 Phase 4C: prepared Human Final Authority brief and draft record while leaving human decision fields unset.
- Attempt-002 Phase 4C: excluded the noncanonical duplicate GEMINI-B submission from semantic analysis and used the UI recapture as canonical Cross Exposure evidence.
- Attempt-002 Phase 4C: ran custom validation and existing validators; all final checks passed.
- Attempt-002 Phase 4C: final attempt status set to `READY_FOR_HUMAN_DECISION`; `core_conformance: NOT_EVALUATED`, `formal_release_evidence: false`, and `alpha4_authorized: false`.
- Recorded run start UTC timestamp as `2026-07-18T11:10:54Z`.
- Confirmed `/mnt/e/madp-codex-pilot-core-baseline` was absent before creating a detached baseline worktree.
- Confirmed no existing Phase 1 output files were present under the Core run directory before creating logs.
- Read only the Phase 1-authorized additional source files.
- Created `logs/` under the Core run directory for command and operator logs.
- Created detached baseline worktree at `/mnt/e/madp-codex-pilot-core-baseline`.
- Verified detached baseline worktree HEAD exactly matched `2a29ddfebe4d9664d3a4043a01d8728fa525d049`.
- Generated the compact bundle into the Core run artifact directory.
- Generated the compact bundle a second time into `/tmp/tmp.o5USricokv/compact-bundle`.
- Compared both generated bundle directories with `diff -ru`; no differences were reported.
- Validated the compact bundle.
- Calculated SHA-256 and byte counts for the bundle, manifest, and tested-baseline Core Candidate Profile.
- Ran the requested baseline and Core worktree validators.
- Removed the temporary baseline worktree after all requested validations succeeded.
- Confirmed `experiment.yaml` has no diff.
- Confirmed sibling run directories were not read.
- Confirmed Phase 2 output targets did not already exist before creation.
- Verified `/tmp/tmp.o5USricokv` contained only the Phase 1 second compact bundle generation files and matched the saved compact bundle output byte-for-byte.
- Deleted `/tmp/tmp.o5USricokv` after verification.
- Created Phase 2 dynamic role input exactly from human-supplied values.
- Generated and validated the dynamic role plan.
- Confirmed the generated dynamic role plan status is `READY`.
- Confirmed the generated Blind First Round plan status is `PLAN_VALID`.
- Created participant register with distinct new chat contexts and explicit non-proof note for technical independence.
- Created the Blind First Round common participant initial prompt.
- Created the Blind First Round operator send checklist with all checkboxes blank.
- Calculated dynamic role input, dynamic role plan, participant register, participant initial prompt, and information set hashes.
- Created the information set manifest with exact-byte concatenation method and hash.
- Ran the Phase 2 validators.
- Confirmed no raw response directory exists.
- Confirmed `experiment.yaml` has no diff after Phase 2.
- Did not send prompts to any external AI service.
- Confirmed Phase 3A rendered prompt and capture-register targets did not already exist.
- Recomputed the common information set hash before Phase 3A file creation and confirmed it matched `a754c49463e74c2fe79ed039438da070ed3ea0259fd55c87c71195a901f26925`.
- Created participant-specific rendered prompts for CHATGPT-A, CLAUDE-A, and GEMINI-A.
- Verified each rendered prompt differs from the common template only by the permitted `participant_id` and `model_label` substitutions.
- Calculated SHA-256 and byte counts for each rendered prompt.
- Created the empty `raw/` directory and did not create any raw response files.
- Created `capture-register.yaml` with `cross_exposure_authorized: false` and `cross_exposure_started: false`.
- Updated `information-set-manifest.yaml` with participant prompt rendering metadata while preserving the common information set hash.
- Updated `operator-send-checklist.md` with unfilled send/capture metadata fields.
- Verified `capture-register.yaml` and `information-set-manifest.yaml` load with PyYAML.
- Verified `raw/` is empty.
- Ran the Phase 3A validators.
- Confirmed `experiment.yaml` has no diff after Phase 3A.
- Did not create chats or send prompts to external AI services.
- Entered Phase 3B waiting state. Codex will not operate external AI services and will wait for human `SEND_CONFIRMED` reports before recording send timestamps.
- Received a `RAW_RESPONSE_SUBMISSION` for `CHATGPT-A` before receiving the corresponding `SEND_CONFIRMED` report.
- Recorded the raw response submission as human action #5.
- Captured UTC receive time as `2026-07-18T13:12:53Z`.
- Confirmed `raw/initial-response-CHATGPT-A.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `raw/initial-response-CHATGPT-A.md`.
- Calculated SHA-256 and byte count for `raw/initial-response-CHATGPT-A.md`.
- Updated `capture-register.yaml` for the CHATGPT-A response capture only. Because `SEND_CONFIRMED` was not received, `sent_at_utc` remains `null` and `send_status` records `SEND_CONFIRMED_MISSING`.
- Recorded a participant-output deviation: submission metadata confirms model label `GPT-5.6 Sol`, while the raw response header states `GPT-5.6 Thinking`.
- Did not compare, summarize, critique, integrate, or share the CHATGPT-A response with other participants.
- Verified `capture-register.yaml` still has `cross_exposure_authorized: false` and `cross_exposure_started: false` after the partial capture update.
- Verified only one raw response file is present after CHATGPT-A capture.
- Confirmed `experiment.yaml` has no diff after CHATGPT-A capture.
- Received a `RAW_RESPONSE_SUBMISSION` for `CLAUDE-A` before receiving the corresponding `SEND_CONFIRMED` report.
- Recorded the raw response submission as human action #6.
- Captured UTC receive time as `2026-07-18T13:18:07Z`.
- Confirmed `raw/initial-response-CLAUDE-A.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `raw/initial-response-CLAUDE-A.md`.
- Calculated SHA-256 and byte count for `raw/initial-response-CLAUDE-A.md`.
- Updated `capture-register.yaml` for the CLAUDE-A response capture only. Because `SEND_CONFIRMED` was not received, `sent_at_utc` remains `null` and `send_status` records `SEND_CONFIRMED_MISSING`.
- Did not compare, summarize, critique, integrate, or share the CLAUDE-A response with other participants.
- Verified `capture-register.yaml` still has `cross_exposure_authorized: false` and `cross_exposure_started: false` after the CLAUDE-A capture update.
- Verified two raw response files are present after CLAUDE-A capture and GEMINI-A remains `NOT_RECEIVED`.
- Confirmed `experiment.yaml` has no diff after CLAUDE-A capture.
- Received a `RAW_RESPONSE_SUBMISSION` for `GEMINI-A` before receiving the corresponding `SEND_CONFIRMED` report.
- Recorded the raw response submission as human action #7.
- Captured UTC receive time as `2026-07-18T13:22:25Z`.
- Confirmed `raw/initial-response-GEMINI-A.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `raw/initial-response-GEMINI-A.md`.
- Calculated SHA-256 and byte count for `raw/initial-response-GEMINI-A.md`.
- Updated `capture-register.yaml` for the GEMINI-A response capture only. Because `SEND_CONFIRMED` was not received, `sent_at_utc` remains `null` and `send_status` records `SEND_CONFIRMED_MISSING`.
- Did not compare, summarize, critique, integrate, or share the GEMINI-A response with other participants.
- Performed Phase 3B completion checks after all three raw responses were captured.
- Verified exactly three raw initial response files are present.
- Recomputed raw response SHA-256 values and confirmed they match `capture-register.yaml`.
- Verified all three captures are marked before Cross Exposure, with `exposed_response_refs: []`.
- Verified `cross_exposure_authorized: false` and `cross_exposure_started: false`.
- Verified participant register initial response filenames match captured raw response references.
- Verified rendered prompt hashes remain unchanged from Phase 3A.
- Recomputed common information set hash and confirmed it remains `a754c49463e74c2fe79ed039438da070ed3ea0259fd55c87c71195a901f26925`.
- Confirmed `experiment.yaml` has no diff after Phase 3B.
- Ran the Phase 3B validators; all passed.
- Did not perform Cross Exposure, comparison, critique, integration, convergence classification, Core conformance classification, decision record creation, or metrics finalization.
- Confirmed `send-reconciliation.yaml` did not already exist before creating it.
- Recomputed raw response hashes and byte counts before Phase 3C reconciliation; all matched expected values.
- Created `send-reconciliation.yaml` from retrospective human attestation with `sent_at_utc: null` for all events.
- Updated `capture-register.yaml` to record `send_status: SENT`, `send_time_status: UNKNOWN`, and `send_confirmation_status: RETROSPECTIVE_HUMAN_ATTESTATION` for all participants without inferring send times.
- Recorded CHATGPT-A model label conflict separately: UI-confirmed `GPT-5.6 Sol`; raw self-reported `GPT-5.6 Thinking`; raw preserved and self-reported label not treated as authoritative.
- Reverified `send-reconciliation.yaml` and `capture-register.yaml` load with PyYAML.
- Reverified all raw response SHA-256 values and byte counts after Phase 3C; raw files were not modified.
- Verified Cross Exposure remains unauthorized and not started.
- Ran the Phase 3C validators; all passed.
- Confirmed `experiment.yaml` has no diff after Phase 3C.
- Did not read sibling run directories.
- Did not perform convergence classification, participant quality evaluation, Core conformance final judgment, best-proposal selection, material dissent evaluation, or decision result creation.
- Confirmed the Cross Exposure artifact directory did not already exist before creating it.
- Recomputed initial raw response SHA-256 values and byte counts before constructing the Cross Exposure packet; all matched expected values.
- Created `artifacts/cross-exposure/`.
- Created Cross Exposure prompt template exactly from the human-supplied text.
- Created participant-specific rendered prompts for CHATGPT-A, CLAUDE-A, and GEMINI-A using only the permitted substitutions.
- Verified each rendered prompt differs from the template only by `PARTICIPANT_ID`, `MODEL_LABEL`, and `OWN_INITIAL_RESPONSE_REF`.
- Computed the Cross Exposure common information set hash from exact bytes of the six specified files and no separators.
- Created Cross Exposure information set manifest, capture register, and operator checklist.
- Verified the manifest and capture register load with PyYAML.
- Verified all three participants have the same attached initial response order.
- Verified each participant's newly exposed response refs are exactly the other two initial responses.
- Verified Cross Exposure raw response files do not exist.
- Ran the Phase 4A validators; all passed.
- Confirmed `experiment.yaml` has no diff after Phase 4A.
- Confirmed the Blind First Round capture register has no diff from before Phase 4A.
- Did not send anything to external AI, create chats, analyze response content, compare or summarize initial responses, classify convergence, judge Core conformance, determine dissent, or create a decision record.
- Human reported before Phase 4B send that the three original Blind First Round chat contexts are unavailable.
- Recorded Cross Exposure blocker: `ORIGINAL_PARTICIPANT_CHATS_UNAVAILABLE`.
- Did not start Phase 4B.
- Did not substitute new chats for the original chat contexts.
- Did not send Cross Exposure prompts to external AI.
- Did not create cross-exposure raw response files.
- Did not compare, summarize, evaluate, integrate, classify convergence, judge Core conformance, or create a decision record.
- Did not modify Phase 4A packet files, Blind First Round raw responses, raw response hashes, Blind First Round capture register, or `experiment.yaml`.
- Received human authorization to rerun from Blind First Round as `CORE-ATTEMPT-002` inside the existing `ALPHA3_CORE_CANDIDATE` run.
- Recorded this restart authorization as cumulative human action #13 and attempt-local human action #1.
- Did not reset the original workflow completion timer.
- Confirmed `attempts/attempt-002/` did not exist before creation.
- Confirmed `artifacts/attempt-register.yaml` did not exist before creation.
- Recomputed old raw response SHA-256 values only for preservation verification; did not inspect, summarize, copy into attempt-002 participant packets, or otherwise reuse old raw response content.
- Created `artifacts/attempt-register.yaml`.
- Created attempt-002 directory structure, attempt metadata, local logs, dynamic role input, participant register, Blind First Round prompt files, information-set manifest, capture register, and send checklist.
- Byte-copied the existing compact bundle, compact bundle manifest, and common Blind First Round prompt template into attempt-002.
- Verified the compact bundle and manifest copy hashes and byte counts match expected values.
- Generated and validated the attempt-002 dynamic role plan.
- Detected and corrected an attempt-002 information-set hash ordering error before finalization. Corrected hash uses the human-specified byte order: task, attempt-002 compact bundle Markdown, attempt-002 prompt template, attempt-002 participant register, attempt-002 dynamic role plan.
- Verified attempt-002 rendered prompts differ from the template only by participant_id and model_label.
- Verified attempt-002 raw directory is empty.
- Verified attempt-002 information set does not include prior attempt output references.
- Verified attempt-002 participant IDs and chat context IDs differ from attempt-001.
- Verified `cross_exposure_authorized: false` and `cross_exposure_started: false` for attempt-002.
- Updated `attempt.yaml` and `attempt-register.yaml` status to `READY_FOR_BLIND_FIRST_ROUND` after validation passed.
- Ran the attempt-002 validators; all passed.
- Confirmed `experiment.yaml` has no diff after attempt-002 packet preparation.
- Did not create chats, send prompts to external AI, create raw responses, start Cross Exposure, compare participant answers, integrate proposals, create a decision record, modify release state, change `formal_release_evidence`, or change `alpha4_authorized`.
- Received a `RAW_RESPONSE_SUBMISSION` with legacy participant_id `CHATGPT-A` after attempt-002 was active. Recorded it as cumulative human action #14 and attempt-local action #2; rejected it for attempt-002 capture and did not save raw response content.
- Received a `RAW_RESPONSE_SUBMISSION` with participant_id `CHATGPT-B` before raw capture authorization. Recorded it as cumulative human action #15 and attempt-local action #3; held it without file changes at receipt time.
- Received human authorization for attempt-002 Blind First Round send/raw capture and for treating the already submitted `CHATGPT-B` response as capture対象. Recorded it as cumulative human action #16 and attempt-local action #4.
- Captured UTC timestamp `2026-07-18T14:38:20Z` after raw capture authorization.
- Confirmed `attempts/attempt-002/raw/initial-response-CHATGPT-B.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `attempts/attempt-002/raw/initial-response-CHATGPT-B.md`.
- Calculated SHA-256 and byte count for `attempts/attempt-002/raw/initial-response-CHATGPT-B.md`.
- Updated attempt-002 Blind First Round capture register for `CHATGPT-B` only.
- Did not infer `sent_at_utc`; it remains `null` with `send_time_status: UNKNOWN`.
- Did not mark chat continuity confirmed; continuity remains `NOT_CONFIRMED`.
- Did not compare, summarize, critique, integrate, or share the `CHATGPT-B` response with other participants.
- Verified Cross Exposure remains unauthorized and not started.
- Received a `RAW_RESPONSE_SUBMISSION` with participant_id `CLAUDE-B`. Recorded it as cumulative human action #17 and attempt-local action #5.
- Captured UTC timestamp `2026-07-18T14:44:25Z` for the CLAUDE-B raw submission.
- Confirmed `attempts/attempt-002/raw/initial-response-CLAUDE-B.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `attempts/attempt-002/raw/initial-response-CLAUDE-B.md`.
- Calculated SHA-256 and byte count for `attempts/attempt-002/raw/initial-response-CLAUDE-B.md`.
- Updated attempt-002 Blind First Round capture register for `CLAUDE-B` only.
- Did not infer `sent_at_utc`; it remains `null` with `send_time_status: UNKNOWN`.
- Did not mark chat continuity confirmed; continuity remains `NOT_CONFIRMED`.
- Did not compare, summarize, critique, integrate, or share the `CLAUDE-B` response with other participants.
- Received a `RAW_RESPONSE_SUBMISSION` with participant_id `GEMINI-B`. Recorded it as cumulative human action #18 and attempt-local action #6.
- Captured UTC timestamp `2026-07-18T14:49:54Z` for the GEMINI-B raw submission.
- Confirmed `attempts/attempt-002/raw/initial-response-GEMINI-B.md` did not already exist before writing it.
- Preserved only the text between `-----BEGIN RAW RESPONSE-----` and `-----END RAW RESPONSE-----` in `attempts/attempt-002/raw/initial-response-GEMINI-B.md`.
- Calculated SHA-256 and byte count for `attempts/attempt-002/raw/initial-response-GEMINI-B.md`.
- Updated attempt-002 Blind First Round capture register for `GEMINI-B` only.
- Did not infer `sent_at_utc`; it remains `null` with `send_time_status: UNKNOWN`.
- Did not mark chat continuity confirmed; continuity remains `NOT_CONFIRMED`.
- Did not compare, summarize, critique, integrate, or share the `GEMINI-B` response with other participants.
- All three attempt-002 Blind First Round initial raw responses are now captured.
- Received human authorization for attempt-002 chat continuity post-hoc reconciliation. Recorded it as cumulative human action #19 and attempt-local action #7.
- The message did not contain the `CONTINUITY_REOPEN_ATTESTATION`; no continuity reconciliation file was created yet.
- Did not update capture register continuity fields or attempt status for continuity.
- Did not create Cross Exposure packet, send external AI prompts, compare responses, summarize responses, critique responses, integrate proposals, or create a decision record.
- Received `CONTINUITY_REOPEN_ATTESTATION` for attempt-002. Recorded it as cumulative human action #20 and attempt-local action #8.
- Captured UTC timestamp `2026-07-18T15:00:24Z` immediately after receiving the attestation.
- Created `attempts/attempt-002/artifacts/blind-first-round/continuity-reconciliation.yaml`.
- Recorded all three participant continuity results as PASS based on human attestation.
- Recorded `actual_chat_urls_recorded: false`.
- Updated attempt-002 Blind First Round capture register continuity fields for `CHATGPT-B`, `CLAUDE-B`, and `GEMINI-B`.
- Updated attempt-002 status to `READY_FOR_CROSS_EXPOSURE_PACKET_PREPARATION`.
- Reverified all three initial raw response hashes and byte counts; no raw files were modified.
- Verified Cross Exposure remains unauthorized and not started.
- Verified attempt-002 Cross Exposure packet has not been created and Cross Exposure raw response files do not exist.
- Ran the continuity-phase validators; all passed.
- Confirmed `experiment.yaml` has no diff.
- Did not create Cross Exposure packet, send external AI prompts, compare responses, summarize responses, critique responses, integrate proposals, or create a decision record.
- Received human authorization for attempt-002 Phase 4A Cross Exposure packet preparation. Recorded it as cumulative human action #21 and attempt-local action #9.
- Confirmed attempt-002 `artifacts/cross-exposure/` did not exist before creation.
- Created attempt-002 Cross Exposure prompt template exactly from the human-supplied text.
- Created participant-specific Cross Exposure rendered prompts for `CHATGPT-B`, `CLAUDE-B`, and `GEMINI-B`.
- Recomputed attempt-002 initial raw response SHA-256 values and byte counts; all matched expected values.
- Verified rendered prompts differ from the template only by participant_id, model_label, and own_initial_response_ref.
- Computed `cross_exposure_common_information_set_hash`: `3e9978ad568c4a16032b9353293a3887b935bc9117e6c18ae6adee30580d537e`.
- Created attempt-002 Cross Exposure information-set manifest, capture register, and operator checklist.
- Verified manifest and capture register load with PyYAML.
- Verified all three participants have identical attachment order and newly exposed refs are exactly the other two initial responses.
- Verified attempt-002 Cross Exposure raw response files do not exist.
- Updated attempt status to `READY_FOR_CROSS_EXPOSURE`.
- Ran the Phase 4A validators; all passed.
- Confirmed `experiment.yaml` has no diff.
- Did not send Cross Exposure prompts, create chats, start Cross Exposure, create cross-exposure raw responses, compare or evaluate participant answers, classify convergence, judge dissent, determine best proposal, or create a decision record.
- Received explicit human authorization for attempt-002 Phase 4B Cross Exposure send/raw capture. Recorded it as cumulative human action #22 and attempt-local action #10.
- Updated attempt-002 waiting state: `status: CROSS_EXPOSURE_AUTHORIZED`, `cross_exposure_authorized: true`, `cross_exposure_started: false`, and `cross_exposure_started_at_utc: null`.
- Updated attempt-002 Cross Exposure capture register to `cross_exposure_authorized: true` while keeping `cross_exposure_started: false`.
- Did not operate external AI, send Cross Exposure prompts, create Cross Exposure raw responses, compare or evaluate responses, classify convergence, judge dissent, determine best proposal, update `experiment.yaml`, or create a decision record.
- Received `CROSS_EXPOSURE_SEND_CONFIRMED` for `CHATGPT-B`.
- Recorded the human external send operation as cumulative human action #23 and attempt-local action #11.
- Recorded the send confirmation message as cumulative human action #24 and attempt-local action #12.
- Captured UTC timestamp `2026-07-18T15:32:41Z` immediately after receiving the send confirmation.
- Updated attempt-002 status to `CROSS_EXPOSURE_IN_PROGRESS`.
- Updated `cross_exposure_started: true` and `cross_exposure_started_at_utc: 2026-07-18T15:32:41Z`.
- Updated attempt-002 Cross Exposure capture register for `CHATGPT-B` send only.
- Did not create any Cross Exposure raw response file.
- Did not compare, summarize, critique, evaluate, integrate, classify convergence, judge dissent, determine best proposal, update `experiment.yaml`, or create a decision record.

### 13. CHATGPT-B Cross Exposure raw submission and capture

- cumulative_workflow_human_action: 25
- attempt_local_human_action: 13
- source: human `RAW_RESPONSE_SUBMISSION` message with `participant_id: CHATGPT-B`
- codex_capture_timestamp_utc: `2026-07-18T15:40:41Z`
- captured_participant_id: `CHATGPT-B`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-CHATGPT-B.md`
- raw_response_sha256: `21600ecebc974cd8e9c1d561e3b6f9c4c2f046e850edb81dd0febb8f821c0ae5`
- raw_response_bytes: 48180
- model_label_confirmed_by_human: `GPT-5.6 Sol`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- response_status: `CAPTURED`
- cross_exposure_authorized: true
- cross_exposure_started: true
- cross_exposure_started_at_utc: `2026-07-18T15:32:41Z`
- response_content_compared_or_evaluated: false
- decision_record_created: false
- cross_exposure_response_shared_with_other_participants: false

### Attempt-002 action 15. GEMINI-B Cross Exposure raw submission and capture

- cumulative_workflow_human_action: 27
- attempt_local_human_action: 15
- source: human `RAW_RESPONSE_SUBMISSION` message with `participant_id: GEMINI-B`
- codex_capture_timestamp_utc: `2026-07-18T15:57:43Z`
- captured_participant_id: `GEMINI-B`
- send_confirmation_status: `MISSING_BEFORE_RAW_CAPTURE`
- send_status: `UNCONFIRMED`
- sent_at_utc: null
- send_time_status: `UNKNOWN`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-GEMINI-B.md`
- raw_response_sha256: `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482`
- raw_response_bytes: 24741
- raw_response_hash_duplicate_of: `attempts/attempt-002/raw/initial-response-GEMINI-B.md`
- expected_prior_participant_outputs_seen: true
- response_self_reported_prior_participant_outputs_seen: false
- cross_exposure_metadata_status: `CONFLICT_RECORDED`
- model_label_confirmed_by_human: `3.1 Pro`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- response_status: `CAPTURED`
- cross_exposure_authorized: true
- cross_exposure_started: true
- cross_exposure_started_at_utc: `2026-07-18T15:32:41Z`
- attempt_status: `CROSS_EXPOSURE_RECONCILIATION_REQUIRED`
- response_content_compared_or_evaluated: false
- decision_record_created: false
- cross_exposure_response_shared_with_other_participants: false

### 14. CLAUDE-B Cross Exposure raw submission and capture

- cumulative_workflow_human_action: 26
- attempt_local_human_action: 14
- source: human `RAW_RESPONSE_SUBMISSION` message with `participant_id: CLAUDE-B`
- codex_capture_timestamp_utc: `2026-07-18T15:49:39Z`
- captured_participant_id: `CLAUDE-B`
- send_confirmation_status: `MISSING_BEFORE_RAW_CAPTURE`
- send_status: `UNCONFIRMED`
- sent_at_utc: null
- send_time_status: `UNKNOWN`
- raw_response_path: `attempts/attempt-002/raw/cross-exposure-CLAUDE-B.md`
- raw_response_sha256: `0de4538cc3e4810a50ee8324cb639fb6dc0053d6a26758a7cb4c4039430a5fa1`
- raw_response_bytes: 62298
- model_label_confirmed_by_human: `Opus 4.8`
- other_participant_outputs_seen_before_response_capture: false
- external_web_research_observed: false
- raw_response_preserved_unedited: true
- response_status: `CAPTURED`
- cross_exposure_authorized: true
- cross_exposure_started: true
- cross_exposure_started_at_utc: `2026-07-18T15:32:41Z`
- response_content_compared_or_evaluated: false
- decision_record_created: false
- cross_exposure_response_shared_with_other_participants: false


### 21. Phase 4E-A identifier reconciliation and Phase 4E resume

- cumulative_workflow_human_action: 33
- attempt_local_human_action: 21
- authorized_phase: `ATTEMPT_002_PHASE_4E_IDENTIFIER_RECONCILIATION_AND_RESUME`
- source: human clarification and authorization message replacing the previous Phase 4E identifier gate
- prior_recorded_human_action_confirmed: `32 / 20`
- stopped_phase4e_authorizations_recounted: false
- raw_input_identifier: `HFA-001`
- final_record_identifier: `Eruhitsuji`
- official_identifier: `Eruhitsuji`
- same_human_authority: true
- raw_input_file_modified: false
- final_decision_record_modified: false
- decision_draft_modified: false
- decision_semantic_content_changed: false
- identifier_reconciliation_artifact_created: true
- dev_004_recorded: true
- core_conformance: `DEGRADED`
- completion_ended_at_utc: `2026-07-18T18:07:34Z`
- completion_time_seconds: 25000
- metrics_finalized: true
- experiment_yaml_reflected: true
- selected_work_package_executed: false
- field_trial_executed: false
- release_authorized: false
- formal_release_evidence: false
- a3_rel_001_completed: false
- a3_rel_005_completed: false
- alpha4_authorized: false
- next_preregistered_workflow: `MARKDOWN_VALIDATOR`
- next_workflow_authorized: false


### 22. PRIVACY-1 public identifier redaction authorization

- cumulative_workflow_human_action: 34
- attempt_local_human_action: 22
- authorized_phase: `CORE_ATTEMPT_002_PRIVACY_1_PUBLIC_IDENTIFIER_REDACTION`
- source: human authorization message approving public identifier redaction before publication
- public_replacement_identifier: `HFA-001`
- original_identifier_value_recorded_in_public_logs: false
- identifier_mapping_published: false
- private_original_preserved_outside_repository: true
- private_backup_path_recorded_in_public_repository: false
- unredacted_raw_hfa_input_removed_from_public_repository: true
- public_redacted_input_created: true
- human_decision_semantic_content_changed: false
- core_conformance: `DEGRADED`
- commit_created: false
- push_performed: false
- pr_created: false
- merge_performed: false
- release_authorized: false
- formal_release_evidence: false
- a3_rel_001_completed: false
- a3_rel_005_completed: false
- alpha4_authorized: false


### Human Final Authority termination and Rapid Prerelease transition

- authorized_phase: `EXPERIMENT_TERMINATION_AND_RAPID_PRERELEASE_TRANSITION`
- source: Human Final Authority message approving termination of `EXP-CODEX-PILOT-001` and adoption of Rapid Prerelease policy
- explicit_human_action_number_supplied: false
- experiment_status: `TERMINATED_BY_HUMAN_FINAL_AUTHORITY`
- termination_class: `RESOURCE_CONSTRAINT_AND_PRIORITY_CHANGE`
- completed_workflows:
  - `ALPHA3_CORE_CANDIDATE`
- cancelled_workflows:
  - `MARKDOWN_VALIDATOR`
  - `MANUAL_MULTI_AI`
  - `STANDARD_ALPHA3`
- remaining_workflow_artifacts_created: false
- comparative_conclusion_authorized: false
- core_candidate_evidence_preserved: true
- rapid_prerelease_decision_record_created: `docs/planning/DEC-MADP-RAPID-PRERELEASE-001.yaml`
- alpha4_implementation_authorized_by_human_development_decision: true
- alpha4_prerelease_authorized_by_human_development_decision: true
- stable_release_authorized: false
- formal_release_evidence: false
- a3_rel_001_completed: false
- a3_rel_005_completed: false
- git_commit_performed: false
- push_performed: false
- pull_request_created: false
- merge_performed: false
- tag_created: false
- github_release_created: false
- pages_publication_performed: false


### 23. Rapid Prerelease governance record commit and PR authorization

- cumulative_workflow_human_action: 35
- attempt_local_human_action: 23
- authorized_phase: `RAPID_PRERELEASE_GOVERNANCE_RECORD_COMMIT_AND_PR`
- source: Human Final Authority reauthorization approving use of currently configured repository-local Git email for commit metadata without recording the email value
- git_identity_user_name_valid: true
- git_identity_email_configured: true
- git_identity_email_approved_by_human: true
- git_identity_github_noreply_required: false
- git_identity_use_config_only: true
- private_identifier_occurrences: 0
- private_email_occurrences: 0
- private_backup_path_occurrences: 0
- identifier_mapping_occurrences: 0
- old_raw_input_path_references: 0
- commit_message: `Record pilot termination and rapid prerelease policy`
- merge_authorized: false
- tag_authorized: false
- github_release_authorized: false
- pages_publication_authorized: false
- alpha4_body_implementation_authorized_in_this_phase: false
- distribution_artifact_generation_authorized: false
