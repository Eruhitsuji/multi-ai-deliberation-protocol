# MADP Agent Skills

These folders are the shared Agent Skills source for ChatGPT, Claude Code, and other compatible agents.

## Included skills

- `madp-start`: choose a safe starting path and initialize a session.
- `madp-facilitator`: run the deliberation workflow.
- `madp-participant`: respond to a bounded relay without claiming extra authority.
- `madp-recorder`: create checkpoints, minutes, and portable exports.
- `madp-help`: diagnose onboarding, command, import, export, and recovery problems.

## ChatGPT

ChatGPT Skills follow the Agent Skills open format. In ChatGPT, open **Skills**, choose **New skill**, and use the available upload or editor flow. Review every skill before installation. The generated alpha.3 release artifacts include upload-oriented skill packages.

## Claude Code

Copy the selected skill directory to either:

- `~/.claude/skills/<skill-name>/` for personal use; or
- `.claude/skills/<skill-name>/` inside a project.

Then invoke `/madp-start` or ask Claude to begin a MADP discussion.

## Generic fallback

When Skills are unavailable, use `bootstrap/alpha3/quick-start.md` or the generated verified bootstrap. Skill availability never changes protocol authority.
