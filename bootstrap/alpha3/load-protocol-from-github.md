---
bootstrap_version: 0.8-draft
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
  VALIDATION_TOOLS:
  - scripts/generate_validation_receipt_v030_alpha3.py
  - docs/profiles/VALIDATION_EVIDENCE-v0.3.0-alpha.3.md
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
    - VALIDATION_TOOLS
    schema_validation_requirement: EXECUTED
    minimum_provenance: HASH_VERIFIED
  FIELD_TRIAL:
    required_sets:
    - CORE
    - PORTABILITY
    - TEAM
    - HELP
    - VALIDATION_TOOLS
    schema_validation_requirement: EXECUTED
    minimum_provenance: HASH_VERIFIED
source_inventory_digests:
  QUICK: ba8c4b88c55de4d73ea82292fcaa38d2825096f3e08df041985bdab57be692c0
  VERIFIED: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
  FIELD_TRIAL: c2f319b54f12389ea8728b0e6c6e7875c3485c1bf93b71faa16e4a4951437297
---

# Load MADP v0.3.0-alpha.3 From GitHub

Load the alpha.2 core and selected alpha.3 source sets from one immutable GitHub commit before applying an alpha.3 start profile. This loader is informative and cannot override normative sources or higher-priority authority.

The caller provides:

- `MADP_GITHUB_OWNER`;
- `MADP_GITHUB_REPOSITORY`;
- a 40-character hexadecimal `MADP_COMMIT_SHA`;
- `MADP_LOAD_PROFILE`: `QUICK`, `VERIFIED`, or `FIELD_TRIAL`.

Do not substitute `main`, `master`, a tag, or another movable ref for the commit SHA.

## Source-set selection

Use only the source sets named by `load_profiles.<MADP_LOAD_PROFILE>.required_sets`.

- `QUICK` loads the shared protocol core.
- `VERIFIED` and `FIELD_TRIAL` additionally load portability, team, Help, and deterministic validation tools.
- `FIELD_TRIAL` uses the same normative source coverage as `VERIFIED` and requires receipt-bound evidence suitable for formal usability evaluation.
- Migration, model-comparison, Skill-adapter, and advanced-profile sources are feature sets. Load them when that feature is used; they are not part of ordinary QUICK completeness.

The selected ordered path list must match the corresponding `source_inventory_digests` value using `sha256-newline-paths-v1`: SHA-256 of every selected path joined by `\n`, with one final `\n`.

## Capability preflight

Before retrieving individual sources, record whether the environment can:

- retrieve exact bytes;
- compute SHA-256;
- execute a JSON Schema validator;
- read a generated complete bundle.

Select one source mode: `RAW_FILES`, `GITHUB_CONNECTOR`, `PROVIDED_TEXT`, `COMPLETE_BUNDLE`, or `NONE`.

When exact retrieval, hashing, or required schema validation is unavailable, prefer a commit-bound complete bundle. When no viable mode exists, emit one `INCOMPLETE` report immediately with a concrete complete protocol bundle upload or corrected-access next action. Do not spend a long run fabricating per-file attempts that cannot succeed.

## Retrieval procedure

For each selected path, attempt the exact commit-pinned Raw GitHub URL:

```text
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/<path>
```

A GitHub connector, repository file API, user-provided exact text, or generated complete protocol bundle is allowed only when provenance resolves to the same repository, commit, and path.

For each source:

- report `READ`, `PARTIALLY_READ`, or `FAILED`;
- preserve a non-empty `source_ref`;
- compute SHA-256 of the exact bytes as `content_sha256` when possible;
- never infer, reconstruct, or silently replace unread content.

## Schema validation and receipts

For VERIFIED and FIELD_TRIAL, use `scripts/generate_validation_receipt_v030_alpha3.py` or an equivalent deterministic validator.

At minimum validate:

1. `registries/v0.3.0-alpha.2/commands.yaml` with `schemas/v0.3.0-alpha.2/command-registry.schema.yaml`;
2. `registries/v0.3.0-alpha.3/commands.yaml` with `schemas/v0.3.0-alpha.3/command-registry.schema.yaml`;
3. the final load report with `schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml`.

Preassign the final report receipt ID, include it in `validation_receipt_refs`, then compute the receipt over the complete report document using `MADP_CANONICAL_JSON_V1`. Registry receipts use `RAW_BYTES`.

