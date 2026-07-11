# MADP v0.3.0-alpha.3 プロトコル概要

## 1. 位置付け

alpha.3はalpha.2の権限、安全性、state、relayの規則を継承し、導入、複数人チーム、限定対応AI、形式逸脱回答、動的役割、議事録、Help、利用者動線を追加します。

## 2. 議論開始

`DELIBERATION_PLAN`に議題、主要目標、中心質問、成果物、成功条件、範囲、決定権者、終了条件を記録します。`goal_gate: REQUIRED`では、人間による確認前に本論を開始しません。

## 3. 運用モード

- `LIGHT`: 日常的な検討。最小限の目標、役割、要約を使用します。
- `STANDARD`: 比較、研究、設計。claim分類、review、議事録を使用します。
- `ASSURED`: 高リスク、正式評価、開発。verified bootstrap、schema検証、evidence管理、独立reviewを要求します。

facilitatorは危険度の上昇に応じてmodeのupgradeを提案できますが、根拠なくmodeを下げてはいけません。

## 4. 参加者

参加者は`HUMAN`、`AI_MODEL`、`AI_ROLE_ACTOR`、`TEAM_PROXY`、`OBSERVER`に分類します。対応能力に応じて`FULL_CONFORMANCE`、`ASSISTED_CONFORMANCE`、`OPINION_ONLY`、`OBSERVER`を割り当てます。

`OPINION_ONLY`の意見には価値がありますが、facilitator、state maintainer、approverとして扱わず、raw responseを保存してから必要に応じて正規化します。

## 5. 形式逸脱回答

入力は寛容に受け取り、canonical artifactへの採用は厳格に行います。raw responseを保存し、parse、validation、recovery、ambiguity、dispositionを`RESPONSE_INGEST_RECORD`へ記録します。

正規化は構文・表現の変換であり、意味や権限の創作ではありません。元回答にない承認、証拠、確信度、permissionは追加禁止です。

## 6. 役割

分析役割は固定人格ではなく、現在の論点に必要な機能として扱います。facilitatorは用語定義、反例、証拠、risk、usability、統合などの分析役を追加、停止、終了できます。decision owner、approver、veto holder、facilitatorの交代など権限に関わる変更には人間確認が必要です。

## 7. チーム

複数人の議論では、発言者、伝達者、参加channel、decision policy、named approver、veto、abstention、material dissentを記録します。沈黙は同意ではありません。代理伝達された発言を本人の直接発言と同一視しません。

## 8. 議事録

`SESSION_MINUTES`は人間向け記録です。proposal、decision、approval、dissent、action item、未解決点を分離します。AI生成時点では`AUTO_GENERATED_DRAFT`であり、人間のreviewやapprovalを自動的に意味しません。

## 9. Help

Help assistantはprotocolの説明、診断、copy block、repair proposalを提供しますが、canonical state、decision、approval、external executionを変更しません。議論中のHelp modeでは議論stateを一時停止し、`RESUME`で元のphaseへ戻ります。

## 10. 利用者動線

内部roundの境界だけを理由に停止しません。ユーザー操作が必要な停止では`NEXT_ACTION_CARD`を提示し、現在地、主操作、受理入力、完了後の処理、代替操作、Help経路を示します。
