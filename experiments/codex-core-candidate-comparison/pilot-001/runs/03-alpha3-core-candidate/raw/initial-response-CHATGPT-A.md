participant_id: CHATGPT-A
model_label: GPT-5.6 Thinking
prior_participant_outputs_seen: false
external_web_research_used: false
authority: PROPOSE_ONLY

### 1. Recommended decision

**最初に実施すべきwork package：Codexをoperatorとして使用する4方式のCore Candidate比較実験**

比較対象は次の4方式とする。

1. `MANUAL_MULTI_AI`
2. `STANDARD_ALPHA3`
3. `ALPHA3_CORE_CANDIDATE`
4. `MARKDOWN_VALIDATOR`

理由は、4方式のpilot環境は存在する一方、実測比較結果がまだなく、Core Candidate等の追加改善やalpha.4検討の根拠が不足しているためである。また、比較実験は正式field trialとは別のevidence pathであり、`A3-REL-001`を直接完了しないため、**短期間で完了する診断的work package**として明確に限定する必要がある。

推奨順序は次のとおりとする。

1. 4方式の比較実験
2. 比較結果に基づく限定的な安定化・改善判断
3. alpha.3正式field trial、`A3-REL-001`、続いて`A3-REL-005`

この順序は、正式field trialを比較実験で代替するものではない。比較により明らかになった重大なusability、authority、evidence-integrity上の問題を放置したまま正式field trialへ進み、試行をやり直すリスクを抑えるための順序である。

添付compact bundleは`EXPERIMENTAL_COMPACT_BUNDLE`であり、`formal_release_evidence: false`である。また、bundle自体が`PROTOCOL_LOAD_REPORT`、正式FIELD_TRIAL artifact、release authorization、execution authorizationではないと明記されている。したがって、本回答はbundleの存在を根拠に、protocol load、field-trial conformanceまたはrelease readinessを認定しない。

---

### 2. Alternative comparison

評価は、現時点の固定情報に基づく相対評価である。実測値ではない。

| 候補                             | release progress        | evidence value                                     | human burden                               | authority and safety risk                       | implementation cost         | reversibility               | dependency on unavailable evidence      | risk of premature optimization |
| ------------------------------ | ----------------------- | -------------------------------------------------- | ------------------------------------------ | ----------------------------------------------- | --------------------------- | --------------------------- | --------------------------------------- | ------------------------------ |
| **A. 4方式比較実験を先行**              | 低。`A3-REL-001`を直接進めない   | 高。方式間の差、負担、失敗形態を測定可能                               | 中。4方式の実行と人間評価が必要                           | 低〜中。境界を守れば低いが、比較結果をrelease evidenceと誤認する危険がある   | 中。scaffoldは存在するが実行・記録・評価が必要 | 高。実装変更前の診断である               | 中。独立性、測定条件、operator authorizationが未確認   | 低。改善前に実測を得る                    |
| **B. 正式field trialを先行**        | 高。`A3-REL-001`へ直接寄与     | 高。ただし主にalpha.3の正式usabilityとrelease readinessに関する証拠 | 高。正式な観察、binding、receipts、human sign-offが必要 | 中。証拠不足やchecker PASSを承認と誤認すると高まる                 | 中〜高                         | 中。失敗時にはtrial再実施が必要になり得る     | 高。正式field-trial packageと実行準備の完成状態が不明    | 中。比較で発見できた問題を抱えたまま試す可能性        |
| **C. Core Candidate等を直ちに追加改善** | 低〜中。改善内容によっては将来寄与       | 低。どの改善が必要かを示す比較結果がない                               | 中〜高。設計・実装・再検証が必要                           | 中。authority境界や既存alpha.3 invariantsを意図せず変更する危険   | 高                           | 中。schemaやruntime変更は戻しにくい    | 高。改善対象、効果、優先度の実測根拠がない                   | **高**                          |
| **D. alpha.4の設計・実装準備を先行**      | alpha.3 releaseには低い     | 現時点では低い。version changeの必要性を裏付ける比較証拠がない             | 高                                          | 中〜高。未承認versionへのscope driftや黙示的authorizationの危険 | 高                           | 低〜中。設計・実装が進むほどsunk costが増える | **非常に高い**。比較証拠とhuman decision recordがない | **非常に高い**                      |
| **E. evidence gate付き段階方針**     | 中〜高。比較後にrelease pathへ接続 | **非常に高い**。比較証拠と正式release evidenceを分離して蓄積           | 高。ただし不要な再試行を削減できる                          | 低〜中。各段階でhuman gateを置けば管理可能                      | 中〜高                         | 高。各段階で停止、修正、順序変更が可能         | 中。各段階の必要証拠を順次収集する                       | 低                              |

