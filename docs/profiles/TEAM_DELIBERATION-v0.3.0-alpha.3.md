# Team Deliberation Profile v0.3.0-alpha.3

This profile supports multiple human participants alongside AI participants.

## Setup

1. Register each participant and participation channel.
2. Separate organizational role, deliberation role, and authority role.
3. Select a decision method.
4. Name decision owners, approvers, and veto holders where applicable.
5. Set `silence_counts_as_consent: false`.
6. Define privacy and dissent handling.
7. Attach every asynchronous response to the state revision reviewed.

Direct statements, proxy statements, imported minutes, and facilitator summaries are distinct provenance classes. A statement relayed by one human on behalf of another remains unconfirmed unless the represented person or an authorized process confirms it.

A recommendation, majority tendency, model convergence, and formal approval are separate states. Material dissent remains in state and minutes, including whether it was resolved, accepted as a trade-off, deferred, or overridden by an authorized policy.

Private input is excluded from relays, external AI prompts, shared state, and minutes unless the source permits its use for the stated purpose.
