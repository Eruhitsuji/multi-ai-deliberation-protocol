participant_id: CLAUDE-A
model_label: Opus 4.8
prior_participant_outputs_seen: false
external_web_research_used: false
authority: PROPOSE_ONLY

---

## 0. 読み取り範囲の申告（Read-coverage declaration）

以下は本回答の前提となる読み取り状況であり、`PROTOCOL_LOAD_REPORT` でも load report の代替でもありません。本申告は自己申告であり、machine evidence ではありません。

* `task/prompt.md`: 全文読み取り完了。
* `MADP-v0.3.0-alpha.3-core-compact.md`（frontmatter に `source_count: 7`、`formal_release_evidence: false`、`source_commit: 2a29ddf...`）:

| index | path | 読み取り状況 |
|---|---|---|
| 1 | `protocol/MADP-v0.3.0-alpha.3.md` | 全文読み取り |
| 2 | `registries/v0.3.0-alpha.3/commands.yaml` | 部分読み取り。frontmatter・composition・alias policy・command_groups・aliases・先頭 23 command entry を全項目読み取り。残り 28 entry は `command` 名と `default_authority_boundary` のみ確認し、`required_arguments` 等の全項目は未確認。 |
| 3 | `registries/v0.3.0-alpha.3/workflow-macros.yaml` | 全文読み取り |
| 4 | `docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md` | 全文読み取り |
| 5 | `docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md` | 全文読み取り |
| 6 | `docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md` | 全文読み取り |
| 7 | `bootstrap/alpha3/quick-start.md` | 全文読み取り |

* 埋め込み per-file SHA-256 および `source_inventory_sha256` は**再計算していない**（bundle 内の宣言値を読んだだけ）。したがって provenance は `SOURCE_REFERENCED` 相当ですらなく、**未検証**として扱ってください。
* 構造的整合の観察（推測ではなく bundle 内記述の照合）: 継承 alpha.2 command 20 件 + 追加 alpha.3 command 31 件 = 51 件で、protocol 本文の「51 canonical commands」と一致。これは registry 一貫性の弱い示唆であり、conformance 証拠ではありません。
* 本回答は `PROTOCOL_LOAD_REPORT.status: COMPLETE`、formal release evidence、field-trial conformance、alpha.4 authorization のいずれも主張しません。

---

## 1. Recommended decision

**最初に実施する work package: 候補1 — Codex を operator とする 4方式 Core Candidate 比較実験の完了（WP-1）。**

理由（簡潔に）:

1. **既に in-flight であり、中断コストが最も高い。** 比較 pilot 環境は作成済みで、Blind First Round は現に進行中である。Blind First Round profile は「initial response 確定前に prior conclusion が露出した場合は `ANCHORING_EXPOSED` に分類する」と定めており、中断・再開は blind 条件そのものを毀損しうる。他の候補を先に挟むと、この一回性の資産を失う。
2. **限界費用が最小で、reversibility が最も高い。** 有料 API も orchestration も不要で、成果物は `formal_release_evidence: false` / `alpha4_authorized: false` を維持する探索的 artifact に閉じる。誤った結論でも破棄すれば済む。
3. **正式 field trial の失敗コストを事前に下げる。** `A3-REL-001` は実用時 manual usability evidence と human sign-off を要求する高コスト・一回性の手続きである。Core Candidate profile が挙げる測定項目（completion time、human actions、canonical commands、corrections、unclear next actions、authority/stale-state errors、Blind First Round status、dissent preservation、decision reconstruction、user burden）は、field trial で顕在化すれば再実施を強いる類の usability 欠陥を、はるかに安価に先出しできる。
4. **候補3・候補4を正当化する前提が今はまだ存在しない。** 比較実測結果がない状態での Core Candidate 追加改善（候補3）は premature optimization であり、alpha.4 着手（候補4）は明示的な人間の decision record を欠く。

**明示する限界:** WP-1 は release progress を一切生まない。`A3-REL-001` は WP-1 では前進せず、公開 bootstrap は alpha.2 のままである。この点は §6 の最強反対論として扱う。

