---
language: ja
translation_of: docs/en/commands.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# コマンド

[English](../en/commands.md) | 日本語

alpha.2では、registryに基づく20個のcommandを定義します。厳密なargumentとauthority boundaryは[`registries/v0.3.0-alpha.2/commands.yaml`](../../registries/v0.3.0-alpha.2/commands.yaml)を参照してください。

## 構文

```text
/madp <command> [--key value] [--key=value] [--flag]
```

LIST argumentは繰り返すと値を蓄積します。SCALAR argumentの重複は拒否されます。

## 分類

- Context・relay: `share-context`, `issue-relay`, `request-review`
- Read-only state: `summarize-state`, `check-authority`, `status`, `todo-list`
- Decision・workflow: `propose-decision`, `approve`, `reject`, `defer`, `prioritize`, `pause`, `resume`
- TODO: `todo-add`, `todo-update`, `todo-done`, `todo-defer`, `todo-promote`
- External boundary: `external-action`

## 例

```text
/madp request-review --target_role VALIDATOR --review_focus schema --review_focus authority
/madp todo-add --title "テストを書く" --priority HIGH
/madp todo-update --todo_id TODO-001 --status IN_PROGRESS
/madp todo-done --todo_id TODO-001 --completion_basis "CI成功"
```

terminal TODO state（`DONE`, `CANCELLED`）は変更できません。alpha.2の`external-action`は実行されません。
