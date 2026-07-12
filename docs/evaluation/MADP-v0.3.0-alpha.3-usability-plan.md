# MADP v0.3.0-alpha.3 Usability Plan

Manual protocol-conformance trials must begin with `bootstrap/alpha3/load-protocol-from-github.md` and retain the highest active, non-superseded `MADP-PROTOCOL-LOAD-REPORT-v2` revision bound to the tested commit.

Release-signoff trials use the `FIELD_TRIAL` load profile. They require executed schema validation, `HASH_VERIFIED` provenance, an exact file inventory with SHA-256 values, and a matching `PROFILE_SOURCE_BINDING` for the selected start profile.

A failed report may be retained and superseded by a later revision with the same `report_id`. Only the highest active revision is eligible for a session.

A trial without a valid report may be retained as a negative bootstrap or degraded-mode observation, but it must not count toward protocol-conformance metrics or A3-REL-001 sign-off.

Manual trials use `MADP-FIELD-TRIAL-EVIDENCE-v2` and `results_version: 6`. One participant/run pair creates one `run_evidence` record containing the tested commit, protocol load report, report receipt ID, start-profile binding, and raw observation inventory. Scenario rows contain only scenario outcomes, one `run_id`, and the required `observation_refs`.

## Run-normalized evidence

- `run_id` is unique.
- participant ID plus run index is unique.
- a run must support at least one scenario result.
- a scenario must reference an existing run and existing observation IDs.
- loader reports, profile bindings, and raw observation hashes are not copied into every scenario row.
- the canonical report locator is `trial://<run_id>/protocol-load-report`.
- repository validation targets use `repo://<repository-relative-path>`.

Existing results-version 5 evidence may be preserved as historical input. Use `scripts/migrate_field_trial_results_v5_to_v6.py` before attempting release sign-off. Migration fails closed when rows assigned to one participant/run pair contain conflicting loader reports or profile bindings.

## Receipt-bound evidence

`manual_trials.validation_receipts` stores complete `VALIDATION_RECEIPT` documents. A release-signoff run must reference:

- one receipt that validates the complete `PROTOCOL_LOAD_REPORT` using `MADP_CANONICAL_JSON_V1`;
- every receipt named by the report's `schema_validation_records`;
- repository-bound validation records for both the inherited alpha.2 command registry and the alpha.3 command registry;
- the exact selected start-profile SHA-256;
- repository-relative raw observation files and matching SHA-256 values.

The release checker validates the field-trial evidence schema and receipt schemas, then recomputes artifact hashes, schema hashes, JSON Schema results, profile hashes, and every raw-observation hash. Unresolved, unused, self-reported, hash-mismatched, unknown-run, or unknown-observation references do not count as evidence.

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
