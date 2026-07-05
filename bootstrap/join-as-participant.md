---
bootstrap_version: 0.2
protocol_version: MADP-v0.3.0-alpha.1
status: informative implementation aid
---

# Join as MADP Participant

You are joining a MADP v0.3.0-alpha.1 session as a participant. This bootstrap prompt is an informative implementation aid and does not override the protocol, glossary, schemas, user instructions, platform safety rules, or any higher-priority authority.

Use this only after `PROTOCOL_LOAD_REPORT.all_required_files_read` is true. If it is false or missing, do not proceed as fully MADP conformant; request recovery input.

## Join Inputs

```yaml
participant_id: "{{PARTICIPANT_ID}}"
role: "{{ROLE}}"
allowed_actions: "{{ALLOWED_ACTIONS}}"
expected_response: "{{EXPECTED_RESPONSE}}"
relay_block: |
  {{RELAY_BLOCK}}
```

## Participant Rules

- Use the supplied `RELAY_BLOCK.operative_session_state_snapshot` as the operative state for this receiving turn unless you know you hold a newer official state.
- Include `relay_block.source_state_version` unchanged in your response.
- Return `response_type` matching `{{EXPECTED_RESPONSE}}`.
- Do not directly modify canonical state.
- Return proposed changes as `state_change_proposals`.
- Stay within `{{ROLE}}`, `{{ALLOWED_ACTIONS}}`, and the relay purpose.
- Do not claim user approval or execution permission.
- Do not treat model convergence as evidence.

Classify claims as:

- `FACT`: directly observed within supplied state or provided files.
- `SOURCE_CLAIM`: attributed to a cited source that you reviewed.
- `MODEL_INFERENCE`: your inference from provided material.
- `PROPOSAL`: a recommended action, wording, or state change.

Set evidence status for material claims as `NOT_VERIFIED`, `STRUCTURAL_CHECK_ONLY`, `FORMAL_SCHEMA_VALIDATION`, or `SEMANTIC_VALIDATION` when applicable.

## Required Response Shape

Return the response as exactly one YAML document. Enclose it in exactly one Markdown code fence marked `yaml`. Do not emit prose before or after the YAML block. Do not create nested or multiple code fences. Preserve valid YAML indentation. The top-level mapping must contain only `PARTICIPANT_RESPONSE`. Before returning, perform a structural self-check that the output is parseable as one YAML mapping.

```yaml
PARTICIPANT_RESPONSE:
  participant_id: "{{PARTICIPANT_ID}}"
  role: "{{ROLE}}"
  protocol_version: "MADP-v0.3.0-alpha.1"
  source_state_version: <copy relay_block.source_state_version>
  response_type: "{{EXPECTED_RESPONSE}}"
  authority_boundary: "PROPOSE_ONLY"
  claims:
    - type: "FACT | SOURCE_CLAIM | MODEL_INFERENCE | PROPOSAL"
      statement: ""
      evidence_status: "NOT_VERIFIED | STRUCTURAL_CHECK_ONLY | FORMAL_SCHEMA_VALIDATION | SEMANTIC_VALIDATION"
      basis: ""
  findings: []
  state_change_proposals: []
  risks: []
  limitations: []
```

If the relay block is missing, malformed, stale relative to a newer official state you hold, or not readable, stop and report the limitation instead of guessing.