---

## 2. Alternative comparison

評価は 5 段階の定性ラベル（`VERY_LOW` / `LOW` / `MEDIUM` / `HIGH` / `VERY_HIGH`）による**提案者の主観的見積り**であり、実測値ではない。数値化された測定は存在しないため推測していない。

| 軸 | 候補1 比較実験 | 候補2 field trial → `A3-REL-001` | 候補3 Core等の追加改善 | 候補4 alpha.4 設計/実装準備 | 候補5 段階的組合せ |
|---|---|---|---|---|---|
| release progress | NONE（gate を直接完了しない） | VERY_HIGH（唯一 release blocker を動かす） | NONE | NONE（むしろ後退リスク） | HIGH（順序次第） |
| evidence value | HIGH（comparison evidence として） | VERY_HIGH（formal release evidence として） | LOW（比較前は根拠薄） | VERY_LOW | HIGH |
| human burden | MEDIUM | HIGH（sign-off と observation 記録を伴う） | MEDIUM–HIGH | HIGH | HIGH（総量は最大） |
| authority / safety risk | LOW–MEDIUM（比較結果を release 証拠と誤用するリスク） | MEDIUM（checker PASS を sign-off と誤認するリスク） | LOW | HIGH（暗黙の alpha.4 承認に滑るリスク） | MEDIUM（境界の混線） |
| implementation cost | LOW（環境構築済み） | MEDIUM | MEDIUM–HIGH | VERY_HIGH | HIGH |
| reversibility | VERY_HIGH | MEDIUM（sign-off は取り消しにくい） | MEDIUM（schema 変更は移行負債化） | LOW | MEDIUM |
| dependency on unavailable evidence | LOW（証拠を生成する側） | LOW（独立に実施可能） | VERY_HIGH（比較結果に依存） | VERY_HIGH | MEDIUM |
| risk of premature optimization | LOW | LOW | VERY_HIGH | VERY_HIGH | MEDIUM |

### 候補ごとの利点・欠点・現時点で不足している証拠

**候補1: 4方式比較実験**
* 利点: 環境が既存で限界費用が低い。Blind First Round の一回性を活かせる。usability 欠陥を安価に先出しできる。`formal_release_evidence: false` を保ったまま実施でき authority 境界を侵さない。
* 欠点: release blocker を一切動かさない。公開 bootstrap は alpha.2 のまま滞留。実験が自己目的化する drift リスク。4方式の operator 条件を揃えないと比較不能な artifact だけが増える。
* 不足証拠: 4方式の実測値そのもの（存在しない）。参加者の independence group と correlation の確定情報。各方式の運用条件の等価性。測定の再現手順が確定しているか。

**候補2: 正式 field trial → `A3-REL-001`**
* 利点: 唯一 release gate を前進させる。`A3-REL-001` 完了が `A3-REL-005`（final-main audit）の entry condition であり、この順序は不可逆な依存関係として正しい。alpha.2 → alpha.3 の公開 bootstrap 更新経路を開く。
* 欠点: human burden が最大で、実施中の usability 欠陥発見が再実施を招く。sign-off は取り消しにくく reversibility が低い。VERIFIED/FIELD_TRIAL load report は `schema_validation_records`、receipt、独立再計算可能性を要求するため準備が重い。
* 不足証拠: field trial の実施計画・観測記録様式が確定しているか。validation receipt executor（tool / deterministic runtime / CI）が稼働可能か。sign-off を行う named human が確定しているか。これらはいずれも与えられておらず、推測しない。

**候補3: Core Candidate / Macro / compact bundle / dynamic role planning の追加改善**
* 利点: 既知の設計課題（`claim_candidate` への移行、dissent 表現など）を前進させられる。
* 欠点: **比較結果が存在しない現時点では改善方向を正当化できない。** Core Candidate profile 自身が「既存 alpha.3 `FACT` 表現の削除許可ではない。置換 schema、negative fixture、移行ロジック、安全不変条件テストが揃うまで既存 field を維持する」と定めており、先行改善は移行負債を増やす。premature optimization リスクが最大級。
* 不足証拠: どの方式のどの操作が実際に負担・誤りを生んだかの実測。compact bundle が実際に読み込まれたかの独立した証拠（bundle の存在は ingestion の証拠ではない）。

