# MADP v0.3.0-alpha.3 Communication Alignment Profile（参考訳）

状態: 任意の規範的implementation profile。

## 目的

coreのgoal gate、claim ledger、revision ruleを重複実装せず、intent、assumption、scope、assertion、state、acceptanceの齟齬を防ぎます。

## Alignment contract

`advanced-profiles.schema.yaml`の`alignment_contract`を使用し、purpose、assumption、scope、claim-label policy、acceptance criteria、checkpoint policyを記録します。

decisionへmaterialな影響を与えるassumptionは、確認またはrejectされるまで`QUESTION_REQUIRED`とします。facilitatorは未解決assumptionを暗黙にfactへ変換してはいけません。

## Scope checkpoint

次の場合に`scope_check`を出力します。

- 設定revision intervalへ到達した
- 新しいpolicyまたはdecision familyが現れた
- confirmed planにない新しいoutput typeを導入した
- 現在topicがconfirmed scope外に見える

`SCOPE_EXPANSION`または`OUT_OF_SCOPE`では、拡張topicの実質作業前にgoal revisionが必要です。materialな選択がなければ、`IN_SCOPE`はuser pauseなしで継続できます。

## Assertion policy

model内部confidenceは直接観測可能なevidenceではありません。assertion strengthをprovenanceとverification statusへ合わせます。十分なevidenceなしの強いfact表現はassertion mismatchとして記録し、reviewへrouteします。
