# MADP v0.3.0-alpha.3 — ChatGPT・Claude Skills活用

vendor-neutralなsourceを正本とし、Claude向け`SKILL.md`、ChatGPT向けinstructions、generic bootstrapを生成します。adapterはprotocolの権限境界を変更しません。

facilitator、participant、recorder、Helpを別skillとして扱います。Help skillは議論の決定者にならず、recorder skillは議事録を承認済みと主張しません。scriptや外部toolを使用するskillでは、file、network、code execution、send、commitなどのpermissionを個別に扱います。
