# Multi-AI Deliberation Protocol (MADP)

[English](README.md) | 日本語

> 現在公開中のプレリリース: **MADP-v0.3.0-alpha.2**
>
> release tag: `MADP-v0.3.0-alpha.2`
>
> release commit: `207e24290e0a66bf0dd34e13f9b3525a42a5a6c9`

MADPは、複数のAI、役割分離されたAIインスタンス、人間の検証者、実行エージェントによる熟議を、構造化して安全に進めるためのサービス非依存プロトコルです。最終決定者は常にユーザーです。

## 初めて使う場合

1. [はじめに](docs/ja/getting-started.md)でMADPの全体像を確認します。
2. [基本的な使用方法](docs/ja/basic-usage.md)で課題を定義し、議論方式を選びます。
3. [実践ガイド一覧](docs/ja/practical-guides.md)から目的に合うworkflowへ進みます。

最初の試行には[単体生成AIモデル・単一チャット](docs/ja/single-model-single-chat.md)が適しています。役割分離を強める場合は[単体生成AIモデル・複数チャット](docs/ja/single-model-multi-chat.md)、model diversityが必要な重要判断では[複数生成AIモデル](docs/ja/multi-model-deliberation.md)を使用します。

## 重要な原則

- TODOは決定ではありません。
- 決定は承認ではありません。
- 承認は実行権限ではありません。
- レビューはmerge承認ではありません。
- AI同士の一致は証拠ではありません。
- 外部操作には、対象操作ごとの明示的なユーザー承認が必要です。

## 現在の状態

```yaml
current_published_prerelease: MADP-v0.3.0-alpha.2
release_tag: MADP-v0.3.0-alpha.2
release_commit: 207e24290e0a66bf0dd34e13f9b3525a42a5a6c9
release_preparation_workflow_run: 29135177099
release_preparation_workflow_result: success
alpha2_merged_to_main: true
alpha2_release_ready: true
alpha2_tagged: true
alpha2_published: true
published_at: UNKNOWN
previous_published_prerelease: MADP-v0.3.0-alpha.1
```

公開日時は、利用可能なconnectorからGitHub Release APIのauthoritative timestampを取得できなかったため、推測せず`UNKNOWN`として記録しています。tagとrelease commitが完全一致することは確認済みです。

## 日本語ガイド

### 最初に読む

- [日本語ドキュメント入口](docs/ja/README.md)
- [はじめに](docs/ja/getting-started.md)
- [基本的な使用方法](docs/ja/basic-usage.md)
- [実践ガイド一覧](docs/ja/practical-guides.md)
- [基本概念](docs/ja/concepts.md)
- [説明用用語集](docs/ja/glossary.md)
- [よくある質問](docs/ja/faq.md)

### 議論方式

- [複数生成AIモデルでの議論](docs/ja/multi-model-deliberation.md)
- [単体生成AIモデル・複数チャットでの議論](docs/ja/single-model-multi-chat.md)
- [単体生成AIモデル・単一チャットでの議論](docs/ja/single-model-single-chat.md)

### 実践利用

- [権限モデル](docs/ja/authority-model.md)
- [コマンド](docs/ja/commands.md)
- [AI駆動開発](docs/ja/ai-development.md)
- [コンテキスト共有とrelay](docs/ja/context-relay.md)
- [TODO lifecycle](docs/ja/todo-lifecycle.md)
- [レビューワークフロー](docs/ja/review-workflow.md)

## release資料

- [alpha.2 prerelease README](README-v0.3.0-alpha.2.md)
- [alpha.2 release notes](docs/releases/MADP-v0.3.0-alpha.2.md)

## 翻訳方針

日本語文書は非規範的な説明資料です。翻訳のscope、同期方法、source commitの扱いは[翻訳ポリシー](docs/TRANSLATION_POLICY.md)を参照してください。

## 規範的な仕様

規範的な仕様は英語版です。

- [MADP-v0.3.0-alpha.2 Protocol](protocol/MADP-v0.3.0-alpha.2.md)
- [MADP-v0.3.0-alpha.2 Glossary](protocol/GLOSSARY-v0.3.0-alpha.2.md)
- [Schemas](schemas/v0.3.0-alpha.2/)
- [Command Registry](registries/v0.3.0-alpha.2/commands.yaml)

日本語文書と英語の規範文書に差異がある場合、英語版が優先されます。

## Validation

```bash
python scripts/check_translation_docs.py
python scripts/check_release_readiness_v030_alpha2.py
```

## License

MIT Licenseです。詳細は[LICENSE](LICENSE)を参照してください。
