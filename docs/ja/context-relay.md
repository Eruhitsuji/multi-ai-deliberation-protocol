---
language: ja
translation_of: docs/en/context-relay.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# コンテキスト共有とrelay

[English](../en/context-relay.md) | 日本語

> この文書は非規範的な説明ガイドです。コンテキスト転送は権限を付与しません。

## bounded contextが必要な理由

会話全体のコピーはnoiseとcostが大きく、古い決定を再導入する危険があります。MADPでは、次の作業に必要なoperative stateだけを転送します。

context packageでは、次を答えられるようにします。

- 現在の目的は何か
- 何が決定済みか
- 何が未解決か
- どのartifactが関係するか
- どの権限が利用可能か
- どの操作が禁止されているか

## 推奨package内容

```yaml
context_package:
  protocol_version: MADP-v0.3.0-alpha.2
  purpose: independent review
  current_state:
    goal: command runtimeをレビューする
    branch: feature/example
    commit: 0123456789abcdef0123456789abcdef01234567
  artifacts:
    - path: scripts/apply_command.py
      role: implementation
    - path: scripts/test_command_runtime.py
      role: regression tests
  unresolved:
    - grant replay protectionを確認する
  authority:
    allowed: [read, test, review]
    prohibited: [edit, commit, push, merge, tag, release]
```

## receiptの原則

受信側は、次を記録したreceiptを返します。

- 実際に利用でき、読んだファイル
- 欠落または未読ファイル
- 理解した目的と制約
- state versionまたはcommit identity
- 理解した権限
- 曖昧さや矛盾

receiptは理解確認にすぎません。転送された主張の真実性を証明せず、操作権限も与えません。

## relay mode

- `DELIBERATION`: 構造化された検討を継続
- `INFORMATION_TRANSFER`: boundedな情報やartifactを転送
- `REVIEW_REQUEST`: 独立レビューを依頼
- `TASK_HANDOFF`: scope付きtaskを引き継ぐ
- `EVIDENCE_TRANSFER`: 検証・調査証拠を転送
- `RECOVERY`: loadやrelay失敗後にstateを復元

## stale stateとconflict

受信側がより新しいofficial stateを持つ場合、commit identityが矛盾する場合、またはpackageが現在のuser instructionを超える権限を主張する場合はfail closedにします。

次からapprovalを推測してはいけません。

- context packageが存在すること
- 複数AIが合意したこと
- 過去のreviewが成功したこと
- TODOが完了したこと
- branchがmerge可能であること
