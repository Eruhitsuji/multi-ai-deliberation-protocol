# MADP v0.3.0-alpha.3 Blind First-Round Review Profile（参考訳）

状態: 任意の規範的implementation profile。

## 目的

独立した初期見解と、その後の相互開示・修正を分離し、anchoringと同調を減らします。

## Sequence

1. `BLIND_INITIAL_POSITION`: 他participantの結論を見せず、question、evidence scope、authority boundaryだけを提示します。
2. `CROSS_EXPOSURE`: 他の見解を開示し、最も強い批判、failure condition、不足evidenceを求めます。
3. `REVISION`: 変更・維持・撤回したclaimと、その理由を記録します。
4. `INTEGRATION`: independent convergence、correlated convergence、残存dissentを比較します。

## 必須control

- 各roundをsession ID、source state version、information-set hash、participant independence groupへbindします。
- normalization前のraw initial responseを保存します。
- 同じ共有chat内の複数roleを独立した初期見解として数えません。
- cross-exposure後だけに生じた一致をindependent convergenceと表現しません。
- participantは`OPINION_ONLY`のまま参加できます。review参加はapproval authorityを付与しません。
- material dissentはintegrationとminutesまで可視状態を保ちます。

## Failure handling

初期roundで既存結論を誤って開示した場合、runを`ANCHORING_EXPOSED`として分類します。通常のreview evidenceとしては利用できますが、blind-round evidenceには算入しません。
