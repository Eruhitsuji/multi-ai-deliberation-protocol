---
language: en
source_commit: a5d3d3877cbf5081bf82e0a476f6686cab6c350f
translation_status: CURRENT
normative: false
---

# MADP English Documentation

English | [日本語](../ja/README.md)

> These are explanatory guides. The normative sources remain in `protocol/`, `schemas/`, and `registries/`.

## Start here

- [Getting started](getting-started.md)
- [Basic usage and workflow selection](basic-usage.md)
- [Practical guide index](practical-guides.md)
- [Core concepts](concepts.md)
- [Explanatory glossary](glossary.md)
- [Frequently asked questions](faq.md)

## Deliberation patterns

- [Multiple AI models](multi-model-deliberation.md)
- [One model across multiple chats](single-model-multi-chat.md)
- [One model in one chat](single-model-single-chat.md)

## Practical guides

- [Authority model](authority-model.md)
- [Commands](commands.md)
- [AI-driven development](ai-development.md)
- [Context sharing and relay](context-relay.md)
- [TODO lifecycle](todo-lifecycle.md)
- [Review workflow](review-workflow.md)

## Translation governance

- [Translation policy](../TRANSLATION_POLICY.md)
- [`docs/translations.yaml`](../translations.yaml) records the managed language pairs and source commit.
- `python scripts/check_translation_docs.py` validates pairing and metadata.

## Version status

- Published: `MADP-v0.3.0-alpha.1`
- Release candidate ready, not yet tagged or published: `MADP-v0.3.0-alpha.2`
- `release_ready: true`
- Tagging and GitHub Release publication remain separate actions.

## Normative sources

- [`protocol/MADP-v0.3.0-alpha.2.md`](../../protocol/MADP-v0.3.0-alpha.2.md)
- [`protocol/GLOSSARY-v0.3.0-alpha.2.md`](../../protocol/GLOSSARY-v0.3.0-alpha.2.md)
- [`schemas/v0.3.0-alpha.2/`](../../schemas/v0.3.0-alpha.2/)
- [`registries/v0.3.0-alpha.2/commands.yaml`](../../registries/v0.3.0-alpha.2/commands.yaml)
