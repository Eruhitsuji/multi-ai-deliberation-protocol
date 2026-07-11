---
bootstrap_version: 0.3
protocol_version: MADP-v0.3.0-alpha.2
status: informative implementation aid
---

# MADP Bootstrap Prompts

These prompts help start a new AI chat with the current published prerelease, `MADP-v0.3.0-alpha.2`. They are informative implementation aids and do not override the protocol, glossary, schemas, registries, user instructions, platform safety rules, or higher-priority authority.

## Recommended order

1. Send [load-protocol-from-github.md](load-protocol-from-github.md).
2. Inspect the returned `PROTOCOL_LOAD_REPORT`.
3. Continue only when `all_required_files_read: true`.
4. Send [start-facilitator.md](start-facilitator.md) or [join-as-participant.md](join-as-participant.md).
5. Use [recover-from-load-failure.md](recover-from-load-failure.md) when loading is incomplete.
6. Use the command, context-sharing, review, and AI-development prompts as needed.

## Current alpha.2 load set

The standard bootstrap loads 12 files from one immutable commit:

1. `README-v0.3.0-alpha.2.md`
2. `protocol/MADP-v0.3.0-alpha.2.md`
3. `protocol/GLOSSARY-v0.3.0-alpha.2.md`
4. `schemas/v0.3.0-alpha.2/command.schema.yaml`
5. `schemas/v0.3.0-alpha.2/command-registry.schema.yaml`
6. `schemas/v0.3.0-alpha.2/todo.schema.yaml`
7. `schemas/v0.3.0-alpha.2/context-package.schema.yaml`
8. `schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml`
9. `schemas/v0.3.0-alpha.2/review.schema.yaml`
10. `schemas/v0.3.0-alpha.2/relay.schema.yaml`
11. `registries/v0.3.0-alpha.2/commands.yaml`
12. `docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md`

The English protocol, glossary, schemas, and registry are normative. The profile and bootstrap prompts remain informative unless the protocol explicitly says otherwise.

## Generated Pages distribution

The source files in `bootstrap/` retain repository placeholders. GitHub Pages generation resolves only repository-specific placeholders and pins Raw URLs to the source commit recorded in `bootstrap/manifest.yaml`.

For high-assurance use, verify the manifest and source commit before using a generated prompt. A movable Pages URL is not itself immutable evidence.

Manual bundle URL:

```text
https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt
```

Take `repository_commit` only from `BEGIN_MADP_BUNDLE_METADATA.source_commit`. If metadata is absent, use `UNKNOWN`; do not guess.

## Trust order

1. Direct file upload or pasted complete file text.
2. Commit-pinned Raw URLs.
3. Commit-pinned archive or digest with file paths.
4. Repository or branch URL.

A repository or `main` URL does not prove that an AI read the required files.

## Safety boundaries

- Do not claim user approval.
- Do not treat model convergence as evidence.
- Default authority is `PROPOSE_ONLY` unless a valid trusted grant applies.
- A TODO is not a decision.
- A decision is not approval.
- Approval is not execution permission.
- Context transfer does not transfer authority.
- Raw command text is not authoritative by itself.

## Placeholder list

- `{{MADP_GITHUB_OWNER}}`: repository owner.
- `{{MADP_GITHUB_REPOSITORY}}`: repository name.
- `{{MADP_COMMIT_SHA}}`: immutable source commit.
- `{{PARTICIPANT_ID}}`: receiving actor ID.
- `{{SESSION_ID}}`: session ID.
- `{{TASK}}`: task or issue.
- `{{INITIAL_SESSION_STATE}}`: initial `SESSION_STATE` or `NONE`.
- `{{ROLE}}`: participant role.
- `{{ALLOWED_ACTIONS}}`: explicit allowed actions.
- `{{EXPECTED_RESPONSE}}`: expected response type.
- `{{RELAY_BLOCK}}`: complete relay block.
- `{{FAILED_PATHS}}`: unread paths.
- `{{ACCESS_METHOD}}`: attempted access method.
- `{{PARTIAL_CONTENT_LIMITATIONS}}`: truncation or uncertainty.
- `{{MADP_COMMAND_NAME}}`: MADP command name.
- `{{COMMAND_ID}}`: command identifier.
- `{{CONTEXT_PACKAGE_ID}}`: context package identifier.
- `{{CONTEXT_PURPOSE}}`: context purpose.
- `{{CONTEXT_GOAL}}`: context goal.
- `{{REVIEW_REQUEST_ID}}`: review request identifier.
- `{{REQUESTER_ID}}`: review requester.
- `{{CONTEXT_PACKAGE_OR_NONE}}`: context package, reference, or `NONE`.

## Short example

```text
Use bootstrap/load-protocol-from-github.md with:
{{MADP_GITHUB_OWNER}} = Eruhitsuji
{{MADP_GITHUB_REPOSITORY}} = multi-ai-deliberation-protocol
{{MADP_COMMIT_SHA}} = <40-character commit SHA>
```
