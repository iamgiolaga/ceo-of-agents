# Schema: lifecycle frontmatter of analyses and notes

Analyses and notes in an hq (for example the dated files in `departments/<id>/`, `YYYY-MM-DD-<slug>.md`, and the documents of an initiative in `initiatives/<slug>/`) start with this frontmatter, so the CoS, the departments and the workers can tell what is current without reading every file. The generated `CLAUDE.md` carries the same block in its "Documents" section, because departments do not read the plugin's schemas.

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

- A new document is `current`. The weekly brief's hygiene step reports a current document whose `as_of` is more than 90 days old, so its owner can refresh it or the CEO can archive it.
- When a newer document replaces it, the old one gets `status: superseded` and `superseded_by`; its body stays as it is.
- An archived document moves to `archive/`, keeping its path (`departments/engineering/x.md` becomes `archive/departments/engineering/x.md`), with `status: archived`. Archiving happens only when the CEO asks or agrees (see "Archiving").
- `.ignore` at the hq root lists `archive/`. Search tools that follow `.ignore` files (Claude Code's search among them) then skip the archive unless `archive/` is named as the path. Git does not read `.ignore`: archived files stay tracked.

## Where documents go

- Work for one department, done in one go: `departments/<id>/YYYY-MM-DD-<slug>.md`.
- Work that spans several sessions or departments: the folder of its initiative, `initiatives/<slug>/YYYY-MM-DD-<dept-id>-<slug>.md` (see `schemas/initiative.md`). The brief names the initiative; the handoff carries `initiative: <slug>`.

## Folder indexes

Every folder that holds documents has a `README.md` index: `departments/<id>/README.md`, `initiatives/README.md` (one line per initiative, format in `schemas/initiative.md`) and `initiatives/<slug>/README.md`. Agents read the index first and open only the documents they need.

One line per document or subfolder, newest first:

```
- [YYYY-MM-DD-<slug>.md](YYYY-MM-DD-<slug>.md): <what it answers, in one line>
- [YYYY-MM-DD-<slug>.md](YYYY-MM-DD-<slug>.md): <what it answered, in one line> (superseded)
- [<subfolder>/](<subfolder>/): <what it holds, in one line>
```

- Whoever adds, supersedes or archives a document updates the index of its folder in the same change: a department for its own folder and for the documents it writes into an initiative, the CoS for the rest.
- A superseded document keeps its line with ` (superseded)` until it is archived; an archived one leaves the index.
- The charter, the folder's `status.md` and the index itself are not listed.
- An empty index is the single line `- none`.
- `decisions/README.md` and `inbox/README.md` keep their own formats; `archive/` has no index.

## Archiving

Archiving removes nothing from git, so it is an hq write, but the CEO approves what goes: the CoS proposes a list (the weekly brief's hygiene step, or the close of an initiative) and moves only the paths the CEO approves.

1. For each approved path, create the parent folder under `archive/` and `git mv <path> archive/<path>`. An initiative moves as one folder: `initiatives/<slug>/` becomes `archive/initiatives/<slug>/`.
2. Set `status: archived` in the frontmatter of each moved document. A document with no frontmatter gets the block, with `as_of` set to the date of the last commit that touched it (`git log -1 --format=%cs -- <path>`). An initiative's `status.md` keeps its own format.
3. Indexes: remove the document's line from its folder's `README.md`. For an initiative, move its line in `initiatives/README.md` to `## Archived`, pointing to `../archive/initiatives/<slug>/status.md`.
4. Links: point the links in current files (`company/state.md`, `status.md` files, indexes, current documents) to the new path. Decision records and briefs stay as they are, because they are dated records; their old paths still resolve with `archive/` in front.
5. Commit with notice, for example `chore: archive 4 documents (<ORG_ID>-A12)`, and remove the A item that carried the list, if there is one.

## Out of scope

Files with a format of their own keep it and get no lifecycle frontmatter: decision records (`decisions/`, immutable, with their own status line), `company/` files (`state.md`, `decision-queue.md`, `vision.md`, `strategy.md`, briefs), charters, agent files, `inbox/` notes, folder indexes (`README.md`) and an initiative's `status.md`.

A document written before this schema existed has no frontmatter and is read as `current` with an unknown `as_of`; add the frontmatter when the document is next touched.
