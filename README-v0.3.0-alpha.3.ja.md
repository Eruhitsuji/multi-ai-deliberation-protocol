# MADP v0.3.0-alpha.3 — 包括的・案内型・チーム対応の熟議

状態: experimental field useのため`main`へmerge済みですが、release-ready・tagged・publishedではありません。

alpha.3はalpha.2を置換せず、互換supersetとして拡張します。alpha.2の20 canonical commandを保持し、alpha.3の31 commandを追加します。`status`、`pause`、`resume`はalpha.2の意味を維持し、詳細session操作には`session-status`、`session-resume`、Help復帰には`help-exit`を使用します。

artifactはsession ID、source state version、artifact revisionへbindされます。`goal-confirm`はplan statusだけを変更し、実質的transitionの前に別の正確な`session-start`が必要です。

protocol-load report、command registry、validation receipt、advanced-profile artifactには専用schemaがあります。release readinessは手書きの`DONE`や自由文の`VALID`ではなく、report、repository target、schema、start profile、raw observationのhashを独立再計算できるmachine-generated evidenceとreceipt chainを要求します。

## Bootstrapの順序

alpha.3の利用は2段階です。

1. `bootstrap/alpha3/load-protocol-from-github.md`を1つの固定commitに対して実行し、`COMPLETE`の`PROTOCOL_LOAD_REPORT`を取得します。
2. `bootstrap/alpha3/quick-start.md`または`bootstrap/alpha3/verified-start.md`を適用します。

start profileはprotocolを読み込みません。load reportが存在しない、または不完全な場合、未読ruleを推測せず`PROTOCOL_NOT_LOADED`で停止します。VERIFIEDとFIELD_TRIALではdeterministic validation toolを読み込み、registry validationをactual receiptへbindします。

## 任意のadvanced profile

source/participant independence、blind first-round review、生成AI governance、AI開発task contract、communication alignment、assurance mode、opinion mapping、dissent lifecycle、session retention/recoveryの任意profileを提供します。これらはcore authorityやrelease gateを弱めません。

現在は実用を通じてA3-REL-001のusability evidenceを収集中です。問題を報告する場合は、使用commit、client、scenario、期待動作、実動作、回復回数、不要pause、authority error、raw observation hashを記録してください。alpha.2はfield-trial sign-offとfinal-main auditが完了するまで現在の公開bootstrapです。

この日本語文書はinformative translationです。規範的な英語sourceと矛盾する場合、英語の規範sourceを優先します。
