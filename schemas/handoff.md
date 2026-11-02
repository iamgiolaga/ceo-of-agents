# Schema: handoff note (`inbox/`)

A handoff is what a department (or any outside surface) leaves for the chief of staff (CoS) at the end of its work. One file per handoff. The CoS processes it (intake) and deletes it in the same commit; git history keeps it.

## Filename

`inbox/YYYY-MM-DD-<from>-to-<to>-<slug>.md`

- `<from>` and `<to>` are department ids or `cos`; `<slug>` is kebab-case.

## Frontmatter (all fields required)

| Field | Allowed values |
|---|---|
| `from` | department id, `cos`, or `ceo` |
| `to` | department id or `cos` |
| `date` | `YYYY-MM-DD` |
| `needs_ceo_decision` | `yes` or `no` |
| `proposed_card` | one-line question, or `none` |

If `needs_ceo_decision` is `yes`, `proposed_card` must be a question and the CoS adds a decision card (with a new D code) to company/decision-queue.md. If `no`, `proposed_card` is `none`.

## Sections (exact H2 headings, in this order)

1. `## Ask or finding`: 2 to 5 lines.
2. `## Done`: what changed and where (file paths, branches, PRs).
3. `## Links`: files, issues or PRs; `- none` if empty.

## Minimal valid example

```markdown
---
from: engineering
to: cos
date: 2026-01-15
needs_ceo_decision: yes
proposed_card: Should we drop support for the oldest mobile OS version?
---

## Ask or finding
Usage of the oldest supported OS is under 1% (source: analytics, 2026-01-14).
Dropping it removes two compatibility shims.

## Done
- Drafted the removal on branch `chore/drop-old-os`; PR opened, not merged.

## Links
- departments/engineering/2026-01-15-old-os-usage.md
```

## Validation checklist

- Filename matches the pattern; `from`/`to` in the name equal the frontmatter fields.
- All five frontmatter fields present; `date` is valid.
- `needs_ceo_decision` and `proposed_card` are consistent (yes with a question, no with `none`).
- The three H2 headings exist, in order; Ask or finding is at most 5 lines.
- No secrets, credentials or sensitive personal data in the note.
- The CoS deletes the file in the same commit that processes it.
