---
language: ja
translation_of: docs/en/practical-guides.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADP実践ガイド

[English](../en/practical-guides.md) | 日本語

最初に[基本的な使用方法](basic-usage.md)を読み、その後に目的へ合うガイドを選びます。

| ガイド | 目的 | 利用方法 | 主な成果物 | 期待できる効果 |
|---|---|---|---|---|
| [複数生成AIモデル](multi-model-deliberation.md) | 重要な判断でmodel diversityを使う | modelごとにproposer、critic、validator、facilitatorを割り当てる | evidence statusと不一致を残したoption比較 | 1つのmodel framingへの依存を減らす |
| [単体生成AI・複数チャット](single-model-multi-chat.md) | 1providerでrole分離する | version付きcontext packageを複数chatへ配る | findingを1つのfacilitator chatへ統合したstate | anchoringとcontext混在を減らす |
| [単体生成AI・単一チャット](single-model-single-chat.md) | 軽量sessionを素早く実行する | 1会話内でphaseとroleを明示的に分ける | recommendation、unresolved risk、TODO | MADPを最も簡単に始められる |
| [AI駆動開発](ai-development.md) | software developmentの各段階でauthorityを制御する | analysis、edit、test、review、commit、merge、releaseを分離する | 検証済み変更とrepository action boundary | permissionの暗黙拡張を防ぐ |
| [コンテキスト共有とrelay](context-relay.md) | operative stateだけを転送する | bounded context packageを送りreceiptを受け取る | version・authority情報付きhandoff | context driftと古い履歴の再利用を減らす |
| [TODO lifecycle](todo-lifecycle.md) | workをdecisionと混同せず追跡する | TODOを作成、進行、block、defer、complete、cancelする | 監査可能なwork stateとcompletion basis | 未完了作業とdependencyを可視化する |
| [レビューワークフロー](review-workflow.md) | 品質とriskについて独立evidenceを得る | scoped review requestを発行しfindingをdispositionする | finding、reproduction evidence、remediation status | review evidenceをapproval・merge authorityから分離する |

## 推奨学習順

1. 基本的な使用方法
2. 単体生成AI・単一チャット
3. 単体生成AI・複数チャット
4. 複数生成AIモデル
5. コンテキスト共有とrelay
6. TODO lifecycle
7. レビューワークフロー
8. repository操作やexternal actionがある場合はAI駆動開発

## riskに応じた選択

- **低影響・可逆的:** 単体生成AI・単一チャット
- **中程度のcomplexityまたはrole conflict:** 単体生成AI・複数チャット
- **高影響・evidence争い・重要review:** 複数生成AIモデル
- **externalまたは不可逆操作:** 議論方式に関係なくauthority check、review、明示的user checkpointを追加

## 共通output contract

すべての実践workflowで、次を可視化します。

```yaml
workflow_output:
  issue_and_scope: REQUIRED
  fixed_requirements: REQUIRED
  evidence_and_assumptions: REQUIRED
  alternatives_or_findings: REQUIRED
  unresolved_risks: REQUIRED
  user_decision_status: REQUIRED
  todos: OPTIONAL
  authority_for_next_action: REQUIRED
```

良いworkflowは回答を長くするだけではありません。境界を明確にし、evidenceを改善し、handoffを再現可能にし、次の行動を安全にします。