**候補4: alpha.4 設計検討 / 実装準備**
* 利点: 長期的な構造整理の先取り。
* 欠点: 前提となる比較証拠と人間評価が両方欠落。alpha.4 は明示的に `DEFERRED` であり、着手には別個の human decision record が必要。準備行為が暗黙の承認として解釈される authority リスクが最も高い。
* 不足証拠: 比較証拠一式、その人間評価、alpha.4 を要する具体的欠陥の同定、明示的 decision record。いずれも存在しない。

**候補5: 段階的組合せ**
* 利点: 本提案（WP-1 → WP-2 → WP-3）は実質これに該当する。証拠経路を分離したまま順序付けられる。
* 欠点: 総人的負担が最大。段階間の境界を厳密に管理しないと、comparison evidence と release evidence が混線する。
* 不足証拠: 人間側に確保可能な時間・回数の見積り（不明であり推測しない）。

---

## 3. Three-stage roadmap

### WP-1: 4方式 Core Candidate 比較実験の完了と comparison evidence の確定

* **objective**: `MANUAL_MULTI_AI` / `STANDARD_ALPHA3` / `ALPHA3_CORE_CANDIDATE` / `MARKDOWN_VALIDATOR` の 4方式について、比較可能な形式で観測記録を取得・固定し、人間評価に足る comparison evidence を作る。release gate は動かさない。
* **concrete deliverables**:
  * 凍結された information set（`task/prompt.md`）の SHA-256 と `experiment.yaml` への記録。
  * 4方式それぞれの raw prompt / raw response の保全記録（正規化前）。
  * participant / correlation register（model family、chat context、independence group、`exposure.state`）。
  * 測定記録（Core Candidate profile の comparative evaluation 項目に対応）。
  * `core_candidate_conformance` 報告（`CONFORMING` / `DEGRADED` / `NONCONFORMING` / `NOT_EVALUATED` と reasons）。
  * comparison evidence summary（`formal_release_evidence: false`、`alpha4_authorized: false` を明記）。
* **entry conditions**: pilot 環境が存在すること（充足済みと供給されている）。information set が `FROZEN` であること。operator 権限が別途承認された範囲に限定されていること。
* **exit conditions**: 4方式すべての raw 記録と測定記録が保全され、independence / correlation と `exposure.state` が記録され（不明なものは `UNKNOWN` のまま）、人間が comparison evidence summary をレビューしたことが記録されている。
* **evidence to collect**: completion time、human actions、canonical command 呼出、corrections、unclear next actions、authority error、stale-state error、Blind First Round status、dissent preservation、decision reconstruction 可否、user burden。加えて各 run の未読・未検証範囲の申告。
* **principal risks**: (a) blind 条件の破綻（`ANCHORING_EXPOSED`）、(b) correlated participant の一致を independent convergence と誤認、(c) comparison evidence の release evidence への誤用、(d) 4方式の運用条件不揃いによる比較不能、(e) compact bundle 添付を ingestion 証拠と誤認。
* **actions that remain prohibited**: release、tag、publication、Pages promotion、deployment、merge、field-trial sign-off、alpha.4 authorization、`A3-REL-001` の完了宣言、`formal_release_evidence: true` への変更、checker PASS の human approval への読み替え、有料 API / 自動 orchestration の必須化。
* **condition for proceeding to WP-2**: comparison run が終了し raw 記録が凍結されていること。かつ **WP-2 は WP-1 の結論に依存しない** — WP-1 の完了（結論の内容ではなく手続きの終了）だけが WP-2 の開始条件である。両者は独立した evidence path である。

### WP-2: alpha.3 正式 field trial と `A3-REL-001` の完了、続く `A3-REL-005` の準備

