# MADP v0.3.0-alpha.3 プロトコル補足（参考訳）

alpha.3はalpha.2のauthority・command・context・TODO・review・relay規則を互換supersetとして継承します。alpha.2 canonical commandをaliasへ変更してはいけません。`status`、`pause`、`resume`は従来の意味を維持します。

すべての主要artifactは`session_id`、`source_state_version`、必要なartifact revisionを持ちます。確認・承認・import・Help復帰は対象revisionと一致しなければ拒否します。

`goal-confirm`は正確なdeliberation plan revisionのstatusだけを`USER_CONFIRMED`へ変更します。sessionは別の正確な`session-start`が成功するまで`ACTIVE`になりません。開始前の実質的state transitionは`SESSION_NOT_STARTED`でfail closedします。

authority-sensitiveなmutationでは、自然言語からID、revision、approver、selected action、expected state versionを推測しません。実行するcanonical commandと全引数、または同等のrevision-bound confirmationを先に記録します。

自由文の`VALID`やmodel自己評価はmachine evidenceではありません。`VALIDATION_RECEIPT`はartifact locator、正確なrevisionまたはversion、canonicalization、artifact hash、schema hash、executor、result、structured errorをbindします。`RAW_BYTES`は正確なbyte、`MADP_CANONICAL_JSON_V1`はkeyを辞書順に並べ不要な空白を除いたUTF-8 JSONをhashします。

VERIFIEDまたはFIELD_TRIALのload reportでは、`schema_validation_records`がrepository target、target hash、artifact identity、schema path/hash、receipt ID、resultを結び付けます。`schemas_applicable`、`schemas_executed`、record、`unvalidated_structured_sources`、`validation_receipt_refs`は一致しなければなりません。receipt IDだけでreceipt artifactがない場合はevidenceではありません。

規範順序は、上位のuser/platform rule、schema、protocol、command registry、protocolが明示したnormative profile、glossary、informative aidの順です。矛盾は仕様欠陥として報告し、解消まで厳しいauthority境界を適用します。
