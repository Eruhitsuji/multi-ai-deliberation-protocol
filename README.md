# Multi-AI Deliberation Protocol (MADP)

> Current release candidate: **MADP-v0.2.5-rc.1**

MADP is a service-neutral protocol for structured deliberation with AI systems, role-separated instances, human validators, and execution agents. It supports research, design, review, software development, and everyday decisions while keeping the user as the sole final decision-maker.

## Status and canonical files

This is a release candidate, not a final or stable release. The user remains the only actor who can approve a final release.

```yaml
current_release_candidate: "MADP-v0.2.5-rc.1"
previous_draft: "MADP-v0.2.5-draft"
status: "release candidate, not final"
```

Canonical repository documents are English.

- [`protocol/MADP-v0.2.5-rc.1.md`](protocol/MADP-v0.2.5-rc.1.md) - behavior, procedures, transitions, authorization
- [`protocol/GLOSSARY-v0.2.5-rc.1.md`](protocol/GLOSSARY-v0.2.5-rc.1.md) - normative term meanings and distinctions
- [`schemas/session-state-v0.2.5-rc.1.schema.yaml`](schemas/session-state-v0.2.5-rc.1.schema.yaml) - fields, types, required properties, enum spelling
- [`LICENSE`](LICENSE) - MIT License

Previous draft documents are retained for history:

- [`protocol/MADP-v0.2.5-draft.md`](protocol/MADP-v0.2.5-draft.md)
- [`protocol/GLOSSARY-v0.2.5-draft.md`](protocol/GLOSSARY-v0.2.5-draft.md)
- [`schemas/session-state-v0.2.5-draft.schema.yaml`](schemas/session-state-v0.2.5-draft.schema.yaml)

Recorded validation status for this release candidate:

- schema validation PASS
- semantic fixture validation PASS
- document consistency PASS
- bootstrap generation PASS
- GitHub Pages deployment PASS
- ChatGPT normal cross-chat relay PASS
- ChatGPT YAML serialization PASS
- ChatGPT malformed relay rejection PASS
- other model interoperability remains pending

README examples are informative. A conflict among authority domains is a specification defect and must be reported.

## Core principles

- The user is the sole final decision-maker.
- Majority vote alone is insufficient.
- Agreement among AI systems is convergence, not evidence.
- `SESSION_STATE` is the single logical source of truth.
- Share operative current state, not full conversation history.
- Separate deliberation outcome, user approval, and execution permission.
- Bind approval to a specific decision revision.
- AI participants may originate only unverified approval assertions.
- Unknown actions, empty scopes, and stale relay states fail closed.
- At most one facilitator may be active.

## Quick start

```text
Use MADP v0.2.5-rc.1.

Issue: Decide the minimum release contents for a small open-source project.
Fixed requirements:
- Keep the release small.
- The user is the final decision-maker.
Criteria:
- Usability
- Maintenance cost
- Extensibility

Start in MINIMAL / COMPACT mode.
Continue all non-blocked facilitator work in the same response.
Ask me only when user input, unavailable evidence, external transfer, or execution permission is required.
```

Before use, an AI should report which canonical files it actually read. A repository URL alone does not prove access. Raw file URLs pinned to a commit SHA are preferred for external review.

```yaml
protocol_load_status:
  requested: true
  confirmed_version: "0.2.5-rc.1"
  files_actually_read:
    - path: "protocol/MADP-v0.2.5-rc.1.md"
      result: "READ"
    - path: "protocol/GLOSSARY-v0.2.5-rc.1.md"
      result: "READ"
    - path: "schemas/session-state-v0.2.5-rc.1.schema.yaml"
      result: "READ"
  formal_schema_validation: false
  unread_or_unavailable_sections: []
```

## Minimal Session State

