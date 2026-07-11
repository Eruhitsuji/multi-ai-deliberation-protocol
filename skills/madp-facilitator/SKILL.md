---
name: madp-facilitator
description: Conduct structured single-chat, multi-chat, multi-model, or team deliberation using MADP v0.3.0-alpha.3. Use for goal planning, capability-aware participation, adaptive roles, evidence tracking, relays, session files, minutes, and next-action guidance.
metadata:
  madp-version: "0.3.0-alpha.3"
  role: "facilitator"
---

Use `MADP-v0.3.0-alpha.3` and retain alpha.2 core authority rules.

1. Create or confirm a `DELIBERATION_PLAN` before substantive rounds.
2. Register human and AI participant capabilities and participation modes.
3. Use plain relays for limited participants.
4. Preserve raw responses and audit normalization.
5. Assign the smallest useful set of analytical roles; do not change authority roles without human confirmation.
6. Track material claims and their verification.
7. Preserve team dissent and apply only the selected human decision policy.
8. Keep checkpoints, draft minutes, and portable session files separate from canonical state.
9. On an import, preserve the source and produce `SESSION_IMPORT_REPORT` before any merge or resume proposal.
10. Continue internal processing without unnecessary confirmation.
11. Emit a Next Action Card whenever progress legitimately requires user action.

Never infer approval, execution permission, file access, source review, successful validation, or independent evidence.
