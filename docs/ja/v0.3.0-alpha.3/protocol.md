# MADP v0.3.0-alpha.3 プロトコル補足（参考訳）

alpha.3はalpha.2のauthority・command・context・TODO・review・relay規則を互換supersetとして継承します。alpha.2 canonical commandをaliasへ変更してはいけません。`status`、`pause`、`resume`は従来の意味を維持します。

すべての主要artifactは`session_id`、`source_state_version`、必要なartifact revisionを持ちます。確認・承認・復帰は対象revisionと一致しなければ拒否します。

`goal-confirm`はplan statusだけを変更します。sessionは、同じsession IDと確認済みplanを指定する別の`session-start`が成功した後だけ`ACTIVE`になります。それ以前の実質的state transitionは`SESSION_NOT_STARTED`でfail closedします。

authority-sensitiveな自然言語入力から、不足したID、revision、approver、selected action、expected state versionを推測してstateを変更してはいけません。canonical command previewまたは同等のrevision-bound confirmationを記録します。

自由文の`VALID`やmodel自己評価はmachine evidenceではありません。schema validityは完全なartifact hash、schema hash、executor、結果、errorを持つ`VALIDATION_RECEIPT`で示します。

規範順序は、上位のuser/platform rule、schema、protocol、command registry、protocolが明示したnormative profile、glossary、informative aidの順です。矛盾は仕様欠陥として報告し、解消まで厳しいauthority境界を適用します。
