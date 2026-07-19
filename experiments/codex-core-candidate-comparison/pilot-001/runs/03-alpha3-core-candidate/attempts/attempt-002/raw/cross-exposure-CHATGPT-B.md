以下がCross Exposure後の修正版回答です。

participant_id: CHATGPT-B
model_label: GPT-5.6 Sol
own_initial_response_ref: attempts/attempt-002/raw/initial-response-CHATGPT-B.md
prior_participant_outputs_seen: true
external_web_research_used: false
authority: PROPOSE_ONLY

**読み取り状況:** 添付された5ファイルを全文確認しました。読み取れなかった範囲はありません。3件の初期回答がCross Exposure前にraw保存・SHA-256固定されたことは、このラウンドで与えられた共通事実として扱います。ただし、各digest値およびindependence groupは提示されていないため、私自身によるhash再計算や独立性の検証は行っていません。

## 1. Reviewed responses

次の3件のraw responseを参照しました。

1. **CHATGPT-B（自分自身のBlind First Round回答）**
   参照path: `attempts/attempt-002/raw/initial-response-CHATGPT-B.md`
   添付ファイル: `initial-response-CHATGPT-B.md`
   最初の優先事項として4方式比較実験を提案しています。

2. **CLAUDE-B**
   参照path: `initial-response-CLAUDE-B.md`
   最初の優先事項としてalpha.3正式field trialを提案しています。

3. **GEMINI-B**
   参照path: `initial-response-GEMINI-B.md`
   最初の優先事項として4方式比較実験を提案しています。

上記responseは要約・批評の対象として参照していますが、raw responseそのものを改変された引用として扱っていません。

## 2. Response-by-response critique

### 2.1 CHATGPT-B

#### Strongest points

* 4方式の実測結果が存在しないことを出発点として、追加改善やalpha.4準備より先に測定を置いた点は、premature optimizationを抑える方針として強いです。
* comparison evidenceとformal release evidenceを分離し、比較だけで`A3-REL-001`を完了しない境界を維持しています。
* entry condition、exit condition、収集証拠、禁止actionを各work packageに具体化しており、Acceptance criteriaへの適合度が高いです。
* operator intervention、participant correlation、anchoring、missing data、raw preservationを主要リスクとして扱っています。
* 正式field trial先行論を最も強い反対論として記録し、方針変更条件を示しています。
* Immediate PRについて、実験結果の生成ではなく、measurement planとevidence contractの事前固定に限定しています。

#### Weaknesses

* Alternative comparisonで、正式field trialの`dependency on unavailable evidence`を「高」と評価した点は強すぎます。field trialにはload report、receipts、raw observations、human sign-off等の未取得証拠が必要ですが、**4方式比較結果がfield trial開始の正式な前提条件であるとは共通sourceに書かれていません**。
* Work Package 2に`A3-REL-001`と`A3-REL-005`をまとめたため、manual usability evidence取得とfinal-main auditの間の独立したgateが見えにくくなっています。
* Work Package 3でalpha.4検討にfield-trial findingsを事実上の必須材料として扱いましたが、固定情報が明示的に要求している最低条件は「4方式の比較可能な証拠」「人間評価」「別のhuman decision record」です。field-trial evidenceは重要ですが、供給情報だけから絶対的な前提条件とまでは断定できません。
* PR案で新しいYAMLやmanifestの種類を比較的具体的に挙げましたが、追加repository参照をしていないため、既存artifactとの重複有無は不明です。

#### Unsupported assumptions

* 比較結果がfield trialの対象方式やprofileを決めると暗黙に想定している部分。
* field trialが比較結果なしでは高い手戻りリスクを持つという相対評価。
* 比較後にbaseline変更が必要となる可能性を、順序決定上の主要理由として重く扱ったこと。

これらは合理的なrisk hypothesisですが、確認済み事実ではありません。

#### Missing evidence

* comparison scaffoldが現在の状態で実行可能か。
* 4方式間のoperator assistanceを同等にできるか。
* 適切なindependence groupを確保できるか。
* field trialの具体的なreadinessと必要残作業。
* 比較結果がfield-trial設計を実際に変更するか。
* 1つのpilot taskによる結果の再現性。

#### Acceptance criteriaとの適合

概ね適合しています。特に、最初のwork packageの明示、3段階の順序、比較とfield trialの分離、authority境界、alpha.4非承認、反対論、PR non-goalsは明確です。

改善点は、`A3-REL-001`と`A3-REL-005`を別gateとしてより明瞭に分離すること、および未確認の依存関係を相対評価で断定しないことです。

#### Authorityまたはrelease boundaryの問題

重大なauthority逸脱はありません。`PROPOSE_ONLY`、Human Final Authority、no external action、release非承認を維持しています。

ただし、「field trial対象を比較結果から選択する」という表現は、comparison resultがformal release pathを自動的に決めるように読まれないよう修正が必要です。

---

### 2.2 CLAUDE-B

#### Strongest points

* `A3-REL-001`がrelease critical pathであり、比較実験がrelease gateを直接閉じないという、他2回答より強いrelease-progress視点を提示しています。
* formal field trialに必要となるload report、profile binding、validation receipts、raw observation inventory、human sign-offを具体的に整理しています。
* checker PASSとhuman sign-offを明確に分離しています。
* 自分の推奨に使った仮定をA1～A3として明示し、それらが誤っていれば推奨が成立しないと認めています。
* 比較先行論を強いdissentとして詳細に記録し、自分の推奨を「僅差」と評価している点は適切です。
* Immediate PRをdocsと空templateに限定し、release-gate effectを「なし」としています。

