
# MADP v0.3.0-alpha.3 Glossary

Status: normative additions to the alpha.2 glossary.

- **Alpha.2 Canonical Superset**: The alpha.3 command namespace retains every alpha.2 canonical command and adds new canonical commands without shadowing inherited names.
- **Canonical Command**: The registry-defined name stored after parsing. It is distinct from an input alias.
- **Command Alias**: A non-authoritative convenience spelling resolved to one canonical command. An alias cannot equal a canonical name.
- **Revision-Bound Artifact**: A session artifact carrying `session_id`, `source_state_version`, and, when mutable, its own positive revision.
- **Validation Evidence Manifest**: Machine-generated evidence that required checkers executed, including checker hashes and results.
- **Adaptive Role**: A temporary analytical function that does not change authority.
- **Assisted Conformance**: Participation mediated into protocol-compatible form.
- **Capability Profile**: A record of supported, unsupported, unknown, and extension capabilities.
- **Claim Ledger**: Revision-bound claims with type, importance, provenance, verification, contradiction, and decision usability.
- **Help Exit**: Revision-bound restoration of the phase recorded when Help began; represented by `help-exit`.
- **Normalization Record**: An auditable, revision-bound mapping from preserved raw text to a proposed interpretation.
- **Opinion-Only Participation**: Contribution without approval, execution, or direct canonical-state authority.
- **Plain Relay**: A bounded natural-language relay for limited-capability participants.
- **Session Import Report**: A non-mutating report produced before any imported session action can be confirmed.
- **Tolerant Ingestion / Strict Canonicalization**: Many input formats may be ingested, while only validated and auditable interpretations enter canonical records.
- **Validation Receipt**: A machine-executed record binding an artifact locator, exact revision or version, canonicalization method, artifact hash, schema hash, executor, result, and structured errors. Model self-assessment is not a validation receipt.
- **MADP Canonical JSON v1**: UTF-8 JSON with lexicographically sorted keys, no insignificant whitespace, preserved Unicode, and non-finite numbers forbidden; identified as `MADP_CANONICAL_JSON_V1`.
- **Schema Validation Record**: A load-report entry binding one repository target and hash to one schema and hash, one receipt ID, and one validation result.
- **Transition Validation Authority**: The deterministic authority to attest whether a state transition satisfies protocol conditions; distinct from human decision authority.
- **Independence Group**: Sources or participants that share material provider, model, retrieval, data, context, or prompt lineage and therefore must not be counted as fully independent without evidence.
- **Scope Check**: A revision-bound classification of the current topic as `IN_SCOPE`, `SCOPE_EXPANSION`, or `OUT_OF_SCOPE`.
- **Assurance Mode**: `NORMAL`, `REVIEW_REQUIRED`, or `STRICT`, describing how missing evidence or unresolved authority affects transition validation.
