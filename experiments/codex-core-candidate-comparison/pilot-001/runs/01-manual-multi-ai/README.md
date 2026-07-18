# Run 01: MANUAL_MULTI_AI

Run status: `NOT_STARTED`

## Codexの役割

Codexは記録・ファイル整理・SHA-256計算・metrics補助だけを担当します。Codex自身の回答をMADP参加者の回答として使用しません。

## 使用する共通情報

- `../../task/prompt.md`
- 人間が選択した外部AIサービスの新規chat context

標準alpha.3 protocol、Core Candidate、Workflow Macroを実行規則として使用しません。

## 手順

1. taskが`FROZEN`であることを確認する。
2. 各参加者へ、他参加者の回答を見せずに同一promptを送る。
3. 初期回答を受領した順に`raw/initial-response-<participant-id>.md`へ保存する。
4. 保存直後にSHA-256を計算し、cross exposure前であることを記録する。
5. 全初期回答を固定した後だけ、比較・批評・統合を行う。
6. 人間の最終判断を`artifacts/decision-record.md`へ記録する。
7. 実測metricsを`../../experiment.yaml`へ転記する。

## 保存するもの

```text
raw/initial-response-*.md
raw/cross-exposure-*.md
raw/final-discussion.md
logs/operator-actions.md
logs/commands.log
artifacts/decision-record.md
run-notes.md
```

## Codex開始指示

```text
MANUAL_MULTI_AI runのoperatorとして作業してください。
あなた自身は議論回答を生成せず、人間が貼り付けた外部AIのraw responseを
別ファイルへ保存し、hashと時系列を記録してください。
まず作成予定ファイルと操作手順だけを提示し、人間の確認を待ってください。
```

## 完了条件

- raw初期回答がcross exposure前に固定されている
- participantとindependence groupが記録されている
- Codexのoperator作業が参加者回答として混入していない
- metricsが推測ではなく実測されている
- Human Final Authorityが記録されている
