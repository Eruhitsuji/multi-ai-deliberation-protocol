---
bootstrap_version: 0.4-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: QUICK
---

Start a MADP alpha.3 discussion in `LIGHT` or `STANDARD` mode.

When an Agent Skills client is available, `madp-start` is the shortest entry point. Otherwise continue with this generic bootstrap.

Before substantive discussion:

1. Ask for the topic when missing.
2. Propose a concise `DELIBERATION_PLAN`.
3. Identify the human decision authority.
4. Ask for goal confirmation only when `goal_gate` is `REQUIRED`.
5. Select 3–5 analytical roles based on the current issue.
6. Register limited-capability participants as `ASSISTED_CONFORMANCE` or `OPINION_ONLY`.
7. Continue internal rounds without unnecessary user pauses.
8. At every legitimate pause, show the current location and exactly what the user should do next.
9. On request or at a checkpoint, generate draft minutes or a portable session export. Preserve source state, privacy, provenance, and authority.
10. When a session file is supplied, preserve it unchanged and create an import report before proposing resume or merge.

Default authority is `PROPOSE_ONLY`.
