---
bootstrap_version: 0.7-draft
protocol_version: MADP-v0.3.0-alpha.3
bootstrap_role: PROTOCOL_LOADER
report_version: MADP-PROTOCOL-LOAD-REPORT-v2
repository_template: '{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}'
commit_template: '{{MADP_COMMIT_SHA}}'
inventory_digest_algorithm: sha256-newline-paths-v1
source_sets:
  CORE:
  - README-v0.3.0-alpha.2.md
  - protocol/MADP-v0.3.0-alpha.2.md
  - protocol/GLOSSARY-v0.3.0-alpha.2.md
  - schemas/v0.3.0-alpha.2/command.schema.yaml
  - schemas/v0.3.0-alpha.2/command-registry.schema.yaml
  - schemas/v0.3.0-alpha.2/todo.schema.yaml
  - schemas/v0.3.0-alpha.2/context-package.schema.yaml
  - schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml
  - schemas/v0.3.0-alpha.2/review.schema.yaml
  - schemas/v0.3.0-alpha.2/relay.schema.yaml
  - registries/v0.3.0-alpha.2/commands.yaml
  - docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md
  - README-v0.3.0-alpha.3.md
  - protocol/MADP-v0.3.0-alpha.3.md
  - protocol/GLOSSARY-v0.3.0-alpha.3.md
  - schemas/v0.3.0-alpha.3/deliberation.schema.yaml
  - schemas/v0.3.0-alpha.3/command.schema.yaml
  - schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml
  - schemas/v0.3.0-alpha.3/command-registry.schema.yaml
  - schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml
  - registries/v0.3.0-alpha.3/commands.yaml
  - docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md
  PORTABILITY:
  - schemas/v0.3.0-alpha.3/session-portability.schema.yaml
  - docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md
  TEAM:
  - docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md
  HELP:
  - docs/profiles/MADP_HELP-v0.3.0-alpha.3.md
  MIGRATION:
  - schemas/v0.3.0-alpha.3/migration.schema.yaml
  - docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md
  MODEL_COMPARISON:
  - docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md
  SKILL_ADAPTERS:
  - docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md
  - skills/README.md
  - skills/madp-start/SKILL.md
  - skills/madp-facilitator/SKILL.md
  - skills/madp-participant/SKILL.md
  - skills/madp-recorder/SKILL.md
  - skills/madp-help/SKILL.md
  ADVANCED_PROFILES:
  - schemas/v0.3.0-alpha.3/advanced-profiles.schema.yaml
  - docs/profiles/SOURCE_AND_PARTICIPANT_INDEPENDENCE-v0.3.0-alpha.3.md
  - docs/profiles/BLIND_FIRST_ROUND_REVIEW-v0.3.0-alpha.3.md
  - docs/profiles/GENAI_USE_GOVERNANCE-v0.3.0-alpha.3.md
  - docs/profiles/AI_DEV_TASK_CONTRACT-v0.3.0-alpha.3.md
  - docs/profiles/COMMUNICATION_ALIGNMENT-v0.3.0-alpha.3.md
  - docs/profiles/ASSURANCE_MODES-v0.3.0-alpha.3.md
  - docs/profiles/OPINION_MAPPING_EXTENSION-v0.3.0-alpha.3.md
  - docs/profiles/DISSENT_LIFECYCLE-v0.3.0-alpha.3.md
  - docs/profiles/SESSION_RETENTION_AND_RECOVERY-v0.3.0-alpha.3.md
load_profiles:
  QUICK:
    required_sets:
    - CORE
    schema_validation_requirement: REPORT_ONLY
    minimum_provenance: SOURCE_REFERENCED
  VERIFIED:
    required_sets:
    - CORE
    - PORTABILITY
    - TEAM
    - HELP
    schema_validation_requirement: EXECUTED
    minimum_provenance: HASH_VERIFIED
  FIELD_TRIAL:
    required_sets:
    - CORE
    - PORTABILITY
    - TEAM
    - HELP
    schema_validation_requirement: EXECUTED
    minimum_provenance: HASH_VERIFIED
