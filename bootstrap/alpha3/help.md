---
bootstrap_version: 0.5-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: HELP
---

Provide protocol support only. Request the minimum session ID, state version, phase, and problem description. Do not mutate canonical state or claim a repair was applied. In-session Help records the prior phase and exits only through revision-bound `help-exit`; the alpha.2 canonical `resume` command retains its general paused-workflow meaning.
