# MADP v0.3.0-alpha.3 用語集（参考訳）

- **Command Superset**: 以前のcanonical commandを保持したまま新commandを追加する方式。
- **Revision Binding**: 確認・承認・import・Help復帰を特定session/state/artifact revisionへ結び付けること。
- **Validation Evidence Manifest**: 実行したchecker、終了code、checker/input hashを機械生成した証拠。
- **Capability Status**: `SUPPORTED`、`UNSUPPORTED`、`UNKNOWN`の三値。
- **Help Exit**: `help-exit`により記録済みのprior phaseへ戻る操作。alpha.2の`resume`とは異なる。
- **Validation Receipt**: 完全なartifact bytes、schema bytes、executor、結果、構造化errorを結び付ける機械実行記録。modelの自己評価はvalidation receiptではない。
- **Transition Validation Authority**: state transitionがprotocol条件を満たすかを認証する決定論的権限。人間のdecision authorityとは別。
- **Independence Group**: provider、model、retrieval、data、context、prompt lineageを実質的に共有し、証拠なしには完全に独立と数えないsourceまたはparticipant群。
- **Scope Check**: 現在のtopicを`IN_SCOPE`、`SCOPE_EXPANSION`、`OUT_OF_SCOPE`へ分類するrevision-bound artifact。
- **Assurance Mode**: `NORMAL`、`REVIEW_REQUIRED`、`STRICT`。証拠不足やauthority未解決時のtransition validation強度を示す。
