# Run 03: ALPHA3_CORE_CANDIDATE

Run status: `NOT_STARTED`

## Codexの役割

CodexはCore Candidate runの実験operatorです。compact bundle、dynamic role plan、Workflow Macro展開、raw evidence、validatorを扱います。Codexは参加者、承認者、実行許可者、最終判断者ではありません。

## 使用するsource

- `../../task/prompt.md`
- `docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md`
- `docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md`
- `registries/v0.3.0-alpha.3/workflow-macros.yaml`
- `docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md`
- PR #15後のcompact bundleとmanifest
- 必要に応じてdynamic role plan

## 手順

1. baseline commitとtask hashを記録する。
2. compact bundleとmanifestを生成・検査し、artifact hashを保存する。
3. 利用可能な外部AIサービスを人間が記入し、dynamic role planを生成・検査する。
4. Blind First Roundの参加者とindependence groupを人間が確認する。
5. 各初期回答をcross exposure前に保存・hash化する。
6. Workflow Macroを使用する場合、展開予定canonical commandとhuman gateを記録する。
7. Macroをatomic commandとして処理しない。
8. 人間の明示確認なしにdecision approval、external action、ファイル変更を実行しない。
9. 実測metricsを`../../experiment.yaml`へ転記する。

## 保存するもの

```text
raw/initial-response-*.md
raw/cross-exposure-*.md
raw/transcript.md
logs/operator-actions.md
logs/macro-expansions.md
logs/commands.log
artifacts/compact-bundle/
artifacts/dynamic-role-plan.yaml
artifacts/decision-record.md
run-notes.md
```

## Codex開始指示

```text
ALPHA3_CORE_CANDIDATE runのoperatorとして作業してください。
compact bundleとdynamic role planを使用できますが、それらをload完了や独立性の証明と
みなさないでください。最初にsource binding、Blind参加者候補、Macro展開予定、
human gate、保存予定証拠を提示し、人間の確認を待ってください。
```

## 完了条件

- Blind First Roundの初期回答がcross exposure前に固定された
- 相関のある参加者を独立票として数えていない
- Macro展開とcanonical commandが対応付けられた
- DecisionとExecution Authorizationが分離された
- compact bundleの存在だけでload COMPLETEを主張していない
- Human Final Authorityが維持された
