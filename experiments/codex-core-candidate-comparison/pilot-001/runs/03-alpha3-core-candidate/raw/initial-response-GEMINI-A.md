```yaml
participant_id: GEMINI-A
model_label: 3.1 Pro
prior_participant_outputs_seen: false
external_web_research_used: false
authority: PROPOSE_ONLY

```

添付された共通情報セット（`task/prompt.md` および `MADP-v0.3.0-alpha.3-core-compact.md`）の全範囲を完全に読み取りました [source: 1, 2]。読み取れなかった範囲はありません。本提案では、既知の事実、現時点で不足している情報、未確認の事実、および仮定を厳格に区別し、推測や想定に基づく回答の誘導を排除して独立した提案を行います [source: 1]。

---

### 1. Recommended decision

**最初に実施すべき最優先 work package：Codexをoperatorとして使用する4方式のCore Candidate比較実験の実施と完了**

**選定理由：**
現時点では、4方式（`MANUAL_MULTI_AI`, `STANDARD_ALPHA3`, `ALPHA3_CORE_CANDIDATE`, `MARKDOWN_VALIDATOR`）を比較するpilot環境が構築されているのみであり、実測による比較結果や証拠はまだ存在していません [source: 1]。Core Candidate Profileは、標準のalpha.3、手動比較、およびMarkdown+validatorワークフローとの比較評価を通じて、作業時間、人的負担、権限・状態エラー、Blind First Roundのステータスなどを測定することを明示的に要求しています [source: 2]。
この比較結果（formal comparison evidence）を得る前に、Core Candidateの追加改善を行うことは客観的な根拠を欠く時期尚早な最適化（premature optimization）となります [source: 1]。また、比較実験の結果が存在しない段階でalpha.3の正式なfield trial（`A3-REL-001`）やalpha.4の検討へと進むことは、実験的証拠と正式なリリース証拠の混同を招き、Human Final Authorityによる適切な開発方針の判断を妨げるリスクがあります [source: 1, 2]。したがって、まずは比較実験を完了し、比較可能な証拠を収集することが唯一の論理的かつ安全な着手点です [source: 1, 2]。

---

### 2. Alternative comparison

次の比較表は、提示された主要候補を8つの必須評価軸および現在の証拠状況に基づいて比較したものです [source: 1]。

| 評価軸 | 1. 4方式のCore Candidate比較実験の実施 (推奨) | 2. alpha.3正式field trial (`A3-REL-001`完了目指す) | 3. Core Candidate等の追加改善 | 4. alpha.4設計検討・実装準備の開始 |
| --- | --- | --- | --- | --- |
| **release progress** | 直接的なalpha.3リリース要件の充足にはならない [source: 1]。リリース判断の前提となる評価データを提供する [source: 1, 2]。 | `A3-REL-001`の完了に直接寄与し、リリースへの直接的な進捗となる [source: 1]。 | リリース要件に直接寄与しない [source: 1]。未検証機能の追加による遅延リスクがある [source: 1]。 | alpha.3のリリースには寄与せず、現在`DEFERRED`の次期方針に分岐する [source: 1]。 |
| **evidence value** | 4方式の効率、負担、安全性に関する客観的な実測比較データが得られる [source: 1, 2]。 | 実用時の手動操作性に関する証明（manual usability evidence）が得られる [source: 1]。 | 実証データがないまま変更するため、証拠としての価値は低い [source: 1]。 | 比較証拠なしに検討されるため、方針決定の根拠証拠としては機能しない [source: 1]。 |
| **human burden** | 4方式それぞれのオペレーションおよび結果の評価を行う人的負担が発生する [source: 1, 2]。 | 実環境での運用および手動承認（human sign-off）を行う重い人的負担が発生する [source: 1]。 | 仕様決定やコードレビューの負担が生じる [source: 1]。検証負担が将来に先送りされる [source: 1]。 | 新たな設計決定レコード作成やレビューの負担が人間に発生する [source: 1]。 |
| **authority and safety risk** | AIは`PROPOSE_ONLY`を維持し、Codexもoperatorの範囲内に留まるため低リスクである [source: 1]。 | 早期運用による不具合リスクがあるが、Human Final Authorityにより統制される [source: 1, 2]。 | 実証なしの改善により、権限境界やスキーマ不変条件を破壊するリスクがある [source: 1, 2]。 | 比較証拠なしにalpha.4へ進む権限越権リスクを伴う [source: 1]。 |
| **implementation cost** | 実験環境（scaffold）が既に存在するため、追加の実装コストは低い [source: 1]。 | 正式な環境構築、証拠収集、および監査対応のコストが必要となる [source: 1, 2]。 | 機能追加・修正のためのエンジニアリングコストが直接発生する [source: 1]。 | 設計・新規実装・移行のための非常に高いエンジニアリングコストが発生する [source: 1]。 |
| **reversibility** | 純粋な実験・評価タスクであるため、完全に可逆である [source: 1, 2]。 | 実施自体は可逆だが、得られた承認の取り消しには判断のやり直しを伴う [source: 1]。 | コードの変更を伴うため、差し戻しのコストとリポジトリ汚染のリスクがある [source: 1]。 | バージョンの分岐や設計の混迷を招き、差し戻しのコストが極めて高い [source: 1]。 |
| **dependency on unavailable evidence** | 不足している証拠への依存はなく、実験の実施自体が目的である [source: 1]。 | Core Candidateなどの実験的成果物の評価結果が未定の状態で進むことになる [source: 1]。 | 「改善が必要である」という未計測の仮定（不在の比較結果）に強く依存する [source: 1]。 | 「4方式の比較評価結果」という現在完全に不在の証拠に依存している [source: 1]。 |
| **risk of premature optimization** | 計測と評価を目的とするため、時期尚早な最適化のリスクはない [source: 1, 2]。 | 比較評価を飛ばすことで、最適なワークフローを見落とすリスクがある [source: 1, 2]。 | データなき改善であり、時期尚早な最適化の典型的なリスクを負う [source: 1]。 | 根拠なき次期バージョンへの跳躍であり、極めて高い最適化誤認リスクを伴う [source: 1]。 |