#### Weaknesses

* 「公開bootstrapがalpha.2のままである乖離は、時間経過とともに増大する運用リスク」という主張は、実害や利用状況が提供されていないため未確認の推論です。
* 比較artifactがmainに蓄積し、`A3-REL-005`の監査面積を増やすという主張は、artifact配置や監査scopeをrepositoryで確認していないため未確認です。
* field trialの「dependency on unavailable evidence」をLOWとしていますが、load report、evidence runner、named approver、受入基準のreadiness自体が未確認です。比較結果への依存は低くても、未取得のformal evidenceへの依存は高い可能性があります。
* field trialのreversibilityを、tag・publicationに近づくことを理由に低めに評価しています。しかしfield trialの実施自体と、後続のrelease actionは分離すべきです。
* WP1からWP2への移行条件で`A3-REL-005`の実施可否を挟み、blocker検出時にはWP2へ進まないとしています。これにより、three-stage roadmap上で`A3-REL-005`が明示されない中間workとして扱われ、順序が読みにくくなっています。
* alpha.4検討条件として`A3-REL-001`と`A3-REL-005`の完了を必須としていますが、これは保守的な追加gateであり、固定情報に明示された必須条件ではありません。

#### Unsupported assumptions

CLAUDE-B自身も次を未確認仮定として開示しています。

* human ownerが単一または少数である。
* 比較artifactがfinal-main auditの監査面積を増やす。
* field-trial entry conditionはdocument追加だけで充足可能である。

さらに、次も未確認です。

* field trial observationを先に得ると比較metricが適切に較正される。
* 公開bootstrapのalpha.2継続による現実の損害が発生している。
* 現在のmain近傍で早期監査を行うことが監査コストを下げる。

#### Missing evidence

* field trialの準備状況。
* named human approver。
* evidence runnerとrelease checkerの実行実績。
* comparison artifactの保存pathとfinal-main audit scope。
* 公開bootstrapのalpha.2継続による実害。
* comparisonとfield trialの実際の人的コスト。
* formal field trialで使用すべきprofileまたは実行形態。

#### Acceptance criteriaとの適合

ほぼ適合しています。

特に比較evidenceとrelease evidenceの分離、alpha.4非承認、authority境界、反対論は明確です。

一方、`A3-REL-005`がroadmap内の独立したstageまたは明確なsub-gateとして配置されていないため、Acceptance criteria 6の表現をさらに明瞭にできました。

#### Authorityまたはrelease boundaryの問題

直接のauthority逸脱はありません。

ただし、field trial先行の理由として「release critical path」を重視しすぎると、human burden、evidence quality、比較実験の目的を従属させる可能性があります。これはauthority violationではありませんが、promptの「実装速度だけで最適化しない」という原則との緊張があります。

---

### 2.3 GEMINI-B

#### Strongest points

* 比較実験を第一優先とし、比較・field trial・final-main auditを3段階に分けたため、`A3-REL-001`と`A3-REL-005`の順序が視覚的に明確です。
* 8つの必須評価軸をすべて含めています。
* comparison evidenceをformal release evidenceへ流用しないこと、checker PASSをhuman approvalとしないこと、相関participantの一致を独立収束としないことを明示しています。
* WP1のmetricsと禁止actionを具体化しています。
* Alpha.4について`KEEP_DEFERRED`を選び、比較証拠とhuman decision recordが必要であるとしています。
* Immediate PRのrelease-gate effectとnon-goalsは明確です。

#### Weaknesses

* 評価表に絶対的・過度に強い表現があります。

  * 比較実験のauthority riskを「極めて低い」。
  * unavailable evidenceへの依存を「なし」。
  * premature optimization riskを「ゼロ」。
  * alpha.4のevidence valueを「皆無」。
  * alpha.4 implementation costを「莫大」。

  これらは実測値もrepository確認もなく、相対評価としても断定が強すぎます。
* 正式field trialを比較前に行うこと自体をpremature optimizationに近いものとして扱っています。しかしfield trialはrelease requirementであり、実装改善とは異なるため、必ずしもoptimizationではありません。
* WP1 exit後に、人間が「正式field trialに適用すべき方式およびprofileを選択する」としています。これは、4方式比較の勝者をformal field trialへ直接採用するという未確認の前提です。comparison pathとrelease-evidence pathは別であり、比較結果がformal profile authorizationを代替してはなりません。
* WP2で「選択方式による正式field trial」を提案していますが、Core Candidate artifactは`formal_release_evidence: false`であり、正式field trialで使用可能かは別途確認が必要です。
* WP3で`release_ready: true`、`tagged: true`、`published: true`への状態変更提案をdeliverableに含めています。人間への「release authorization request」としては可能ですが、readiness decision、tag、publicationという別actionを一括状態変更のように扱うとauthority境界が曖昧になります。
* 「本Work Packageを以てrelease cycleは完了する」としていますが、audit完了、人間のrelease decision、実際のtag・publicationは分離すべきです。
* 方針変更条件として、「比較を省略してもCore Candidate等が圧倒的に優れるという根拠」を要求していますが、比較を行わずにその優位性を示す条件は循環的です。
* 最終部に未閉鎖のコードフェンスと`[cite: 1]`が残っており、形式上の品質問題があります。

