# MADP Command System v0.3.0-alpha.3

Status: normative implementation profile for command discovery and parsing.

## Design

Commands use lowercase kebab-case canonical names and are organized by workflow group: `SESSION`, `PLANNING`, `PARTICIPANT`, `ROLE`, `RELAY`, `INGESTION`, `EVIDENCE`, `RECORDS`, `TEAM`, `HELP`, and `PORTABILITY`.

The command registry is the source of truth for canonical names, arguments, authority boundaries, effects, and prohibited effects. A parser may accept a documented alias, but it must store both the original invocation and the canonical command. Aliases never change authority.

## Human-friendly core

A first-time user should be able to operate the common workflow with:

- `start`
- `status`
- `checkpoint`
- `save` or `backup`
- `load` or `restore`
- `resume`
- `minutes`
- `help`
- `end`

These resolve to canonical registry commands. Unknown or ambiguous input is denied safely and routed to command help.

## Safety

- Read-only status and help commands cannot mutate canonical state.
- Export and record commands cannot disclose private content without confirmation.
- Import first creates a report and cannot silently merge or replace state.
- A session command never grants approval or execution authority for a substantive decision.
- Deprecated aliases remain documented until a migration note removes them.
