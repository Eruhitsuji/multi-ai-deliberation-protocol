---
language: ja
translation_of: docs/en/concepts.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 基本概念

## 意味の分離

```text
TODO != decision
decision != approval
approval != execution permission
review != merge approval
agreement != evidence
```

## 役割

- **USER**: 唯一の最終決定者です。
- **FACILITATOR**: 熟議と現在有効なstateを調整します。
- **PARTICIPANT**: 範囲を限定した分析やproposalを提供します。
- **VALIDATOR / REVIEWER**: evidence、構造、実装を確認しますが、実行権限は継承しません。
- **EXECUTION AGENT**: 別途与えられたpermissionの範囲内だけで操作します。

## 現在有効なstate

受信側が必要とする最小限のcurrent stateを共有します。context package、review request、relay artifactは情報を移しますが、authorityは移しません。

## Fail-closed

未知のcommand、不正なdocument、未検証・不適切なauthority assertion、明示的permissionのないexternal actionは適用しません。
