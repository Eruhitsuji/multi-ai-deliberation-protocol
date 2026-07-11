# MADP v0.3.0-alpha.3 Usability Plan

Manual protocol-conformance trials must begin with `bootstrap/alpha3/load-protocol-from-github.md` and retain a `COMPLETE` `MADP-PROTOCOL-LOAD-REPORT-v1` bound to the tested commit. `quick-start.md` and `verified-start.md` are post-load profiles, not protocol loaders.

A trial without a complete load report may be retained as a negative bootstrap or degraded-mode observation, but it must not count toward protocol-conformance completion metrics or A3-REL-001 sign-off.

Manual trials must cover new-user startup, alpha.2 canonical `status`/`pause`/`resume`, detailed `session-status`, external relay recovery, limited participants, import confirmation, minutes review, team approval, and Help exit.

Release thresholds:

- task completion rate >= 90%;
- next-action understood rate >= 90%;
- median recovery attempts <= 1;
- critical authority errors = 0;
- critical unnecessary pauses = 0;
- unnecessary pause rate <= 5% of eligible workflow transitions.

An unnecessary pause is a user stop where no decision, missing information, external relay, safety/authority boundary, materially different path, or budget boundary required user action. Classification must identify the scenario, transition, reason, and reviewer; reclassifying a pause without recorded rationale is not permitted.