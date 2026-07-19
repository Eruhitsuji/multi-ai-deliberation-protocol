---
bootstrap_version: '0.1'
protocol_version: MADP-v0.3.0-alpha.4
bootstrap_role: PROTOCOL_LOADER
report_version: MADP-PROTOCOL-LOAD-REPORT-v3
repository_template: '{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}'
commit_template: '{{MADP_COMMIT_SHA}}'
inventory_digest_algorithm: sha256-newline-paths-v1
source_sets:
  CORE:
    - protocol/MADP-v0.3.0-alpha.3.md
    - registries/v0.3.0-alpha.3/commands.yaml
    - README-v0.3.0-alpha.4.md
    - protocol/MADP-v0.3.0-alpha.4-core-usability.md
    - docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md
    - registries/v0.3.0-alpha.4/workflow-macros.yaml
    - bootstrap/alpha4/quick-start.md
  ASSURANCE:
    - protocol/GLOSSARY-v0.3.0-alpha.3.md
    - schemas/v0.3.0-alpha.3/deliberation.schema.yaml
    - schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml
    - schemas/v0.3.0-alpha.4/protocol-load-report.schema.yaml
    - bootstrap/alpha4/verified-start.md
load_profiles:
  QUICK:
    required_sets:
      - CORE
    schema_validation_requirement: REPORT_ONLY
    minimum_provenance: SOURCE_REFERENCED
    authorized_start_profiles:
      - bootstrap/alpha4/quick-start.md
  VERIFIED:
    required_sets:
      - CORE
      - ASSURANCE
    schema_validation_requirement: EXECUTED
    minimum_provenance: HASH_VERIFIED
    authorized_start_profiles:
      - bootstrap/alpha4/quick-start.md
      - bootstrap/alpha4/verified-start.md
source_inventory_digests:
  QUICK: 25483e1cf887033d6b1df96c711990b89fe459078b81fb57137f995dfe89fd5c
  VERIFIED: 37e11df7cf15d4f481fc15dd9682ef903eb604c5d53f84f7948c8221cc75fa31
---

# Load MADP v0.3.0-alpha.4 from GitHub

Load the selected alpha.3 compatibility sources and alpha.4 Core Usability sources from one immutable GitHub commit before applying an alpha.4 start profile.

The caller supplies:

- `MADP_GITHUB_OWNER`;
- `MADP_GITHUB_REPOSITORY`;
- a 40-character lowercase hexadecimal `MADP_COMMIT_SHA`;
- `MADP_LOAD_PROFILE`: `QUICK` or `VERIFIED`.

Do not replace the commit SHA with `main`, another branch, or a movable tag.

## Retrieval

For each selected path, use the exact commit-pinned Raw GitHub URL:

```text
https://raw.githubusercontent.com/{{MADP_GITHUB_OWNER}}/{{MADP_GITHUB_REPOSITORY}}/{{MADP_COMMIT_SHA}}/<path>
```

A GitHub connector, repository file API, user-provided exact text, or generated alpha.4 Core distribution bundle is acceptable only when provenance resolves to the same repository, commit, path, and bytes.

Never infer, reconstruct, or silently replace unread content.

## Bundle access

A generated bundle may be used with `access_method: COMPLETE_BUNDLE` only when:

- its manifest validates against `schemas/v0.3.0-alpha.4/core-compact-bundle-manifest.schema.yaml`;
- repository and source commit match the requested load;
- the selected profile paths are present exactly once;
- per-source paths, byte counts, roles, and SHA-256 values match;
- the bundle and manifest pass canonical regeneration validation.

A bundle does not prove model ingestion or conformance.

## Report revisions

- The first report uses a stable `report_id` and `revision: 1`.
- A retry reuses the `report_id`, increments the revision, and identifies the superseded revision.
- Exactly one revision may be active.
- Start profiles use only the highest active, non-superseded revision.

## Required output

Return this YAML before deliberation:

```yaml
PROTOCOL_LOAD_REPORT:
  report_version: MADP-PROTOCOL-LOAD-REPORT-v3
  report_id: PLR-001
  revision: 1
  supersedes: null
  active: true
  protocol_version: MADP-v0.3.0-alpha.4
  compatibility_base: MADP-v0.3.0-alpha.3
  load_profile: QUICK
  repository: owner/repository
  repository_commit: 40-lowercase-hex-commit
  inventory_digest_algorithm: sha256-newline-paths-v1
  source_inventory_digest: 25483e1cf887033d6b1df96c711990b89fe459078b81fb57137f995dfe89fd5c
  status: COMPLETE
  files:
    - path: protocol/MADP-v0.3.0-alpha.3.md
      status: READ
      access_method: RAW_URL
      source_ref: commit-pinned source reference
      content_sha256: null
  all_required_files_read: true
  schema_validation_capability: UNAVAILABLE
  schema_validation_executed: false
  inferred_unread_content: false
  provenance_level: SOURCE_REFERENCED
  bundle_binding: null
  authorized_start_profiles:
    - path: bootstrap/alpha4/quick-start.md
      repository: owner/repository
      repository_commit: 40-lowercase-hex-commit
      source_ref: commit-pinned source reference
      content_sha256: null
  limitations:
    - schema validation was not executed
  next_action:
    command: APPLY_START_PROFILE
    accepted_input: bootstrap/alpha4/quick-start.md
```

The `files` array must contain exactly the selected path inventory in frontmatter order.

## Completion

Set `status: COMPLETE` only when:

- repository and commit are explicit and immutable;
- the selected path inventory and digest match frontmatter;
- every required source appears exactly once and is `READ`;
- every source has a non-empty `source_ref`;
- `all_required_files_read` is true;
- `inferred_unread_content` is false;
- the revision is active and not superseded;
- the selected profile's validation and provenance requirements are satisfied;
- authorized start profile entries match the same repository and commit.

For `QUICK`, schema validation may be unavailable, but the limitation must be explicit.

For `VERIFIED`, schema validation must be executed, provenance must be `HASH_VERIFIED`, and every source and authorized profile must have a SHA-256.

Otherwise set `status: INCOMPLETE`, set `next_action.command: RECOVER_PROTOCOL_SOURCE`, stop, and do not apply a start profile.