#### Unsupported assumptions

* 4方式比較が客観的な「優劣」を決められる。
* 比較結果によってformal field trialの方式・profileを選択する。
* field trial前の比較に実質的な依存証拠が存在しない。
* formal field trialは「本番試用」である。
* `A3-REL-005`完了後にそのままrelease cycleが完了する。
* alpha.4準備のコストが非常に大きい。

#### Missing evidence

* 比較結果が正式field trialのprofile選定に利用可能か。
* comparison armとformal field-trial profileの関係。
* release readiness、tag、publicationを分離する実際のdecision/action workflow。
* 実験回数、task数、operator interventionの統制。
* PRで新規experiment schemaを追加する必要性。
* Core Candidateをformal field trialに使用できることを示すauthorizationまたはevidence。

#### Acceptance criteriaとの適合

内容面では大部分に適合しています。

特に3段階順序、`A3-REL-001`から`A3-REL-005`への順序、authority境界、alpha.4非承認は明確です。

ただし、未確認の測定値やriskを絶対表現した点はAcceptance criteria 12との緊張があります。また、比較結果からformal field-trial方式を自動選択する構造はAcceptance criteria 3のevidence-path分離を弱めます。

#### Authorityまたはrelease boundaryの問題

実際のreleaseやexternal actionを実行してはいません。

ただし、WP3に`tagged: true`、`published: true`への状態変更提案を含めたこと、および比較結果からformal field-trial profileを選ぶ構造は、decision、authorization、executionの分離をさらに明示すべき箇所です。

## 3. Comparison with your initial response

### Retained claims

Cross Exposure後も次を維持します。

1. **最初のwork packageは4方式比較実験とする。**
2. 比較実験と正式field trialは別のevidence pathである。
3. 比較結果だけで`A3-REL-001`を完了しない。
4. 追加Core改善は、実測比較なしには正当化しない。
5. alpha.4 implementationは引き続きdeferredかつunauthorizedである。
6. Human Final Authorityを維持する。
7. checker PASS、participant agreement、model consensusはhuman approvalではない。
8. raw responses、exposure、correlation、operator interventionを保存・測定する。
9. 比較実験の結果は1件のpilotに限定されたevidenceとして扱い、一般性能へ過度に一般化しない。
10. 最も強い反対論は「release critical path上の正式field trialを先にすべき」という立場である。

固定情報では、比較実測結果はまだ存在せず、比較実験はfield trialと別であり、比較だけで`A3-REL-001`を完了できません。またalpha.4検討前には比較可能な証拠と人間評価が必要です。

### Changed claims

#### 変更1: field trialのunavailable evidence依存度

**変更前**

> alpha.3正式field trialの`dependency on unavailable evidence`は「高」。

**変更後**

> `dependency on unavailable evidence`は「中～高／readiness未確認」とする。

理由は、field trialには未取得のformal evidenceが多数必要ですが、**比較結果自体がfield trialの正式なentry conditionであるとは供給情報から確認できない**ためです。

#### 変更2: `A3-REL-001`と`A3-REL-005`のstage配置

**変更前**

> Work Package 2にformal field trial、`A3-REL-001`、`A3-REL-005`をまとめる。

**変更後**

> Work Package 2をformal field trialと`A3-REL-001`に限定し、Work Package 3の冒頭で`A3-REL-005` final-main auditを独立gateとして扱う。

これにより、`A3-REL-005`が`A3-REL-001`完了後の監査であることを明確にします。

#### 変更3: comparisonとfield-trial方式の関係

**変更前**

> 比較結果を人間が評価した後、field-trial対象と条件を選択する。

**変更後**

> 比較結果はfield-trial計画に情報を与え得るが、comparisonの「勝者」をformal field-trial profileとして自動採用しない。field trialで使用するprofile、load report、binding、authorityはrelease-evidence pathで別途確認する。

#### 変更4: Alpha.4に必要なfield-trial evidence

**変更前**

> alpha.4 authorizationにはcomparisonとfield-trial findingsの双方を実質的な必須条件とする。

**変更後**

> 固定情報上の最低条件は、比較可能な4方式evidence、人間評価、別のhuman decision recordである。field-trial findingsは重要なdecision inputになり得るが、供給情報だけから常に絶対必須とは断定しない。

#### 変更5: Immediate PRのartifact scope

**変更前**

> comparison run-plan YAML、metric-definition YAML、各種manifest templateを含むPR。

**変更後**

> まずdocs、既存formatを利用するtemplate、measurement dictionary、checklistに限定する。新規normative schemaの追加は、repository確認により既存schemaでは不足すると分かった場合の別decisionとする。

### Withdrawn claims

1. **field trialは比較結果に強く依存するという一般的主張**を撤回します。
   正確には、field trialは独自のformal evidence readinessに依存します。比較結果への依存は、trial designを変更するかどうかが確認されるまで不明です。

2. **field-trial findingsがalpha.4検討の常時必須条件であるという主張**を撤回します。
   これは保守的gateとして提案可能ですが、固定sourceから直接導ける必須条件ではありません。

3. **比較後にfield-trial方式を選択するという表現**を撤回します。
   comparison armとformal field-trial authorizationを混同しないためです。

### New claims

