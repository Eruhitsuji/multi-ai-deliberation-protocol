# MADP v0.3.0-alpha.3 生成AI利用Governance Profile（参考訳）

状態: 研究室・組織向けの任意の規範的implementation profile。

## Policy context

このprofileを使用するsessionでは、次を記録します。

- information classification
- 禁止入力と入力最小化
- approved service、および保持・training利用・保存条件
- output verification level
- disclosure・recordkeeping要件
- responsibility allocation
- exception、incident、定期review手順

## Information class

推奨する最小classは`PUBLIC`、`INTERNAL`、`CONFIDENTIAL`、`PERSONAL_OR_HIGHLY_CONFIDENTIAL`です。組織はより厳しいclassを追加できますが、既存のhandling ruleを暗黙に弱めてはいけません。

## Verification level

- `LOW`: 可逆かつ低影響のoutputではuser self-reviewを許容できます。
- `MEDIUM`: claim、citation、calculation、codeにevidence checkまたはtestを行います。
- `HIGH`: 利用前に独立した有資格humanが該当outputとevidenceをreviewします。

## Responsibility

AIはaccountableなdecision ownerではありません。userは意図した利用に責任を持ち、reviewerは実際にreviewした範囲だけに責任を持ちます。approverは定義済みprocessと正確なrevisionを承認し、未確定の将来outputを包括承認しません。administratorはservice設定とincident channelを管理します。

## Exceptionとincident

exceptionにはscope、reason、approver、expiry、storage、deletion条件が必要です。情報開示、fabricated citation、unsafe code、unauthorized useの疑いを記録し、指定incident processへrouteします。反復incidentは個別修正だけで終わらせず、policyまたはtrainingを更新します。
