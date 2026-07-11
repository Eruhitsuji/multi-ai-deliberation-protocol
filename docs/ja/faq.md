---
language: ja
translation_of: docs/en/faq.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# よくある質問

[English](../en/faq.md) | 日本語

> このFAQは非規範的な説明文書です。version付き英語仕様が優先されます。

## MADPはAIモデルですか？

いいえ。MADPは、user、AI system、validator、execution agentの間の作業を構造化するprotocolです。

## 複数AIが同意すれば正しいと証明できますか？

いいえ。AI同士の一致はconvergenceであり、独立したevidenceではありません。重要な主張は再現可能な検査、一次資料、または適切なhuman validationで支える必要があります。

## TODOはdecisionと同じですか？

いいえ。TODOは作業記録です。decisionは結果を選択します。approvalとexecution permissionもさらに別です。

## decisionをapproveすると実行も許可されますか？

いいえ。approvalは特定のdecision revisionに結び付きます。外部実行には別のaction-specific permissionが必要です。

## reviewはmergeを許可しますか？

いいえ。reviewはevidenceを追加します。Ready for review、merge、tag、releaseにはそれぞれ別のgovernance decisionが必要です。

## なぜ英語をnormative sourceとして維持するのですか？

既存のprotocol、schema、registry、CI、bootstrap prompt、commit-pinned linkが安定した英語pathを利用しているためです。pathを維持することでinteroperabilityを壊しません。日本語文書は説明用の翻訳です。

## 別AIへ引き継ぐとき、なぜ会話全体をコピーしないのですか？

全履歴はnoiseが多く、obsolete stateを含む可能性があります。bounded context packageでは、現在の目的、artifact、未解決項目、evidence、authority boundaryを転送します。

## 必要な情報が不足している場合はどうしますか？

安全に進められるnon-blocked workは継続し、不足inputを記録します。そのinputに依存する操作はfail closedにします。approval、evidence、authorityを作り出してはいけません。

## MADPはshell commandやrepository操作を実行しますか？

protocolはworkflowを記述し、権限境界を表現できますが、実装側がexecution boundaryを強制する必要があります。alpha.2のinternal runtimeは外部操作を実行しません。

## `release_ready: false`は何を意味しますか？

implementation完了やmainへのmergeを、tag作成・release公開の許可として解釈してはいけないことを意味します。

## 翻訳はどのように維持しますか？

`docs/en/`と`docs/ja/`に対応ファイルを置き、source commitを記録し、日本語文書をnon-normativeと明記し、`python scripts/check_translation_docs.py`を実行します。
