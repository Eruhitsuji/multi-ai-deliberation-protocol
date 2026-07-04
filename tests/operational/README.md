# Operational Test Records

These records document manual operational tests that informed release-candidate decisions.

Some records are historical evidence for earlier candidates. Do not rewrite their `tested_protocol_version` or observed facts when preparing a newer candidate.

Current records:

- `chatgpt-bootstrap-normal-001.yaml`: normal ChatGPT bootstrap and cross-chat relay dry run.
- `chatgpt-relay-mismatch-001.yaml`: fail-closed rejection of a relay source-state/snapshot mismatch.
- `claude-rc2-raw-url-load-smoke-001.yaml`: Claude rc.2 Raw URL load smoke test.
- `gemini-rc2-uploaded-bundle-load-smoke-001.yaml`: Gemini rc.2 uploaded complete-bundle load smoke test.
- `gemini-manual-paste-load-001.yaml`: Gemini protocol load recovery by pasted canonical text when external URL retrieval was unavailable.
- `gemini-uploaded-bundle-smoke-001.yaml`: Gemini uploaded-bundle smoke test that exposed source-commit provenance ambiguity.
- `rc2-release-readiness.yaml`: rc.2 release-readiness checklist, ready for user release decision.

The Claude and Gemini rc.2 records report the same protocol version and source commit, and both report all four canonical files as read. Formal schema validation was outside the scope of these runtime load tests, and universal interoperability is not claimed.

Additional malformed relay categories, stale-state cases, facilitator recovery paths, and concurrent-state cases remain pending.
