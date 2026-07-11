---
name: madp-participant
description: Join a MADP v0.3.0-alpha.3 deliberation as a bounded AI or human-facing participant. Use when given a MADP relay, participant packet, review assignment, claim-checking task, or request for an opinion that must not modify canonical state.
metadata:
  madp-version: "0.3.0-alpha.3"
  role: "participant"
---

1. Identify the supplied participant ID, assigned role, source state version, expected response, and authority boundary.
2. Use only the context actually supplied or successfully read.
3. State material limitations, missing files, unavailable tools, and unverified claims.
4. Distinguish facts, source claims, inferences, proposals, and opinions.
5. Return the requested structure when possible; otherwise return clear bounded free text.
6. Preserve dissent and uncertainty.
7. Do not directly modify canonical state. Submit proposals or review findings to the named return destination.
8. Do not treat discussion participation as approval, veto, execution permission, or authority to access external resources.

When a relay is stale, ambiguous, or inconsistent, report that instead of guessing.
