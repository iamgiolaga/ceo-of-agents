# Schema: lifecycle frontmatter of analyses and notes

Analyses and notes in an hq (for example the dated files in `departments/<id>/`, `YYYY-MM-DD-<slug>.md`) start with this frontmatter, so the CoS, the departments and the workers can tell what is current without reading every file. The generated `CLAUDE.md` carries the same block in its "Documents" section, because departments do not read the plugin's schemas.

```yaml
---
status: current          # current | superseded | archived
as_of: 2026-01-15        # the date the content was true
source_commit: 1a2b3c4   # optional: only for a document derived from code or data in a repo
superseded_by: departments/engineering/2026-02-01-audit.md   # only when status is superseded
---
```

## Fields

| Field | Required | Rule |
|---|---|---|
| `status` | yes | `current`, `superseded` or `archived` |
| `as_of` | yes | `YYYY-MM-DD`: the date the content was true, not the date of the last edit |
| `source_commit` | no | The commit (short or full sha) of the repo the document was derived from. A reader compares it with the repo's default branch to see whether the code has moved on |
| `superseded_by` | only with `status: superseded` | The hq path of the document that replaces it |

## Lifecycle

- A new document is `current`.
- When a newer document replaces it, the old one gets `status: superseded` and `superseded_by`; its body stays as it is.
- An archived document moves to `archive/`, keeping its path (`departments/engineering/x.md` becomes `archive/departments/engineering/x.md`), with `status: archived`. Archiving happens only when the CEO asks or agrees, as an hq commit.
- `.ignore` at the hq root lists `archive/`. Search tools that follow `.ignore` files (Claude Code's search among them) then skip the archive unless `archive/` is named as the path. Git does not read `.ignore`: archived files stay tracked.

## Out of scope

Files with a format of their own keep it and get no lifecycle frontmatter: decision records (`decisions/`, immutable, with their own status line), `company/` files (`state.md`, `decision-queue.md`, `vision.md`, `strategy.md`, briefs), charters, agent files and `inbox/` notes.

A document written before this schema existed has no frontmatter and is read as `current` with an unknown `as_of`; add the frontmatter when the document is next touched.
