# MADP v0.3.0-alpha.4 Core Distribution Bundle

Status: prerelease distribution candidate profile. This profile defines a deterministic single-file delivery format for the alpha.4 Core Usability implementation. It does not create a tag, GitHub Release, stable release, formal release evidence, or external-action authorization.

## Purpose

The bundle reduces loading burden for GitHub-first and copy-and-paste use while preserving exact commit, path, byte-count, and SHA-256 provenance for every embedded source.

The bundle is useful for:

- supplying a complete alpha.4 Core Usability source set through one file;
- verifying that the distributed bytes match one repository commit;
- supporting QUICK and VERIFIED protocol loading;
- producing reproducible GitHub Actions artifacts without requiring a local checkout.

## Required sources

The canonical source order is defined by `scripts/generate_alpha4_core_compact_bundle.py` and includes:

- the alpha.3 compatibility protocol, glossary, canonical command registry, and deliberation schema;
- the alpha.4 README and Core Usability extension;
- the alpha.4 Workflow Macro profile and registry;
- the alpha.4 Core Usability and protocol-load-report schemas;
- the alpha.4 loader, QUICK start, and VERIFIED start profiles.

Every source is embedded byte-for-byte between machine-readable begin and end markers.

## Manifest binding

The companion manifest records:

- repository and immutable source commit;
- protocol and compatibility-base versions;
- bundle hash and byte count;
- loader hash and load-profile inventory digests;
- ordered source paths, roles, hashes, and byte counts;
- explicit false values for model-ingestion proof, formal release evidence, and external-action authorization.

A checker must regenerate the complete canonical bundle and manifest and require exact equality. Recomputing only the outer bundle hash is insufficient.

## Loading

The bundle may be used as `access_method: COMPLETE_BUNDLE` in `MADP-PROTOCOL-LOAD-REPORT-v3` when:

- the manifest validates;
- repository and source commit match the report;
- all selected profile sources are present exactly once;
- source hashes and bytes match;
- canonical regeneration passes.

The loader still requires a report. The bundle itself is not a `PROTOCOL_LOAD_REPORT`.

## Evidence and authority boundary

- Possession of the bundle does not prove that a model read every source.
- A model statement that it loaded the bundle is self-report unless independently verified.
- Agreement among AI systems is not evidence.
- Human Final Authority remains required.
- A Human Decision is not external-action authorization.
- The bundle does not complete A3-REL-001 or A3-REL-005.
- The bundle is not formal FIELD_TRIAL evidence.
- The generated artifact is a prerelease candidate input, not a published release.

## Failure behavior

Reject the bundle when any of these occur:

- repository, commit, protocol version, or compatibility base mismatch;
- duplicate, missing, reordered, or unexpected source paths;
- source bytes differ from the claimed commit;
- loader inventory digests do not match the loader path lists;
- embedded metadata or bytes differ from the manifest;
- appended or altered instructions cause canonical regeneration mismatch;
- privacy or authority boundaries are violated.
