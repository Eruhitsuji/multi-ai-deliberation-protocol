# Run 04: MARKDOWN_VALIDATOR

Run status: `NOT_STARTED`

## Codexの役割

Codexはtyped Markdown/YAML recordの作成補助、raw response保存、SHA-256計算、local validator実行を担当します。完全なalpha.3 runtime、Core Candidate runtime、Workflow Macro実行は使用しません。

## 使用するsource

- `../../task/prompt.md`
- `schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml`
- 人間が指定した最小限のtyped record形式
- 必要なlocal validator

## 手順

1. baseline commitとtask hashを記録する。
2. authority、participant、claim/evidence、dissent、decisionの最小record構造を固定する。
3. 人間が外部AIの回答を取得し、raw fileへ保存する。
4. Blind First Roundを行う場合、初期回答をcross exposure前に保存・hash化する。
5. typed recordへ参照を追加する。raw responseを要約で置き換えない。
6. validatorを実行し、失敗と修正を記録する。
7. 人間の最終判断とdecision reconstruction結果を保存する。
8. 実測metricsを`../../experiment.yaml`へ転記する。

## 保存するもの

```text
raw/initial-response-*.md
raw/cross-exposure-*.md
raw/transcript.md
records/participants.yaml
records/claims-evidence.yaml
records/dissent.yaml
records/decision.yaml
logs/operator-actions.md
logs/commands.log
artifacts/validation-result.txt
run-notes.md
```

## Codex開始指示

```text
MARKDOWN_VALIDATOR runのoperatorとして作業してください。
標準alpha.3 runtimeやWorkflow Macroを実行せず、typed recordとlocal validatorだけで
raw record、authority、evidence、dissent、decision境界を保持してください。
最初にrecord構造、作成予定ファイル、validator commandを提示し、人間の確認を待ってください。
```

## 完了条件

- full alpha.3 runtimeを使用していない
- raw responseとtyped recordの参照が維持された
- authorityとdecision boundaryが記録された
- dissentを削除せず保持した
- validatorの失敗と修正が保存された
- Human Final Authorityが維持された
