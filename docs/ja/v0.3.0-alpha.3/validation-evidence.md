# MADP v0.3.0-alpha.3 Validation Evidence Profile（参考訳）

状態: VERIFIEDおよびFIELD_TRIAL evidence向けの規範的implementation profile。decision authorityまたはexecution authorityを付与しません。

## 目的

自由文の`VALID`や`schema checked`を、正確なartifact byteとschema byteからdeterministic checkerが再計算できるreceiptへ置き換えます。

## Receipt生成

`scripts/generate_validation_receipt_v030_alpha3.py`または同等の決定論的implementationを使用します。

`VALIDATION_RECEIPT`には次を記録します。

- artifact IDと、正確な正のrevisionまたはversion string
- artifact locator
- `RAW_BYTES`または`MADP_CANONICAL_JSON_V1`
- artifactとschemaのSHA-256
- validator名とversion
- `PASS`、`FAIL`、`NOT_EXECUTED`
- structured validation errorとlimitation

`MADP_CANONICAL_JSON_V1`は、keyを辞書順にsortし、不要な空白を含まず、Unicodeを保持し、非有限数を禁止したUTF-8 JSONです。

## Load reportのschema-validation record

VERIFIEDまたはFIELD_TRIALの`PROTOCOL_LOAD_REPORT`には`schema_validation_records`を含めます。各recordは1つのloaded targetを1つのschemaと1つのreceiptへbindします。

`schemas_applicable`、`schemas_executed`、validation record、`validation_receipt_refs`は相互に一致しなければなりません。対応するreceipt artifactがないreceipt IDはevidenceではありません。

## Release evidence

release sign-off時、usability checkerは次を再計算します。

1. load-report schema結果とcanonical report hash
2. 全参照receiptのschema
3. 各repository targetとschemaのhash
4. targetのJSON Schema結果
5. 選択start profileのhash
6. raw observation fileのhash

model self-reportをreceipt executorとして認めません。post-hoc deterministic validationはstructural validityを確立できますが、modelが実際にsourceを読んだことや意味を理解したことを遡って証明しません。retrieval evidenceとusability evidenceは分離します。

## Failure handling

validation失敗時はstructured errorを含む`FAIL` receiptを出力します。artifact byte不足、schema byte不足、hash不一致、未解決receipt reference、未検証のapplicable targetがある場合、VERIFIED/FIELD_TRIALをcompleteにできません。
