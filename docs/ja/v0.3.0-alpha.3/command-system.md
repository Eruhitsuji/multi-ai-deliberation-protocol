# MADP コマンド体系 v0.3.0-alpha.3（参考訳）

alpha.3 command registryはalpha.2の20 canonical commandとalpha.3の31 commandからなる51 commandのsupersetです。canonical nameはaliasより優先します。`status`、`pause`、`resume`を別commandのaliasとして再定義しません。

parserはraw input、invoked name、canonical command、alias使用有無を保存します。runtimeは外部操作を行わず、stale revision、順序違反、authority不足をfail closedで拒否します。
