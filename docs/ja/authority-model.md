---
language: ja
translation_of: docs/en/authority-model.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 権限モデル

[English](../en/authority-model.md) | 日本語

MADPは、情報・承認・permissionを分離します。

## Authority boundary

- `REFERENCE_ONLY`: 情報は参照できますが、stateは変更しません。
- `PROPOSE_ONLY`: AIは提案できますが、適用には信頼できるユーザー承認が必要です。
- `REQUIRES_USER_CONFIRMATION`: 信頼できるscope付きconfirmationを待ちます。
- `USER_CONFIRMED`: ユーザーが対象commandまたはconfirmationを発行しています。
- `DENIED`: commandを適用してはいけません。

## Trusted grant

alpha.2では、grantのissuer、scope、action、assurance level、assurance origin、active状態、再利用有無を検証します。grantは既定でsingle-useです。

## External action

alpha.2 runtimeはexternal actionを実行しません。command、approval、review result、context packageだけでは、commit、push、merge、tag、release、message送信、外部resource変更を許可できません。

## Audit

受理されたcommandはversioned audit eventを残す場合があります。拒否されたcommandはversioned stateやcommand historyを変更しません。