1. **比較実験にはoperator intervention normalizationが必要です。**
   各方式への説明、修正、再入力、format repairを同じ分類で記録しなければ、human burden比較が歪みます。

2. **aborted runとunusable runを除外せず、結果として記録すべきです。**
   成功runだけを比較すると、方式のrecoverabilityやfailure burdenが失われます。

3. **「decision relevance」を測定項目に追加すべきです。**
   観測された方式差がrelease safetyに関係するのか、単なるUI・記述量・利便性差なのかを区別します。

4. **formal field trialの観察をcomparison armのデータとして再利用してはなりません。**
   task、operator assistance、evidence purposeが異なるためです。

5. **Alpha.4 dispositionの変更を二段階化すべきです。**

   * 現在: `CONSIDER_AFTER_COMPARISON`、`alpha4_authorized: false`
   * 比較後: 必要なら`PREPARE_DECISION_RECORD_ONLY`
   * 実装開始: 別のhuman decision recordがある場合のみ

## 4. Agreement classification

### Blind First Round時点での一致

raw initial responsesがCross Exposure前に固定されていたという共通情報に基づくと、次の一致はBlind First Round時点で既に存在していました。

* CHATGPT-BとGEMINI-Bは、4方式比較実験を第一優先とした。
* 3回答すべてが、段階的roadmapを支持した。
* 3回答すべてが、comparison evidenceとformal release evidenceを分離した。
* 3回答すべてが、`A3-REL-001`の後に`A3-REL-005`を扱う必要を認識した。
* 3回答すべてが、追加Core改善を比較結果なしに進めることへ否定的だった。
* 3回答すべてが、alpha.4を現在承認しなかった。
* 3回答すべてがHuman Final Authority、no external action、checker PASS非承認を維持した。
* 3回答すべてが`formal_comparison_evidence_available: false`、`formal_release_evidence_complete: false`とした。

ただし、participantのindependence groupが提示されていないため、これを最終的なindependent convergenceとは分類しません。

### Cross Exposure後の一致

他回答を参照した後、私は次を追加で受け入れました。

* CLAUDE-Bが強調したrelease critical pathを、比較先行案の主要なdissentとしてより重く扱う。
* `A3-REL-001`と`A3-REL-005`を別gateとして明示する。
* field-trial readinessが十分高い場合には、順序変更が合理的である。
* Immediate PRでは、新規schemaよりもdocs・measurement plan・templateを優先する。
* 比較とfield trialのどちらもhuman burdenが高く、実測なしに相対コストを断定しない。

これらはCross Exposure後の更新であり、Blind First Roundの独立一致として数えません。

### 共通sourceまたは共通promptに由来する可能性

次の一致は、共通promptまたはcompact bundleに直接記載されているため、participant間の独立推論だけでなく、共通sourceによって生じた可能性が高いです。

* 比較結果がまだ存在しない。
* formal field trialが未完了。
* 比較実験とfield trialは別のevidence path。
* 比較結果だけで`A3-REL-001`を完了しない。
* `A3-REL-005`は`A3-REL-001`後のfinal-main audit。
* alpha.4はdeferred。
* Human Final Authority。
* checker PASSはhuman approvalではない。
* paid APIやautomatic orchestrationをCore必須にしない。
* correlated participantの一致をindependent convergenceとして数えない。

### Evidenceにより裏付けられた一致

次は添付sourceに直接裏付けられています。

* Core Candidateはrelease blockerを完了せず、alpha.4 implementationを承認しない。
* raw initial responses、exposure、participant correlation、dissent、human decisionを分離して保存する必要がある。
* minimum Core bindingはformal FIELD_TRIAL evidenceを代替しない。
* comparative evaluationの測定対象にはcompletion time、human actions、commands、corrections、authority/stale-state errors、dissent preservation等が含まれる。
* Cross Exposure後の一致を独立初期responseとして扱わない。

### Evidence未確認の一致

次は複数回答で言及されましたが、現時点では実測またはrepository確認がありません。

* 比較実験の方がfield trialより低コストである。
* field trialが比較実験より人的負担が大きい。
* 比較artifactが`A3-REL-005`の監査面積を増やす。
* field trialを先にすると比較metricが改善される。
* 比較を先にするとfield trialの手戻りが減る。
* Core Candidateがstandard alpha.3より有用である。
* 4方式を同じoperator assistanceで比較できる。
* 3participantが適切に独立したgroupである。
* 現在のscaffoldが実験を完走できる。
* formal field trialがすぐに実行可能である。

この段階では、最終的なconvergence classificationを決定しません。

## 5. Residual disagreement and dissent

### 5.1 最初の優先順位

主要な不一致は残っています。

* **CHATGPT-B・GEMINI-B:** 比較実験を先行。
* **CLAUDE-B:** formal field trialを先行。

私は比較先行を維持しますが、field-trial-firstをmaterial dissentとして残します。

### 5.2 Release progressとevidence qualityの優先関係

* field-trial-firstは、唯一の直接release pathを優先します。
* comparison-firstは、方式差とhuman burdenを測定してから高コストのformal trialへ進むことを優先します。

どちらが適切かは、field-trial readiness、比較実験の実行コスト、release timing、比較結果がtrial設計を変更する可能性によって変わります。

### 5.3 Formal field trialで使用する方式

GEMINI-Bは比較結果からformal field trial方式を選ぶ構造を提案しています。