#### 各候補の利点・欠点・現時点で不足している証拠

* **候補1（比較実験の実施）：**
* **利点**：実測データに基づいて人間が客観的な方針決定（alpha.3の移行やCore改善の要否）を行えること [source: 1, 2]。安全なsandbox内で運用課題を抽出できること [source: 1, 2]。
* **欠点**：この実験だけでは`A3-REL-001`完了やリリース承認には直接結びつかないこと [source: 1]。
* **不足している証拠**：4方式それぞれの完了時間、操作数、エラー率、Blind First Roundの有効性などの実測比較証拠 [source: 1, 2]。


* **候補2（alpha.3正式field trial）：**
* **利点**：alpha.3のリリース要件である`A3-REL-001`の直接的な完了を目指せること [source: 1]。
* **欠点**：Core Candidate等との効率比較がないまま手動運用試験を進めるため、負担の大きな手順を固定化する懸念があること [source: 1, 2]。
* **不足している証拠**：正式な運用環境における実用時の手動操作性に関する証拠（manual usability evidence）および人間の承認（human sign-off）[source: 1]。


* **候補3（Core Candidate等の追加改善）：**
* **利点**：機能強化やプロファイルの洗練が理論上可能になること [source: 1]。
* **欠点**：実測データによる正当化なしに変更を行うため、複雑性を増すだけの時期尚早な最適化となること [source: 1]。
* **不足している証拠**：現在のCore CandidateやWorkflow Macroが「どこにボトルネックを持ち、何が不足しているか」を示す比較実験の測定結果 [source: 1, 2]。


* **候補4（alpha.4設計・実装準備）：**
* **利点**：次期プロトコルの検討を早期に開始できること [source: 1]。
* **欠点**：alpha.4の独立実装は現在`DEFERRED`であり、人間による評価と決定レコードなしに開始することは原則に反すること [source: 1]。
* **不足している証拠**：alpha.4への移行を正当化するための「4方式の比較可能な証拠」および人間による明示的な決定レコード [source: 1]。



---

### 3. Three-stage roadmap

以下の3つの主要 work package は、実験的比較から正式評価、そして最終監査へと至る厳密な順序付けに従っています [source: 1, 2]。

#### Work Package 1: Core Candidate 4方式比較実験の実施と評価

