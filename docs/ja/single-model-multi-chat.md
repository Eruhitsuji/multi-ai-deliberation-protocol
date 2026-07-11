---
language: ja
translation_of: docs/en/single-model-multi-chat.md
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# 実践ガイド：単体生成AIモデルを複数チャットで使う

[English](../en/single-model-multi-chat.md) | 日本語

## 目的

同じ生成AIモデルでも、チャットを分けてroleとcontextを分離します。利用できるproviderが1つだけでも、proposer、critic、validator、facilitatorを分けて運用したい場合に向いています。

## 期待できる効果

- 直前の会話によるanchoringを弱められる
- role instructionとevidence scopeを分離できる
- fresh chatで以前のoutputをreviewできる
- handoffとcontext packageを明示できる
- 複数providerより運用負担が小さい

ただし、underlying modelのbiasは共通です。完全に独立したexpertではなく、contextを分離したroleとして扱います。

## 推奨chat構成

```text
Chat 1: FACILITATOR / operative state
Chat 2: PROPOSER / solution design
Chat 3: CRITIC / failure analysis
Chat 4: VALIDATOR / evidenceとcompletion確認
```

小規模taskではfacilitatorとproposerを兼任し、3chatでも運用できます。

## 準備

1. facilitator chatでissue definitionを作ります。
2. version付きのcompact context packageを作ります。
3. 同じpackageを各participant chatへ渡します。
4. participant固有のrole instructionだけを追加します。
5. 使用したcontext revisionを示すreceiptを各chatへ要求します。

## context package例

```yaml
context_package:
  id: CTX-ARCH-001
  revision: 2
  goal: "deployment designを選ぶ"
  fixed_requirements:
    - "既存server 1台"
    - "5分以内にrollback可能"
  evidence:
    - id: E-01
      statement: "現在のpeak loadは40 requests/second"
      assurance: USER_PROVIDED
  unresolved_questions:
    - "launch後のexpected load"
  authority:
    allowed: ["analyze", "propose", "review"]
    not_allowed: ["edit", "send", "merge", "publish"]
```

## role prompt例

### Proposer chat

```text
PROPOSERとして行動してください。CTX-ARCH-001 revision 2から実現可能な2案を作り、implementation effort、reliability、rollback behaviorを比較してください。userの代わりに決定しないでください。
```

### Critic chat

```text
CRITICとして行動してください。提案が失敗すると仮定し、hidden assumption、operational failure、security issue、evidence gapを特定してください。具体的なcounterexampleとtestを返してください。
```

### Validator chat

```text
VALIDATORとして行動してください。各claimを固定要件と提供evidenceに照らして確認し、根拠のないclaimをUNVERIFIEDとしてください。completion conditionを満たすか明示してください。
```

## 実行手順

1. critic outputを見せずにproposerを実行します。
2. original contextとproposalをcriticへ渡します。
3. original contextと両方のresponseをvalidatorへ渡します。
4. structured findingだけをfacilitator chatへ戻します。
5. operative stateを更新しrevisionを増やします。
6. requirementが変わった場合は全active chatへ新packageを配ります。
7. 実際のdecisionをuserへ確認します。

## 得られる結果

facilitatorは次を出力します。

- option比較
- proposerとcriticの不一致
- 主要claimごとのevidence status
- 推奨next step
- user decision status
- 未解決作業のTODO

## context driftを防ぐ方法

- 全message先頭へcontext IDとrevisionを書く
- materialな変更後はold revisionのresponseを拒否する
- 会話全体を別chatへ貼らない
- claim、evidence、finding、decisionをstructured formで移す
- finding作成chatを記録するが、identityをauthorityにしない

## よくある失敗

- 1つのchatで複数roleを切り替え、以前のinstructionを残す
- facilitatorがcritical findingを要約で消す
- requirement変更後に一部participantだけ更新する
- fresh chatをunderlying modelから独立していると誤認する
- trusted user actionなしに「approved」を転記する

## 終了条件

全active chatが同じoperative revisionを使い、material findingが整理され、userがdecisionまたはdeferを行い、implementationやexternal actionが別権限として残っていれば終了できます。