#### 各候補の利点・欠点・不足証拠

| 候補                   | 利点                                                                                                                                                                       | 欠点                                                                          | 現時点で不足している証拠                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **A. 4方式比較実験**       | 実装変更前に、completion time、human actions、corrections、authority errors、Blind First Round、dissent preservation、decision reconstruction、user burdenを比較できる。alpha.4判断にも必要な基礎を提供する | release blockerを直接閉じない。実験設計が不統一なら結果が比較不能になる                                 | 4方式の実測結果、参加者のindependence group、exposure状態、所要時間、人間操作数、error counts、評価者判断                                      |
| **B. 正式field trial** | `A3-REL-001`に必要なmanual usability evidenceとhuman sign-offを直接収集できる。完了後に`A3-REL-005`へ進める                                                                                    | 高い人間負担を伴い、比較で事前発見できた問題によりtrialを再実施する可能性がある                                  | 完全なFIELD_TRIAL load report、profile binding、validation receipts、raw observation inventory、実用時観察、human sign-off |
| **C. 追加改善**          | 明確な問題が既知なら、正式trial前に修正できる                                                                                                                                                | 現在は比較結果がなく、問題の頻度、重大性、改善効果が不明。pilotへの過適合やscope creepの危険がある                   | 改善対象ごとの再現事例、severity、発生率、方式間差、before/after評価、regression evidence                                              |
| **D. alpha.4準備**     | 将来のversion選択肢を整理できる可能性がある                                                                                                                                                | 現在`DEFERRED`であり、開始に必要な比較証拠とhuman decision recordがない。alpha.3 release作業を分散させる | version changeを必要とする比較結果、alpha.3では解決困難な問題、migration影響、費用対効果、人間による開始決定                                         |
| **E. 段階方針**          | 比較、改善、正式release evidenceを別々のgateとして扱い、判断可能性と安全性を両立する                                                                                                                     | gateが曖昧だと工程が長期化する。比較が終わらない研究workstreamになる危険がある                              | 各stageの固定exit criteria、time-box、decision owner、停止条件、測定受入基準                                                    |

**総合判断：候補Eを採用し、その第1段階として候補Aを実施する。**

---

### 3. Three-stage roadmap

## Work Package 1 — 4方式Core Candidate比較実験

**Objective**

同一information setと同一taskを用いて4方式を実行し、方式ごとの有用性、負担、失敗形態およびauthority安全性について比較可能な証拠を作る。

**Concrete deliverables**

* 4方式それぞれの凍結されたprimary output
* 各runのmode、participant、operator、information-set bindingを記録したrun manifest
* raw promptおよびraw responseの保存記録
* Blind First Roundのexposure記録
* participant correlation／independence group記録
* completion time、human actions、canonical commands、corrections、unclear next actionsの測定
* authority error、stale-state error、normalization error等のissue log
* dissent preservationおよびdecision reconstructionの評価
* local validator結果と、validatorの限界を明記した記録
* 人間評価者による比較rubric
* formal comparison evidenceとformal release evidenceを区別したcomparison report

**Entry conditions**

* `task/prompt.md`が`FROZEN`のまま維持されている
* 比較対象baseline commitとscaffold merge commitがrun manifestに記録される
* 4方式に同一のinformation setを提供する手順が固定される
* Codex operator workflowについて、別途human authorizationが存在する
* participant identity、model label、chat context、independence groupを推測せず記録できる
* Blind First Roundでは初期回答が他participantの結論へexposureされる前に固定される
* 有料APIまたは自動agent orchestrationをCore必須条件としない
* manual copy-and-pasteおよびlocal validationを利用可能な実行経路として維持する

