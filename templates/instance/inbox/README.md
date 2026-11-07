# Inbox

Handoffs from departments (or from the CEO's other surfaces) to the chief of staff. One file per handoff. The CoS checks this folder at every session start, processes each note (with the `intake` skill) and deletes it in the same commit. Git history keeps it.

## Filename

`YYYY-MM-DD-<from>-to-<to>-<slug>.md`, for example `2026-01-15-engineering-to-cos-release-checklist.md`.

## Format

```markdown
---
from: <department id>
to: cos
date: YYYY-MM-DD
needs_ceo_decision: yes | no
proposed_card: <one-line question, or none>
initiative: <slug>   # only when the brief named an initiative
---

## Ask or finding
2-5 lines.

## Done
What changed and where (files, branches, links).

## Links
Files, issues, PRs.
```

If `needs_ceo_decision` is `yes`, the CoS adds a card to `company/decision-queue.md` with its own `{{ORG_ID}}-D<n>` code.

Departments never edit `company/state.md` or `company/decision-queue.md`; they report through this folder.