私はこれに同意しません。比較結果は参考情報になり得ますが、formal field trialで使用するprofileやbindingは、release-evidence pathで別途確認されるべきです。

### 5.4 Alpha.4 disposition

* CHATGPT-B・CLAUDE-B: `CONSIDER_AFTER_COMPARISON`
* GEMINI-B: `KEEP_DEFERRED`

両者とも現在の`alpha4_authorized: false`には一致しています。違いは、現在の状態名を「継続defer」とするか、「比較後に検討」と明示するかです。

私は`CONSIDER_AFTER_COMPARISON`を維持しますが、これはimplementation authorizationではなく、比較後にhuman reviewを行う条件付きdispositionです。

### 5.5 `A3-REL-001`・`A3-REL-005`とalpha.4の関係

CLAUDE-Bは、alpha.4検討前に両release gateの完了を要求しています。

これは保守的で合理性がありますが、固定情報に明示されたalpha.4検討の必須条件は比較evidenceとhuman evaluationです。したがって、release gate完了を追加条件とするかはhuman decisionに残します。

### 5.6 失敗条件

次の場合、比較先行案は失敗または再検討が必要です。

* comparison scaffoldが実行不能で、大幅な実装変更が必要。
* 適切なindependence groupを確保できない。
* operator interventionを方式間で統制・記録できない。
* field trialが既に実行可能で、実施機会に失効期限がある。
* comparison結果がfield-trial設計に影響しないことが事前に確認される。
* 比較によりalpha.3 releaseが不合理に長期間停止する。

## 6. Evidence gaps

最終判断前に、少なくとも次の確認が必要です。

### Comparison experiment

* 3件のraw responseのactual SHA-256 digest。
* participantごとのindependence groupとcorrelation metadata。
* Cross Exposure前後のinformation-set hash。
* 4方式すべてのscaffold readiness。
* operator authorityの具体的scope。
* operator interventionの測定・分類方法。
* metricの操作的定義。
* aborted run、timeout、format failureの扱い。
* task数、repeat数、順序効果の統制。
* completion time、人間action、corrections、authority error等の実測。
* comparison artifactをformal comparison evidenceと呼べる受入条件。
* 1つのpilotから一般化できる範囲。

### Formal field trial

* `A3-REL-001`の詳細な受入基準。
* named human approver。
* trial task、scope、participants、stop conditions。
* 使用するauthorized profileとexact source binding。
* active load reportの存在と妥当性。
* validation receipt、schema records、raw observation inventory。
* evidence runnerとrelease checkerの実行可能性。
* human sign-offを結び付けるexact revision。
* trialの実施時期と機会制約。

### Repository確認

このラウンドでは禁止されているため確認していません。

* bound commits以降の変更。
* comparison scaffoldの実際のfile構成。
* 既存measurement schema、template、checker。
* comparison artifactがmain audit scopeに含まれるか。
* field-trial planning documentが既に存在するか。
* `A3-REL-005`の正確なaudit scope。
* Core Candidateをformal field trialで使用可能か。
* alpha.4を必要とする既知のversion-level defect。

## 7. Revised proposal

### 7.1 Recommended decision

最初に実施するwork packageとして、**Codexをoperatorとして使用する4方式のCore Candidate比較実験**を提案します。

主な理由は次のとおりです。

* 4方式の実測比較結果がまだ存在しない。
* Core Candidate Profile自身が4方式相当の比較と具体的metricsを要求している。
* comparisonは追加Core改善やalpha.4準備より可逆性が高い。
* alpha.4検討前には比較可能な証拠と人間評価が必要と明示されている。
* 方式差、operator burden、authority errorsを測定せずに追加改善するとpremature optimizationになり得る。

ただし、comparisonはrelease gateを直接進めません。そのため、field trialが既に実行可能で時間制約があると人間が確認した場合は、第一優先をfield trialへ変更できる条件付き提案とします。

### 7.2 Alternative comparison

以下は実測値ではなく、現在のinformation setに基づく暫定的な相対評価です。

| 候補                    | release progress | evidence value           | human burden | authority / safety risk | implementation cost | reversibility | unavailable evidence依存 | premature optimization |
| --------------------- | ---------------- | ------------------------ | ------------ | ----------------------- | ------------------- | ------------- | ---------------------- | ---------------------- |
| 1. 4方式比較              | 間接的              | 高いcomparison value       | 中～高・未測定      | 低～中                     | 中・readiness不明       | 高             | 低～中                    | 低                      |
| 2. Formal field trial | 直接的に高い           | 高いrelease-evidence value | 高い可能性・未測定    | 中                       | 中～高・readiness不明     | 中             | 中～高                    | 低～中                    |
| 3. Core等の追加改善         | 直接効果不明           | 現時点では低い                  | 中            | 中                       | 中～高                 | 中             | 高                      | 高                      |
| 4. alpha.4準備          | alpha.3には直接効果なし  | 現時点では低い                  | 中～高          | 高                       | 高                   | 低～中           | 非常に高い                  | 非常に高い                  |
| 5. 段階的方針              | 段階的              | 高い                       | 合計は高い        | gate次第                  | 中～高                 | 各gateでは高い     | 段階ごとに限定                | 低                      |

#### 候補1: 4方式比較実験

**利点**

* Core Candidateの効果と負担を実測できる。
* 改善対象をevidenceに結び付けられる。
* alpha.4検討の明示的な前提を満たす方向へ進む。
* baselineを変更せずに実施できれば可逆性が高い。

