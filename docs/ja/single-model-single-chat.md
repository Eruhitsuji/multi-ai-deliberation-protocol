---
language: ja
translation_of: docs/en/single-model-single-chat.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 実践ガイド：単体生成AIモデルを単一チャットで使う

[English](../en/single-model-single-chat.md) | 日本語

## 目的

独立participantより速度と簡単さを優先するとき、1つのchatを軽量なMADP sessionとして使います。個人の意思決定、初期計画、brainstorming、requirement整理、MADPの学習に向いています。

## 効果と制限

効果:

- handoff負担がない
- operative stateを1か所で確認できる
- userと高速にiterationできる
- conclusionをTODOへ変換しやすい

制限:

- participant roleは同じcontext内でsimulationされる
- 後続reasoningが前のmessageへ強くanchorされる
- self-reviewはindependent reviewより弱い
- 不一致を早く統合しすぎる可能性がある

## 推奨運用

連続的に「自己議論」させるのではなく、phaseを明示的に分けます。

```text
Phase 1: issue clarification
Phase 2: independent option generation
Phase 3: critic pass
Phase 4: validator pass
Phase 5: facilitator synthesis
Phase 6: user decision
Phase 7: TODOとnext actionの記録
```

## 開始prompt

```text
この単一chat内で軽量MADP workflowを使用してください。

目的: [目的]
固定要件:
- [要件]
評価基準:
- [基準]

phaseを明確に分け、各phaseでactive roleを表示してください。
以前のoutputを黙って書き換えず、materialな不一致を残し、
根拠のない事実をUNVERIFIEDとし、external actionの前で停止してください。
userが唯一の最終決定者です。
```

## 詳細な手順

### 1. 課題を明確化する

facilitatorがgoalを言い換え、曖昧さを特定し、compact stateを作ります。

```yaml
operative_state:
  issue: "backup strategyを選ぶ"
  fixed_requirements:
    - "recovery point objectiveが24時間未満"
    - "常時稼働serverを追加しない"
  criteria: [recovery reliability, cost, maintenance effort]
  decision_status: OPEN
```

### 2. optionを生成する

最初は評価せずに複数案だけを作ります。premature convergenceを防ぎます。

### 3. critic passを行う

option記述を固定し、failure mode、hidden assumption、missing evidenceを調べます。

### 4. validator passを行う

各optionを全fixed requirementへ照合します。不明情報に依存するclaimは`UNVERIFIED`のままにします。

### 5. synthesisする

facilitatorが比較表を作り、minority concernを残し、recommendationとuser decisionを区別します。

### 6. userが決定する

userは特定revisionの承認、拒否、追加cycle、deferを選べます。

### 7. 後続作業を記録する

未解決evidence、experiment、implementation workをTODOに変換します。

## 最終output例

```yaml
session_result:
  recommendation:
    revision: 1
    option: "暗号化したdaily object-storage backup"
    basis:
      - "server追加禁止を満たす"
      - "maintenance burdenが最小"
  user_decision: PENDING
  unresolved:
    - "restore durationが未計測"
  todos:
    - id: TODO-001
      title: "full restore testを実行する"
      status: OPEN
  authority:
    external_action_allowed: false
```

## 品質を高める方法

- 評価前に2～3案を出す
- role間へ明確な区切りを入れる
- criticに対象claimを正確に引用させる
- validatorにrequirement matrixを行ごとに確認させる
- 重要度が上がったらfresh chatでfinal reviewする
- operative stateを定期要約するが、unresolved findingは削除しない

## よくある失敗

- role labelだけ変わり、reasoningが1つの意見のまま続く
- model自身のrecommendationをuser approvalとして扱う
- earlier constraintがlater messageから消える
- planが存在するだけでTODOをDONEにする
- 新しい依頼なしにplanningからexternal executionへ進む

## 別方式へ切り替える条件

high-impact decision、materialな不一致、evidence争い、security・release boundary、independent reviewが信頼性を変える場合は、複数chatまたは複数modelへ切り替えてください。