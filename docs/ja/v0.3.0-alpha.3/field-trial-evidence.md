# MADP v0.3.0-alpha.3 Field-Trial Evidence Profile 日本語参考訳

状態: release sign-off証拠のための規範的評価profile。

## 目的

loader provenance、validation receipt、start-profile binding、raw observationをモデルrunごとに一度だけ保存し、scenario単位の結果は独立してreviewできる形にします。

## 証拠モデル

`schemas/v0.3.0-alpha.3/field-trial-evidence.schema.yaml`を使用します。

- `run_evidence`はparticipantとrun indexの組ごとに1件です。
- run recordはtested commit、activeなprotocol load report、report receipt、start-profile binding、raw observation inventoryを保持します。
- `scenario_results`はscenarioごとに1件とし、正確に1つの`run_id`を参照します。
- 各scenarioは評価根拠となる`observation_refs`を列挙します。
- global validation receiptはartifactとschemaのbindingが同一の場合だけrun間で共有できます。

## 不変条件

1. load report、profile binding、raw observationをscenario rowごとに複製しません。
2. scenarioは未知のrunまたはobservationを参照できません。
3. 各runは少なくとも1件のscenario resultを支えます。
4. participant IDとrun indexの組は一意です。
5. raw observation pathはrepository-relativeとし、SHA-256を独立再計算します。
6. report receiptは`trial://<run_id>/protocol-load-report`へbindします。
7. metricsはscenario rowから再計算し、手書きaggregateを権威ある値として扱いません。
8. results-version 5の既存証拠は歴史的inputであり、release利用前にmigrationが必要です。

## Migration

```text
python scripts/migrate_field_trial_results_v5_to_v6.py \
  --input old-results.yaml \
  --output migrated-results.yaml
```

migrationは同一runのrun-level evidenceをdeduplicateし、legacy raw observationをrun-scoped observation recordへ変換します。同一participant/run内でload reportまたはprofile bindingが競合する場合はfail closedします。

## Release boundary

このprofileが変更するのは証拠表現だけです。usability thresholdを緩和せず、歴史的観察を合格証拠へ変換せず、releaseを承認せず、decision authorityも変更しません。
