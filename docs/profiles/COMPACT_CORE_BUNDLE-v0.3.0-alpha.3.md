# MADP v0.3.0-alpha.3 Compact Core Bundle

Status: experimental distribution profile. It does not replace the formal GitHub loader, a `PROTOCOL_LOAD_REPORT`, validation receipts, or FIELD_TRIAL evidence.

## Purpose

Reduce platform-specific failure caused by loading many commit-pinned files by generating one deterministic Markdown bundle containing the minimum Core Candidate sources required for human-mediated use.

The compact bundle is intended for environments that can reliably accept one uploaded or pasted file but cannot retrieve many GitHub files by exact commit.

## Included sources

The generator embeds exactly these repository sources, in order:

1. the alpha.3 protocol;
2. the canonical command registry;
3. the Workflow Macro registry;
4. the Core Candidate Profile;
5. the Workflow Macro Profile;
6. the Blind First Round Profile;
7. the alpha.3 quick-start bootstrap.

Every source is preserved byte-for-byte inside the generated bundle and recorded with path, role, byte count, and SHA-256 in a companion manifest.

## Provenance boundary

A generated bundle binds to:

```yaml
repository: owner/name
source_commit: 40-character-lowercase-commit
protocol_version: MADP-v0.3.0-alpha.3
profile: MADP_CORE_CANDIDATE
formal_release_evidence: false
```

The compact bundle does not prove that a model read every embedded byte. A consumer must not emit `PROTOCOL_LOAD_REPORT.status: COMPLETE` merely because the compact bundle exists.

Formal `FIELD_TRIAL` use still requires the existing loader, applicable Schema validation, validation receipts, raw observation inventory, and evidence collection path.

## Deterministic generation

```bash
python scripts/generate_alpha3_core_compact_bundle.py tmp/core-compact \
  --repository Eruhitsuji/multi-ai-deliberation-protocol \
  --source-commit <40-character-commit>

python scripts/check_alpha3_core_compact_bundle.py tmp/core-compact \
  --repository Eruhitsuji/multi-ai-deliberation-protocol \
  --source-commit <40-character-commit>
```

Generate the directory twice and compare it byte-for-byte before distribution.

## Safety boundary

The bundle does not grant approval authority, execution authorization, release authorization, publication authorization, or permission to infer missing IDs, revisions, state versions, exposure states, or evidence status.
