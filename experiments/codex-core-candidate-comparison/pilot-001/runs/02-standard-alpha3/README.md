# Run 02: STANDARD_ALPHA3

Run status: `NOT_STARTED`

## Codexの役割

Codexは標準alpha.3 runの実験operatorです。protocol sourceの準備、canonical command記録、raw response保存、validator実行を担当します。Codex自身は参加者・承認者・最終判断者ではありません。

## 使用するsource

- `../../task/prompt.md`
- `protocol/MADP-v0.3.0-alpha.3.md`
- `registries/v0.3.0-alpha.3/commands.yaml`
- 必要な標準alpha.3 schemaとbootstrap

次を使用してはいけません。

- `MADP_CORE_CANDIDATE` Profile
- Workflow Macro registry/profile
- Core compact bundleをCore workflowとして扱うこと

## 手順

1. baseline commitとtask hashを記録する。
2. 標準alpha.3 sourceを読み取り、使用sourceのpathとSHA-256を記録する。
3. 人間が外部AI参加者を登録する。
4. canonical commandと全引数を実行順に`logs/commands.log`へ記録する。
5. `goal-confirm`と`session-start`を分離する。
6. raw response、state transition、拒否、修正を保存する。
7. 人間の最終判断後、実測metricsを`../../experiment.yaml`へ転記する。

## 保存するもの

```text
raw/transcript.md
raw/participant-response-*.md
logs/operator-actions.md
logs/commands.log
artifacts/protocol-binding.yaml
artifacts/decision-record.md
run-notes.md
```

## Codex開始指示

```text
STANDARD_ALPHA3 runのoperatorとして作業してください。
Core Candidate ProfileとWorkflow Macroは使用しないでください。
最初に使用する標準alpha.3 source、予定canonical command、作成予定証拠を提示し、
人間の確認前にsessionやstateを進めないでください。
```

## 完了条件

- standard alpha.3だけを使用した
- canonical commandと引数が記録された
- session-start前の実質的state変更がない
- authority-sensitive値を推測していない
- Human Final Authorityが維持された