* **objective**: 実用条件下の manual usability evidence を取得し、named human による sign-off をもって `A3-REL-001` の完了を目指す。その後 `A3-REL-005`（final-main audit）の entry を満たす。
* **concrete deliverables**: FIELD_TRIAL 相当の `PROTOCOL_LOAD_REPORT`（`MADP-PROTOCOL-LOAD-REPORT-v2`、`all_required_files_read: true`、`inferred_unread_content: false`）と `PROFILE_SOURCE_BINDING`；`schema_validation_records` と対応する `VALIDATION_RECEIPT` 実体；validation evidence manifest（command、result、return code、checker hash、input/output hashes）；raw observation inventory と repository-relative file hash；human sign-off 記録。
* **entry conditions**: WP-1 の run が終了し記録が凍結されている。receipt executor（tool / deterministic runtime / CI）が利用可能。sign-off を行う named human が確定している。**現時点でこれらの充足状況は与えられておらず、充足していると仮定しない。**
* **exit conditions**: `A3-REL-001` が human sign-off をもって完了記録されている。receipt 参照と receipt 実体が対応し、独立に再計算可能である。`A3-REL-005` の entry condition が満たされている。
* **evidence to collect**: 実用時 usability 観測、schema validation 記録、receipt、evidence manifest、未実行チェックの明示的限界記述。
* **principal risks**: (a) checker PASS を sign-off と誤認、(b) receipt 参照だけで receipt 実体を欠く「構造的にはもっともらしいが束縛されていない」証拠、(c) 抜粋表示を schema-valid と主張、(d) WP-1 の comparison 記録を release evidence に流用、(e) implementation-status ファイルの自己申告を証拠と誤認。
* **actions that remain prohibited**: `A3-REL-005` の `A3-REL-001` 完了前実施、tag / publication / deployment、alpha.4 authorization、comparison evidence による release blocker の完了。
* **condition for proceeding to WP-3**: `A3-REL-001` の human sign-off が記録され、`A3-REL-005` の disposition（実施済み／実施予定）が明確であること。かつ WP-1 の comparison evidence を人間が評価済みであること。

### WP-3: 比較証拠に基づく Core Candidate 系改善と alpha.4 disposition の decision record 作成

* **objective**: WP-1 の実測に裏づけられた範囲でのみ Core Candidate Profile / Workflow Macro / compact bundle / dynamic role planning を改善し、同時に alpha.4 の可否を人間の decision record として明文化する（承認ではなく判断の記録）。
* **concrete deliverables**: 実測欠陥に紐づいた改善提案リスト（各項目に対応する観測 ID を付す）；`claim_candidate` 等の移行を行う場合は置換 schema・negative fixture・移行ロジック・安全不変条件テストを揃えた提案；alpha.4 に関する human decision record（承認・却下・継続 defer のいずれか）。
* **entry conditions**: WP-1 の comparison evidence が人間評価済み。WP-2 の `A3-REL-001` が完了済み。改善提案の各項目が特定の観測に紐づいていること。
* **exit conditions**: 各改善が観測根拠つきで採否記録されている。alpha.4 disposition が明示的 decision record として存在する。既存 alpha.3 表現の削除を伴う変更は、移行資材が揃わない限り行われていない。
* **evidence to collect**: 改善前後の再測定（可能な場合）、移行安全性テスト結果、alpha.4 を要すると主張する欠陥の具体的同定。
* **principal risks**: (a) 観測に紐づかない「感触ベース」の改善、(b) 既存 `FACT` 表現の早期削除による移行負債、(c) 改善作業が事実上の alpha.4 実装に滑る、(d) decision record 作成を authorization と混同。
* **condition for proceeding**: 本 roadmap の範囲はここまで。以降は別の human decision record の管轄。

---

## 4. Immediate next PR proposal

以下は**提案のみ**であり、コード作成・commit・merge・release 操作は行っていない。

* **proposed PR title**:
  `docs(experiment): add pilot-001 comparison evidence recording templates and independence register (no results)`

