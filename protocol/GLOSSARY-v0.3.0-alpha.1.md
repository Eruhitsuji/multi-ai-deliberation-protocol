# MADP Glossary v0.3.0-alpha.1

Normative terms use the exact spelling below.

- **Affirmative Approval**: `APPROVE`, `APPROVE_WITH_CONDITIONS`, or `APPROVE_WITH_CHANGES` bound to a specific decision revision.
- **Assurance Level**: confidence category attached to an assertion or grant. Core values are `UNVERIFIED_ASSERTION`, `USER_CONFIRMED`, and `EXTERNALLY_VERIFIED`.
- **Assurance Origin**: provenance category explaining where trusted assurance came from. Core values are `USER_ACTION` and `EXTERNAL_VALIDATION`.
- **Canonical Source**: an editable normative protocol, glossary, or multi-file schema artifact.
- **Convergence**: agreement among AI roles, models, or instances. Convergence is not evidence.
- **Decision Revision**: the exact numbered revision to which approval is bound.
- **Execution Gate**: the fail-closed check performed immediately before an external, privileged, irreversible, or permission-sensitive action.
- **Facilitator**: a participant whose machine-readable `type` is `FACILITATOR`. Free-form role text does not confer facilitator authority.
- **Generated Distribution**: a reproducible non-editable artifact derived from canonical sources, such as a self-contained schema or upload bundle.
- **Governance Artifact**: a non-normative but release-blocking repository artifact, such as the traceability matrix.
- **MADP_JCS_V1**: the RFC 8785-based canonicalization profile restricted to the MADP JSON-compatible data model.
- **Migration Evidence**: external structured evidence used to justify preservation or transformation of legacy authority during migration.
- **Operative Session State Snapshot**: the bounded current state embedded in a relay block.
- **Permission Grant**: active authority with recognized action, non-empty scope, trusted assurance, and explicit origin.
- **Permission Request**: non-authoritative requested authority. It may represent unknown actions for escalation.
- **POST_INGRESS_BASELINE**: digest provenance showing a new local integrity baseline computed after receipt; it does not prove transport or sender authenticity.
- **PROPOSE_ONLY**: authority boundary that permits analysis and proposals but no privileged execution.
- **Quarantine**: safe target-version representation of an item that cannot retain authoritative status. A migration completed with quarantined items is still `COMPLETED`, not `PARTIAL`.
- **Relay Block**: the transfer root containing relay metadata and an operative snapshot.
- **Role Actor**: a role played within the same model/context. It has independence level `I0` unless separately instantiated.
- **Session State**: the sole logical source of truth for a deliberation session.
- **Snapshot Digest**: digest over `relay_block.operative_session_state_snapshot` only.
- **Trusted Grant**: a grant supported by `USER_CONFIRMED`/`USER_ACTION` or `EXTERNALLY_VERIFIED`/`EXTERNAL_VALIDATION` plus reference.
- **USER_ESCALATION_REQUIRED**: non-authoritative status indicating that user review is required before authority may be granted.
- **Validation Receipt**: structured record identifying the validator, schema, instance, result, and error count for an executed validation.