source_inventory_digests:
  QUICK: ba8c4b88c55de4d73ea82292fcaa38d2825096f3e08df041985bdab57be692c0
  VERIFIED: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
  FIELD_TRIAL: 7a4d1cb37d9e4ba3e8a305084009da563fdbcf7985e19156e24bf37f5a459a13
---

# Load MADP v0.3.0-alpha.3 From GitHub

Load the alpha.2 core and the selected alpha.3 source sets from one immutable GitHub commit before applying an alpha.3 start profile. This loader is informative and cannot override normative sources or higher-priority authority.

The caller must provide:

- `MADP_GITHUB_OWNER`;
- `MADP_GITHUB_REPOSITORY`;
- a 40-character hexadecimal `MADP_COMMIT_SHA`;
- `MADP_LOAD_PROFILE`: `QUICK`, `VERIFIED`, or `FIELD_TRIAL`.

Do not substitute `main`, `master`, a tag, or another movable ref for the commit SHA.

## Source-set selection

Use only the source sets named by frontmatter `load_profiles.<MADP_LOAD_PROFILE>.required_sets`.

- `QUICK` loads the shared protocol core.
- `VERIFIED` additionally loads portability, team, and Help sources.
- `FIELD_TRIAL` uses the same normative source coverage as `VERIFIED` and requires hash-verified provenance suitable for formal usability evidence.
- Migration, model-comparison, Skill-adapter, and advanced-profile sources are feature sets. Load them when that feature is used, but they are not part of ordinary QUICK completeness.

The selected ordered path list must match the corresponding frontmatter `source_inventory_digests` value using `sha256-newline-paths-v1`: SHA-256 of every selected path joined by `\n`, with one final `\n`.

## Capability preflight

Before retrieving individual sources, record whether the environment can retrieve exact bytes, compute SHA-256, execute a JSON Schema validator, and read a generated complete bundle. Select one source mode: `RAW_FILES`, `GITHUB_CONNECTOR`, `PROVIDED_TEXT`, `COMPLETE_BUNDLE`, or `NONE`.

When exact retrieval, hashing, or required schema validation is unavailable, prefer a commit-bound complete bundle. When no viable mode exists, emit one `INCOMPLETE` report immediately with a concrete bundle-upload or corrected-access next action. Do not spend a long run fabricating per-file attempts that cannot succeed.

## Retrieval procedure

For each selected path, attempt the exact commit-pinned Raw GitHub URL:

```text
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/<path>
```

A GitHub connector, repository file API, user-provided exact text, or generated complete protocol bundle is allowed only when provenance resolves to the same repository, commit, and path.

For each source:

- report `READ`, `PARTIALLY_READ`, or `FAILED`;
- preserve a non-empty `source_ref`;
- compute and record the SHA-256 of the exact bytes as `content_sha256` when possible;
- never infer, reconstruct, or silently replace unread content.

## Report revisions and recovery

A failed load remains in chat history. Therefore, retries do not require there to be only one report document.

- The first report uses a stable `report_id` and `revision: 1`.
- A retry reuses the same `report_id`, increments `revision`, and identifies the prior revision in `supersedes`.
- Exactly one revision may have `active: true`.
- A superseded revision remains evidence but is not eligible to start a session.
- Start profiles use only the highest active, non-superseded revision.

## Required output

Return one YAML document for each load attempt, before deliberation:

