# MADP Agent Skills v0.3.0-alpha.3

The five canonical Agent Skills are shared source for ChatGPT, Claude Code, and compatible clients:

- `madp-start`: start, inspect, import, or recover a session;
- `madp-facilitator`: conduct deliberation and maintain revision-bound records;
- `madp-participant`: contribute within a bounded role and authority;
- `madp-recorder`: create checkpoints, minutes, exports, and import reports;
- `madp-help`: explain or recover the workflow without state authority.

Skills are informative adapters. They do not override protocol, schemas, the command registry, user instructions, or platform rules. The release generator produces the same five-skill set for ChatGPT ZIP upload and Claude `.claude/skills/` installation. CI rejects missing, extra, or version-divergent adapters.

Canonical command names take precedence over aliases. In particular, `status`, `resume`, and `pause` retain their alpha.2 meanings. Use `session-status`, `session-resume`, and `help-exit` for the distinct alpha.3 operations.