* **Objective**：Codexをoperatorとして使用し、4方式（`MANUAL_MULTI_AI`, `STANDARD_ALPHA3`, `ALPHA3_CORE_CANDIDATE`, `MARKDOWN_VALIDATOR`）の客観的なパフォーマンスおよび人的負担の比較証拠を収集する [source: 1, 2]。
* **Concrete deliverables**：
* 4方式すべての実行ログおよびハッシュ化された実験記録 [source: 1, 2]。
* 比較メトリクス（所要時間、コマンド数、エラー数、Blind First Round保持状況）をまとめた評価レポート [source: 1, 2]。


* **Entry conditions**：
* Pilot比較環境およびCodex operator scaffoldが正常に構築されていること [source: 1]。
* タスクステータスが `FROZEN` であること [source: 1]。


* **Exit conditions**：
* 4方式それぞれの実験実行が完了し、アーティファクトが収集・ハッシュ検証されていること [source: 1, 2]。
* 人間（human owner）が全4ワークフローの結果をレビューし、比較証拠を評価していること [source: 1]。


* **Evidence to collect**：
* 完了時間、人間の介入アクション数、正規コマンド発行数、訂正数 [source: 2]。
* 権限エラーおよび古い状態（stale state）エラーの発生頻度 [source: 2]。
* Blind First Roundのステータス（アンカリングの有無、独立性の保持）および反対意見（dissent）の保存状態 [source: 2]。


* **Principal risks**：
* 同じモデルファミリや共有チャットに由来する相関のある回答を、独立した収束（independent convergence）と誤認するリスク [source: 1, 2]。
* 実験結果（formal comparison evidence）を、正式なリリース証拠（formal release evidence）と混同して取り扱うリスク [source: 1]。


* **Actions that remain prohibited**：
* 実験結果のみを理由とした `A3-REL-001` の完了表明 [source: 1]。
* `alpha4_authorized: true` の主張や、alpha.4実装の開始 [source: 1]。
* AIまたはCodexによる自動承認、マージ、リリース、または外部アクションの実行 [source: 1]。


* **Condition for proceeding to the next work package**：
* 人間が4方式の比較結果を評価し、alpha.3の正式field trialで採用すべき運用構成を決定した上で、次段階への移行を明示的に承認すること [source: 1, 2]。



#### Work Package 2: alpha.3正式Field Trialの実施 (`A3-REL-001`の完了)

* **Objective**：Work Package 1の知見を取り入れたalpha.3の正式な実地試験（field trial）を実施し、実用時の手動操作性に関する証拠を収集して `A3-REL-001` を完了する [source: 1, 2]。
* **Concrete deliverables**：
* 実環境でのセッション記録、ロードレポート、検証レシート（`VALIDATION_RECEIPT`）、およびスキーマ検証記録 [source: 2]。
* `A3-REL-001` 完了要件を満たす実用時の手動操作性証拠（manual usability evidence）および人間による署名（human sign-off）[source: 1, 2]。


* **Entry conditions**：
* Work Package 1 が完了し、人間により評価されていること [source: 1]。
* 正式な field trial のための環境および検証ツールが準備されていること [source: 1, 2]。


* **Exit conditions**：
* すべての必須スキーマ検証およびランタイムシーケンス検証が PASS していること [source: 2]。
* 人間による実用性の確認および明示的な sign-off が記録され、`A3-REL-001` が完了ステータスになること [source: 1, 2]。


* **Evidence to collect**：
* `goal-confirm` から `session-start` への正しいシーケンス検証記録 [source: 2]。
* 正規コマンド（`response-ingest`, `response-normalize`, `minutes-approve` 等）による変更不可逆性および権限境界の順守記録 [source: 2]。
* ツールまたは決定論的ランタイムが生成したハッシュバインド済みの検証レシート（`VALIDATION_RECEIPT`）[source: 2]。


* **Principal risks**：
* チェッカーの PASS やモデルの自己評価（self-assessment）を、人間の承認やリリース許可と誤認するリスク [source: 1, 2]。
* 検証未実行のソースがあるにもかかわらず、状態を VERIFIED または ASSURED と不当に表明するリスク [source: 2]。


* **Actions that remain prohibited**：
* alpha.3の正式リリース（tagging, publishing, Pages promotion）の実行 [source: 1]。
* 有料APIや有料自動orchestrationサービスをCoreの必須条件とすること [source: 1]。
* 人間の最終承認なしに行われるあらゆる外部システムへの自動反映 [source: 1]。


