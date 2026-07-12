# MADP v0.3.0-alpha.3 Field-Trial Collection Profile

状態: 評価支援のための参考訳です。protocolのauthorityやrelease thresholdは変更しません。

## 目的

1回の実用model runから、protocol load report、validation receipt、start profile binding、observation hashをscenarioごとに手作業で複製せず、再現可能なrun-normalized evidence packageを作成します。

## Tool

`scripts/collect_field_trial_evidence_v030_alpha3.py`を使用します。

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py prepare \
  --config collection-config.yaml \
  --output docs/evaluation/evidence/v0.3.0-alpha.3/RUN-001/package.yaml
```

observation pathをrepository-relativeにして独立に再hashできるよう、出力先はrepository内でなければなりません。

## prepareの動作

`prepare`は次を行います。

1. tested commitとcheckout済みcommitの一致を要求する
2. activeかつ`COMPLETE`な`FIELD_TRIAL` load reportを読む
3. repository上のtargetとschemaの実byteからvalidation receiptを再生成する
4. normalized load reportのreceiptを生成する
5. selected start profileのauthorizationとhashを確認する
6. observation fileをpackage directoryへcopyしてSHA-256を記録する
7. 8つのscenario rowを作成する
8. 全scenarioにobservation referenceとreview fieldが揃った場合だけ`READY`にする

scenario評価が不足するpackageは`DRAFT`です。`DRAFT`は収集中の記録として有効ですが、正式trial evidenceへmergeできません。

## checkとmerge

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py check \
  --package RUN-001/package.yaml \
  --require-ready
```

```text
python scripts/collect_field_trial_evidence_v030_alpha3.py merge \
  --base-results docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml \
  --package RUN-001/package.yaml \
  --package RUN-002/package.yaml \
  --output combined-results.yaml
```

`merge`はparticipant、receipt、run ID、trial IDの競合を拒否し、aggregate metricsを再計算します。統合結果は`IN_PROGRESS`のままで、sign-offは設定しません。human sign-offとrelease state変更は別のauthority-sensitive actionです。

## normalization boundary

collectorは`validation_receipt_refs`を、`schema_validation_records`から生成したreceiptとrun-bound protocol-load-report receiptだけに再構築する場合があります。この処理は`REBUILT_VALIDATION_RECEIPT_REFERENCE_SET`として明示されます。tested commit、loaded source hash、report status、report revision、start profile authorityは変更しません。

## Safety invariant

- missing source hashや未読protocol内容を捏造しない
- `DRAFT`を`READY`として扱わない
- trial resultを承認しない
- A3-REL-001を完了にしない
- `release_ready`、tag、release、publish、Pages promotionを行わない
- raw observationの実byteをauthorityとし、後続hash mismatchはfail-closedする
- collection packageは`MADP-FIELD-TRIAL-COLLECTION-v1`と`schemas/v0.3.0-alpha.3/field-trial-collection.schema.yaml`を使用する

この日本語文書はinformative translationです。矛盾する場合は英語の規範sourceを優先します。
