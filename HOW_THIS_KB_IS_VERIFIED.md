# How this knowledge base is verified

This repository separates automated content checks from evidence that a procedure was reviewed or executed. A successful build means the article has the required metadata and sections, unique identifiers and body content, accepted taxonomy values, and working generated local links. It does **not** mean every procedure was run against a live service or production environment.

## Evidence statuses

| Status | What it means |
|---|---|
| `concept_reviewed` | The article was reviewed for scope, safety, clarity, and support logic. Execution is not claimed. |
| `vendor_source_checked` | The concept review was completed and the changing procedure was checked against current official vendor documentation. Execution is not claimed. |
| `lab_executed` | The documented procedure was executed in an authorized lab and attributable evidence is committed. |
| `needs_review` | The article needs technical or source review before operational use. |
| `archived` | The article is retained for history and should not guide current work. |

The current 38-article library is conservatively marked `concept_reviewed`. There is no committed, attributable execution evidence supporting a `lab_executed` label. Official links in an article are references, not proof that the linked procedure was rechecked on the article's review date.

## Promotion rules

- Promote to `vendor_source_checked` only after checking the relevant procedure against official vendor documentation and updating `reviewed_on`.
- Promote to `lab_executed` only when the exact procedure is executed in an authorized lab and a sanitized evidence file records the date, environment boundary, steps, outcome, limitations, and artifact path.
- Never store credentials, tokens, recovery keys, tenant identifiers, personal data, or employer data as evidence.
- A CI pass may be cited as a content/build check only. It is not procedure-execution evidence.

Before operational use, confirm authorization, organizational policy, current vendor guidance, and recovery or escalation requirements.
