# MADP v0.3.0-alpha.3 — Inclusive, Guided, and Team-Aware Deliberation

Status: merged to `main` for experimental field use; not release-ready, tagged, or published.

Alpha.3 extends the published alpha.2 core. It is an **additive compatible layer**, not a replacement command namespace.

## Review hardening

- all 20 alpha.2 canonical commands remain canonical;
- 31 alpha.3 commands are added, for 51 canonical commands total;
- `status`, `resume`, and `pause` keep alpha.2 meanings;
- `session-status`, `session-resume`, and `help-exit` are distinct;
- plans, roles, claims, responses, Help, and records are bound to session and state revision;
- parser and bounded runtime tests exercise all command names and critical sequencing;
- schema rejects important unverified factual claims used for decisions, approval records without approvers/revision, missing named approvers, and OPINION_ONLY authority escalation;
- migration tests transform actual alpha.2 inputs and record failures as well as success;
- release readiness requires machine-generated validation evidence, not handwritten `DONE` claims;
- ChatGPT and Claude distributions contain the same five Agent Skills;
- translation audit is explicitly a freshness/marker audit, not semantic-equivalence proof.

## Bootstrap order

Alpha.3 use has two separate phases:

1. run `bootstrap/alpha3/load-protocol-from-github.md` against one immutable commit and obtain a `COMPLETE` `PROTOCOL_LOAD_REPORT`;
2. apply `bootstrap/alpha3/quick-start.md` or `bootstrap/alpha3/verified-start.md`.

Start profiles do not load the protocol. When the load report is missing or incomplete, they must fail closed with `PROTOCOL_NOT_LOADED` instead of inferring unread rules.

## Normative source order

1. higher-priority user and platform rules;
2. normative schemas for artifact structure;
3. protocol core and versioned protocol extension;
4. versioned command registry for command names and metadata;
5. normative implementation profiles explicitly named by the protocol;
6. glossary;
7. informative bootstraps, Skills, translations, and guides.

Conflicts are defects and must be reported. The stricter authority boundary applies until resolved.

## Release status

```yaml
implementation_status: RELEASE_CANDIDATE_CONTENT_READY
integration_status: MERGED_TO_MAIN
evaluation_status: FIELD_TRIAL_IN_PROGRESS
release_ready: false
tagged: false
published: false
manual_usability_sign_off: collecting_practical_use_evidence
final_main_audit: waiting_for_field_trial
```

Practical-use observations and defects should identify the tested commit. Alpha.2 remains the current published bootstrap until field-trial evidence is signed off and the final-main audit passes.