A `schema_validation_record` binds one loaded repository target to one schema and receipt. `schemas_applicable` is the unique set of record schema paths. `schemas_executed` is the unique set of schema paths whose records are `PASS`. Every record receipt and the final report receipt must resolve to an actual `VALIDATION_RECEIPT`.

`unvalidated_structured_sources` concerns loaded instance documents for which an applicable repository schema exists. Schema-definition documents are checked as schemas by the validator and are not silently classified as validated instances.

The chat-visible output may remain the load report only, but every referenced receipt must be preserved as a retrievable artifact and supplied with formal trial evidence. A receipt ID without the receipt artifact is not evidence.

## Report revisions and recovery

A failed load remains in chat history.

- The first report uses a stable `report_id` and `revision: 1`.
- A retry reuses the same `report_id`, increments `revision`, and identifies the prior revision in `supersedes`.
- Exactly one revision may have `active: true`.
- A superseded revision remains evidence but is not eligible to start a session.
- Start profiles use only the highest active, non-superseded revision.

## Required output

Return one YAML report for each load attempt, before deliberation:

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
  source_inventory_digest: "<digest for selected load profile>"
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
  schema_validation_records:
    - target_ref: repo://registries/v0.3.0-alpha.3/commands.yaml
      target_sha256: "<sha256>"
      artifact_type: COMMAND_REGISTRY
      artifact_id: COMMANDS-A3
      artifact_version: MADP-COMMAND-REGISTRY-v0.2
      schema_path: schemas/v0.3.0-alpha.3/command-registry.schema.yaml
      schema_sha256: "<sha256>"
      receipt_ref: VAL-REGISTRY-A3
      result: PASS | FAIL
  unvalidated_structured_sources: []
  inferred_unread_content: false
  provenance_level: HASH_VERIFIED | SOURCE_REFERENCED | SELF_ATTESTED
  authorized_start_profiles:
    - path: bootstrap/alpha3/quick-start.md
      repository: "{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}"
      repository_commit: "{{MADP_COMMIT_SHA}}"
      source_ref: "exact commit-pinned source reference"
      content_sha256: "<sha256 of exact profile bytes>"
  validation_receipt_refs:
    - VAL-REGISTRY-A2
    - VAL-REGISTRY-A3
    - VAL-PLR-001-R1
  limitations: []
  next_action:
    command: APPLY_START_PROFILE | RECOVER_PROTOCOL_SOURCE
    accepted_input: bootstrap/alpha3/quick-start.md | bootstrap/alpha3/verified-start.md | complete protocol bundle upload | corrected source access
```

The `files` array contains exactly one entry for every selected required path, in selected inventory order, without omissions, additions, or duplicates.

`authorized_start_profiles` is empty for every `INCOMPLETE` report. For a `COMPLETE` report it is:

- only `quick-start.md` for QUICK;
- `quick-start.md` and `verified-start.md` for VERIFIED or FIELD_TRIAL.

Each authorization includes the exact profile-byte SHA-256. When applying a profile, the caller provides `PROFILE_SOURCE_BINDING` whose repository, commit, path, source reference, profile hash, and inventory digest match the active report.

## Completion conditions

Set `status: COMPLETE` only when:

- repository and commit are explicit and immutable;
- inventory digest matches the selected profile;
- every selected source is present once and `READ`;
- every source has a non-empty provenance reference;
- `all_required_files_read` is true;
- `inferred_unread_content` is false;
- the report revision is active and highest for its `report_id`;
- validation and provenance satisfy the selected load profile.

For QUICK, schema validation may be unavailable or not executed, but the limitation is explicit. `SOURCE_REFERENCED` or stronger provenance is required.

For VERIFIED and FIELD_TRIAL:

- schema validation is `EXECUTED`;
- both command registries have PASS records and actual receipts;
- `schemas_applicable`, `schemas_executed`, records, and receipt references agree;
- `unvalidated_structured_sources` is empty;
- the final report has a deterministic PASS receipt;
- every selected file and authorized profile has a valid SHA-256;
- provenance is `HASH_VERIFIED`.

If any requirement fails, set `status: INCOMPLETE`, set `authorized_start_profiles: []`, include at least one specific limitation, use `RECOVER_PROTOCOL_SOURCE`, stop, and report `PROTOCOL_SOURCE_UNAVAILABLE`. Prefer complete protocol bundle upload when direct retrieval or hashing is unavailable. Do not apply a start profile or begin a MADP session.
