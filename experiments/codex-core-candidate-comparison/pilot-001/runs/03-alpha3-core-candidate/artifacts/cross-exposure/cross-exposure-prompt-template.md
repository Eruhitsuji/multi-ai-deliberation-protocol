あなたはMADP Core Candidate比較実験のCross Exposure参加者です。

participant_id: <PARTICIPANT_ID>
model_label: <MODEL_LABEL>
own_initial_response_ref: <OWN_INITIAL_RESPONSE_REF>
prior_participant_outputs_seen: true
external_web_research_used: false
authority: PROPOSE_ONLY

Blind First Roundの3件の初期回答は、すべてCross Exposure開始前にraw形式で保存・SHA-256固定されています。

このメッセージには、次の共通information setが同一順序で添付されています。

1. task/prompt.md
2. MADP-v0.3.0-alpha.3-core-compact.md
3. initial-response-CHATGPT-A.md
4. initial-response-CLAUDE-A.md
5. initial-response-GEMINI-A.md

own_initial_response_refで指定されたファイルが、あなた自身のBlind First Round初期回答です。
残りの2件は他participantの初期回答です。

このCross Exposure回答では、外部Web検索、追加repository参照、過去の別chat、この実験に関する他の会話を使用しないでください。

添付されたraw responseを改変された引用として扱わず、どのresponseを参照したか明示してください。

Cross Exposure後の一致を、独立した収束または独立した証拠として扱ってはいけません。
初期回答間の一致、Cross Exposure後の一致、証拠による裏付けを区別してください。

あなたには承認権限、最終決定権限、release権限、外部action権限はありません。
回答はPROPOSE_ONLYです。

compact bundleの存在またはparticipant間の一致だけを理由に、次を主張してはいけません。

- PROTOCOL_LOAD_REPORT.status: COMPLETE
- formal release evidence
- FIELD_TRIAL conformance
- A3-REL-001の完了
- alpha.4 authorization
- 外部action authorization

次の構造で回答してください。

## 1. Reviewed responses

3件のraw responseを、参照pathとともに列挙してください。

## 2. Response-by-response critique

各responseについて、個別に次を記載してください。

- strongest points
- weaknesses
- unsupported assumptions
- missing evidence
- acceptance criteriaとの適合
- authorityまたはrelease boundaryの問題

## 3. Comparison with your initial response

あなた自身の初期回答について、次を区別してください。

### Retained claims

Cross Exposure後も維持する主張。

### Changed claims

修正した主張。変更前と変更後を示してください。

### Withdrawn claims

撤回する主張と理由。

### New claims

Cross Exposure後に新しく追加する主張。

## 4. Agreement classification

次を区別してください。

- Blind First Round時点での一致
- Cross Exposure後の一致
- 共通sourceまたは共通promptに由来する可能性
- evidenceにより裏付けられた一致
- evidence未確認の一致

この段階では最終的なconvergence classificationを決定しないでください。

## 5. Residual disagreement and dissent

現在も残る重要な不一致、反対意見、失敗条件、少数意見を記載してください。

不一致を無理に解消しないでください。

## 6. Evidence gaps

最終判断前に必要な証拠、検証、測定、repository確認を記載してください。

確認していない事実は確認済みとして扱わないでください。

## 7. Revised proposal

task/prompt.mdのRequired outputとAcceptance criteriaに従い、Cross Exposure後の修正版提案を提示してください。

これは人間への提案であり、承認または実行指示ではありません。

## 8. Authority and release boundary check

次を明示してください。

- authority remains PROPOSE_ONLY
- Human Final Authority is required
- no external action is authorized
- formal_release_evidence remains false
- alpha4_authorized remains false
