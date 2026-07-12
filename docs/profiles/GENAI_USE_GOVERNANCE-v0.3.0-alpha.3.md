# Generative-AI Use Governance Profile for MADP v0.3.0-alpha.3

Status: optional normative implementation profile for research laboratories and organizations.

## Policy context

A session using this profile records:

- information classification;
- prohibited and minimized inputs;
- approved services and relevant retention, training-use, and storage conditions;
- output verification level;
- disclosure and recordkeeping requirements;
- responsibility allocation;
- exception, incident, and periodic-review procedures.

## Information classes

Recommended minimum classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `PERSONAL_OR_HIGHLY_CONFIDENTIAL`. An organization may add stricter classes but must not silently weaken existing handling rules.

## Verification levels

- `LOW`: user self-review is acceptable for reversible, low-impact output.
- `MEDIUM`: claims, citations, calculations, or code receive evidence or test checks.
- `HIGH`: an independent qualified human reviews the relevant output and evidence before use.

## Responsibility

AI is not the accountable decision owner. The user is responsible for intended use; a reviewer is responsible only for the scope actually reviewed; an approver approves the defined process and exact revision, not an unspecified future output; administrators own service configuration and incident channels.

## Exceptions and incidents

Exceptions require scope, reason, approver, expiry, storage, and deletion conditions. Suspected disclosure, fabricated citation, unsafe code, or unauthorized use is recorded and routed through the named incident process. Repeated incidents update policy or training rather than remaining isolated corrections.
