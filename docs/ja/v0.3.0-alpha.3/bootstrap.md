# alpha.3 Bootstrap利用ガイド

## 選択

- 通常の検討: `bootstrap/alpha3/quick-start.md`
- 高リスク、研究、正式review、開発: `bootstrap/alpha3/verified-start.md`
- URL、ZIP、YAML、file非対応のAI: `bootstrap/alpha3/invite-limited-participant.md`
- protocolの質問: `bootstrap/alpha3/help.md`

## Quick

議題を確認し、簡潔な`DELIBERATION_PLAN`を提案し、人間のdecision authorityを明示します。3〜5個の分析役を選び、不要なround境界ではユーザーを止めません。

## Verified

同一commitに固定されたmanifestとcomplete bundleを使用します。必要fileのread status、schema検証能力、participant authority、privacy、team decision policy、claim ledgerを確認してから本論へ進みます。

## 外部AI

copy対象は`BEGIN_MADP_COPY_BLOCK`から`END_MADP_COPY_BLOCK`までです。回答は改変せず進行chatへ戻します。YAMLが使えないAIには通常文章または番号付きlistを依頼します。

## 次の操作

ユーザー操作が必要な停止では、現在地、主操作、貼り付け先、受理形式、代替操作、Helpを示します。
