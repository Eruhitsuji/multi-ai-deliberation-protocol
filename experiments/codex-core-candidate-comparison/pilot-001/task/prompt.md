# Pilot-001 共通タスク

Task status: `FROZEN`

このファイル全体を、4方式すべてで同じinformation setとして使用する。

この課題は、MADPの実装、release、merge、publicationまたはalpha.4開始を自動的に承認するものではない。すべての出力は人間による今後の方針決定のための提案である。

---

## Task statement

現在のMADP v0.3.0-alpha.3の状態を踏まえ、今後実施する次の3つの主要work packageについて、優先順位、実施順序および各段階の移行条件を提案してください。

中心となるdecision questionは次のとおりです。

> MADPは次に何を最優先し、その後どのような順序とevidence gateで開発・評価を進めるべきか。

少なくとも、次の候補を比較してください。

1. Codexをoperatorとして使用する4方式のCore Candidate比較実験を実施する。
2. alpha.3の正式field trialを実施し、`A3-REL-001`の完了を目指す。
3. Core Candidate、Workflow Macro、compact bundleまたはdynamic role planningを追加改善する。
4. alpha.4の設計検討または実装準備を開始する。
5. 上記を組み合わせた段階的な方針を採用する。

複数の候補を段階的に採用してもよいが、最初に実施するwork packageを1つ明確に選択してください。

検討対象は、次の3つの主要work package、またはalpha.4開始可否について別の人間によるdecision recordが作成されるまでの範囲とします。

## Context supplied to every workflow

以下を、この実験における固定された共通事実として扱ってください。

### Project state

* 対象protocolは`MADP-v0.3.0-alpha.3`である。
* alpha.3のrelease-candidate contentは実装され、mainへ統合されている。
* alpha.3は`release_ready: false`、`tagged: false`、`published: false`である。
* alpha.3の正式field trialは完了していない。
* `A3-REL-001`は、実用時のmanual usability evidenceとhuman sign-offを要求している。
* `A3-REL-005`は、`A3-REL-001`完了後のfinal-main auditである。
* 現在公開されている正式bootstrapは、alpha.3 release authorizationが得られるまでalpha.2のままである。

### Core Candidate state

* Core Candidate ProfileとWorkflow Macroは、alpha.3上の実験的workstreamとして実装されている。
* Core compact bundleとdynamic role planningも実装されている。
* これらのartifactは`formal_release_evidence: false`である。
* Core Candidate比較実験は、alpha.3 release gateを直接完了しない。
* compact bundleが存在するだけでは、AIが内容を完全に読み込んだ証拠にはならない。
* dynamic role planはadvisoryであり、AI serviceの自動呼出し、human approvalまたは最終判断を行わない。

### Comparison experiment state

* 次の4方式を比較するpilot環境が作成されている。

  1. `MANUAL_MULTI_AI`
  2. `STANDARD_ALPHA3`
  3. `ALPHA3_CORE_CANDIDATE`
  4. `MARKDOWN_VALIDATOR`

* 実験環境が存在するだけであり、4方式の実測比較結果はまだ存在しない。

* この比較実験は、正式field trialとは別の実験である。

* 比較結果だけで`A3-REL-001`を完了してはならない。

* 比較artifactは`alpha4_authorized: false`を維持する。

### Version strategy

* alpha.3は現在のexperimental baselineである。
* alpha.4の独立実装は現在`DEFERRED`である。
* alpha.4開始を検討する前に、4方式について比較可能な証拠を収集し、人間が評価する必要がある。
* alpha.4を開始する場合は、別の明示的なhuman decision recordが必要である。

### Fixed principles

* Human Final Authorityを維持する。
* AIは承認権限、release権限またはexternal action権限を持たない。
* MADP Coreの使用やconformance testingに、有料APIまたは有料agent orchestration serviceを必須としない。
* manual copy-and-pasteとlocal validationをfirst-class mechanismとして維持する。
* Blind First Roundを有効な独立収束として扱う場合は、少なくとも2つの適切な独立groupが必要である。
* correlated participant間の一致をindependent convergenceとして扱わない。
* formal comparison evidenceとformal release evidenceを区別する。
* checkerのPASSをhuman sign-offまたはrelease authorizationとして扱わない。

### Bound commits

* alpha.3 comparison baseline commit:
  `2a29ddfebe4d9664d3a4043a01d8728fa525d049`
* Codex comparison scaffold merge commit:
  `b812ab9fa22f0945e4b068ed8a75dd62fc4fb060`

この課題では、上記以降に発生した可能性のある変更を推測してはならない。

