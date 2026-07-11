# MADP コマンド体系 v0.3.0-alpha.3

状態: コマンド探索・解析に関する規範的実装プロファイルです。

canonical commandは小文字kebab-caseで記録し、SESSION、PLANNING、PARTICIPANT、ROLE、RELAY、INGESTION、EVIDENCE、RECORDS、TEAM、HELP、PORTABILITYに整理します。

初回利用者向けには `start`、`status`、`checkpoint`、`save`／`backup`、`load`／`restore`、`resume`、`minutes`、`help`、`end` をaliasとして使用できます。aliasは入力上の利便性だけを提供し、authorityを変更しません。元の入力とcanonical commandの両方を記録します。

statusとhelpはstateを変更できません。exportはprivate情報を無断で含められません。importは最初にreportを作成し、確認なしにstateを置換・統合できません。
