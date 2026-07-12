# MADP v0.3.0-alpha.3 Source・Participant独立性Profile（参考訳）

状態: 任意の規範的implementation profile。意思決定authorityを変更せず、独立性評価を具体化します。

## 目的

別々のparticipantに見えるという理由だけで、相関したsource、model role、retrieval経路を独立したevidenceとして扱うことを防ぎます。

## 必須record

aggregation、verification、review routingへ独立性が影響するsourceまたはparticipantごとに、`schemas/v0.3.0-alpha.3/advanced-profiles.schema.yaml`の`independence_record`を使用します。

少なくともprovider、model family、data origin、retrieval provider、context origin、prompt lineage、independence group、不明事項を記録します。

## 規則

1. 同じmodelとchat contextを共有する複数roleは、同じindependence groupに属します。
2. 同じproviderまたは同じretrieval経路の出力は、自動的には独立とみなしません。
3. lineageが不明な場合は、不明と記録し、暗黙に独立扱いしません。
4. participant数とindependence-group数を別々に報告します。
5. 相関した出力の多数派は、verified evidenceでもapprovalでもありません。
6. reliability weightingには外部測定されたtask固有evidenceを使用できますが、modelのself-confidenceだけでauthorityや真偽を決めてはいけません。
7. 独立性が低い、material disagreementがある、またはprovenanceが弱い場合は、自動多数決ではなくreview escalationを行います。

## Aggregation境界

このprofileはaggregation結果、specialist review、追加evidence要求を提案できます。decisionの承認、minority dissentの抑制、action実行はできません。
