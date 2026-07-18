# Codex実行環境によるMADP Core Candidate比較実験

Status: `DRAFT`  
Evidence class: `EXPERIMENTAL_COMPARISON`  
Formal release evidence: `false`

このディレクトリは、CodexをMADP参加者ではなく、実験の準備・記録・検証を行うoperatorとして使用するためのpilot環境です。

## 基準

- Repository: `Eruhitsuji/multi-ai-deliberation-protocol`
- Baseline commit: `2a29ddfebe4d9664d3a4043a01d8728fa525d049`
- Comparison schema: `schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml`
- Comparison checker: `scripts/check_alpha3_core_candidate_experiments.py`
- Pilot validator: `experiments/codex-core-candidate-comparison/pilot-001/validate.py`
- `formal_release_evidence`は常に`false`
- `alpha4_authorized`は常に`false`
- Codexはhuman sign-off、release authorization、最終意思決定を代行しない

## ディレクトリ

```text
pilot-001/
├── AGENTS.md
├── README.md
├── experiment.yaml
├── validate.py
├── task/
│   └── prompt.md
├── runs/
│   ├── 01-manual-multi-ai/
│   ├── 02-standard-alpha3/
│   ├── 03-alpha3-core-candidate/
│   └── 04-markdown-validator/
└── review/
    └── human-review.md
```

各runディレクトリには、実行前の情報、raw transcript、操作ログ、生成物、評価メモを保存します。raw記録は上書きせず、変更が必要な場合は新しいrevisionファイルを追加します。

## 実験の進め方

### 1. taskを固定する

`task/prompt.md`のプレースホルダを、4方式で共通して使用する1つのbounded decision taskへ置き換えます。

固定後、UTF-8 bytesのSHA-256を計算します。

```bash
python -c "from pathlib import Path; import hashlib; p=Path('experiments/codex-core-candidate-comparison/pilot-001/task/prompt.md'); print(hashlib.sha256(p.read_bytes()).hexdigest())"
```

得られた値を`experiment.yaml`の`task.prompt_sha256`へ記録します。taskの変更後にrunを継続してはいけません。変更する場合は新しいpilotを作成します。

### 2. 実行順序を先に決める

学習効果を減らすため、4方式の順序をrun開始前に決めて`review/human-review.md`へ記録します。

### 3. 4つの独立した作業環境を作る

同じbaseline commitから、runごとに別worktreeと別Codex threadを使用します。

```bash
git worktree add ../madp-codex-pilot-manual -b experiment/pilot-001-manual 2a29ddfebe4d9664d3a4043a01d8728fa525d049
git worktree add ../madp-codex-pilot-standard -b experiment/pilot-001-standard 2a29ddfebe4d9664d3a4043a01d8728fa525d049
git worktree add ../madp-codex-pilot-core -b experiment/pilot-001-core 2a29ddfebe4d9664d3a4043a01d8728fa525d049
git worktree add ../madp-codex-pilot-markdown -b experiment/pilot-001-markdown 2a29ddfebe4d9664d3a4043a01d8728fa525d049
```

ブランチ名が既に存在する場合は、同じcommitから新しい名前を付けます。run間でCodex threadを再利用しません。

### 4. Codexへoperator指示を与える

各worktreeでCodexを開始し、最初に次を指示します。

```text
このrunでは、experiments/codex-core-candidate-comparison/pilot-001/AGENTS.mdと、
対象runディレクトリのREADME.mdに従ってください。
あなたは実験operatorです。MADP参加者、承認者、最終意思決定者ではありません。
最初は実行せず、読み取るファイル、作成する証拠、実行予定コマンドを提示してください。
```

Codexはリポジトリ操作、ファイル保存、hash計算、validator実行、差分整理を担当します。外部AIへの問い合わせと最終判断は人間が行います。

### 5. runごとに証拠を保存する

最低限、次を保存します。

```text
raw/transcript.md
raw/participant-response-*.md
logs/operator-actions.md
logs/commands.log
artifacts/
run-notes.md
```

- 外部AIの応答は要約ではなくraw textを保存する
- Blind First Round対象の初期回答はcross exposure前に保存・hash化する
- Codexが実行したcommandと失敗も記録する
- 人間の操作数、修正回数、不明な次操作をrun中に記録する

### 6. experiment.yamlへ転記する

各run完了後、`experiment.yaml`の該当runを更新します。

- `participants`
- `blind_first_round`
- `metrics`
- `result`
- raw responseのpathとSHA-256
- `tested_commit`
- protocolまたはbundleのbinding

Codexは測定値を推測してはいけません。不明な値はrunを`DRAFT`のままにします。

### 7. 検証する

pilot固有のrecord、task hash、baseline、release境界を検査します。

```bash
python experiments/codex-core-candidate-comparison/pilot-001/validate.py
```

Core Candidateの既存fixtureとchecker群も確認します。

```bash
python scripts/check_alpha3_core_candidate_experiments.py
```

checkerのPASSはhuman reviewやrelease authorizationを意味しません。

## 方式別の境界

### `MANUAL_MULTI_AI`

Codexは記録・hash・validator実行だけを担当します。議論回答は人間が別AIサービスから取得して貼り付けます。

### `STANDARD_ALPHA3`

標準alpha.3 protocolとcanonical commandを使用します。Core Candidate ProfileとWorkflow Macroは使用しません。

### `ALPHA3_CORE_CANDIDATE`

Core Candidate Profile、Workflow Macro、Blind First Roundを使用します。必要に応じてPR #15で追加したcompact bundleとdynamic role planを利用できます。

### `MARKDOWN_VALIDATOR`

完全なalpha.3 runtimeを使わず、typed MarkdownまたはYAMLとlocal validatorでauthority、evidence、dissent、decision境界を保持します。

## 実験終了条件

pilotは次の条件を満たすまで`DRAFT`です。

- 同一のtaskとacceptance criteriaを4方式で使用した
- 4つのrunが別contextで行われた
- raw recordとhashが保存された
- 全metricsが実測値で記録された
- pilot validatorと既存checkerが成功した
- 人間が結果と限界をレビューした

このpilotだけで`A3-REL-001`を完了したり、alpha.4を開始したりしてはいけません。
