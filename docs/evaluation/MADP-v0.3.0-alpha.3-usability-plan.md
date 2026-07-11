# MADP-v0.3.0-alpha.3 Usability Evaluation Plan

This plan turns observed workflow problems into repeatable acceptance trials. It does not treat automated simulation as a substitute for human testing.

## Participants

At least one person unfamiliar with MADP and one person familiar with MADP should complete the manual set. A participant may complete more than one scenario, but results must identify the participant class.

## Required scenarios

1. Start a simple single-chat discussion with Quick Bootstrap.
2. Start a ChatGPT/Claude external review and return the response.
3. Invite a limited-capability AI using Plain Relay.
4. Recover from malformed or free-text output.
5. Run a multi-human team decision with named approvers and dissent.
6. Generate and review session minutes.
7. Use a separate Help chat and return to the facilitator chat.

## Acceptance criteria

- Task completion rate is at least 90 percent.
- Critical authority errors are zero.
- Unnecessary round-boundary pauses are zero.
- At least 90 percent of pauses communicate the next action correctly.
- Median recovery attempts for format failure is at most one.
- No participant mistakes AI opinion for user or team approval.

## Recording

Use `docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml`. Do not mark the manual gate PASS until observed results meet all mandatory thresholds. Automated walkthroughs may detect missing instructions and state transitions but cannot provide human comprehension evidence.
