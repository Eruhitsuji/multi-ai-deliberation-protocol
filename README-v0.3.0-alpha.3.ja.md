# MADP v0.3.0-alpha.3 — 包括的・案内型・チーム対応の熟議

状態: release candidate内容をレビュー中であり、未タグ・未公開です。

alpha.3はalpha.2を置換せず、互換supersetとして拡張します。alpha.2の20 canonical commandを保持し、alpha.3の31 commandを追加します。`status`、`pause`、`resume`はalpha.2の意味を維持し、詳細なsession操作には`session-status`、`session-resume`、Help復帰には`help-exit`を使用します。

artifactはsession ID、source state version、artifact revisionへ束縛されます。release readinessは手書きのDONE宣言ではなく、現在のcheckerと入力hashに一致する機械生成evidence manifestを要求します。

この日本語文書はinformative translationです。規範的な英語sourceと矛盾する場合、英語の規範sourceを優先します。