* **Condition for proceeding to the next work package**：
* `A3-REL-001` の要件である manual usability evidence と human sign-off が完全に揃い、次の監査タスク（`A3-REL-005`）への移行が許可されること [source: 1]。



#### Work Package 3: 最終 main 監査 (`A3-REL-005`) とリリース承認判定

* **Objective**：`A3-REL-001` 完了後のメインブランチに対する最終監査（`A3-REL-005`）を実施し、人間が alpha.3 の正式リリース承認、または alpha.4 への移行方針を最終決定する [source: 1, 2]。
* **Concrete deliverables**：
* `A3-REL-005` 最終 main 監査レポート（検証証拠マニフェストと現行スクリプトの照合結果）[source: 1, 2]。
* 人間の最終権限者による正式なリリース承認決定レコード、または alpha.4 開始のための決定レコード [source: 1, 2]。


* **Entry conditions**：
* `A3-REL-001` が正式に完了していること [source: 1]。
* すべてのリリースブロッカーが解消され、監査対象の main ブランチが確定していること [source: 1, 2]。


* **Exit conditions**：
* `A3-REL-005` 監査が正常に完了し、人間の権限者による方針決定（リリース実行または deferred 状態の変更）が記録されること [source: 1, 2]。


* **Evidence to collect**：
* evidence runner によって独立して再計算・検証された完全なロードレポート、プロファイルバインディング、および検証レシートのリンク [source: 2]。
* 既知の制限事項（検証が完全に実行されなかった翻訳やファイルがある場合の明示的な記録）[source: 2]。


* **Principal risks**：
* 監査完了前に誤って自動デプロイやタグ付けがトリガーされる権限違反リスク [source: 1]。
* 過去の experimental baseline との互換性破壊を見落とすリスク [source: 1, 2]。


* **Actions that remain prohibited**：
* AI単独での `release_ready: true` 変更、タグ付け、公開、デプロイ [source: 1]。
* 人間の明示的な決定レコードなしに行われる `alpha4_authorized: true` への変更 [source: 1]。


* **Condition for proceeding to the next work package**：
* 本 work package の完了により、人間による最終的な release action（alpha.3の公開）、または次期サイクル（alpha.4）の正式スタートという外部アクションへ移る [source: 1, 2]。



---

### 4. Immediate next PR proposal

Work Package 1（4方式比較実験）を安全かつ迅速に開始するため、以下の独立した初期提案（PR）を作成します [source: 1]。本提案はコードやリポジトリの操作を伴わない純粋な提案です [source: 1]。

* **proposed PR title**：
`test(pilot-001): add core candidate comparison experiment metrics schema and evaluation documentation`
* **scope**：
* Codex が operator として4方式の実験結果（時間、人的アクション数、コマンド数、エラー頻度、Blind First Roundステータス等）を記録・収集するための JSON/YAML スキーマの追加 [source: 1, 2]。
* 人間が比較証拠を評価するための基準とチェックリストを定めた評価ガイドドキュメント（Markdown）の追加 [source: 1, 2]。


* **files または artifact の種類**：
* `tests/pilot-001/schemas/comparison-metrics.schema.yaml` (実験評価メトリクス用スキーマ) [source: 1, 2]
* `tests/pilot-001/docs/evaluation-guide.md` (4方式比較評価ガイドおよび手順書) [source: 1, 2]


* **validation**：
* 追加されたスキーマ自体が有効な YAML/JSON Schema であり、テスト用のモックデータ（ダミーの実験結果フィクスチャ）に対して既存のローカルバリデータ（有料API不使用）で正しく PASS / REJECT を判定できることを検証する [source: 1, 2]。


* **release-gate effect**：
* **影響なし（None）**。本PRは実験用環境（scaffold）およびドキュメントへの追加であり、alpha.3 のリリースブロッカーである `A3-REL-001` や `A3-REL-005` の完了には一切影響しない [source: 1]。
* すべてのアーティファクトは `formal_release_evidence: false` および `alpha4_authorized: false` を維持する [source: 1]。


