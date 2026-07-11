# MADP Agent Skills 利用ガイド v0.3.0-alpha.3

`skills/` はChatGPT、Claude Code、その他のAgent Skills対応クライアントで共有する正本です。

- `madp-start`: 開始・再開・import・helpの入口
- `madp-facilitator`: 議論進行
- `madp-participant`: 境界付き参加
- `madp-recorder`: checkpoint、議事録、export/import
- `madp-help`: 操作支援

ChatGPTではSkills画面のNew skillからuploadまたはeditorを使用します。Claude Codeでは各folderを `.claude/skills/` または `~/.claude/skills/` に配置し、`/madp-start`を使用できます。Skillsが利用できない場合はgeneric bootstrapを使用します。

Skillの利用可否はauthorityを変更しません。ファイル、ネットワーク、コード実行能力が不明な場合は利用可能と推測してはいけません。
