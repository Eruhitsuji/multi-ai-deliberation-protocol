# MADP Command System v0.3.0-alpha.3

Status: normative implementation profile.

This profile specializes the command behavior defined by the alpha.3 protocol. It cannot override the protocol, command registry, command schema, or user authority.

## Registry composition

`registries/v0.3.0-alpha.3/commands.yaml` is an `ALPHA2_CANONICAL_SUPERSET`:

- inherited alpha.2 canonical commands: 20;
- alpha.3 canonical additions: 31;
- total canonical commands: 51;
- registry version: `MADP-COMMAND-REGISTRY-v0.2`.

All inherited alpha.2 commands remain representable by an alpha.3 command block.

## Collision policy

Canonical names always win. An alias may not equal any canonical name.

Therefore:

- `status` is the inherited broad workflow-status command;
- `session-status` is the explicit alpha.3 session report;
- `resume` resumes a workflow paused by `pause`;
- `session-resume` resumes a specific interrupted or imported session at an expected state version;
- `help-exit` exits Help;
- bare `RESUME` is not a Help command.

The previous alpha.3 aliases `status -> session-status` and `resume -> session-resume` are removed before release because they collided with inherited canonical commands.

## Parser record

A valid command block records:

- `invoked_name`;
- resolved canonical `command`;
- `alias_used`;
- command class and authority boundary;
- raw input;
- validation result;
- intended and prohibited effects.

Aliases never change authority or required arguments.

## Runtime boundary

The reference runtime is bounded internal-state validation. It never executes external actions. Safety-sensitive commands are applied only after exact sequencing and revision checks.
