# Multi-AI Deliberation Protocol (MADP)

[English](README.md) | 日本語

> 現在公開中のプレリリース: **MADP-v0.3.0-alpha.1**
>
> mainに統合済みの次期版: **MADP-v0.3.0-alpha.2**（未タグ・未公開）

MADPは、複数のAI、役割分離されたAIインスタンス、人間の検証者、実行エージェントによる熟議を、構造化して安全に進めるためのサービス非依存プロトコルです。最終決定者は常にユーザーです。

## 重要な原則

- TODOは決定ではありません。
- 決定は承認ではありません。
- 承認は実行権限ではありません。
- レビューはmerge承認ではありません。
- AI同士の一致は証拠ではありません。
- 外部操作には、対象操作ごとの明示的なユーザー承認が必要です。

## 現在の状態

```yaml
current_published_prerelease: MADP-v0.3.0-alpha.1
current_main_development_version: MADP-v0.3.0-alpha.2
alpha2_merged_to_main: true
alpha2_tagged: false
alpha2_published: false
alpha2_release_ready: false
```

## 日本語ガイド

- [日本語ドキュメント入口](docs/ja/README.md)
- [はじめに](docs/ja/getting-started.md)
- [基本概念](docs/ja/concepts.md)
- [権限モデル](docs/ja/authority-model.md)
- [コマンド](docs/ja/commands.md)

## 規範的な仕様

規範的な仕様は英語版です。

- [MADP-v0.3.0-alpha.2 Protocol](protocol/MADP-v0.3.0-alpha.2.md)
- [MADP-v0.3.0-alpha.2 Glossary](protocol/GLOSSARY-v0.3.0-alpha.2.md)
- [Schemas](schemas/v0.3.0-alpha.2/)
- [Command Registry](registries/v0.3.0-alpha.2/commands.yaml)

日本語文書と英語の規範文書に差異がある場合、英語版が優先されます。

## License

MIT Licenseです。詳細は[LICENSE](LICENSE)を参照してください。
