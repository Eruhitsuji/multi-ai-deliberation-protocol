---
language: ja
translation_of: docs/en/multi-model-deliberation.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 実践ガイド：複数生成AIモデルでの議論

[English](../en/multi-model-deliberation.md) | 日本語

## 目的

異なる生成AIモデルを、役割分離されたparticipantとして利用します。学習data、推論傾向、tool access、失敗傾向の違いを活用したい場合に向いています。architecture選定、research synthesis、policy比較、risk分析、重要なreviewなどで有効です。

## 期待できる効果

- model固有の仮定やblind spotを発見しやすい
- 1社・1modelのframingへ依存しにくい
- adversarial reviewを強化できる
- participantの意見とfacilitatorの統合結果を分離できる
- 不一致を消さず、監査可能な形で残せる

model間の一致はproofではありません。evidence確認は別途必要です。

## 推奨role

```yaml
participants:
  - id: MODEL-A
    role: PROPOSER
    assignment: "実現可能な最善案を構築する"
  - id: MODEL-B
    role: CRITIC
    assignment: "失敗条件、counterexample、隠れたcostを探す"
  - id: MODEL-C
    role: VALIDATOR
    assignment: "evidence qualityと固定要件を確認する"
  - id: FACILITATOR
    role: FACILITATOR
    assignment: "stateを維持し、比較し、不一致を保存する"
```

facilitatorは別modelでもuserでも構いませんが、特定participantへ隠れたauthorityを与えてはいけません。

## 準備

全participantへ同じcontext packageを渡します。

- goalとdecision question
- fixed requirementと対象外
- evaluation criteriaと必要ならweight
- source付きの既知事実
- 現在のdecision revision
- 必須output format
- 与えたauthorityと、与えていないauthority

role固有の指示だけを追加で渡します。

## participant prompt例

```text
あなたはMADP熟議のPARTICIPANT [ID]です。
Role: [ROLE]
Scope: [ASSIGNMENT]

提供されたcontext packageだけをoperative shared stateとして使用してください。
user approval、execution permission、evidenceのない事実を推測しないでください。
次を返してください。
1. position
2. evidenceとassumption
3. riskとcounterargument
4. confidenceとuncertainty
5. 他roleへの質問
6. operative stateへの変更提案
```

## 実行手順

1. **独立round**：他modelの回答を見せずに各modelへ回答させます。
2. **receipt確認**：protocol version、context revision、roleの理解を確認します。
3. **cross-examination**：競合するclaimだけを提示し、反論または修正を求めます。
4. **evidence reconciliation**：事実衝突、価値判断衝突、scope誤解を分離します。
5. **facilitator synthesis**：多数決ではなく共通基準で比較表を作ります。
6. **user checkpoint**：選択、追加evidence、保留をuserへ確認します。
7. **outcome記録**：decisionをrevisionへbindし、後続作業をTODOへ変換します。

## 得られる結果の例

```yaml
deliberation_result:
  options:
    - id: A
      strengths: ["実装が最速"]
      weaknesses: ["single point of failure"]
      fixed_requirements_met: true
    - id: B
      strengths: ["fault isolationが最良"]
      weaknesses: ["運用complexityが高い"]
      fixed_requirements_met: true
  disagreements:
    - topic: "traffic growth予測"
      type: EVIDENCE_GAP
      positions:
        MODEL-A: "低成長"
        MODEL-B: "不確実で高成長の可能性あり"
  recommendation: B
  user_decision_required: true
```

## 品質管理

- 可能ならparticipant順をrandomizeする
- claim作成model名を後続participantへ見せない
- 外部事実にはcitationまたは`UNVERIFIED`を要求する
- severe riskを指摘したminority findingを残す
- 全optionを同じcriteriaで評価する
- 大きなrevision後はfresh validatorを使う

## よくある失敗

- **consensus cascade**：後続modelが最初の回答へ追従する
- **model prestige bias**：有名modelの意見を根拠なく優先する
- **context drift**：participantごとに異なる要件が渡る
- **false independence**：複数UIが同じunderlying modelを使っている
- **authority leakage**：participantの「approved」「merge可能」を権限として扱う

## 終了条件

共通基準に基づく比較が完成し、重大な不一致とevidence gapが可視化され、userがdecisionまたはdeferを行い、次のexternal action boundaryが明示されれば終了できます。