# MADP v0.3.0-alpha.3 用語集（参考訳）

- **Command Superset**: 以前のcanonical commandを保持したまま新commandを追加する方式。
- **Revision Binding**: 確認・承認・import・Help復帰を特定session/state/artifact revisionへ結び付けること。
- **Validation Evidence Manifest**: 実行したchecker、終了code、checker/input hashを機械生成した証拠。
- **Capability Status**: `SUPPORTED`、`UNSUPPORTED`、`UNKNOWN`の三値。
- **Help Exit**: `help-exit`により記録済みのprior phaseへ戻る操作。alpha.2の`resume`とは異なる。
- **Validation Receipt**: artifact locator、正確なrevisionまたはversion、canonicalization、artifact/schema hash、executor、result、structured errorをbindするmachine-executed record。model自己評価はValidation Receiptではありません。
- **MADP Canonical JSON v1**: keyを辞書順にsortし、不要な空白を含まず、Unicodeを保持し、非有限数を禁止したUTF-8 JSON。識別子は`MADP_CANONICAL_JSON_V1`。
- **Schema Validation Record**: 1つのrepository targetとhashを、1つのschemaとhash、receipt ID、validation resultへbindするload-report entry。
- **Transition Validation Authority**: state transitionがprotocol条件を満たすかをattestする決定論的authority。human decision authorityとは別です。
- **Independence Group**: provider、model、retrieval、data、context、prompt lineageをmaterialに共有し、evidenceなしには完全独立として数えないsourceまたはparticipantのgroup。
- **Scope Check**: 現在topicを`IN_SCOPE`、`SCOPE_EXPANSION`、`OUT_OF_SCOPE`に分類するrevision-bound artifact。
- **Assurance Mode**: evidence不足や未解決authorityがtransition validationへ与える影響を示す`NORMAL`、`REVIEW_REQUIRED`、`STRICT`。
