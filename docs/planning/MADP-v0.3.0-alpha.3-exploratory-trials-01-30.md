# MADP v0.3.0-alpha.3 Exploratory Trials #01-#30

Status: design-input corpus; not, by itself, formal release evidence.

## Source and evidence boundary

The reviewed archive contains the chat transcripts, appendices, user comments,
and selected deliverables for trials #01 through #30.

```yaml
archive_file: madp_test.zip
archive_sha256: 2cf9a9d50eb48f740307a1c9f71d99f6155e36cf73af6fc9722360d6c4c2e2ab
archive_size_class: approximately_1_3_mib
reviewed_trial_range: "#01-#30"
```

These records are valuable for product direction, usability findings, loader
compatibility, and experimental design. They do not automatically satisfy
`A3-REL-001`. A trial counts as formal release evidence only when it is collected
against the exact tested commit through the required FIELD_TRIAL load,
receipt-bound evidence, scenario review, and human sign-off path.

## Trial generations

| Range | Main commit | Interpretation |
|---|---|---|
| #01-#04 | `93ee04d14a9e2e79ea4ee44a8c3bdb3b714444ad` | Pre-loader exploration. Useful for workflow and role ideas, not protocol-load evidence. |
| #05-#14 | `6cf8bac92c5bdb911e5e6832401ba5b7d10202ff` | First loader generation. Exposed load latency, service differences, command discoverability, and failure handling. |
| #15-#30 | `7183e2345c1cea5cc67f776d6996b0e34b2c0f6b` | Hardened-baseline QUICK exploration across ChatGPT, Claude, Gemini, and Copilot families. |

## Trial index

| ID | Primary model or service | Main focus retained for the next update |
|---|---|---|
| #01 | GPT-5.6 Sol High | Light workflow, backup topic, relay and external opinion participation. |
| #02 | GPT-5.6 Sol High | Verified-start usability and multi-detector / person-detection deliberation. |
| #03 | Claude Opus 4.8 Medium | Project-file startup and facilitator-style exploration. |
| #04 | Gemini Flash | Session setup and non-loader behavior. |
| #05 | GPT-5.6 Sol High | Loader, profile binding, relay, export and import behavior. |
| #06 | Claude Opus 4.8 Medium | Loader behavior and `OPINION_ONLY` participation. |
| #07 | GPT-5.6 Sol High | Information-bias deliberation and human-facing flow. |
| #08 | Gemini Flash | Loader compatibility and failure experience. |
| #09 | Claude Opus 4.8 Medium | Human-readable facilitation and an AI-driven development standard draft. |
| #10 | GPT-5.6 Sol High | Command-choice UX and Pol.is schema / hashing extension drafts. |
| #11 | GPT o3 Medium | Loader behavior on a faster ChatGPT-family model. |
| #12 | GPT-5.5 Fast | Loader behavior on the fastest tested ChatGPT-family mode. |
| #13 | GPT-5.6 Medium | Loader behavior on a medium reasoning mode. |
| #14 | Claude Opus 4.8 Medium | Loader and facilitator comparison. |
| #15 | GPT-5.6 Medium | Minimal laptop-priority session and goal-to-start sequencing. |
| #16 | GPT-5.6 Sol High | The same minimal usability task under a higher reasoning mode. |
| #17 | GPT-5.6 Sol High | AI-driven development and assigning work to multiple coding agents. |
| #18 | Claude Fable 5 High | AI-driven development design with external proposal-only participants. |
| #19 | Gemini 3.1 Pro | GitHub loader compatibility. |
| #20 | Gemini 3.1 Pro | ZIP-based repository loading fallback. |
| #21 | Microsoft Copilot Search Mode | Quick-start and loader interpretation. |
| #22 | Microsoft Copilot Think Deeper | Fail-closed loader and source-access behavior. |
| #23 | GPT-5.6 Sol High | Value and limits of separate chats using the same model family. |
| #24 | GPT-5.5 High | Convergence when participant opinions conflict. |
| #25 | GPT-5.6 Sol High | Applying the File over App principle to MADP. |
| #26 | GPT-5.6 Sol High | MADP with Kiro for AI-driven development; guide artifact. |
| #27 | GPT-5.6 Sol High | Ideal number of external AI services. |
| #28 | Claude Opus 4.8 Medium | Dynamic role mapping and service-capability allocation. |
| #29 | GPT-5.6 Sol High | Comparison of model and service characteristics. |
| #30 | GPT-5.6 Sol High facilitator plus separately prompted reviewers | Competitors, strengths, weaknesses, MADP Core, Blind First Round, command layers, evidence, and version strategy. |

