---
bootstrap_version: 0.1
protocol_version: MADP-v0.2.5-rc.1
status: informative implementation aid
---

# MADP Bootstrap Prompts

These prompts help start a new AI chat that does not already know MADP. They are informative implementation aids. They do not override the protocol, glossary, schema, user instructions, platform safety rules, or any higher-priority authority.

Use these prompts to make the receiving AI load the pinned MADP files, report what it actually read, and avoid guessing when a required file is unread or only partially read.

## Template and Generated Prompts

In the source repository, the files in `bootstrap/` are source templates. They intentionally keep the repository-specific placeholders listed below.

Generated prompt files are produced for GitHub Pages by resolving only those repository-specific placeholders. The generated canonical Raw URLs for `MADP-v0.2.5-rc.1` are pinned to the source commit recorded in `bootstrap/manifest.yaml`. The GitHub Pages latest URL is movable, but the generated file contents point at one specific commit.

For high-assurance use, verify the generated `manifest.yaml`, the source repository, and the source commit before pasting a generated prompt into a new AI chat. Session-specific placeholders such as `{{PARTICIPANT_ID}}`, `{{SESSION_ID}}`, `{{TASK}}`, and `{{RELAY_BLOCK}}` still need to be filled in at use time.

## Bootstrap vs Protocol, Profiles, and Templates

- Protocol: the normative behavior, authorization, state, relay, and conformance rules.
- Glossary: normative meanings for explicitly marked terms.
- Schema: machine-readable field names, required fields, types, and enum spellings.
- Profile: a future reusable domain rule set built on the protocol.
- Template: a future starter kit for a recurring workflow.
- Bootstrap prompt: an informative startup aid for a new chat.

If this bootstrap text conflicts with the protocol, glossary, or schema, treat the conflict as a defect and follow the authority order in the protocol.

## Recommended Order

1. Send [load-protocol-from-github.md](load-protocol-from-github.md) with commit-pinned Raw URLs.
2. Inspect the returned `PROTOCOL_LOAD_REPORT`.
3. If `all_required_files_read: true`, send either [start-facilitator.md](start-facilitator.md) or [join-as-participant.md](join-as-participant.md).
4. Provide `SESSION_STATE` for facilitator startup or `RELAY_BLOCK` for participant startup.
5. If loading failed or was partial, use [recover-from-load-failure.md](recover-from-load-failure.md).

## Trust Order for Source Material

1. Direct file upload or pasted full file text from the user.
2. Commit-pinned Raw URLs for each canonical file.
3. Commit-pinned repository archive or digest with file paths.
4. Repository top URL or branch URL.

A repository top URL is not proof that a model read the files. A branch URL such as `main` can move and should not be the standard bootstrap source for release work.

## Public GitHub Repository Limits

Some AI chats cannot fetch URLs, cannot access GitHub, fetch rendered pages instead of raw files, truncate long files, or summarize content without reading it. The receiving AI must report these limits in `PROTOCOL_LOAD_REPORT.limitations` and must not reconstruct unread protocol content from general knowledge.

## Manual Paste Fallback

Some AI environments cannot directly retrieve GitHub, Raw URLs, or GitHub Pages. This is an external retrieval limitation, not necessarily a failure to understand MADP once the required text is supplied.

If `all_required_files_read: false`, open the generated complete bundle in a browser:

```text
https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt
```

Copy the entire page, from the first `BEGIN_FILE` line through the final `END_FILE` line, and paste it into the same AI chat. Then request a new `PROTOCOL_LOAD_REPORT`. The receiving AI must identify the four files from the bundle boundaries, report `access_method: "PASTED_TEXT"`, and set `all_required_files_read: true` only when all four required files were completely received.

The Pages URL is a movable deployment URL and intentionally does not contain `{{MADP_COMMIT_SHA}}`. The generated bundle content and manifest remain tied to the source commit. The receiving AI must take `repository_commit` only from `BEGIN_MADP_BUNDLE_METADATA.source_commit`. Do not select a repository commit by searching the canonical file contents for a 40-character hexadecimal string. If metadata is missing, use `repository_commit: "UNKNOWN"` and do not guess. For uploaded bundle files, report `access_method: "UPLOADED_FILE"`; for pasted text, report `access_method: "PASTED_TEXT"`.

## Operational Limitations

Chat UI rendering or model output formatting can break Markdown code fences or YAML indentation. Treat `PROTOCOL_LOAD_REPORT`, `FACILITATOR_START_REPORT`, and `PARTICIPANT_RESPONSE` as machine-readable only after parsing them with a YAML parser. If the YAML does not parse, do not treat the response as machine-valid even when a human can understand the intent.

Record logical behavior and serialization separately. A participant dry run can preserve authority, state, and response type while still failing machine-readable serialization.

```yaml
dry_run_result:
  behavioral_conformance: "PASS"
  yaml_serialization: "PASS | FAIL | NOT_VERIFIED"
```

## Placeholder List

- `{{MADP_GITHUB_OWNER}}`: GitHub owner or organization.
- `{{MADP_GITHUB_REPOSITORY}}`: Repository name.
- `{{MADP_COMMIT_SHA}}`: Immutable commit SHA used in Raw URLs.
- `{{PARTICIPANT_ID}}`: Actor identifier for the receiving AI.
- `{{SESSION_ID}}`: Session identifier for a new or existing MADP session.
- `{{TASK}}`: User task or issue to deliberate.
- `{{INITIAL_SESSION_STATE}}`: Initial `SESSION_STATE`, or `NONE` when no state exists yet.
- `{{ROLE}}`: Participant role, such as `REVIEWER` or `VALIDATOR`.
- `{{ALLOWED_ACTIONS}}`: Explicit allowed actions for the participant.
- `{{EXPECTED_RESPONSE}}`: Required response type for the participant.
- `{{RELAY_BLOCK}}`: Full relay block supplied to a participant.
- `{{FAILED_PATHS}}`: Files that were not read successfully.
- `{{ACCESS_METHOD}}`: Method used for failed or partial access.
- `{{PARTIAL_CONTENT_LIMITATIONS}}`: Known truncation, omissions, or uncertainty.

## Short Usage Examples

Load the protocol from a pinned commit:

```text
Use bootstrap/load-protocol-from-github.md with:
{{MADP_GITHUB_OWNER}} = example-owner
{{MADP_GITHUB_REPOSITORY}} = multi-ai-deliberation-protocol
{{MADP_COMMIT_SHA}} = 0123456789abcdef0123456789abcdef01234567
```

Start a facilitator after a successful load report:

```text
Use bootstrap/start-facilitator.md with:
{{PARTICIPANT_ID}} = facilitator
{{SESSION_ID}} = MADP-SESSION-001
{{TASK}} = Decide release readiness
{{INITIAL_SESSION_STATE}} = NONE
```

Join a participant using a relay block:

```text
Use bootstrap/join-as-participant.md with:
{{PARTICIPANT_ID}} = reviewer-1
{{ROLE}} = REVIEWER
{{ALLOWED_ACTIONS}} = PROPOSE_ONLY
{{EXPECTED_RESPONSE}} = review_findings
{{RELAY_BLOCK}} = <paste full RELAY_BLOCK here>
```