**欠点**

* release gateを直接閉じない。
* 4方式分のoperator・human負担がある。
* independenceやoperator interventionが不適切だと結果が歪む。
* 1件のpilotでは一般化が限定的。

**不足証拠**

* 実測結果。
* independence metadata。
* metric definitions。
* scaffold readiness。
* operator intervention comparability。
* repeatability。

#### 候補2: alpha.3正式field trial

**利点**

* `A3-REL-001`に直接対応する。
* manual usability evidenceとhuman sign-offを収集できる。
* `A3-REL-005`へ進むrelease critical pathである。

**欠点**

* formal evidence chainの人的・技術的負担が大きい可能性がある。
* readinessが不明。
* comparisonとrelease evidenceを混同する危険がある。
* trial後に大きなCore変更を行う場合、再trialまたは再auditが必要になる可能性がある。

**不足証拠**

* valid load report。
* exact profile binding。
* receiptsとrunner readiness。
* raw observation procedure。
* named approver。
* detailed acceptance criteria。

#### 候補3: Core Candidate等の追加改善

**利点**

* 実測で確認されたfrictionやsafety defectを修正できる。

**欠点**

* 現在は改善対象を示す実測がない。
* baselineを動かし、比較可能性やfinal-main auditを複雑にする可能性がある。

**不足証拠**

* failure pattern。
* cause analysis。
* before/after metrics。
* migration・compatibility・negative tests。

#### 候補4: alpha.4設計・実装準備

**利点**

* version-level変更が必要と判明した場合に将来設計を整理できる。

**欠点**

* 現在はDEFERRED。
* version-level changeの必要性が未確認。
* alpha.3で解決可能な問題をalpha.4へ拡大する危険がある。

**不足証拠**

* comparison results。
* human evaluation。
* alpha.3内で解決不能なrequirement。
* migration・compatibility plan。
* explicit human decision record。

#### 候補5: 段階的方針

**利点**

* comparison、release evidence、audit、version decisionを分離できる。
* 各gateで停止・再評価できる。

**欠点**

* 全体のhuman burdenと期間が増える。
* gateを曖昧にすると複数evidence pathが混在する。

**不足証拠**

* 各stageのreadiness。
* human capacity。
* transition decision criteria。

### 7.3 Three-stage roadmap

#### Work Package 1: Four-method comparison experiment

**Objective**

固定されたinformation setとbaselineに対して4方式を実行し、boundedなcomparison evidenceを作成する。

**Concrete deliverables**

* 各armのexact prompt、raw response、operator log。
* information-set hashとbaseline binding。
* participant・independence・correlation register。
* exposure records。
* metric dictionary。
* operator intervention log。
* completed、aborted、failed runを含むrun manifest。
* completion time、human actions、commands、corrections、unclear next actions、authority/stale-state errors、dissent preservation、decision reconstruction、user burdenの測定。
* decision-relevance assessment。
* limitationsとresidual dissentを含むcomparison report。
* `formal_release_evidence: false`、`alpha4_authorized: false`の明示。

**Entry conditions**

* frozen taskのexact bytesとhashが全armで一致。
* raw initial responseがCross Exposure前に固定。
* independence groupを推測しない。
* valid Blind First Roundと分類する場合、少なくとも2つの適切な独立groupを確認。
* metric、operator intervention、failure handlingを実行前に固定。
* Codex operatorの別途与えられたscopeが記録・hash・validation・organizeに限定。
* scaffold preflightが完了。
* substantive Core変更を比較前に行わない。

**Exit conditions**

* 4方式すべてについて、成功・失敗・未完了理由が記録されている。
* raw artifactが保存され、normalizationで上書きされていない。
* measurements、missing values、intervention、correlation、exposureが明示されている。
* comparison reportがhuman reviewに提出されている。
* humanがcomparison evidenceの品質と次stageへの移行を判断している。
* release evidenceまたはFIELD_TRIAL conformanceを主張していない。

**Evidence to collect**

* Core Profileで列挙された比較metrics。
* operator intervention。
* recovery burden。
* aborted-run原因。
* arm間のinstruction・assistance差。
* Blind First Round status。
* residual dissent。
* decision reconstruction。
* resultのtask依存性と一般化限界。

**Principal risks**

* correlated responsesをindependent evidenceと数える。
* Cross Exposure後の一致をBlind convergenceと数える。
* operator assistanceの偏り。
* successful runだけを選択する。
* validator PASSをapprovalと扱う。
* comparisonからformal profile authorizationを推論する。
* 1件のpilotから一般化する。

**Actions that remain prohibited**

* merge、commit、release、tag、publish、deployment。
* field-trial sign-off。
* `A3-REL-001`または`A3-REL-005`完了宣言。
* alpha.4 implementation。
* external action。
* paid APIやautomatic orchestrationのCore必須化。
* comparisonの勝者をformal field-trial profileとして自動採用すること。

**Condition for proceeding to Work Package 2**

Human Final Authorityが次を記録した場合に進む。

* comparison evidenceがdecision-usefulである。
* formal field trialのprofile、binding、scopeは別release pathで確認する。
* blocking defectがない、またはbounded remediationが完了している。
* trial readiness、named approver、evidence procedureが確認されている。

comparison evidenceが不十分なら、追加runまたはmeasurement修正を行う。

#### Work Package 2: alpha.3 formal field trial and `A3-REL-001`

