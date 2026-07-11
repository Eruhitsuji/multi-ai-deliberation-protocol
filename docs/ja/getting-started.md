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

- [基本概念](concepts.md)
- [権限モデル](authority-model.md)
- [コマンド](commands.md)
- 規範的な詳細: [`protocol/MADP-v0.3.0-alpha.2.md`](../../protocol/MADP-v0.3.0-alpha.2.md)
