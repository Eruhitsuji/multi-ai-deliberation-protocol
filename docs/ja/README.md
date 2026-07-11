---
language: ja
translation_of: docs/en/README.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADP 日本語ドキュメント

[English documentation](../en/README.md) | 日本語

> このディレクトリは日本語の非規範的ガイドです。規範的な仕様は英語版`protocol/`、`schemas/`、`registries/`を参照してください。不一致がある場合は英語版が優先されます。

## 最初に読む

- [はじめに](getting-started.md)
- [基本的な使用方法とworkflow選択](basic-usage.md)
- [実践ガイド一覧](practical-guides.md)
- [基本概念](concepts.md)
- [説明用用語集](glossary.md)
- [よくある質問](faq.md)

## 議論方式

- [複数生成AIモデルでの議論](multi-model-deliberation.md)
- [単体生成AIモデル・複数チャットでの議論](single-model-multi-chat.md)
- [単体生成AIモデル・単一チャットでの議論](single-model-single-chat.md)

## 実践ガイド

- [権限モデル](authority-model.md)
- [コマンド](commands.md)
- [AI駆動開発](ai-development.md)
- [コンテキスト共有とrelay](context-relay.md)
- [TODO lifecycle](todo-lifecycle.md)
- [レビューワークフロー](review-workflow.md)

## 翻訳管理

- [翻訳ポリシー](../TRANSLATION_POLICY.md)
- [`docs/translations.yaml`](../translations.yaml)で日英ペアとsource commitを管理します。
- `python scripts/check_translation_docs.py`でpairingとmetadataを検証します。

## バージョン状態

- 公開中: `MADP-v0.3.0-alpha.1`
- release candidate準備完了・未タグ・未公開: `MADP-v0.3.0-alpha.2`
- `release_ready: true`
- tag作成とGitHub Release公開は別操作です。

## 規範文書

- [`protocol/MADP-v0.3.0-alpha.2.md`](../../protocol/MADP-v0.3.0-alpha.2.md)
- [`protocol/GLOSSARY-v0.3.0-alpha.2.md`](../../protocol/GLOSSARY-v0.3.0-alpha.2.md)
- [`schemas/v0.3.0-alpha.2/`](../../schemas/v0.3.0-alpha.2/)
- [`registries/v0.3.0-alpha.2/commands.yaml`](../../registries/v0.3.0-alpha.2/commands.yaml)