```yaml
PROTOCOL_LOAD_REPORT:
  report_version: MADP-PROTOCOL-LOAD-REPORT-v2
  report_id: PLR-001
  revision: 1
  supersedes: null
  active: true
  protocol_version: MADP-v0.3.0-alpha.3
  load_profile: QUICK | VERIFIED | FIELD_TRIAL
  repository: "{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}"
  repository_commit: "{{MADP_COMMIT_SHA}}"
  inventory_digest_algorithm: sha256-newline-paths-v1
  source_inventory_digest: "<digest for the selected load profile>"
  capability_preflight:
    exact_byte_retrieval: true | false
    sha256_available: true | false
    schema_validator_available: true | false
    complete_bundle_available: true | false
    selected_source_mode: RAW_FILES | GITHUB_CONNECTOR | PROVIDED_TEXT | COMPLETE_BUNDLE | NONE
  status: COMPLETE | INCOMPLETE
  files:
    - path: protocol/MADP-v0.3.0-alpha.3.md
      status: READ | PARTIALLY_READ | FAILED
      access_method: RAW_URL | GITHUB_CONNECTOR | PROVIDED_TEXT | COMPLETE_BUNDLE | OTHER
      source_ref: "commit-pinned URL, connector reference, or bundle entry"
      content_sha256: "<64 lowercase hexadecimal characters or null>"
  all_required_files_read: true | false
  schema_validation_capability: EXECUTED | AVAILABLE_NOT_EXECUTED | UNAVAILABLE
  schema_validation_executed: true | false
  schemas_applicable: []
  schemas_executed: []
  unvalidated_structured_sources: []
  inferred_unread_content: false
  provenance_level: HASH_VERIFIED | SOURCE_REFERENCED | SELF_ATTESTED
  authorized_start_profiles:
    - path: bootstrap/alpha3/quick-start.md
      repository: "{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}"
      repository_commit: "{{MADP_COMMIT_SHA}}"
      source_ref: "exact commit-pinned source reference"
  validation_receipt_refs: []
  limitations: []
  next_action:
    command: APPLY_START_PROFILE | RECOVER_PROTOCOL_SOURCE
    accepted_input: bootstrap/alpha3/quick-start.md | bootstrap/alpha3/verified-start.md | corrected source access
```

The `files` array must contain exactly one entry for every selected required path, in the selected inventory order, without omissions, additions, or duplicates.

`authorized_start_profiles` is empty for every `INCOMPLETE` report. For a `COMPLETE` report it is:

- only `quick-start.md` for a `QUICK` load;
- `quick-start.md` and `verified-start.md` for `VERIFIED` or `FIELD_TRIAL`.

When applying an authorized profile, the caller must provide a `PROFILE_SOURCE_BINDING` whose repository, commit, path, and source reference match the active report and the selected `authorized_start_profiles` entry.

## Completion conditions

Set `status: COMPLETE` only when:

- repository and commit are explicit and immutable;
- `source_inventory_digest` matches the selected profile inventory;
- every selected source is present exactly once and is `READ`;
- every file has a non-empty provenance reference;
- `all_required_files_read` is `true`;
- `inferred_unread_content` is `false`;
- the report revision is the active, highest revision for its `report_id`;
- schema validation satisfies the selected load profile;
- provenance satisfies the selected load profile.

For `QUICK`, schema validation may be unavailable or not executed, but that limitation must be explicit. `SOURCE_REFERENCED` or stronger provenance is required.

For `VERIFIED` and `FIELD_TRIAL`, schema validation must be `EXECUTED`, `schema_validation_executed` must be `true`, every applicable schema must be listed in `schemas_executed`, `unvalidated_structured_sources` must be empty, at least one machine-generated validation receipt must be referenced, every `content_sha256` must be present, and provenance must be `HASH_VERIFIED`.

If any requirement fails, set `status: INCOMPLETE`, set `authorized_start_profiles: []`, include at least one specific limitation, use `RECOVER_PROTOCOL_SOURCE`, stop, and report `PROTOCOL_SOURCE_UNAVAILABLE`. Prefer `complete protocol bundle upload` as the accepted recovery input when direct retrieval or hashing is unavailable. Do not apply a start profile or begin a MADP session. Validate the final report against `schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml` when a validator is available.
