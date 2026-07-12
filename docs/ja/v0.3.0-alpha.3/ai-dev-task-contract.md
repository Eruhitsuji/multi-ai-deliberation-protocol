# MADP v0.3.0-alpha.3 AI開発Task Contract Profile（参考訳）

状態: alpha.2 AI-driven development profileを拡張する任意の規範的implementation profile。

## 目的

scope、authority、acceptance、test integrityを明示的contractとして表現し、AI支援開発taskをmodel間でportableにします。

## Context architecture

- `A-CORE`: prohibition、authority boundary、固定environment、task contract、output contract、acceptance criteria。常に提供します。
- `A-EXT`: example、網羅table、長いdecision history、任意guidance。必要時に取得します。

## Task contract

各taskで次を特定します。

- goalとnon-goal
- 変更可能・変更禁止file
- environmentとdependency constraint
- 期待artifact
- 正確なacceptance check
- 追加可能なtestと、弱めてはいけないtest
- 別authorizationが必要なexternal action
- changed file、test、未実行check、assumption、limitationのreport要件

## Integrity rule

1. patch proposalはrepository modification permissionではありません。
2. design approvalはwrite、commit、push、PR作成、merge、tag、releaseの承認ではありません。
3. agentは失敗implementationを通す目的だけでtestまたはacceptance criteriaを変更してはいけません。
4. security、authorization、destructive operation、acceptance-policy変更、standard-document変更にはhuman reviewが必要です。
5. 一般化できる予防ruleがある場合、failureをtask template、development standard、review checklistへfeedbackします。
