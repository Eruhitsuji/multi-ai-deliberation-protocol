# Blind First-Round Review Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Purpose

Reduce anchoring and conformity by separating an independent initial position from later cross-exposure and revision.

## Sequence

1. `BLIND_INITIAL_POSITION`: provide the question, evidence scope, and authority boundary without prior participant conclusions.
2. `CROSS_EXPOSURE`: disclose the other positions and request the strongest criticism, failure conditions, and missing evidence.
3. `REVISION`: record claims changed, retained, or withdrawn and the reason for each change.
4. `INTEGRATION`: compare independent convergence, correlated convergence, and residual dissent.

## Required controls

- Bind each round to one session ID, source state version, information-set hash, and participant independence group.
- Preserve the raw initial response before normalization.
- Do not count multiple roles in one shared chat as independent initial positions.
- Do not describe agreement reached only after cross-exposure as independent convergence.
- A participant may remain `OPINION_ONLY`; review participation does not grant approval authority.
- Material dissent remains visible through integration and minutes.

## Failure handling

If the initial round accidentally reveals prior conclusions, classify the run as `ANCHORING_EXPOSED`; it may remain useful as ordinary review evidence but not blind-round evidence.