* **scope**:
  1. 4方式共通の観測記録テンプレート（測定項目、記録単位、未測定時の `UNKNOWN` 記法を含む）。
  2. participant / correlation register テンプレート（participant_id、model_label、provider、chat context、independence_group、correlation notes、`exposure.state`、`exposed_response_refs`）。
  3. `core_candidate_conformance` 報告テンプレート（`status` と `reasons`）。
  4. read-coverage / 未検証範囲の申告テンプレート（本回答 §0 に相当する様式）。
  5. `experiment.yaml` への information-set digest 記録欄の追加（**digest 値そのものは人間または承認済み operator workflow が記入**）。
  6. 各テンプレート frontmatter に `formal_release_evidence: false` と `alpha4_authorized: false` を固定値として記載。

* **files または artifact の種類**: Markdown テンプレート、YAML テンプレート、実験メタデータ YAML の欄追加。**protocol 本体、command registry、schema、bootstrap、既存 profile は変更しない。**

* **validation**: local Markdown / YAML 構文検証と、該当する場合の schema 検証。実行した検証コマンドと結果を PR 記述に残す。検証未実行の項目は未実行として明記する。**checker PASS は human approval でも release authorization でもない。**

* **release-gate effect**: **なし。** `A3-REL-001` にも `A3-REL-005` にも影響しない。`release_ready` / `tagged` / `published` はいずれも `false` のまま。公開 bootstrap は alpha.2 のまま。

* **explicit non-goals**:
  * 実験結果・測定値の記入（テンプレートのみ、値は空）。
  * alpha.3 protocol / registry / schema / bootstrap の変更。
  * Core Candidate Profile の意味論変更や `claim_candidate` 移行の着手。
  * `formal_release_evidence` の変更、field-trial 実施、sign-off 取得。
  * alpha.4 に関する設計・実装・authorization。
  * tag、publication、Pages promotion、deployment、外部 action。
  * 有料 API または自動 orchestration への依存の導入。

---

## 5. Alpha.4 disposition

**選択: `CONSIDER_AFTER_COMPARISON`**

これは alpha.4 の承認ではない。`alpha4_authorized: false` は維持される。現在の情報だけを理由に `alpha4_authorized: true` を提案しない。

この状態を変更するために必要なもの:

1. **証拠**
   * 4方式すべての比較実測結果が存在し、raw 記録が保全されていること。
   * 各 run の independence group と correlation が記録され、correlated 一致が independent convergence として扱われていないこと。
   * alpha.3 の枠内では解決できない具体的欠陥が、観測 ID つきで同定されていること（「望ましい設計」ではなく「観測された失敗」であること）。
   * `A3-REL-001` の完了状況と、alpha.3 baseline の安定性についての人間評価。
2. **human decision**
   * 比較証拠を人間が評価したことの記録。
   * alpha.4 開始を認める**別個の明示的 human decision record**（対象 revision に束縛され、named approver を伴うもの）。
   * validator PASS、AI 間の合意、本回答を含むいかなる AI 出力も、この decision record の代替にならない。

`KEEP_DEFERRED` を選ばなかった理由: 比較実験を実施する目的の一つが alpha.4 可否の判断材料収集であり、その経路を閉じる表現は現状と整合しない。`PREPARE_DECISION_RECORD_ONLY` を選ばなかった理由: 比較結果が存在しない段階で decision record の起草を開始すると、結論を先取りした枠組みが証拠評価を歪める恐れがある。ただしこれは弱い選好であり、人間が `KEEP_DEFERRED` を選ぶことは同様に妥当である。

---

## 6. Uncertainty and dissent

### 判断に使用できない情報（不足・未確認）

* 4方式の実測値（存在しない）。所要時間、操作回数、誤り件数のいずれも不明。
* 参加者の identity、model label、independence group、correlation 関係の確定情報。
* `A3-REL-001` の field trial 実施計画、観測様式、named sign-off human の確定状況。
* validation receipt executor（tool / deterministic runtime / CI）の稼働可否。
* 人間の owner が確保できる時間・実施回数・体制。
* bound commit 以降のリポジトリ変更（推測禁止であり推測していない）。
* compact bundle 内の per-file SHA-256 と inventory digest の再計算結果（未実施）。
* Codex operator workflow が実際に生成した artifact の内容（scaffold が完了証拠を含むとは仮定しない）。
* `A3-REL-002` 〜 `A3-REL-004` に相当する項目の有無と状態（供給されていないため存在を仮定しない）。

