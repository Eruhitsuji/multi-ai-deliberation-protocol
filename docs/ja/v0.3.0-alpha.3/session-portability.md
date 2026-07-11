# MADP セッション可搬性 v0.3.0-alpha.3（参考訳）

exportはsource session/state revision、privacy、redaction、hash inventoryを保持します。importは元ファイルを変更せず、最初にrevision付きimport reportを作成します。`session-import-confirm`はimport IDとreport revisionが一致した場合だけ選択操作を適用できます。
