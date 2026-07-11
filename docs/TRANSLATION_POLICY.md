# MADP Translation Policy

## Normative language

English is the normative language for MADP protocol, glossary, schemas, registries, and release-governance artifacts.

Canonical normative paths remain unchanged:

- `protocol/`
- `schemas/`
- `registries/`

Translations must not move, replace, or silently redefine these sources.

## Documentation layout

User-facing explanatory guides are organized by language:

- `docs/en/` — English explanatory guides
- `docs/ja/` — Japanese explanatory guides

The root `README.md` remains the English project landing page. `README.ja.md` is the Japanese landing page.

## Translation status

Translated documents are non-normative unless a future release explicitly declares otherwise. Every translated guide must include:

- `language`
- `translation_of`
- `source_commit`
- `translation_status`
- `normative: false`

Recommended statuses:

- `CURRENT`
- `NEEDS_REVIEW`
- `STALE`

If a translation conflicts with the English normative source, the English source takes precedence.

## Change management

Changes to protocol semantics must be made in the English canonical source first. Explanatory guides and translations are updated afterward in a separate documentation change or in the same pull request with an explicit synchronization note.

Existing canonical paths must not be moved merely to make the language layout symmetrical. Stable paths, commit-pinned URLs, bootstrap generators, CI, traceability, and external review packages depend on them.