## Cross-trial findings

### Loading and portability

- Loading many commit-pinned files can take too long, especially in some
  ChatGPT-family environments.
- Claude-family runs were often faster and more conversational, but this is an
  observed usability difference rather than a protocol guarantee.
- Gemini and Copilot runs showed that URL, exact-byte, or ZIP capabilities vary
  materially by service and mode.
- A loader must fail closed when exact required content cannot be obtained.
- The next distribution experiment should compare a compact commit-bound bundle
  with the current multi-file loader, without weakening formal provenance.

### Human-facing operation

- Users can lose track of the current question and the exact next input.
- Choice-oriented Next Actions and a facilitator that returns decisions to the
  human at appropriate points are easier to use.
- Natural-language operation is needed for beginners, while canonical commands
  must remain available and machine-recorded.
- A common output contract should expose Current State, Current Question,
  Facilitator Action, Human Decision Required, Next Action, and Canonical
  Expansion without forcing every model into the same prose style.

### Participant diversity and correlation

- Separate chats using the same model can create useful alternative paths, but
  they must be recorded as correlated or semi-independent rather than counted as
  independent evidence.
- Dynamic role assignment should consider available services, capabilities,
  usage constraints, information access, and independence groups.
- Manual copy-and-paste is a useful safety and accessibility boundary, not merely
  a temporary workaround.

### Deliberation quality

- Convergence procedures must preserve unresolved dissent and record why a human
  proceeded despite it.
- Agreement reached after participants see one another's responses is not
  independent corroboration.
- Blind First Round provides a baseline before direct cross-participant exposure
  and should remain a Core requirement for multi-participant deliberation.
- Raw responses must remain distinct from normalization, claims, summaries, and
  decisions.

## Trial #30 decision

The primary #30 chat correctly stopped protocol loading with
`PROTOCOL_LOAD_REPORT.status: INCOMPLETE` and continued as ordinary research and
design discussion. It was therefore not a formal MADP session and is not
FIELD_TRIAL evidence. The separately prompted reviewers are design inputs whose
independence and correlation must not be overstated.

After reviewing those inputs, the human owner accepted the planning direction
recorded as `DEC-MADP-CORE-001`. The decision is authoritative as a human
repository-planning decision, not as proof of protocol conformance.

The accepted direction is:

1. preserve alpha.3 as the experimental baseline;
2. defer alpha.4 implementation;
3. make non-metered manual use and local validation first-class Core behavior;
4. retain Human Final Authority and Blind First Round;
5. retain fine-grained canonical commands as the machine layer;
6. add eight human-facing Workflow Macros as a non-atomic expansion layer;
7. separate claim form, verification state, and multidimensional evidence;
8. retain minimum protocol binding in Core and complete receipt chains in
   Assured / formal FIELD_TRIAL use;
9. compare four workflows before deciding whether alpha.4 begins.

The authoritative planning record for this repository is
`docs/planning/DEC-MADP-CORE-001.yaml`.

## Next comparative experiment

Use one bounded decision task across:

1. ordinary manual multi-AI copy-and-paste;
2. standard alpha.3;
3. alpha.3 with the Core Candidate Profile and Workflow Macros;
4. Markdown plus typed files and a local validator.

Record at least completion time, human actions, canonical commands, unclear next
actions, corrections, authority errors, stale-revision errors, Blind First Round
status, dissent preservation, decision reconstruction, and perceived burden.
