# Model Response Comparison Profile v0.3.0-alpha.3

Use this profile to compare responses to controlled prompts without overgeneralizing from one run.

Record the exact prompt and hash, provider, product, displayed model label, reasoning mode, chat condition, web and tool availability, file and URL access, run index, regeneration status, refusal, clarification request, truncation, response path, evaluator identity, and blinding status.

A single response supports only an observed-output statement for that run. It does not establish a stable model capability. Repeated runs should use randomized order and preserve all raw outputs.

Outputs from the same model or chat belong to the same independence group unless a documented reason supports a different classification.
