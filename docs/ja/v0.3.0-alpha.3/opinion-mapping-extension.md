# MADP v0.3.0-alpha.3 Opinion Mapping Extension（参考訳）

状態: 任意のadvisory extension。formal decision authorityを変更しません。

## 目的

formal deliberation前に短いstatementへのstanceを収集し、clusterとbridge statementを特定し、minority concernを保存します。

## Invariant

- `AGREE`は`approve`ではありません。
- popularityはfact verificationではありません。
- clusterはauthorityを持ちません。
- group majorityはexecution permissionではありません。
- 同じmodelとchatからの複数roleでindependent participant数を水増ししません。
- `PASS`、`NOT_SEEN`、`NO_RESPONSE`、`INVALIDATED`を区別します。
- permissionなしにprivate stanceをminutesへ含めません。
- minority dissentは後続claim ledgerとdeliberationから参照可能にします。

## Snapshot binding

`advanced-profiles.schema.yaml`の`opinion_map_report`を使用します。analysisを1つのsource state versionとsnapshot revisionへbindし、canonical semantic digestとraw-byte digestの両方を記録します。participant数とindependence-group数を別々に報告します。

## Formal deliberationへのbridge

preferenceは`OPINION`、提案actionは`PROPOSAL`、percentageとcross-group supportのstatementは`SOURCE_CLAIM`、minority concernはmaterial dissentとして取り込みます。通常のevidence、revision、human-authority gateなしにdecisionへ変換しません。結果は`ADVISORY_ONLY`のままです。