**Exit conditions**

* 4方式すべてについて、完了runまたは理由付きのnon-completion recordが存在する
* raw initial responsesが上書きされず保存されている
* information set、mode、exposure、correlationおよび測定方法が追跡可能である
* 不明なindependenceやexposureが推測で補完されていない
* 各方式について同じ評価軸が適用されている
* 人間評価者が、結果をroadmap判断に利用可能または利用不能と明示している
* 比較artifactが`formal_release_evidence: false`および`alpha4_authorized: false`を維持している

**Evidence to collect**

* task completionの成否および所要時間
* human action数と種類
* canonical command数
* correctionおよびreformat要求数
* unclear next actionの件数
* authority boundary violationまたはnear-miss
* stale-state、revision、ID binding関連error
* Blind First Round conformance status
* correlated convergenceとindependent convergenceの区別
* raw response preservation
* material dissentの保持
* final recommendationの再構成可能性
* evaluatorが感じた認知負担と操作負担

**Principal risks**

* operatorが方式間で異なる補助を行う
* 先行runの結論が後続participantへ漏れる
* correlated participantsを独立証拠として数える
* modeごとの出力量の差を品質差と誤認する
* validator PASSをhuman approvalと扱う
* compact bundleの提供を完全なprotocol ingestionの証拠と扱う
* 比較実験を正式field trialまたはrelease evidenceとして扱う
* 比較が長期化し、release pathを不必要に停止する

**Actions that remain prohibited**

* repository変更、commit、merge、release、tag、publicationまたはdeployment
* field-trial sign-off
* `A3-REL-001`または`A3-REL-005`の完了宣言
* `PROTOCOL_LOAD_REPORT.status: COMPLETE`の推定
* `alpha4_authorized: true`への変更
* AIによる承認または最終判断
* external action
* task開始後のfrozen information setの実質的変更
* 未確認participant属性、hash、revision、timingまたはapprovalの補完

**Condition for proceeding to the next work package**

人間のdecision ownerが比較artifactをレビューし、次を記録した場合に進む。

* 比較可能性が受容可能である
* 重大な測定欠損が明示されている
* field trial前に修正すべき問題と、修正不要な問題が区別されている
* Stage 2のscopeが比較結果へtrace可能である
* 比較結果だけではrelease gateを閉じないことが確認されている

---

## Work Package 2 — 比較結果に基づく限定的な安定化・改善

**Objective**

比較実験で観察された重大または高頻度の問題だけを対象に、正式field trial前の最小限の安定化を行う。改善のための改善を避け、変更不要の場合は明示的なno-change decisionを作る。

**Concrete deliverables**

* comparison finding register
* 各findingのseverity、frequency、affected mode、raw evidenceへの参照
* `REMEDIATE`、`ACCEPT_FOR_FIELD_TRIAL`、`DEFER`、`INSUFFICIENT_EVIDENCE`のhuman disposition
* 変更対象と比較証拠を結ぶtraceability matrix
* 必要な場合のみ、Core Candidate、Workflow Macro、compact bundleまたはdynamic role planningへの限定的修正案
* authority、revision、raw-preservation、Blind First Round、dissentに関するnegative fixtures
* before/afterの再実行結果
* field-trial candidateの固定案
* 変更しない場合の根拠を記録したno-change decision record

**Entry conditions**

* Work Package 1のexit conditionsを満たす
* 人間がdecision-usableと認めた比較結果が存在する
* 修正候補ごとに少なくとも1つの追跡可能な観察がある
* human ownerが変更scopeと優先順位を承認する
* alpha.3 baseline上で行う修正と、将来version候補を区別する
* alpha.4実装をこのwork packageへ混入させない

**Exit conditions**

