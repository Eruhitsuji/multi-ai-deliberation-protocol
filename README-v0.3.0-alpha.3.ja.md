# MADP v0.3.0-alpha.3 — 包括的・案内型・チーム対応の熟議

状態: experimental field useのため`main`へmerge済みですが、release-ready・タグ済み・公開済みではありません。

alpha.3はalpha.2を置換せず、互換supersetとして拡張します。alpha.2の20 canonical commandを保持し、alpha.3の31 commandを追加します。`status`、`pause`、`resume`はalpha.2の意味を維持し、詳細なsession操作には`session-status`、`session-resume`、Help復帰には`help-exit`を使用します。

artifactはsession ID、source state version、artifact revisionへ束縛されます。release readinessは手書きのDONE宣言ではなく、現在のcheckerと入力hashに一致する機械生成evidence manifestを要求します。

## Bootstrapの順序

alpha.3の利用は2段階です。

1. `bootstrap/alpha3/load-protocol-from-github.md`を1つの固定commitに対して実行し、`COMPLETE`の`PROTOCOL_LOAD_REPORT`を取得します。
2. `bootstrap/alpha3/quick-start.md`または`bootstrap/alpha3/verified-start.md`を適用します。

start profileはprotocolを読み込みません。load reportが存在しない、または不完全な場合、未読ルールを推測せず`PROTOCOL_NOT_LOADED`で停止しなければなりません。

現在は実用を通じてA3-REL-001のusability evidenceを収集中です。問題を報告する場合は、使用したcommit、client、scenario、期待した動作、実際の動作、回復回数、不要pause、authority errorの有無を記録してください。alpha.2は、field trialのsign-offとfinal-main auditが完了するまで現在の公開bootstrapです。

この日本語文書はinformative translationです。規範的な英語sourceと矛盾する場合、英語の規範sourceを優先します。