# MADP v0.3.0-alpha.3 用語集

- **Adaptive Role Assignment**: 現在の論点に応じて分析役を追加、停止、終了、再割当する仕組み。
- **Assisted Conformance**: participant自身が完全なschema出力を行えず、mediatorの補助を受ける参加mode。
- **Canonicalization**: raw responseから正本候補を作る厳格な処理。元回答にない意味や権限を追加しない。
- **Claim Ledger**: fact、source claim、inference、proposal、opinionと検証状態を記録する台帳。
- **Deliberation Plan**: 目標、範囲、成果物、成功条件、決定方式、終了条件を定義するartifact。
- **Help Assistant**: protocol利用を支援する非参加型assistant。決定権、承認権、実行権を持たない。
- **Limited-Capability Participant**: URL、file、ZIP、YAMLなどの一部能力を持たない参加者。
- **Next Action Card**: ユーザー操作が必要な停止時に、現在地と具体的な次の操作を示すartifact。
- **Opinion Only**: 自然言語で意見を提供できるが、canonical stateを直接更新できない参加mode。
- **Plain Relay**: protocol全文やYAMLを要求せず、限定した質問を自然言語で渡すrelay。
- **Raw Response**: 参加者から受け取った未変更の原回答。
- **Response Ingestion**: raw responseの形式、parse結果、曖昧性、復旧、受理区分を記録する処理。
- **Session Minutes**: 議論の人間向け記録。正式なdecision logやcanonical stateとは区別する。
- **Team Proxy**: 他の人間の意見を代理伝達する参加者。代理発言は本人の直接発言として扱わない。
- **Tolerant Ingestion / Strict Canonicalization**: 入力形式には寛容でありつつ、正本採用には厳格な検証を要求する原則。
