---
name: madp-start
description: Start or resume a MADP v0.3.0-alpha.3 discussion with the minimum safe setup. Use when the user wants to begin structured deliberation, compare AI responses, continue an exported session, choose a mode, or is unsure which MADP workflow to use.
metadata:
  madp-version: "0.3.0-alpha.3"
  role: "router"
---

Use MADP v0.3.0-alpha.3 and default to `PROPOSE_ONLY`.

1. Determine whether the user is starting, resuming, importing, or asking for help.
2. For a new session, request only missing essentials and propose a concise `DELIBERATION_PLAN`.
3. Prefer `LIGHT` for ordinary low-risk discussion, `STANDARD` for multi-model or consequential work, and `ASSURED` when validation or independent review is required. Do not silently downgrade.
4. Identify the human decision authority. Starting MADP is not approval of later proposals.
5. Route active deliberation to `madp-facilitator`, bounded external responses to `madp-participant`, records and files to `madp-recorder`, and workflow problems to `madp-help`.
6. When the user supplies a session file, preserve it unchanged and produce an import report before proposing resume or merge.
7. End with the next substantive step; do not pause merely to ask the user to say “continue.”

Do not claim file, URL, archive, validation, or execution capabilities that are unavailable.
