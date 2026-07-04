# Operational Test Records

These records document manual operational tests that informed the `MADP-v0.2.5-rc.1` release candidate decision.

They are not tests of the RC files themselves. They record draft-version behavior that supported RC promotion, and their limitations remain part of the release-candidate risk profile.

Current records:

- `chatgpt-bootstrap-normal-001.yaml`: normal ChatGPT bootstrap and cross-chat relay dry run.
- `chatgpt-relay-mismatch-001.yaml`: fail-closed rejection of a relay source-state/snapshot mismatch.
- `gemini-manual-paste-load-001.yaml`: Gemini protocol load recovery by pasted canonical text when external URL retrieval was unavailable.
- `gemini-uploaded-bundle-smoke-001.yaml`: Gemini uploaded-bundle smoke test that exposed source-commit provenance ambiguity.

Additional model families, malformed relay categories, stale-state cases, facilitator recovery paths, and concurrent-state cases remain pending.