* すべての変更が比較findingへtrace可能である
* critical authority／safety問題が未処理のまま残っていない、または人間が明示的にfield trial停止を決定している
* 必要なnegative fixturesとregression validationが存在する
* manual copy-and-paste経路がfirst-class mechanismとして維持されている
* Core利用またはconformance testingに有料APIが必須化されていない
* field-trial candidateの対象bytes、revisionおよびscopeが固定可能である
* human ownerが`PROCEED_TO_FIELD_TRIAL`または`DO_NOT_PROCEED`を記録する

**Evidence to collect**

* 各findingの再現性
* 修正前後のhuman actions、corrections、unclear next actions
* authority errorとstale-state errorの変化
* Blind First Roundおよびdissent preservationへの影響
* manual workflowでの実行可能性
* regression test結果
* 修正により既存alpha.3 invariantsが弱められていないこと
* 変更scopeがpilot固有の過適合でないことを評価したhuman review

**Principal risks**

* 1回のpilot結果への過適合
* Core Candidateとalpha.3本体の境界混同
* schema migrationを不完全なまま開始する
  -既存の`FACT`表現等を、replacement schema、negative fixtures、migration logicなしに削除する
* scope creepによってformal field trialが継続的に延期される
* compact bundle再生成をrelease evidenceと誤認する
* dynamic role planningへ過大なauthorityを持たせる

**Actions that remain prohibited**

* alpha.4 implementation
* 比較証拠のない機能拡張
* human approval gateの削除または自動化
* dynamic role planによるAI service自動呼出し、human approval、最終判断
* release、tag、publicationまたはdeployment
* field-trial conformanceの事前宣言
* checker PASSによるhuman sign-offの代替
* 有料APIまたは有料orchestrationのCore必須化
* external action

**Condition for proceeding to the next work package**

人間が、固定されたfield-trial candidateについて次を確認した場合に進む。

* 正式field trialを無効化し得る既知のcritical blockerがない
* field-trial scope、観察方法、human rolesおよびstop conditionsが定義されている
* 必要なload report、profile binding、validation receiptおよびraw observation管理を準備できる
* Stage 2で変更が行われた場合、対象bytesとvalidation対象が再固定されている
* `A3-REL-001`を完了する権限を持つhuman ownerがfield trial開始を承認する

---

## Work Package 3 — alpha.3正式field trialとrelease-gate評価

**Objective**

実用時のmanual usability evidenceとhuman sign-offを収集し、`A3-REL-001`の完了可否を人間が判断する。`A3-REL-001`完了後に限り、`A3-REL-005`のfinal-main auditを実施し、alpha.3 release可否を別途判断する。

**Concrete deliverables**

* 完全なFIELD_TRIAL用`PROTOCOL_LOAD_REPORT`
* exact profile bytesに結び付いた`PROFILE_SOURCE_BINDING`
* 対象artifact、schema、hash、executorを結び付けるvalidation receipts
* raw field-trial observation
* repository-relative locatorとhashを含むraw observation inventory
* manual usability observation report
* participantおよびhuman operatorの操作記録
* observed failures、workarounds、dissentおよびunresolved blockers
* `A3-REL-001`用human sign-offまたはnon-completion record
* `A3-REL-001`完了後の`A3-REL-005` final-main audit package
* human release decision record

**Entry conditions**

* Work Package 2のexit conditionsを満たす
* field-trial candidateがexact bytesまたは明確なrevisionへ固定される
* FIELD_TRIAL用load reportとprofile source bindingの作成・検証手順が定義される
* validation receiptのexecutorがtool、deterministic runtimeまたはCIとして識別される
* raw observationsを保存し、hashとrepository-relative referenceへ結び付ける手順がある
* human observer、decision owner、sign-off authorityが明示される
* field-trial startが別途human authorizedである
* formal comparison evidenceとformal release evidenceが別管理される

**Exit conditions**

次のいずれかをhuman ownerが記録する。

1. `A3-REL-001`について、必要なmanual usability evidenceとhuman sign-offがそろった
2. `A3-REL-001`は未完了であり、blockerと再試行条件が記録された

`A3-REL-005`は、1が成立した後にのみ開始する。

