---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# Frequently asked questions

English | [日本語](../ja/faq.md)

> This FAQ is explanatory. The versioned English specification takes precedence.

## Is MADP an AI model?

No. MADP is a protocol for structuring work among users, AI systems, validators, and execution agents.

## Does agreement among several AIs prove correctness?

No. Agreement is convergence, not independent evidence. Important claims should be supported by reproducible checks, primary sources, or qualified human validation.

## Is a TODO the same as a decision?

No. A TODO records work. A decision selects an outcome. Approval and execution permission are separate again.

## Does approving a decision authorize execution?

No. Approval is bound to a decision revision. External execution requires separate action-specific permission.

## Can a review authorize merge?

No. A review contributes evidence. Ready-for-review, merge, tag, and release each require their own governance decision.

## Why does MADP keep English normative sources?

The existing protocol, schemas, registries, CI, bootstrap prompts, and commit-pinned links already use stable English paths. Keeping them stable avoids breaking interoperability. Japanese documents are explanatory translations.

## Why not copy the full chat when handing work to another AI?

Full history is noisy and can contain obsolete state. A bounded context package transfers the operative goal, artifacts, unresolved items, evidence, and authority boundaries.

## What should happen when required information is missing?

Proceed with safe non-blocked work, record the missing input, and fail closed for actions that depend on it. Do not invent approval, evidence, or authority.

## Can MADP execute shell commands or repository actions?

The protocol can describe and authorize workflows, but an implementation must enforce its own execution boundary. The alpha.2 internal runtime does not perform external actions.

## What does `release_ready: false` mean?

It means implementation or merge status must not be interpreted as authorization to tag or publish a release.

## How should translations be maintained?

Keep paired files under `docs/en/` and `docs/ja/`, record the source commit, mark Japanese files non-normative, and run `python scripts/check_translation_docs.py`.