**Objective**

実用時のmanual usability evidenceとrevision-bound human sign-offを収集し、`A3-REL-001`の完了可否を人間が判断できるformal release-evidence packageを作成する。

**Concrete deliverables**

* approved field-trial plan。
* valid FIELD_TRIAL `PROTOCOL_LOAD_REPORT`。
* exact `PROFILE_SOURCE_BINDING`。
* schema-validation records。
* complete validation receipts。
* validation evidence manifest。
* raw observation inventoryとhash binding。
* usability observation。
* authority・stale-state・recovery incidents。
* named-human sign-off record。
* `A3-REL-001` review packet。

**Entry conditions**

* trial実施がhumanにより明示的に承認されている。
* named approverと対象revisionが定義されている。
* trial scope、task、stop conditions、privacy handlingが定義されている。
* authorized profileとsource bindingが確認されている。
* evidence runnerとcheckerが実行可能。
* comparison evidenceをformal release evidenceとして流用しない。
* comparison armの「勝者」を自動的に採用しない。

**Exit conditions**

* required observationsがraw形式で保存されている。
* receiptsとbindingsが再計算可能。
* checker結果とlimitationsが記録されている。
* named humanがexact evidence revisionをreviewしている。
* humanが`A3-REL-001`のcomplete、incomplete、blockedを明示している。
* checker PASS単独でcompletionとしない。
* releaseはまだ別decisionがない限り`NOT_AUTHORIZED`。

**Evidence to collect**

* manual copy-and-pasteの実用性。
* local validationの実用性。
* action数、時間、friction、recovery。
* next-action clarity。
* authority errors。
* revision・stale-state handling。
* raw-to-receipt traceability。
* human sign-off basis。

**Principal risks**

* comparison evidenceとの混同。
* self-attested receipt。
* receipt referenceだけでartifactがない。
* observationの事後作成。
* baseline drift。
* checker PASSの過大解釈。
* human sign-offのrevision不一致。

**Actions that remain prohibited**

* AI sign-off。
* `A3-REL-005`の先行完了。
* release、tag、publish、deployment。
* external action。
* alpha.4 authorization。
* field trialからcomparison superiorityを推論すること。

**Condition for proceeding to Work Package 3**

`A3-REL-001`がhuman reviewにより完了と記録され、final-main audit対象となるexact stateが凍結された場合に進む。

不完了またはblockerありの場合は、bounded remediationの要否をhumanが決定する。

#### Work Package 3: `A3-REL-005` final-main audit and evidence-directed disposition

**Objective**

`A3-REL-001`完了後のexact final-main stateを監査し、alpha.3 release可否、bounded remediation、Core改善、alpha.4 decision-record準備のいずれへ進むかを人間が判断できるようにする。

**Concrete deliverables**

* final-main state binding。
* `A3-REL-005` audit plan。
* validation evidence manifest。
* checker、input、output、script hashes。
* audit findingsとunresolved blockers。
* comparison、field-trial、audit findingsのtraceability matrix。
* alpha.3 release decision packet。
* bounded remediation proposal。
* 必要な場合のみalpha.4 decision-record draft。
* acknowledged dissent。

**Entry conditions**

* `A3-REL-001`が完了。
* final-main stateが凍結。
* audit scriptsとrequired checksが特定。
* comparison artifactとrelease artifactの境界が明示。
* audit実施権限が別途存在。

**Exit conditions**

* auditのPASS、FAIL、INCOMPLETEがevidence付きで記録されている。
* blockerがある場合、remediationとre-audit要否が決定されている。
* humanがalpha.3 releaseをapprove、reject、deferのいずれかで記録している。
* alpha.4について`KEEP_DEFERRED`、`PREPARE_DECISION_RECORD_ONLY`、または別途authorizeのいずれかを人間が決定している。
* audit PASSだけでtag・publishを実行していない。

**Evidence to collect**

* current-main inputs。
* checker and runner hashes。
* complete audit outputs。
* unresolved release blockers。
* comparisonで発見された問題がrelease safetyに関係するか。
* field-trial findingsとの整合。
* alpha.3 bounded fixで解決可能か。
* version-level changeの必要性。

**Principal risks**

* audit後のstate変更。
* PASSをrelease authorizationと誤認。
* comparison findingをrelease blockerへ無検証で昇格。
* alpha.3で解決可能な問題をalpha.4へ送る。
* release decisionとtag・publication executionを一括化する。

**Actions that remain prohibited**

* AIによるrelease approval。
* automatic tag、publication、deployment。
* external action。
* human decision recordなしのalpha.4 implementation。
* unresolved blockerの隠蔽。
* dissentの削除。

**Condition for proceeding beyond Work Package 3**

別のhuman decision recordにより、次のいずれかが選択された場合のみ。

* alpha.3 release actionを別途authorizeする。
* bounded alpha.3 remediationを開始する。
  -追加comparisonまたはfield trialを行う。
* alpha.4 decision recordだけを準備する。
* alpha.4 implementationを別途明示的にauthorizeする。
* 継続deferする。

### 7.4 Immediate next PR proposal

**Proposed PR title**

`pilot-001: freeze four-method comparison execution contract and measurement plan`

**Scope**

