# Attempt 002 Cross Exposure operator checklist

Common attachment order for every participant:

1. `experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md`
2. `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/artifacts/compact-bundle/MADP-v0.3.0-alpha.3-core-compact.md`
3. `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/raw/initial-response-CHATGPT-B.md`
4. `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/raw/initial-response-CLAUDE-B.md`
5. `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/raw/initial-response-GEMINI-B.md`

## CHATGPT-B

- rendered prompt path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/artifacts/cross-exposure/rendered-prompt-CHATGPT-B.md`
- rendered prompt SHA-256: `b36f8c189151b286157dd268f8e25826582a94e02ee5dce4e28ad2e3b0e94539`
- expected UI model label: `GPT-5.6 Sol`
- [x] continuity reconciliationがPASS
- [x] 同じ既存chatを開いた
- [x] 新規chatを作成していない
- [x] UI model labelを確認した
- [x] task/prompt.mdを添付した
- [x] compact bundleを添付した
- [x] 3件のinitial raw responseをcanonical順序で添付した
- [x] 5ファイルを1回のmessageへ添付した
- [x] participant用rendered promptを使用した
- [x] Web検索を有効化していない
- [x] 追加情報を与えていない
- [x] actual send UTCを記録した: `2026-07-18T15:32:41Z`
- [x] response receive UTCを記録した: `2026-07-18T15:40:41Z`
- [x] raw responseを編集せず保存した
- [x] raw response SHA-256を計算した: `21600ecebc974cd8e9c1d561e3b6f9c4c2f046e850edb81dd0febb8f821c0ae5`
- [x] Cross Exposure回答を他participantへ再共有していない
- [x] send action number: cumulative `23`, attempt-local `11`
- [x] raw submission action number: cumulative `25`, attempt-local `13`

## CLAUDE-B

- rendered prompt path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/artifacts/cross-exposure/rendered-prompt-CLAUDE-B.md`
- rendered prompt SHA-256: `b747c673d31b22795725f86c4c9c329f01e5dfae0269b61e2c8aa56a720c3845`
- expected UI model label: `Opus 4.8`
- [x] send confirmation received before raw capture: NO — `CROSS_EXPOSURE_SEND_CONFIRMED` missing
- [x] retrospective send attestation received: `RETROSPECTIVE_HUMAN_ATTESTATION`
- [x] continuity reconciliationがPASS
- [x] 同じ既存chatを開いた
- [x] 新規chatを作成していない
- [ ] UI model labelを確認した
- [ ] task/prompt.mdを添付した
- [ ] compact bundleを添付した
- [x] 3件のinitial raw responseをcanonical順序で添付した
- [x] 5ファイルを1回のmessageへ添付した
- [ ] participant用rendered promptを使用した
- [x] Web検索を有効化していない
- [x] 追加情報を与えていない
- [x] exact send UTC unavailable; `sent_at_utc: null`, `send_time_status: UNKNOWN`
- [x] response receive UTCを記録した: `2026-07-18T15:49:39Z`
- [x] raw responseを編集せず保存した
- [x] raw response SHA-256を計算した: `0de4538cc3e4810a50ee8324cb639fb6dc0053d6a26758a7cb4c4039430a5fa1`
- [x] Cross Exposure回答を他participantへ再共有していない
- [x] send action number: `HA-RETRO-CROSS-SEND-CLAUDE-B`
- [x] raw submission action number: cumulative `26`, attempt-local `14`

## GEMINI-B

- rendered prompt path: `experiments/codex-core-candidate-comparison/pilot-001/runs/03-alpha3-core-candidate/attempts/attempt-002/artifacts/cross-exposure/rendered-prompt-GEMINI-B.md`
- rendered prompt SHA-256: `b8e5311ff199b1960e5dbd586505d56af2bf7f1447b92126e6578ad087b97392`
- expected UI model label: `3.1 Pro`
- [x] send confirmation received before raw capture: NO — `CROSS_EXPOSURE_SEND_CONFIRMED` missing
- [x] retrospective send attestation received: `RETROSPECTIVE_HUMAN_ATTESTATION`
- [x] original captured raw metadata conflict recorded: expected `prior_participant_outputs_seen: true`, response self-reported `false`
- [x] original captured raw duplicates initial response: `attempts/attempt-002/raw/initial-response-GEMINI-B.md`
- [x] continuity reconciliationがPASS
- [x] 同じ既存chatを開いた
- [x] 新規chatを作成していない
- [ ] UI model labelを確認した
- [ ] task/prompt.mdを添付した
- [ ] compact bundleを添付した
- [x] 3件のinitial raw responseをcanonical順序で添付した
- [x] 5ファイルを1回のmessageへ添付した
- [ ] participant用rendered promptを使用した
- [x] Web検索を有効化していない
- [x] 追加情報を与えていない
- [x] exact send UTC unavailable; `sent_at_utc: null`, `send_time_status: UNKNOWN`
- [x] response receive UTCを記録した: `2026-07-18T15:57:43Z`
- [x] raw responseを編集せず保存した
- [x] raw response SHA-256を計算した: `cc651d90c59fbedb1c2c40edee050d8b51d6817ee5e9c723c0ea48d7422c5482`
- [x] Cross Exposure回答を他participantへ再共有していない
- [x] send action number: `HA-RETRO-CROSS-SEND-GEMINI-B`
- [x] raw submission action number: cumulative `27`, attempt-local `15`
- [x] same existing chat reopened for UI inspection
- [x] no new message sent during UI inspection
- [x] different Cross Exposure response present in UI
- [x] response was not regenerated
- [x] original captured raw preserved
- [x] UI recapture saved unedited: `attempts/attempt-002/raw/cross-exposure-GEMINI-B-ui-recapture.md`
- [x] UI recapture SHA-256 calculated: `9251f0715198f992988392e78d2077d958e4f5875cff15e67277253500c2802e`
- [x] canonical response status: `CAPTURED_AFTER_RECONCILIATION`
