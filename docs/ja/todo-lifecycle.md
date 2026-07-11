---
language: ja
translation_of: docs/en/todo-lifecycle.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# TODO lifecycle

[English](../en/todo-lifecycle.md) | 日本語

> この文書は非規範的な説明ガイドです。機械検証ではschemaと共有transition tableを参照してください。

## TODOが意味するもの

TODOは、実施または調査すべき作業を記録します。TODOは次のものではありません。

- 意思決定
- 承認
- 実行許可
- 作業が正しいことの証拠
- mergeやreleaseの許可

## 状態

- `OPEN`: 受け入れ済みだが未着手
- `IN_PROGRESS`: 作業中
- `BLOCKED`: 依存関係が解決するまで継続不能
- `DEFERRED`: 意図的に延期
- `DONE`: completion basisを記録して完了
- `CANCELLED`: 意図的に中止

`DONE`と`CANCELLED`はterminalです。alpha.2 runtimeではmetadataも変更できません。

## 代表的な遷移

```text
OPEN -> IN_PROGRESS -> DONE
OPEN -> BLOCKED -> IN_PROGRESS
OPEN -> DEFERRED -> OPEN
OPEN/IN_PROGRESS/BLOCKED/DEFERRED -> CANCELLED
```

`DONE`へ移るときは、genericなstatus updateではなく`todo-done`を使います。完了には明示的な根拠が必要です。

## 良いcompletion basis

completion basisは、検証可能で具体的にします。

```yaml
completion_basis:
  - parser回帰テストが成功
  - authority counterexampleが閉じたことを再現
  - CI run 123456が成功
```

「終わったように見える」「AIが完了と言った」だけでは、強い証拠になりません。

## BLOCKED時に記録すること

TODOを`BLOCKED`にするときは次を残します。

- 何が不足しているか
- 誰または何が解決できるか
- user inputが必要か
- それでも進められる次の安全な作業

## promotion

TODOをpromotionすると、proposalやdecision candidateが作られます。promotion自体は承認ではありません。適切なauthorityが作用するまでproposed stateを維持します。

## 監査ルール

- TODO identifierを安定して維持する
- 削除・cancel後にidentifierを再利用しない
- status changeとcompletion basisを記録する
- 不正なtransitionを拒否する
- terminal itemを書き換えて履歴を変えない