* 4方式の実行条件とarm isolationを文書化。
* measurement dictionaryを固定。
* operator interventionとfailure classificationを定義。
* raw artifact、exposure、correlation、hash、missing-dataの記録templateを定義。
* human review gateとcomparison/release evidence境界を明記。
* 実測値やparticipant回答を事前記入しない。

**Filesまたはartifactの種類**

* comparison execution plan。
* metric dictionary。
* run manifest template。
* operator intervention log template。
* exposure・independence register template。
* comparison review checklist。
* limitations and dissent template。

まずdocsおよび既存artifact formatの再利用に限定します。新しいnormative schemaは、このinformation setだけでは必要性を確認できないためnon-goalとします。

**Validation**

* Markdown・既存formatのlocal validation。
* exact task・bundle hash欄のrequired check。
* 4方式のinformation-set一致check。
* raw-before-normalization check。
* exposure `UNKNOWN` preservation。
* independence group未記入時のfail-closed check。
* `formal_release_evidence: false` check。
* `alpha4_authorized: false` check。
* release、FIELD_TRIAL、human approvalを誤って主張する表現のnegative check。
* checker PASSがhuman approvalではないことの明記。

**Release-gate effect**

**なし。**

このPRは以下を完了しません。

* `A3-REL-001`
* `A3-REL-005`
* release readiness
* tag
* publication
* field-trial sign-off
* alpha.4 authorization

**Explicit non-goals**

* 実際の比較実験実行。
* participant回答生成。
* Core CandidateやWorkflow Macroの修正。
* compact bundleまたはdynamic role planningの変更。
* formal field trial。
* human sign-off。
* 新規normative schema。
* release、merge、commit、tag、publish、deployment。
* external APIまたはagent orchestrationの呼出し。
* 外部action。

### 7.5 Alpha.4 disposition

**選択: `CONSIDER_AFTER_COMPARISON`**

現在の意味は次のとおりです。

```yaml
alpha4_authorized: false
alpha4_implementation: DEFERRED
decision_record_preparation: NOT_YET_AUTHORIZED
```

`PREPARE_DECISION_RECORD_ONLY`へ変更するために必要なもの:

* 4方式comparison evidence。
* participant independenceとlimitationsの記録。
* human evaluation。
* alpha.3内で解決できない可能性があるversion-level issue。
* material dissent。
* decision-record preparationを許可するhuman decision。

`alpha4_authorized: true`へ変更するために必要なもの:

* exact scopeとtarget revision。
* comparison evidenceへのtraceability。
* compatibility・migration・rollback plan。
* safety-invariant tests。
* authority境界の維持。
* Coreにpaid APIやautomatic orchestrationを必須化しないこと。
* 別の明示的なhuman decision record。

field-trial evidenceと`A3-REL-005` findingsは重要な入力になり得ますが、供給情報だけから常にalpha.4検討の絶対前提とは断定しません。

### 7.6 Uncertainty and dissent

**判断に使用できない情報**

* 実測comparison results。
* actual independence groups。
* raw-response digest値。
* repositoryの現在状態。
* scaffold readiness。
* field-trial readiness。
* human capacityとrelease timing。
* exact audit scope。
* alpha.4を必要とする既知defect。

**追加で必要な測定・実験**

* 4方式matched run。
* operator intervention audit。
* repeat runsまたは追加task。
* independence・exposure audit。
* aborted-run analysis。
* field-trial readiness dry-run。
* evidence-runner dry-run。
* comparison findingのdecision relevance評価。

**最も強い反対論**

比較実験はrelease gateを閉じず、`A3-REL-001`が唯一の直接critical pathであるため、formal field trialを第一優先とすべきである。

**方針を変更する条件**

次がhumanにより確認された場合、第一優先をformal field trialへ変更することを支持します。

* field-trial plan、named approver、load-report procedure、raw-observation binding、runnerが準備済み。
* current baselineに既知のblocking safety defectがない。
* comparisonがfield-trial task、profile、measurement planを変更しない見込みが高い。
* field-trial実施機会に時間制約がある。
* comparisonとrelease evidenceを完全に分離したまま、比較を後続で実施できる。
* comparison scaffoldの修復に大きな実装作業が必要。

### 7.7 Final summary

```yaml
first_priority: RUN_FOUR_METHOD_CORE_CANDIDATE_COMPARISON
second_priority: CONDUCT_ALPHA3_FORMAL_FIELD_TRIAL_AND_COMPLETE_A3_REL_001
third_priority: COMPLETE_A3_REL_005_AND_PREPARE_EVIDENCE_DIRECTED_DISPOSITION
alpha3_release_status: NOT_AUTHORIZED
alpha4_status: CONSIDER_AFTER_COMPARISON
formal_comparison_evidence_available: false
formal_release_evidence_complete: false
human_decision_required: true
```

## 8. Authority and release boundary check

```yaml
authority: PROPOSE_ONLY
human_final_authority_required: true
external_action_authorized: false
formal_release_evidence: false
alpha4_authorized: false
release_authorized: false
field_trial_conformance_claimed: false
A3_REL_001_complete: false
PROTOCOL_LOAD_REPORT_COMPLETE_claimed: false
```

* **authority remains PROPOSE_ONLY**
* **Human Final Authority is required**
* **no external action is authorized**
* **formal_release_evidence remains false**
* **alpha4_authorized remains false**

この回答は批評および修正版提案であり、commit、merge、release、tag、publication、deployment、field-trial sign-off、alpha.4開始、その他のexternal actionを実行または承認しません。
