# Pilot-001 共通タスク

Task status: `NOT_FROZEN`

このファイル全体を、4方式すべてで同じinformation setとして使用します。

`NOT_FROZEN`のまま実験を開始してはいけません。以下を具体的な1つのbounded decision taskへ置き換え、statusを`FROZEN`へ変更してください。

---

## Task statement

[ここに、4方式で共通して判断する課題を記入する]

## Context supplied to every workflow

[全方式に同じ順序・同じ内容で提供する背景情報と参照先を記入する]

## Required output

[最終的に必要なdecision、設計案、比較表、実装計画などを記入する]

## Acceptance criteria

1. [基準1]
2. [基準2]
3. [基準3]

## Authority boundary

- AI outputs are proposals only.
- Human Final Authority is required.
- No external action, repository modification, merge, release, publication, or deployment is authorized by this task alone.

## Prohibited assumptions

- Do not infer missing IDs, revisions, measurements, evidence status, participant independence, or human approval.
- Do not treat agreement between correlated participants as independent convergence.
- Do not use outputs from another workflow run before the current run's primary output is frozen.

---

Freeze procedure:

1. Replace every bracketed placeholder.
2. Change `Task status` to `FROZEN`.
3. Commit this file before starting any run.
4. Calculate SHA-256 from this file's exact bytes.
5. Record the digest in `experiment.yaml`.