## Required output

次の構成で回答してください。

### 1. Recommended decision

最初に実施すべきwork packageを1つ明示し、理由を簡潔に説明してください。

### 2. Alternative comparison

少なくとも次の評価軸を含む比較表を作成してください。

* release progress
* evidence value
* human burden
* authority and safety risk
* implementation cost
* reversibility
* dependency on unavailable evidence
* risk of premature optimization

各候補について、利点、欠点および現時点で不足している証拠を記載してください。

### 3. Three-stage roadmap

次の3つの主要work packageを順番に提示してください。

各work packageについて、次を記載してください。

* objective
* concrete deliverables
* entry conditions
* exit conditions
* evidence to collect
* principal risks
* actions that remain prohibited
* condition for proceeding to the next work package

### 4. Immediate next PR proposal

最初のwork packageを開始するための次のPRを1つ提案してください。

次を含めてください。

* proposed PR title
* scope
* filesまたはartifactの種類
* validation
* release-gate effect
* explicit non-goals

実際のコード、commit、mergeまたはrelease操作は行わず、PRの内容を提案するだけにしてください。

### 5. Alpha.4 disposition

次のいずれかを選択してください。

* `KEEP_DEFERRED`
* `CONSIDER_AFTER_COMPARISON`
* `PREPARE_DECISION_RECORD_ONLY`

現在の情報だけを理由として、`alpha4_authorized: true`を提案してはなりません。

選択した状態を変更するために必要な証拠とhuman decisionを明示してください。

### 6. Uncertainty and dissent

次を明示してください。

* 判断に使用できない情報
* 追加で必要な測定または実験
* 推奨方針に対する最も強い反対論
* 反対論が正しい場合に方針を変更する条件

### 7. Final summary

最後に次の形式で要約してください。

```yaml
first_priority: <work package>
second_priority: <work package>
third_priority: <work package>
alpha3_release_status: NOT_AUTHORIZED
alpha4_status: <selected disposition>
formal_comparison_evidence_available: false
formal_release_evidence_complete: false
human_decision_required: true
```

## Acceptance criteria

1. 最初に実施するwork packageが1つ明確に選択されている。
2. 次の3つの主要work packageが順序付けられている。
3. 比較実験と正式field trialが別のevidence pathとして扱われている。
4. 各work packageにentry condition、exit conditionおよび必要なevidenceが定義されている。
5. Core Candidateの追加改善を、比較結果が存在する前提で正当化していない。
6. `A3-REL-001`と`A3-REL-005`の関係が正しく考慮されている。
7. alpha.4開始を現在の情報だけで承認していない。
8. Human Final Authority、release境界およびexternal action境界が維持されている。
9. 有料APIまたは自動orchestrationをCore必須条件としていない。
10. 推奨方針に対する反対論と、方針を変更する条件が示されている。
11. 次のPRのscopeとnon-goalsが具体的に示されている。
12. 不明な測定値、独立性、approvalまたはevidence statusを推測していない。

## Authority boundary

* AI outputs are proposals only.
* Human Final Authority is required.
* No external action, repository modification, commit, merge, release, tag, publication, Pages promotion, deployment, field-trial sign-off, or alpha.4 authorization is authorized by this task alone.
* Codex may record, hash, validate, and organize experiment artifacts only within the separately authorized operator workflow.
* A validator PASS does not constitute human approval.
* The final roadmap is selected by the human owner after reviewing all four workflow results.

## Prohibited assumptions

* Do not infer missing IDs, revisions, measurements, participant identities, model labels, independence groups, timings, hashes, evidence status, or human approval.
* Do not assume that the Codex experiment scaffold contains completed experiment evidence.
* Do not assume that exploratory or comparison evidence satisfies formal release evidence requirements.
* Do not treat agreement between correlated participants as independent convergence.
* Do not treat compact bundle generation as proof of complete model ingestion.
* Do not use outputs from another workflow run before the current run's primary output is frozen.
* Do not silently authorize alpha.4, release, publication, deployment, merge, or external execution.
* Do not optimize the roadmap solely for implementation speed; evidence integrity, human burden and authority safety must also be evaluated.

---

Freeze procedure:

1. Confirm that every section contains the intended fixed information.
2. Keep `Task status` as `FROZEN`.
3. Commit this file before starting any workflow run.
4. Calculate SHA-256 from this file's exact UTF-8 bytes.
5. Record the digest in `experiment.yaml`.
6. Do not edit this file after the first run starts.
7. If any substantive change is required, create a new pilot instead of modifying this task.