その後、final-main audit evidenceを人間がレビューし、次のいずれかを別途記録する。

* release authorized
* release deferred
* release rejected
* additional evidence required

validatorやcheckerのPASSだけではexitしない。

**Evidence to collect**

* 完全なload reportとreport schemaのbinding
* exact start profile bytesとのbinding
* validation receipt本体とreceipt referencesの整合性
* raw observationの完全性とhash
* manual setup、navigation、copy-and-paste、validation、recoveryのusability
* human actions、completion time、error、confusion、workaround
* authority boundaryの理解と維持
* substantive work開始前のgoal confirmationとseparate session start
* revision-bound approvals
* raw ingestion before normalization
* normalizationのhuman confirmation
* dissent visibility
* external executionが行われていないこと
* human sign-offのexact scopeとrevision

**Principal risks**

* comparison artifactをformal field-trial evidenceへ流用する
* incompleteまたはself-attested load reportを受け入れる
* receipt referenceだけがありreceipt artifactが存在しない
* raw observationとprofile bytesのbindingが不足する
* checker PASSをhuman sign-offまたはrelease authorizationと扱う
* `A3-REL-001`完了前に`A3-REL-005`を開始する
* release decisionとexternal execution authorizationを混同する
* field trial中にcandidateを変更し、evidence bindingを失う

**Actions that remain prohibited**

* `A3-REL-001`完了前の`A3-REL-005`開始
* human sign-offなしのrelease authorization
* release、tag、publication、Pages promotionまたはdeployment
* AIによるapprovalまたは最終release判断
* checker PASSだけを根拠とするrelease
* alpha.4 authorizationまたはimplementation
* field-trial evidenceの欠損を推定で補完すること
* external action

**Condition for proceeding beyond this work package**

自動的には次へ進まない。

次のいずれにも別個のhuman decision recordが必要である。

* alpha.3のrelease、tag、publication
* unresolved blockerへの追加修正
* 新たなfield trial
* alpha.4の設計または実装開始
* Core Candidateを正式versionへ取り込むこと

---

### 4. Immediate next PR proposal

**Proposed PR title**

`pilot-001: define frozen four-mode comparison execution and evidence gates`

**Scope**

Codex operatorが、4方式を同じinformation setと固定taskのもとで実行・記録するためのexperiment-control artifactを追加または更新する。

PRは比較結果を作成するものではなく、比較を再現可能かつ監査可能に開始するための実行契約を定義する。

**Filesまたはartifactの種類**

正確なrepository pathは添付情報だけでは確認できないため、次のartifact種類を提案する。

* experiment manifest
* mode別run manifest template
* frozen input inventory
* operator checklist
* Blind First Round exposure record template
* participant correlation／independence register
* raw prompt／response inventory template
* measurement schemaまたはstructured scorecard
* authority and safety issue log
* human evaluation rubric
* comparison synthesis template
* local validator configurationまたはvalidation checklist
* hash manifest
* evidence-status declaration

experiment manifestには少なくとも次を含める。

```yaml
pilot_id: Pilot-001
task_status: FROZEN
modes:
  - MANUAL_MULTI_AI
  - STANDARD_ALPHA3
  - ALPHA3_CORE_CANDIDATE
  - MARKDOWN_VALIDATOR
formal_release_evidence: false
alpha4_authorized: false
human_final_authority: true
external_action_authorized: false
```

実際のID、hash、participant、timingおよびrevisionは、operatorが実測・計算するまでplaceholderまたは`UNKNOWN`とし、推測しない。

**Validation**

* 4つのmode名が固定リストと一致する
* 各modeが同じtask bytesおよびcompact-bundle bytesへbindingされる
* exact UTF-8 bytesからhashを計算する手順が定義される
* primary output freeze前のcross-exposureを禁止する
* raw initial responseの上書きを禁止する
* exposureが不明な場合は`UNKNOWN`を保持する
* independence groupが未確認の場合は推測しない
* 同一model、shared chatまたはshared sourceを独立証拠として数えない
* 比較測定が4方式すべてへ同じ定義で適用される
* validator PASSがhuman approvalにならないことを検査する
* `formal_release_evidence: false`を維持する
* `alpha4_authorized: false`を維持する
* release、merge、publication、deployment、external actionがscope外である
* local validationとmanual copy-and-pasteで実行可能であり、有料APIを必須としない

