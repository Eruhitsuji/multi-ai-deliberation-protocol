# 議事録と記録

`SESSION_MINUTES`、`DECISION_LOG`、`ACTION_ITEM_LOG`、`CLAIM_LEDGER`、`SESSION_STATE`は目的が異なります。議事録に記載されたことだけで正式決定になったとはみなしません。

detail level:

- `QUICK`: 目的、結論、未解決点、次の行動
- `STANDARD`: 参加者、議題、主要意見、decision、dissent、action item
- `AUDIT`: source、state version、claim、authority、normalization、external responseを含む監査記録

AIが生成した議事録は`AUTO_GENERATED_DRAFT`です。人間のreview後に`HUMAN_REVIEWED`、正式承認後に`APPROVED_RECORD`へ変更できます。修正時は元記録を消さずrevisionを残します。
