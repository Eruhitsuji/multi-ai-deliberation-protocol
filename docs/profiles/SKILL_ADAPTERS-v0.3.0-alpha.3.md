# MADP Skill Adapter Profile v0.3.0-alpha.3

Status: normative implementation profile for adapter parity; the skills themselves remain convenience adapters.

The shared Agent Skills source defines exactly five roles:

- `madp-start`
- `madp-facilitator`
- `madp-participant`
- `madp-recorder`
- `madp-help`

ChatGPT instruction adapters, ChatGPT skill archives, and Claude skill directories must all be generated or checked against the same five-role source set. A missing role is drift.

Adapters state the MADP version, expose tool limitations, default to `PROPOSE_ONLY`, preserve raw responses, and never infer file access, approval, execution permission, or independent evidence.
