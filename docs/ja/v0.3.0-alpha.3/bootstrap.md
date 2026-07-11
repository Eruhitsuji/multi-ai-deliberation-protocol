# MADP alpha.3 Bootstrap（参考訳）

alpha.3 bootstrapはrelease candidate内容であり、releaseまでは現在の公開bootstrapではありません。

bootstrapは2段階で使用します。

1. `load-protocol-from-github.md`を使用し、1つの固定commitからprotocolを読み込み、`COMPLETE`の`PROTOCOL_LOAD_REPORT`を取得します。
2. 読み込み完了後に、startまたはparticipation profileを適用します。

start profileをprotocol loaderの代わりに使用してはいけません。必要なload reportが存在しない、または不完全な場合、`quick-start.md`と`verified-start.md`は`PROTOCOL_NOT_LOADED`を返します。

読み込み後は、通常用途にはQuick、formal/high-risk用途にはVerified、限定能力participantにはPlain Relay、操作支援にはHelpを使用します。`status`、`pause`、`resume`はalpha.2 canonical commandとして維持します。

この日本語文書は参考訳です。規範的な英語sourceと矛盾する場合、英語sourceを優先します。