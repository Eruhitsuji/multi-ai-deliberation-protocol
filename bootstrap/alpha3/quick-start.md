---
bootstrap_version: 0.5-draft
protocol_version: MADP-v0.3.0-alpha.3
usage_mode: QUICK
---

Start a LIGHT or STANDARD MADP discussion. Preserve alpha.2 canonical commands: `status`, `pause`, and `resume` are not aliases. Use `session-status`, `session-resume`, and `help-exit` for their explicit alpha.3 operations.

Before substantive work, establish session ID, current state version, a revisioned deliberation plan, human decision authority, and the smallest useful set of roles. Every accepted artifact must be bound to the session and source state revision. Default authority is `PROPOSE_ONLY`.
