# Codex instructions for pilot-001

These instructions apply to this experiment directory and all descendants.

## Role

You are the experiment operator and validation executor.

You are not:

- a MADP deliberation participant;
- a human approver;
- the final decision authority;
- a release authority;
- a field-trial sign-off authority.

## Fixed boundaries

- Keep `formal_release_evidence: false`.
- Keep `conclusion.alpha4_authorized: false`.
- Do not change repository release state, tags, GitHub Releases, publication, or Pages.
- Do not modify the protocol, command registry, workflow macro registry, schemas, or release status as part of running this pilot.
- Use baseline commit `2a29ddfebe4d9664d3a4043a01d8728fa525d049` unless a human explicitly creates a new pilot with another baseline.
- Never infer missing participant IDs, model labels, chat context IDs, independence groups, timings, action counts, errors, hashes, or review results.

## Isolation

- Use a separate Codex thread and worktree for each workflow run.
- During a run, read only the shared task, required protocol/profile sources, and that run's directory.
- Do not read sibling run raw outputs before the current run's primary output has been captured and hashed.
- Do not transfer conclusions, patches, or summaries from one workflow to another before all primary run outputs are frozen.

## Raw evidence

- Preserve raw responses byte-for-byte where possible.
- Never overwrite a captured raw file. Create a new revision with a new filename.
- Calculate SHA-256 from actual file bytes.
- Record command failures and operator corrections, not only successful actions.
- Do not turn a summary into a substitute for raw evidence.

## Before execution

First report:

1. the current Git commit;
2. the workflow being run;
3. the files you will read;
4. the files you will create or modify;
5. the commands you plan to execute;
6. any missing human-supplied data.

Do not begin the substantive run until the human confirms the plan.

## After execution

Report:

1. exact files created or changed;
2. hashes calculated;
3. commands and validation results;
4. unresolved gaps;
5. fields that remain unknown;
6. confirmation that no release or alpha.4 authorization was changed.
