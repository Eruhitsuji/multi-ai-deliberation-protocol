# MADP v0.3.0-alpha.3 用語集（参考訳）

- **Command Superset**: 以前のcanonical commandを保持したまま新commandを追加する方式。
- **Revision Binding**: 確認・承認・import・Help復帰を特定session/state/artifact revisionへ結び付けること。
- **Validation Evidence Manifest**: 実行したchecker、終了code、checker/input hashを機械生成した証拠。
- **Capability Status**: `SUPPORTED`、`UNSUPPORTED`、`UNKNOWN`の三値。
- **Help Exit**: `help-exit`により記録済みのprior phaseへ戻る操作。alpha.2の`resume`とは異なる。
