# MADP v0.3.0-alpha.3 Dissent Lifecycle Profile（参考訳）

状態: 任意の規範的implementation profile。

## 目的

訂正、privacy保護、法的redactionを可能にしながら、material dissentを監査可能なhistoryとして保存します。

`advanced-profiles.schema.yaml`の`dissent_record`を使用します。

## Lifecycle

`OPEN`、`RESOLVED`、`OVERRIDDEN`、`SUPERSEDED`、`REDACTED`はstatus changeであり、silent deletionではありません。original-record hashを保存します。resolutionではresolverとevidenceを記録します。redactionではreasonとaudit tombstoneを使用し、dissentが存在しなかったかのようにhistoryを書き換えません。

named decision authorityが選択した場合、dissentがopenのままdecisionを進められますが、recordでresolvedと表現してはいけません。報復、無許可のidentity disclosure、minority inputの抑制は、このprofileが許可するbehaviorではありません。
