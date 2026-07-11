---
language: ja
translation_of: docs/en/getting-started.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADPを使い始める

[English](../en/getting-started.md) | 日本語

MADPは、ユーザーを唯一の最終決定者として維持しながら、複数AIによる熟議を構造化します。

## 推奨する最初の動線

1. [基本的な使用方法](basic-usage.md)を読みます。
2. 3種類の議論方式から1つを選びます。
3. compactなoperative stateで1回の熟議cycleを実行します。
4. 必要に応じて開発、relay、TODO、reviewのdomain guideへ進みます。

[実践ガイド一覧](practical-guides.md)では、各workflowを目的・利用方法・成果物・期待効果で比較できます。

## 最小の進め方

1. 問題、固定要件、評価基準を明示します。
2. facilitatorと、範囲を限定したparticipant roleを割り当てます。
3. 会話履歴全体ではなく、現在有効なstateだけを共有します。
4. proposal、decision、approval、execution permissionを分離します。
5. 外部操作や不可逆操作には、明示的なユーザー承認を要求します。

## alpha.2のcommand処理

```text
Parse -> Normalize -> Validate -> Authorize -> Apply
```

入力されたcommand文字列だけでは権限になりません。厳密な挙動はversioned protocolとcommand registryを参照してください。

## 次に読む文書

- [基本的な使用方法とworkflow選択](basic-usage.md)
- [実践ガイド一覧](practical-guides.md)
- [基本概念](concepts.md)
- [権限モデル](authority-model.md)
- [コマンド](commands.md)
- 規範的な詳細: [`protocol/MADP-v0.3.0-alpha.2.md`](../../protocol/MADP-v0.3.0-alpha.2.md)
