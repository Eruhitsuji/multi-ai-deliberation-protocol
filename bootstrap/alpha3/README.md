# MADP alpha.3 Bootstrap

Alpha.3 bootstrap is release-candidate content and is not the current published bootstrap until release.

Use the bootstrap in two phases:

1. Load the protocol with `load-protocol-from-github.md` from one immutable commit and obtain a `COMPLETE` `PROTOCOL_LOAD_REPORT`.
2. Apply one start or participation profile.

Do not use a start profile as a substitute for protocol loading. `quick-start.md` and `verified-start.md` must return `PROTOCOL_NOT_LOADED` when the required load report is absent or incomplete.

After loading, choose:

- `quick-start.md` for low-risk or ordinary structured discussion.
- `verified-start.md` for formal, high-risk, research, or development work.
- `invite-limited-participant.md` for an AI or human that cannot use YAML, files, ZIP, or URLs.
- `help.md` to start a separate MADP Help chat.
- Agent Skills when the client supports them.

Every user-facing pause must identify the current location, the exact next action, accepted input, what follows, and an alternative. The bare commands `status`, `pause`, and `resume` retain their alpha.2 canonical meanings; use explicit alpha.3 command names for session-detail and Help operations.