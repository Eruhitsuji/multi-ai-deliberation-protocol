# Dissent Lifecycle Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile.

## Purpose

Preserve material dissent as an auditable history while permitting correction, privacy protection, and lawful redaction.

Use `dissent_record` from `advanced-profiles.schema.yaml`.

## Lifecycle

`OPEN`, `RESOLVED`, `OVERRIDDEN`, `SUPERSEDED`, and `REDACTED` are status changes, not silent deletion. Preserve the original-record hash. Resolution records the resolver and evidence. Redaction uses a reason and audit tombstone; it does not rewrite history as if the dissent never existed.

A decision may proceed while dissent remains open when the named decision authority chooses to do so, but the record must not describe the dissent as resolved. Retaliation, unauthorized identity disclosure, or suppression of minority input is outside this profile's permitted behavior.