```yaml
session_state:
  meta:
    protocol: "MADP"
    protocol_version: "0.2.5-rc.1"
    schema_version: "0.2.5-rc.1"
    session_id: "MADP-EXAMPLE-001"
    state_version: 1
    parent_version: 0
    updated_at: "UNKNOWN"
    updated_by: "facilitator"

  goal: "Select a minimum release structure"

  current_issue:
    id: "ISSUE-001"
    status: "IN_PROGRESS"
    question: "Which files are required?"

  participants:
    - actor_id: "facilitator"
      type: "FACILITATOR"
      role: "FACILITATOR"
      status: "ACTIVE"

  decisions:
    - id: "DEC-001"
      revision: 1
      deliberation_outcome: "USER_DECISION_REQUIRED"
      approval_status: "PENDING"
      summary: "No release structure has been approved yet."

  next_step:
    internal:
      actor: "FACILITATOR"
      task: "Evaluate the minimum structure"
      blocking_input: null
    user:
      action_required: false
      prompt_action: "NO_ACTION_REQUIRED"
      task: null
      response_format: null
```

Validate with the versioned schema. An LLM-only review is `STRUCTURAL_CHECK_ONLY`, not formal validation.

## Condition example

```yaml
id: "COND-001"
statement: "Required tests pass"
applicability: "ACTIVE"
satisfaction: "IN_PROGRESS"
timing: "BEFORE_COMPLETION"
```

`SATISFIED` requires `basis`. `WAIVED_BY_USER` requires both `basis` and `user_confirmation`. `ACTIVE` to `NOT_APPLICABLE` changes require `applicability_basis`.

## Approval example

```yaml
approval:
  decision_id: "DEC-001"
  decision_revision: 2
  approver: "USER"
  assurance_level: "USER_CONFIRMED"
  assurance_origin: "USER_ACTION"
  occurred_at: "UNKNOWN"
  basis: "The user explicitly approved revision 2 in the current chat."
```

An AI may record only `UNVERIFIED_ASSERTION` on its own. Unverified assertions cannot authorize external, irreversible, privileged, or permission-escalated execution.

## Manual relay

The manual profile requires a marked `RELAY_BLOCK` containing metadata and `operative_session_state_snapshot`. The snapshot excludes full conversation history and obsolete detailed history, and is the operative source of truth for the receiving turn unless the receiver already holds newer official state.

Relay identity invariants:

```text
relay_block.session_id = relay_block.operative_session_state_snapshot.meta.session_id
relay_block.source_state_version = relay_block.operative_session_state_snapshot.meta.state_version
```

## Starting a new AI chat

Use the bootstrap prompts when starting an AI chat that has not already loaded MADP:

- [`bootstrap/README.md`](bootstrap/README.md) - overview, trust order, placeholders, and examples
- [`bootstrap/load-protocol-from-github.md`](bootstrap/load-protocol-from-github.md) - load commit-pinned canonical files and emit `PROTOCOL_LOAD_REPORT`
- [`bootstrap/start-facilitator.md`](bootstrap/start-facilitator.md) - initialize a facilitator safely
- [`bootstrap/join-as-participant.md`](bootstrap/join-as-participant.md) - join from a supplied `RELAY_BLOCK`
- [`bootstrap/recover-from-load-failure.md`](bootstrap/recover-from-load-failure.md) - recover when required files were not read

For release work, prefer direct file upload or commit-pinned Raw URLs. Do not rely on a movable branch URL as proof that the receiving AI read the protocol.

The repository `bootstrap/` files are templates. Generated bootstrap prompt files resolve only repository-specific placeholders (`{{MADP_GITHUB_OWNER}}`, `{{MADP_GITHUB_REPOSITORY}}`, and `{{MADP_COMMIT_SHA}}`) and keep session-specific placeholders for the user to fill at use time.

