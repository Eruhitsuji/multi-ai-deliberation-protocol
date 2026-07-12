# MADP v0.3.0-alpha.3 Usability Plan

Manual protocol-conformance trials must begin with `bootstrap/alpha3/load-protocol-from-github.md` and retain the highest active, non-superseded `MADP-PROTOCOL-LOAD-REPORT-v2` revision bound to the tested commit.

Release-signoff trials use the `FIELD_TRIAL` load profile. They require executed schema validation, `HASH_VERIFIED` provenance, an exact file inventory with SHA-256 values, and a matching `PROFILE_SOURCE_BINDING` for the selected start profile.

A failed report may be retained and superseded by a later revision with the same `report_id`. Only the highest active revision is eligible for a session.

A trial without a valid report may be retained as a negative bootstrap or degraded-mode observation, but it must not count toward protocol-conformance metrics or A3-REL-001 sign-off.

Manual trials may contain multiple participants, models, and repeated runs. Every result needs a unique `trial_id`, participant, run index, scenario ID, tested commit, load report, profile binding, raw observation reference and SHA-256, and protocol-load-report receipt ID.

## Receipt-bound evidence

`manual_trials.validation_receipts` stores complete `VALIDATION_RECEIPT` documents. A release-signoff row must reference:

- one receipt that validates the complete `PROTOCOL_LOAD_REPORT` using `MADP_CANONICAL_JSON_V1`;
- every receipt named by the report's `schema_validation_records`;
- repository-bound validation records for both the inherited alpha.2 command registry and the alpha.3 command registry;
- the exact selected start-profile SHA-256;
- a repository-relative raw observation file and matching SHA-256.

The release checker validates receipt schemas and recomputes artifact hashes, schema hashes, JSON Schema results, profile hashes, and raw-observation hashes. Unresolved, unused, self-reported, or hash-mismatched receipts do not count as evidence.

The canonical report locator is `trial://<trial_id>/protocol-load-report`. Repository validation targets use `repo://<repository-relative-path>`.

Manual trials must cover new-user startup, alpha.2 canonical `status`/`pause`/`resume`, detailed `session-status`, external relay recovery, limited participants, import confirmation, minutes review, team approval, and Help exit.

Release thresholds:

- task completion rate >= 90%;
- next-action understood rate >= 90%;
- median recovery attempts <= 1;
- critical authority errors = 0;
- critical unnecessary pauses = 0;
- unnecessary pause rate <= 5% of eligible workflow transitions.

Metrics are recalculated from scenario rows. Handwritten aggregate values must equal the calculated values.

An unnecessary pause is a user stop where no decision, missing information, external relay, safety/authority boundary, materially different path, or budget boundary required user action. Classification must identify the trial, scenario, transition, reason, and reviewer; reclassifying a pause without recorded rationale is not permitted.
