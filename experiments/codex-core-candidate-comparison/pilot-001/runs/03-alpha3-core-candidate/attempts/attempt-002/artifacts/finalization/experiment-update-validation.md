# Experiment update validation

- experiment.yaml pre-update SHA-256: `17928697742e6cd22bb0d3364d799911b2cd6bcf7826334922286303e6518fa1`
- experiment.yaml post-redaction SHA-256: `70eff442041d4a78850cd49e4a40f4eecffc402ab0963e54537d0a474e478d4b`
- experiment.yaml post-redaction bytes: `9455`
- semantic diff summary: only `runs[workflow=ALPHA3_CORE_CANDIDATE]` changed; non-target runs, task, top-level `formal_release_evidence`, experiment status, and conclusion are preserved by semantic comparison against HEAD.
- changed workflow: `ALPHA3_CORE_CANDIDATE`
- untouched workflows: `MANUAL_MULTI_AI`, `STANDARD_ALPHA3`, `MARKDOWN_VALIDATOR`
- untouched top-level fields: `experiment_status`, `formal_release_evidence`, `task`, `decision_ref`, `conclusion`
- schema validation: primary and post-completion validators PASS after Phase 4E; privacy validators pending final run after this manifest refresh.
- semantic validation: Human Final Authority decision content is unchanged; public decision source now references `artifacts/structured-comparison/human-final-authority-input-public-redacted.md`.
- privacy redaction validation: public personal identifier redaction applied; public exact private identifier scan is `0`; old raw input path references are `0`; identifier mapping is not published.
- boundary validation: `formal_release_evidence: false`, `conclusion.alpha4_authorized: false`, `pilot_completed: false`, no release/A3-REL-001/A3-REL-005 authorization.
- completion timestamp validation: original completion timestamp and seconds remain unchanged; privacy redaction is a post-finalization publication-prep phase.
- metrics validation: completion seconds `25000`; Core run Phase 4E metrics remain `33 / 21`; PRIVACY-1 is recorded separately as publication-prep human action `34 / 22` and does not alter the stopped completion timer.

- existing validator result after PRIVACY-1: FAIL due `jsonschema.exceptions.RefResolutionError: unknown url type: ""` in all three requested validators. Schema and script files were not modified.
- custom privacy validation result after PRIVACY-1: PASS.
- git diff --check result after PRIVACY-1: PASS.
- public blocker: existing validator resolver failure must be resolved or explained before publication.
- public blocker: local Git email is configured but not in the required GitHub noreply format.
