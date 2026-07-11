# MADP v0.3.0-alpha.3 — 複数人チームでの議論

人間の組織上の役割、議論上の役割、authority roleを分離します。AIはcriticやrecorderになれますが、明示的な人間のgrantなしにapproverやdecision ownerにはなれません。

決定方式は`SINGLE_DECISION_OWNER`、`NAMED_APPROVERS`、`UNANIMOUS`、`MAJORITY`、`CONSENT_BASED`、`ADVISORY_ONLY`、`EXTERNAL_GOVERNANCE`から選択します。

必須規則:

- 沈黙を同意として数えない。
- material dissentを議事録とdecision recordに残す。
- 代理発言にはreported_byとconfirmation statusを付ける。
- 非同期回答には対象state versionを付ける。
- private inputはpermissionなしに全体state、relay、minutesへ移さない。
- チーム内の合意と正式approvalを区別する。
