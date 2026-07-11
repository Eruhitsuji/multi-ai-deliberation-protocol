# MADP v0.3.0-alpha.3 — 包括的・誘導型・チーム対応の議論

状態: リリース候補内容の実装済み。未タグ・未公開。

MADP v0.3.0-alpha.3は、公開済みalpha.2の安全性・権限境界を維持しながら、実際のWebチャットやチーム利用で必要となる次の機能を追加します。

- 議論開始前の目標、範囲、成果物、終了条件の確認
- `LIGHT`、`STANDARD`、`ASSURED`の運用モード
- 複数人の人間、完全対応AI、限定対応AI、observerの参加
- URL、ZIP、YAML、添付ファイルを扱えないAI向けのPlain Relay
- 形式が崩れた回答のraw保存、取り込み、監査可能な正規化
- 議論進行AIによる分析役割の動的な追加、停止、再割当
- claim単位の出所、検証状況、反対意見の記録
- チームの決定方式、承認者、少数意見、非同期参加の管理
- 人間がレビュー可能な議事録、決定記録、action item
- 独立したMADP Help chatと議論中のHelp mode
- 正当な停止時にユーザーへ次の操作を示すNext Action Card
- ChatGPTとClaude向けのskill adapter

英語版protocol、glossary、schema、registryがnormative sourceです。この日本語版と`docs/ja/v0.3.0-alpha.3/`以下はinformative translationです。意味の衝突がある場合は英語版を優先し、衝突自体を不具合として扱います。

## 安全上の不変条件

- AI同士の一致は、ユーザーまたはチームの承認ではありません。
- contextの移送によって権限は移送されません。
- 正規化で元回答にない承認、証拠、確信度、実行権限を追加してはいけません。
- `OPINION_ONLY`参加者はcanonical stateを直接更新できません。
- チーム参加者の沈黙を同意として扱いません。
- Help assistantと議事録担当には決定権・実行権がありません。
- private情報は許可なくrelayや議事録へ含めません。
- ユーザー操作が必要な停止では、現在地、次の操作、受理可能な入力、代替経路を示します。

## リリース状態

```yaml
implementation_status: RELEASE_CANDIDATE_CONTENT_READY
integration_status: IMPLEMENTATION_BRANCH
release_ready: false
tagged: false
published: false
```

手動usability trialの承認と、mainへmergeした最終commitでのrelease auditは別途必要です。