**Release-gate effect**

`NONE`

このPRが承認・mergeされたとしても、次を意味しない。

* `A3-REL-001`完了
* `A3-REL-005`開始または完了
* formal FIELD_TRIAL evidenceの成立
* alpha.3 release readiness
* `PROTOCOL_LOAD_REPORT.status: COMPLETE`
* alpha.3 release authorization
* alpha.4 authorization

このPRが将来提供し得るのは、実験が実行され、人間が比較可能性を受け入れた場合の**formal comparison evidenceの基盤**のみである。

**Explicit non-goals**

* 4方式の勝者決定
* Core Candidateの正式採用
* Core Candidate、Workflow Macro、compact bundleまたはdynamic role planningの機能追加
* alpha.3 schemaまたはruntimeの変更
* formal field trialの実施
* `A3-REL-001`または`A3-REL-005`の完了
* `PROTOCOL_LOAD_REPORT`の作成済み・COMPLETEという主張
* release、tag、publicationまたはdeployment
* alpha.4設計または実装
* AI serviceの自動呼出し
* human approvalまたは最終判断の自動化
* paid APIまたはpaid orchestrationの必須化
* external action

---

### 5. Alpha.4 disposition

**Selected disposition：`CONSIDER_AFTER_COMPARISON`**

これはalpha.4開始の承認ではない。現時点では引き続き次を維持する。

```yaml
alpha4_authorized: false
alpha4_implementation_status: DEFERRED
```

状態変更の検討に必要な証拠は次のとおりである。

* 4方式の比較可能な実測結果
* participant correlationとBlind First Round状態が追跡可能な比較artifact
* alpha.3またはCore Candidateで反復して発生する問題の記録
* その問題がdocumentation、macro、profileまたは限定的alpha.3修正では十分に解決できない根拠
* version changeのbenefit、migration cost、compatibility impactおよびhuman burden
* authority、evidence、revision、release boundaryへの影響評価
* alpha.3 field-trial／release pathとの競合または依存関係
* unresolved dissentを含むhuman review

必要なhuman decisionは、少なくとも次を明示した別個のdecision recordである。

* alpha.4を開始するか
* design-only、prototype、implementationのどこまでを許可するか
* decision ownerとapprover
* source baseline
* scopeとnon-goals
* required evidence
* stop conditions
* releaseおよびexternal-action境界
* alpha.3との並行作業を許可するか
* authorizationのexact revision

比較結果だけでalpha.4を開始してはならない。比較結果はhuman decisionの入力であり、authorizationそのものではない。

---

### 6. Uncertainty and dissent

#### ファイル読み取り状態

* `task/prompt.md`：全233行を読み取った
* `MADP-v0.3.0-alpha.3-core-compact.md`：全1,732行を読み取った
* 読み取れなかった範囲：なし

ただし、この会話で添付ファイルを読んだことは、正式な`PROTOCOL_LOAD_REPORT`、`status: COMPLETE`、schema validation receipt、FIELD_TRIAL load、field-trial conformanceまたはrelease evidenceを構成しない。

#### 判断に使用できない情報

* 他participantの回答、結論または収束状態
* participant間のindependence group
* 実際のmodel family、shared sourceまたはchat correlation
* 4方式のcompletion time、human action数、error数、品質差
* Codex operator workflowへの具体的authorization record
* scaffold内に存在する可能性がある未提示artifact
* 指定commit以降のrepository状態
* 現在のbranch、PR、CIまたはchecker実行結果
* `A3-REL-001`向けfield-trial packageの準備状況
* human sign-offまたはrelease approval
* 添付外のschema、implementation-status、decision recordまたはmanifestの内容
* compact bundleに含まれないdynamic role planningの詳細
* alpha.4の具体的requirements、migration planまたはcost
* formal comparison evidenceの実在
* formal release evidenceの完成

