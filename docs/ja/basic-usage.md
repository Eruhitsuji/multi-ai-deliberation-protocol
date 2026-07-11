---
language: ja
translation_of: docs/en/basic-usage.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 基本的な使用方法：MADPの進め方を選ぶ

[English](../en/basic-usage.md) | 日本語

> この文書は、初めてMADPを使う人向けの最初の動線です。説明用の非規範文書であり、厳密な規則はversion付きprotocol、schema、registryを参照してください。

## MADPでできること

MADPは、1つまたは複数のAIチャットを利用するときに、分析・決定・承認・実行権限を混同しないための進め方を提供します。一般的には次の成果が得られます。

- 問題と固定要件の明確化
- 役割を分離した分析
- 仮定と未解決riskの可視化
- revisionに紐づくdecisionまたはrecommendation
- lifecycle付きTODO
- review evidence
- 次の行動とauthority boundaryの明確化

## 手順1：課題を定義する

別のチャットを開く前に、最低限次の4項目を書きます。

```yaml
goal: "実用的なdeployment architectureを選ぶ"
fixed_requirements:
  - "既存server上で動作すること"
  - "月額費用が上限以内であること"
evaluation_criteria:
  - reliability
  - implementation effort
  - operating cost
out_of_scope:
  - vendorとの契約交渉
```

## 手順2：議論方式を選ぶ

| 方式 | 向いている用途 | 主な効果 | 主な負担 |
|---|---|---|---|
| [複数生成AIモデル](multi-model-deliberation.md) | 重要な判断、model diversity、adversarial review | 異なるmodel biasと能力を利用できる | 調整量が多い |
| [単体生成AI・複数チャット](single-model-multi-chat.md) | 1つのserviceで役割分離したい場合 | contextを分けた独立分析 | 基盤modelのbiasは共通 |
| [単体生成AI・単一チャット](single-model-single-chat.md) | 素早い判断、MADPの学習 | 最も簡単 | 独立性が最も弱い |

## 手順3：最小限の役割を決める

必要な役割だけを使います。

```yaml
roles:
  facilitator: "現在有効なstateを維持し、焦点を絞った質問をする"
  proposer: "最も実用的な案を構築する"
  critic: "失敗条件と根拠不足を探す"
  validator: "evidence、constraint、完了条件を確認する"
```

facilitatorは要約できますが、意見の不一致を消してはいけません。

## 手順4：このpromptから開始する

```text
MADPを説明用workflowとして使用してください。

目的: [目的]
固定要件:
- [要件]
評価基準:
- [基準]
対象外:
- [項目]

FACILITATORとして行動してください。proposal、decision、approval、TODO、
review、execution permissionを分離し、compactなoperative stateを維持してください。
明示的な依頼なしにuser approvalを主張したり、external actionを実行したり
しないでください。最初に課題を言い換え、必要最小限のparticipant roleを提案してください。
```

## 手順5：1回の熟議cycleを実行する

1. facilitatorが課題を言い換え、不足constraintを検出します。
2. 各participantが独立した立場を提示します。
3. criticがrisk、counterexample、missing evidenceを示します。
4. facilitatorが同じ評価基準で案を比較します。
5. userが選択、拒否、保留、追加検討を指示します。
6. decisionをrevision付きで記録します。
7. 後続作業はTODOにし、approvalと混同しません。

## 得られる結果の例

```yaml
result:
  recommendation: "Option B"
  decision_status: USER_DECISION_REQUIRED
  decisive_reasons:
    - "固定されたdeployment要件を満たす"
    - "運用riskが最も低い"
  rejected_alternatives:
    - option: "Option A"
      reason: "費用上限を超える"
  unresolved_risks:
    - "load test evidenceが不足している"
  next_steps:
    - "代表的なload testを実施する"
```

## 終了条件

次を満たせば、1回のsessionを終了できます。

- 固定要件が満たされているか、userが明示的にwaiveしている
- 主要案を同じ基準で比較している
- 不確実性が可視化されている
- userが決定または保留を行っている
- 実装作業がTODOとして記録されている
- 議論結果だけでexternal actionを許可していない

## よくある失敗

- 複数チャットへ異なる課題定義を渡す
- 多数決をproofとして扱う
- facilitatorがuser approvalを作り出す
- operative stateではなく会話履歴全体をコピーする
- review responseをmerge、公開、送信の許可として扱う

## 次に読む実践ガイド

議論方式を選んだ後、[AI駆動開発](ai-development.md)、[コンテキスト共有](context-relay.md)、[TODO lifecycle](todo-lifecycle.md)、[レビューワークフロー](review-workflow.md)を利用してください。