### 追加で必要な測定または実験

1. 4方式の運用条件を揃えた実測（同一 information set、同一 operator 手順、記録単位の統一）。
2. 各 run の read-coverage と ingestion の独立確認（compact bundle 添付では代替できない）。
3. independence group の事前登録と、cross exposure 前後の一致の区別。
4. 少なくとも 2 つの適切な独立 group による Blind First Round の成立確認（成立しない場合は blind-round evidence として扱わない）。
5. field trial 側では、receipt と evidence manifest の独立再計算テスト。

### 推奨方針に対する最も強い反対論

**「比較実験を先に置くのは、release を無期限に遅らせる実験主義である」。**

具体的には次の主張が成り立つ:

* `A3-REL-001` は唯一の release blocker であり、比較実験はそれを一切前進させない。公開 bootstrap が alpha.2 に留まる期間が延び、alpha.3 実装と公開状態の乖離が拡大する。
* 比較実験は Core Candidate という**実験的 workstream**の評価であって、alpha.3 の release 適格性の評価ではない。release 判断に必要な証拠は field trial からしか得られない。
* 「比較で usability 欠陥を先出しできる」という私の論拠は**未検証の仮説**である。比較実験の測定対象と field trial が要求する manual usability evidence が実際にどの程度重なるかは、実測がない以上不明である。重ならなければ、WP-1 は純粋な遅延にしかならない。
* 人間の可処分時間が限られている場合、WP-1 の消費分だけ WP-2 の質が下がる。人的資源は共有資源であり、「限界費用が低い」は総量制約の下では成立しない。

この反対論は妥当であり、実測がない現時点では私の推奨より優れている可能性がある。

### 反対論が正しい場合に方針を変更する条件（switch conditions）

次のいずれかが成り立つ場合、**WP-1 と WP-2 の順序を入れ替え、候補2 を最初の work package とすることを推奨する**:

1. 人間 owner が alpha.3 の公開を近い時期の目標として明示している場合。
2. field trial の実施体制（named sign-off human、receipt executor、観測様式）が既に整っており、待機コストが発生する場合。
3. 比較実験の完了に必要な追加人的コストが、field trial 1 回分と同等以上と見積もられる場合。
4. 比較実験の測定項目が `A3-REL-001` の要求する manual usability evidence とほとんど重複しないことが確認された場合。
5. alpha.2 のまま公開が続くことによる利用者側の実害（誤った版の参照など）が観測された場合。

逆に、次の場合は WP-1 先行を維持すべきである:

1. Blind First Round が既に進行中で、中断が `ANCHORING_EXPOSED` を招く場合（**現在これに該当すると私は理解している**）。
2. field trial の前提資材（receipt executor、sign-off human）が未整備で、いずれにせよ即時開始できない場合。
3. alpha.3 の manual usability に未解決の疑義があり、field trial 中の発覚が再実施を招く蓋然性が高い場合。

---

## 7. Final summary

```yaml
first_priority: WP-1 Complete the four-workflow Core Candidate comparison experiment and freeze comparison evidence
second_priority: WP-2 Conduct the formal alpha.3 field trial to complete A3-REL-001, then satisfy A3-REL-005 entry
third_priority: WP-3 Evidence-backed Core Candidate improvements and an explicit human decision record on alpha.4
alpha3_release_status: NOT_AUTHORIZED
alpha4_status: CONSIDER_AFTER_COMPARISON
formal_comparison_evidence_available: false
formal_release_evidence_complete: false
human_decision_required: true
```

---

**Authority statement**: 本出力は提案のみ（`PROPOSE_ONLY`）である。承認、release、tag、publication、deployment、merge、field-trial sign-off、alpha.4 authorization のいずれも行っていない。最終的な roadmap の選択は、4方式すべての結果をレビューした後の human owner に属する。
