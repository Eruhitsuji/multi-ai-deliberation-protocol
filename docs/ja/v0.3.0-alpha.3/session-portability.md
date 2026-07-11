# MADP セッション可搬性プロファイル v0.3.0-alpha.3

状態: alpha.3のセッションファイル入出力に関する規範的実装プロファイルです。

ユーザーは、記録、バックアップ、確認、他の生成AIへの引き継ぎ、再開のため、任意の時点でセッションのファイル出力を指定できます。以前に出力したファイルを読み込ませることもできます。ただし、現在の環境に実際のファイル作成・読取能力がない場合、AIは作成・読取・保存・検証したと主張してはいけません。

出力プロファイルは `MINIMAL`、`STANDARD`、`COMPLETE`、`HANDOFF` です。既定ではprivate情報を除外し、含める場合はその出力について明示的な確認を必要とします。manifestにはセッションID、state version、収録内容、redaction、sensitivity、SHA-256 inventoryを記録します。

読み込み時は元ファイルを変更せず保存し、manifest、hash、schema、authority、session/version collisionを可能な範囲で検証して `SESSION_IMPORT_REPORT` を作成します。確認前にcanonical stateを置換・統合してはいけません。許可される提案は、新規セッション作成、既存セッション再開、提案としての統合、隔離、拒否です。

`SESSION_CHECKPOINT` はバックアップや比較の基準点であり、canonical stateの複製・置換・承認ではありません。