* **explicit non-goals**：
* MADP v0.3.0-alpha.3 の規範的（normative）プロトコルやコマンドレジストリの変更 [source: 1, 2]。
* alpha.3 の正式 field trial の完了や `A3-REL-001` の要件充足 [source: 1]。
* alpha.4 の実装準備、設計検討、または `alpha4_authorized: true` の許可 [source: 1]。
* 自動マージ、タグ付け、外部サービス連携、または公開等の外部アクション [source: 1]。



---

### 5. Alpha.4 disposition

**選択したステータス：`CONSIDER_AFTER_COMPARISON**`

**選定理由：**
現在のプロジェクト状態において、alpha.4の独立実装は明示的に `DEFERRED` とされています [source: 1]。ルール上、「alpha.4開始を検討する前に、4方式について比較可能な証拠を収集し、人間が評価する必要がある」と定められており、現時点の情報だけで `alpha4_authorized: true` を提案することは厳しく禁止されています [source: 1]。したがって、比較実験による証拠収集が完了した後に検討を行う `CONSIDER_AFTER_COMPARISON` が最適な配置（disposition）となります [source: 1]。

**ステータスを変更するために必要な証拠と human decision：**

1. **必要な証拠**：Work Package 1 における 4方式（`MANUAL_MULTI_AI`, `STANDARD_ALPHA3`, `ALPHA3_CORE_CANDIDATE`, `MARKDOWN_VALIDATOR`）の完了時間、人的負担、エラー率、盲目性保持等に関する客観的な実測比較結果（formal comparison evidence）[source: 1, 2]。
2. **必要な human decision**：人間（human owner）が上記比較証拠を評価し、現行の alpha.3 路線ではなく alpha.4 の設計・実装へ進むべきであると合意し、その旨を記録した明示的な「人間による決定レコード（human decision record）」を作成して承認すること [source: 1]。

---

### 6. Uncertainty and dissent

本提案を行うにあたり、以下の不確実性、判断限界、および反対論を明示します [source: 1]。

* **判断に使用できない情報**：
* 4方式の各ワークフローにおける実際の所要時間、人的介入回数、およびエラー発生率の実測値（環境は存在するが実験は未実施のため）[source: 1, 2]。
* 比較実験環境における各 AI モデルおよびチャットコンテキスト間の完全な独立性グループの状況（相関の有無の詳細データ）[source: 1, 2]。


* **追加で必要な測定または実験**：
* Work Package 1 で提案した、4方式すべての sandbox 内実行によるパフォーマンス指標（時間、コマンド発出数、エラー数、訂正頻度）の定量的測定 [source: 1, 2]。
* Blind First Round におけるアンカリングの漏洩率および反対意見（dissent）の保持能力に関する定性的評価 [source: 2]。


* **推奨方針に対する最も強い反対論**：
* *反対論*：「現在 alpha.3 はリリース候補コンテンツが既に main に統合されており、目下の最大の目標は alpha.3 の正式リリース（`A3-REL-001` と `A3-REL-005` の完了）である [source: 1]。4方式の Core Candidate 比較実験は alpha.3 のリリースゲートを直接完了するものではなく別実験であるため [source: 1]、まずは最優先で正式な alpha.3 field trial（候補2）を実施すべきである。比較実験を先行させることはリリースの遅延を招く。」


* **反対論が正しい場合に方針を変更する条件**：
* 人間のプロジェクトオーナーが、「Core Candidate Profile の優位性やワークフローの最適化評価よりも、標準の alpha.3 機能セットを用いた即時のリリース承認と field trial 完了（`A3-REL-001`）を最優先する」という明示的な意思決定レコードを作成・署名した場合 [source: 1, 2]。
* または、比較実験を実施せずとも十分な運用安全性と操作性の証拠（manual usability evidence）が既に他の外部試験等で得られており、人間が即時の field trial 開始を指示した場合 [source: 1]。



---

### 7. Final summary

```yaml
first_priority: Core Candidate 4-way comparison experiment (Codex operator)
second_priority: Alpha.3 formal field trial (A3-REL-001)
third_priority: Final-main audit (A3-REL-005) and release decision
alpha3_release_status: NOT_AUTHORIZED
alpha4_status: CONSIDER_AFTER_COMPARISON
formal_comparison_evidence_available: false
formal_release_evidence_complete: false
human_decision_required: true

```
