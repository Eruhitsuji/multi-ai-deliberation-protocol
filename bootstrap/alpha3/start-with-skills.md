# Start MADP with Agent Skills

The canonical `skills/` folders use the Agent Skills open format and are shared across supported clients.

## Fastest path

1. Install or make available `madp-start`.
2. Say: “Start a MADP discussion about …”
3. The skill selects a safe mode, proposes a short goal plan, and routes to facilitator, participant, recorder, or help behavior as needed.

## ChatGPT

Use the Skills page and its New skill upload or editor flow when Skills are available for your plan or workspace. The release artifact contains upload-oriented packages generated from the canonical source. Skills are convenience adapters and never override MADP authority rules.

## Claude Code

Copy the desired folders to `.claude/skills/` for the project or `~/.claude/skills/` for personal use. Invoke `/madp-start` directly or describe the task so Claude can activate it.

## No Skills available

Use `quick-start.md` for ordinary work or `verified-start.md` for commit-pinned loading.

## Recommended set

- Minimum: `madp-start`
- Normal deliberation: `madp-start` + `madp-facilitator`
- Multi-model work: add `madp-participant`
- Long-running or transferable sessions: add `madp-recorder`
- Troubleshooting: add `madp-help`