#### 不足情報

* 共通測定定義と受入threshold
* 方式ごとのrun数
* task順序によるlearning effectを抑える方法
* human burdenを測る評価方法
* evaluatorの選定とblindness
* non-completionの扱い
* participant independence確認方法
* comparison artifactのschemaと保存方法
* Stage 1のtime-box
* Stage 2で修正対象とするseverity threshold
* 正式field trialの対象user、scenario、成功条件およびstop conditions

#### 未確認事実

次は固定情報として提示されていないため、成立を主張しない。

* comparison scaffoldが完全である
* 4方式を直ちに実行できる
* Codexがoperatorとしてauthorization済みである
* validatorが全artifactを検証できる
* Core Candidateがstandard alpha.3より優れている
* field trialが開始可能な状態である
* alpha.3のrelease blockerが`A3-REL-001`以外に存在しない
* `A3-REL-005`が成功する
* alpha.4が必要である
* bundleの全内容が正式protocol loadとして認定されている

#### 本提案で置いた仮定

* 4方式比較を明確にtime-boxできる
* 比較結果をrelease evidenceと混同せず管理できる
* 比較で発見された問題の一部は、alpha.4を開始せず限定的に対処できる
* 正式field trialの前に重大なusability／authority問題を検出する価値が、短い比較実験の遅延を上回る

これらは計画上の仮定であり、確認済み事実ではない。

#### 追加で必要な測定または実験

* 同一task、同一information setによる4方式比較
* 各方式でのcompletion time
* human action数と操作種別
* correction、reformat、recovery回数
* unclear next action件数
* authorityまたはstale-state error件数
* Blind First Round conformance
* raw response preservation
* independent convergenceとcorrelated convergenceの区別
* dissentの保持率
* decision reconstructionの成功度
* evaluator間の評価差
* comparison後の限定的before/after再試験
* 正式field trialにおける実用時manual usability観察

#### 推奨方針に対する最も強い反対論

**最も強い反対論は、正式field trialを最優先すべきだというものである。**

`A3-REL-001`は明確なrelease blockerであり、比較実験はこれを直接完了しない。alpha.3のreleaseを最短で進めることが目的なら、比較を先行させることはrelease-critical evidenceの収集を遅らせる。さらに、Core Candidateは実験的workstreamであり、alpha.3正式field trialはCore Candidate比較結果を必須条件としていない可能性がある。

#### 反対論が正しい場合に方針を変更する条件

次の条件がすべて満たされる場合、最初のwork packageを正式field trialへ変更することが合理的である。

* human ownerがalpha.3 release進捗を比較知識より優先すると明示する
* field-trial candidateが既にexact bytesへ固定されている
* FIELD_TRIAL load report、profile binding、validation receipts、raw observation手順が実行可能な状態である
* human participants、observer、sign-off authorityおよびstop conditionsが確定している
* 既知のcritical authority／safety／usability blockerがない
* 比較を先行しなくてもfield trialが無効化または高確率で再実施にならないとhuman ownerが判断する
* 比較実験を後続または独立並行workstreamとして維持し、formal release evidenceと混同しない

これらが確認された場合の変更案は次のとおりである。

1. 正式alpha.3 field trial
2. 4方式比較実験
3. field-trial結果と比較結果に基づく限定的改善およびversion decision

現時点では、これらの条件が満たされているという情報がないため、初期推奨は変更しない。

---

### 7. Final summary

```yaml
first_priority: FOUR_MODE_CORE_CANDIDATE_COMPARISON_EXPERIMENT
second_priority: EVIDENCE_GATED_ALPHA3_STABILIZATION
third_priority: FORMAL_ALPHA3_FIELD_TRIAL_THEN_A3_REL_005_AUDIT
alpha3_release_status: NOT_AUTHORIZED
alpha4_status: CONSIDER_AFTER_COMPARISON
formal_comparison_evidence_available: false
formal_release_evidence_complete: false
human_decision_required: true
```
