---
language: ja
translation_of: docs/en/review-workflow.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# レビューワークフロー

[English](../en/review-workflow.md) | 日本語

> この文書は非規範的な説明ガイドです。レビューは証拠であり、merge、tag、release、外部操作の承認ではありません。

## レビュー段階

1. **contextを準備する。** branchまたはcommitを固定し、対象artifactを列挙します。
2. **review questionを定義する。** 一般的な感想ではなく、具体的な検査を依頼します。
3. **authorityを設定する。** 原則`PROPOSE_ONLY`とし、別途許可がない限りrepository変更を禁止します。
4. **独立検査を行う。** failureを再現し、周辺variantも試します。
5. **structured findingを返す。** severity、evidence、impact、recommended change、testを含めます。
6. **findingをdispositionする。** accepted、理由付きrejected、deferred、remediatedに分類します。
7. **follow-up reviewを依頼する。** 修正後に元のcounterexampleを再実行します。
8. **次のgovernance actionを別に決める。** Ready for review、merge、tag、releaseは独立です。

## severityの例

- `CRITICAL`: 重大なauthority・safety failure
- `HIGH`: integrity、security、interoperabilityに大きな影響
- `MEDIUM`: 影響範囲が限定された実質的欠陥
- `LOW`: 品質、文書、監査性の問題
- `INFO`: 観察事項や将来改善

severityはreviewer confidenceではなくimpactと悪用可能性で決めます。confidenceは別に記録します。

## finding template

```yaml
finding_id: REVIEW-001
severity: HIGH
confidence: HIGH
title: non-user actorがUSER_COMMANDを適用できる
affected_files:
  - scripts/apply_command.py
evidence:
  - 正確なcode location
  - 実行したcounterexample
impact: 権限のないstate mutationが可能。
recommended_change: grant pathより前に明示的user provenanceを要求する。
recommended_tests:
  - participant approveを拒否
  - generic grantでUSER_COMMANDを昇格できない
```

## follow-up status

明示的なstatusを使います。

- `VERIFIED_FIXED`
- `PARTIALLY_FIXED`
- `NOT_FIXED`
- `NOT_VERIFIED`

test suiteが成功することは重要ですが、それだけでは不十分です。重要なfindingでは、production pathに対して元のcounterexampleを独立に再実行します。

## レビュー完了checklist

- requested fileをすべて読む、または未読として列挙
- requested checkをすべて実行、または未実行理由を説明
- 元のblocking counterexampleを再実行
- 新規findingを分類
- 外部操作を実行していない
- user approvalを主張していない
- remaining riskとquestionを明記
