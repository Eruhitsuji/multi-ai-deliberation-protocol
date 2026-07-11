---
language: ja
translation_of: docs/en/ai-development.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADPを使ったAI駆動開発

[English](../en/ai-development.md) | 日本語

> この文書は非規範的な説明ガイドです。規範的な権限・コマンド規則は、version付きprotocol、schema、registryを参照してください。

## 目的

MADPでは、AI支援による開発工程を段階に分け、ある段階で許可されたことが、次の段階の権限へ自動的に拡張されないようにします。

```text
分析 -> 提案 -> 編集 -> テスト -> レビュー -> commit -> push -> PR -> merge -> tag -> release
```

各矢印は権限境界です。AIにファイル編集を許可しても、commit、push、merge、tag、公開まで許可したことにはなりません。

## 推奨フロー

1. **protocol contextを読み込む。** versionと実際に読んだファイルを記録します。
2. **課題を定義する。** 目的、固定要件、対象外、受入条件を明示します。
3. **TODOを作る。** TODOは作業記録であり、意思決定や承認ではありません。
4. **分析と提案を行う。** 代替案、根拠、仮定、未解決riskを残します。
5. **編集権限を別途確認する。** 編集は明示的かつscope付きで許可される必要があります。
6. **検証する。** 実行command、exit code、重要な結果を記録します。
7. **独立レビューを依頼する。** review responseは証拠ですが、merge承認ではありません。
8. **repository操作を個別に確認する。** commit、push、PR、merge、tag、releaseは別操作です。

## 最小handoff package

別のAIへ引き継ぐときは、少なくとも次を含めます。

- protocol version
- 現在の目的とscope
- branchまたはcommitの識別情報
- 変更済み、または変更予定のファイル
- 実行済みの検証
- 未解決TODO
- 既に与えられた権限
- 明示的に与えられていない権限
- 次に依頼する正確な操作

## 権限記述例

```yaml
authority:
  allowed:
    - repository内ファイルの確認
    - 修正案の提示
    - 指定branch上での編集
    - ローカル検証
  not_allowed:
    - push
    - merge
    - tag作成
    - release公開
```

## レビューの要件

質の高いレビューでは、次を明示します。

- 実際に読んだファイル
- 実際に実行した検査
- severityと根拠付きfinding
- 再現手順
- 推奨修正と追加テスト
- 外部操作を行っていないこと

## fail-closedにすべき場合

次の場合は停止または拒否します。

- 対象branchやrepositoryが曖昧
- 必須ファイルを読めていない
- user approvalが未検証
- command scopeが空、または権限より広い
- stateやreview evidenceが古い
- 外部操作にaction-specificな許可がない
