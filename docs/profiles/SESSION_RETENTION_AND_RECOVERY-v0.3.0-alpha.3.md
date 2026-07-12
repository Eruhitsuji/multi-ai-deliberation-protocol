# Session Retention and Recovery Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Purpose

Extend session portability with retention, recovery, and succession planning.

A retention plan classifies canonical session state, raw external responses, validation receipts, minutes, decision records, and related evidence. It records recovery-point objective, recovery-time objective, immutable or offline-copy requirement, restore-test interval, key custodian, successor custodian, and deletion policy.

A backup claim is not complete until at least one restore test has been performed or the absence of a restore test is explicitly recorded as a limitation. Encryption without key succession is not treated as recoverable retention. Exporting a session does not authorize uploading it to an external service.