When GitHub Pages is enabled for Actions deployments, the publish workflow deploys generated prompts without committing them back to `main`. The Pages URL is a movable latest deployment URL; repository Pages URLs usually follow `https://<owner>.github.io/<repository>/`, and the exact deployment URL is reported by the workflow. The generated prompt contents pin canonical Raw URLs to the recorded source commit. For high-assurance use, check the generated `bootstrap/manifest.yaml` and source commit before use.

For AI environments that cannot retrieve external URLs directly, the Pages artifact also includes a generated complete-protocol bundle at `https://<owner>.github.io/<repository>/bootstrap/complete-protocol-bundle.txt`. This is not a static file committed in the repository; it is generated during the Pages workflow from the canonical source files.

## Validation

MADP v0.2.5-rc.1 validation uses Python 3.11 or newer with `jsonschema` and `PyYAML`.

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_schema.py
python scripts/validate_examples.py
python scripts/validate_semantics.py
python scripts/validate_participant_response.py
python scripts/check_markdown_links.py
python scripts/check_document_consistency.py
python scripts/check_bootstrap_prompts.py
python scripts/test_generate_bootstrap_prompts.py
python scripts/generate_bootstrap_prompts.py tmp/generated-bootstrap-validation --repository ExampleOwner/madp-fixture --commit-sha 0123456789abcdef0123456789abcdef01234567 --workflow-run-id RC_BUNDLE_LOCAL_TEST --generated-by LOCAL
python scripts/check_generated_bootstrap.py tmp/generated-bootstrap-validation --expect tests/generated-bootstrap/local-generation.yaml
```

On Windows PowerShell, using a local virtual environment:

```powershell
python -m venv .venv-validation
.\.venv-validation\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv-validation\Scripts\python.exe scripts\validate_schema.py
.\.venv-validation\Scripts\python.exe scripts\validate_examples.py
.\.venv-validation\Scripts\python.exe scripts\validate_semantics.py
.\.venv-validation\Scripts\python.exe scripts\validate_participant_response.py
.\.venv-validation\Scripts\python.exe scripts\check_markdown_links.py
.\.venv-validation\Scripts\python.exe scripts\check_document_consistency.py
.\.venv-validation\Scripts\python.exe scripts\check_bootstrap_prompts.py
.\.venv-validation\Scripts\python.exe scripts\test_generate_bootstrap_prompts.py
.\.venv-validation\Scripts\python.exe scripts\generate_bootstrap_prompts.py tmp\generated-bootstrap-validation --repository ExampleOwner/madp-fixture --commit-sha 0123456789abcdef0123456789abcdef01234567 --workflow-run-id RC_BUNDLE_LOCAL_TEST --generated-by LOCAL
.\.venv-validation\Scripts\python.exe scripts\check_generated_bootstrap.py tmp\generated-bootstrap-validation --expect tests\generated-bootstrap\local-generation.yaml
```

## Repository structure

```text
.
├── README.md
├── LICENSE
├── protocol/
│   ├── MADP-v0.2.5-rc.1.md
│   ├── GLOSSARY-v0.2.5-rc.1.md
│   ├── MADP-v0.2.5-draft.md
│   └── GLOSSARY-v0.2.5-draft.md
└── schemas/
    ├── session-state-v0.2.5-rc.1.schema.yaml
    └── session-state-v0.2.5-draft.schema.yaml
```

Future `profiles/` define reusable domain rules. Future `templates/` are starter kits built on Core and Profiles, such as software review, literature research, and everyday decision support.

## Migration from v0.2.4-draft

This release contains breaking schema changes. Import old state explicitly:

- map old decision `status` to `deliberation_outcome`;
- initialize `approval_status` to `PENDING` unless a valid current approval is re-established;
- initialize `revision` to `1`;
- map old condition status to `satisfaction` and set `applicability: ACTIVE`, except old `NOT_APPLICABLE` maps to `applicability: NOT_APPLICABLE` and `satisfaction: PENDING`;
- treat old free-form permissions as ungranted requests requiring review.

Active sessions must not auto-upgrade.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
