# MADP v0.3.0-alpha.3 — Inclusive, Guided, and Team-Aware Deliberation

Status: implementation draft; not tagged or published.

MADP v0.3.0-alpha.3 extends the published alpha.2 core with practical workflow support for:

- deliberate goal and scope confirmation before substantive rounds;
- `LIGHT`, `STANDARD`, and `ASSURED` operating modes;
- human, full-capability AI, limited-capability AI, and observer participation;
- plain-text relays for systems that cannot read URLs, ZIP files, YAML, or the complete protocol;
- tolerant response ingestion with strict, auditable canonicalization;
- adaptive analytical role assignment without silently changing authority roles;
- claim-level provenance and verification;
- multi-human team decision policies and dissent preservation;
- reviewable session minutes, decision logs, and action items;
- a dedicated MADP Help assistant and in-session help mode;
- explicit next-action guidance at every legitimate pause;
- ChatGPT and Claude skill adapters generated from shared protocol concepts.

## Normative source set

Until alpha.3 becomes a self-contained release bundle, the implementation draft uses:

1. the published `MADP-v0.3.0-alpha.2` protocol and glossary for unchanged core rules;
2. `protocol/MADP-v0.3.0-alpha.3.md` for alpha.3 additions and overrides;
3. `protocol/GLOSSARY-v0.3.0-alpha.3.md` for new terms;
4. alpha.3 schemas and command registry.

If alpha.3 text conflicts with unchanged alpha.2 safety or authority rules, the stricter rule applies and the conflict is a defect.

## Safety invariants

- AI agreement is not user or team approval.
- Context transfer does not transfer authority.
- A malformed response may be normalized, but normalization must not invent approval, evidence, confidence, or permission.
- `OPINION_ONLY` participants cannot directly update canonical state.
- Team silence never counts as consent.
- Help assistants and recorders have no decision or execution authority.
- Private material is not relayed or placed in minutes without permission.
- A user-facing pause must include a concrete next action, accepted input, and an alternative path.

## Implementation map

- Protocol extension: `protocol/MADP-v0.3.0-alpha.3.md`
- New glossary: `protocol/GLOSSARY-v0.3.0-alpha.3.md`
- Artifact schema: `schemas/v0.3.0-alpha.3/deliberation.schema.yaml`
- Command schema: `schemas/v0.3.0-alpha.3/command.schema.yaml`
- Registry: `registries/v0.3.0-alpha.3/commands.yaml`
- Bootstrap: `bootstrap/alpha3/`
- Team, comparison, help, and skill profiles: `docs/profiles/`
- Automated fixtures: `tests/v0.3.0-alpha.3/fixtures.yaml`
- Validation: `scripts/check_alpha3_implementation.py`
- Traceability: `docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml`

## Release status

```yaml
implementation_status: DRAFT_IMPLEMENTED
release_ready: false
tagged: false
published: false
```

Manual usability trials, bilingual document completion, generated distribution, migration fixtures, and release-candidate audit remain release blockers.
