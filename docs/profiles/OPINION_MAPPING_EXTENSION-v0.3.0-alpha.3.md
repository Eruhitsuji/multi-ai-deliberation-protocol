# Opinion Mapping Extension for MADP v0.3.0-alpha.3

Status: optional advisory extension. It does not alter formal decision authority.

## Purpose

Collect short-statement stances, identify clusters and bridge statements, and preserve minority concerns before formal deliberation.

## Invariants

- `AGREE` is not `approve`.
- Popularity is not fact verification.
- A cluster has no authority.
- A group majority is not execution permission.
- Multiple roles from one model and chat do not inflate independent participant count.
- `PASS`, `NOT_SEEN`, `NO_RESPONSE`, and `INVALIDATED` remain distinct.
- Private stances are not placed in minutes without permission.
- Minority dissent remains available to the later claim ledger and deliberation.

## Snapshot binding

Use `opinion_map_report` from `advanced-profiles.schema.yaml`. Bind analysis to one source state version and snapshot revision. Record both a canonical semantic digest and a raw-byte digest. Report participant count separately from independence-group count.

## Bridge to formal deliberation

Preferences enter as `OPINION`; proposed actions enter as `PROPOSAL`; percentages and cross-group support statements enter as `SOURCE_CLAIM`; minority concerns enter material dissent. None becomes a decision without ordinary evidence, revision, and human-authority gates. The result remains `ADVISORY_ONLY`.
