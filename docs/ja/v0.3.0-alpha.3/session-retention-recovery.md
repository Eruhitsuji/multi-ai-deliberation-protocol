# MADP v0.3.0-alpha.3 Session Retention and Recovery Profile（参考訳）

状態: 任意の規範的implementation profile。

## 目的

session portabilityをretention、recovery、succession planningで拡張します。

retention planはcanonical session state、raw external response、validation receipt、minutes、decision record、関連evidenceを分類します。recovery-point objective、recovery-time objective、immutableまたはoffline copy要件、restore-test interval、key custodian、successor custodian、deletion policyを記録します。

少なくとも1回のrestore testを実施するか、未実施をlimitationとして明示するまで、backup claimをcompleteとしません。key successionのないencryptionはrecoverable retentionとみなしません。session exportはexternal serviceへのuploadをauthorizeしません。
