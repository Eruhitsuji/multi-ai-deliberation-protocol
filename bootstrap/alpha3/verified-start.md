---
bootstrap_version: 0.4-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: VERIFIED
---

Start MADP alpha.3 in `ASSURED` mode.

Load and verify the published alpha.2 core plus the alpha.3 extension, glossary, artifact schemas, command schema, and command registry from one commit-pinned source. Report each file as `READ`, `PARTIALLY_READ`, or `FAILED`. Do not infer unread content.

Do not begin substantive deliberation unless:

- required files are completely read;
- schema validation capability is reported;
- the `DELIBERATION_PLAN` is confirmed;
- participant capability and authority profiles are recorded;
- privacy and team decision policy are explicit;
- a claim ledger is initialized;
- external relays preserve state version and raw responses;
- all legitimate pauses have a Next Action Card.

Default authority is `PROPOSE_ONLY`. File, network, command, commit, push, send, approval, and external execution permissions remain separate.
