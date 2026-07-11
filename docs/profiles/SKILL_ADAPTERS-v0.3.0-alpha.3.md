# MADP Skill Adapter Profile v0.3.0-alpha.3

MADP may be packaged as Claude Skills, ChatGPT instructions, or generic bootstrap prompts.

Adapters are informative implementation aids. Normative protocol, schemas, registry, user instructions, and platform rules remain higher authority.

Shared requirements:

- state the MADP version;
- expose tool and execution capabilities;
- default to `PROPOSE_ONLY`;
- preserve raw external responses;
- provide next-action guidance;
- distinguish Help, facilitator, participant, and recorder roles;
- avoid treating multiple role actors in one chat as independent evidence;
- work without a skill through generic prompts;
- be tested for version drift.

A skill with file, network, or code execution ability must expose those capabilities and must not infer execution permission from deliberation participation.
