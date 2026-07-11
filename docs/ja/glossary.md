---
language: ja
translation_of: docs/en/glossary.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 説明用用語集

[English](../en/glossary.md) | 日本語

> この用語集は非規範的な説明文書です。規範的な意味は`protocol/GLOSSARY-v0.3.0-alpha.2.md`を参照してください。

## Approval

特定のdecision revisionに結び付いたuser-confirmedな受諾です。approvalはexecution permissionではありません。

## Authority boundary

actorまたはcommandが実行できる範囲の上限です。read-only、propose-only、user-confirmedなinternal state change、別途許可されたexternal actionなどがあります。

## Command block

raw MADP commandをparseした後のnormalized structured representationです。command identity、issuer、arguments、authority boundary、intended effectsを記録します。

## Completion basis

TODOが`DONE`へ移った理由を支える記録済みevidenceです。具体的かつ検証可能であるべきです。

## Context package

operative stateと関連artifactのbounded transferです。それ自体ではauthorityを転送しません。

## Decision

選択された結果または結論です。revisionでversion管理され、user approvalが別途必要な場合があります。

## Execution permission

外部または重大な操作を実行するためのaction-specific authorizationです。analysis、proposal、review、approvalとは別です。

## Fail closed

必要なevidence、identity、scope、state freshness、authorityを確認できない場合に拒否または停止することです。

## Grant

action、scope、assurance、activity stateを持つuser-originated authorization artifactです。alpha.2のinternal grantは既定でsingle-useです。

## Non-normative

canonical protocol、schema、registryを上書きしない説明資料です。

## Proposal

候補となる変更または結果です。AIが生成した、またはTODOからpromotionされたというだけではapproveされません。

## Relay

actorまたはAI instance間のstructured transferです。context、task、evidenceを運べますが、implicit approvalは運びません。

## Review response

reviewerが確認・実行・発見・推奨した内容のstructured recordです。evidenceではありますがmerge approvalではありません。

## State version

versioned state documentの単調増加identifierです。新しいofficial stateを古い転送stateで暗黙に置き換えてはいけません。

## TODO

追跡される作業単位です。TODOはdecision、approval、execution permissionではありません。

## Trusted assurance

applicable runtimeまたはpolicyが受理するassurance levelとoriginの組合せです。例として、実際のuser actionに由来するuser confirmationがあります。
