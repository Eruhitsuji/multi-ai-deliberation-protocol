# MADP v0.3.0-alpha.3 Assurance Modes Profile（参考訳）

状態: 任意の規範的implementation profile。

## Mode

- `NORMAL`: standardなrevision・authority controlを用いる、通常の可逆deliberation。
- `REVIEW_REQUIRED`: proposal形式で進行できますが、review完了まで該当transitionをvalidatedとしてattestできません。
- `STRICT`: evidence不足、stale revision、未解決authority、必須independent validationに対してfail closedします。

`advanced-profiles.schema.yaml`の`assurance_state`を使用します。

## Escalationとde-escalation

human、AI facilitator、policy、runtimeはescalationを提案できます。提案したことによって新しいauthorityは得ません。`STRICT`からのde-escalationには独立validation basisが必要です。facilitatorは、自身が元の懸念を提案したという理由だけで自己de-escalationをvalidateしてはいけません。

上位ruleが許す場合、humanはprotocol recommendationをoverrideできますが、結果は`VALIDATED_NORMAL`ではなく`OVERRIDDEN_WITH_DISSENT`として記録します。

## Authority separation

- human decision authorityは組織が何を選ぶかを決定します。
- deterministic transition validationは記録transitionがMADP条件を満たすかを判定します。
- AI facilitationは、別ruleでより狭いroleが与えられない限り`PROPOSE_ONLY`です。
- platform safety ruleはMADP decision authorityとは独立して禁止支援を拒否できます。
