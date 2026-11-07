# Schema: initiative folder

An initiative is one piece of work that spans several sessions or departments, with its own folder `initiatives/<slug>/`. It keeps the material of that work in one place instead of scattering it across department folders, the pending list and `company/state.md`. The chief of staff (CoS) opens, updates and closes initiatives with the `initiatives` skill. Work that one department finishes in one go needs no initiative: it stays in `departments/<id>/`.

## Layout

```
initiatives/
  README.md                       index of initiatives, one line each
  <slug>/
    status.md                     one page: goal, state, next step, links (the CoS only)
    README.md                     index of the documents in this folder
    YYYY-MM-DD-<dept-id>-<slug>.md   documents, with the lifecycle frontmatter of schemas/document.md
```

`<slug>` is short kebab-case, unique among current and archived initiatives. A document written by the CoS uses `cos` as `<dept-id>`.

## `status.md`

One page, under about 60 lines (4 KB): the detail goes in documents that it links. Only the CoS edits it; departments report through their handoffs.

```markdown
---
initiative: <slug>
state: active            # active | paused | done | dropped
opened: YYYY-MM-DD
updated: YYYY-MM-DD      # the last change of state, next step or links
lead: cos                # cos, or the id of the department that leads the work
departments: [<dept-id>, <dept-id>]
---

# <Title>

## Goal
One or two lines: what done looks like, and how it serves the current focus.

## State
One to three lines: where the work stands.

## Next step
One line: what happens next, and who does it.

## Links
- Documents: `README.md` in this folder; documents elsewhere by path
- Decisions: `decisions/NNNN-<slug>.md`
- Issues and pull requests: URLs
- Pending: <ORG_ID>-A<n>, <ORG_ID>-D<n> (the items stay in `company/state.md`)

## Summary
Only on close: three to five lines on the outcome, the decisions taken (by record), and what was left out and where it went.
```

| Field | Rule |
|---|---|
| `initiative` | Same as the folder name |
| `state` | `active` while work goes on; `paused` when the CEO puts it on hold (say why under State); `done` or `dropped` on close |
| `opened`, `updated` | `YYYY-MM-DD`. An `active` initiative whose `updated` date and last commit are both older than 14 days counts as idle in the weekly brief's hygiene step |
| `lead` | `cos` or a department id |
| `departments` | The departments that work on it, `[]` if none yet |

`status.md` and the folder's `README.md` have a format of their own and get no lifecycle frontmatter.

## Folder index: `initiatives/<slug>/README.md`

```markdown
# <Title>: documents

Index of `initiatives/<slug>/`. Read it first and open only the documents you need. `status.md` holds the goal, state and links. One line per document, newest first; whoever adds, supersedes or archives a document here updates this list in the same change.

- none
```

Lines follow the format in `schemas/document.md`, section "Folder indexes".

## Index of initiatives: `initiatives/README.md`

Two sections: `## Current` (active, paused, and closed but not yet archived) and `## Archived`. One line per initiative:

```
- [<slug>](<slug>/status.md): <goal in a few words>; <state>, updated YYYY-MM-DD
- [<slug>](../archive/initiatives/<slug>/status.md): <goal in a few words>; <done|dropped>, archived YYYY-MM-DD
```

An empty section is the single line `- none`.

## In `company/state.md`

An open initiative has one line in "Products and status", which links its page:

`- <Title>: <state in a few words>, see initiatives/<slug>/status.md (as of YYYY-MM-DD)`

The detail lives in `status.md`, so the line stays under the line budget of `schemas/boot-set.md`. Pending items stay in "Waiting on the CEO"; `status.md` only names their codes. On close the line goes.

## Lifecycle

1. **Open**: the CoS creates `status.md`, the folder's `README.md`, its line in `initiatives/README.md` and its line in `company/state.md`. Documents that already exist elsewhere are linked, not moved.
2. **Work**: a brief that names the initiative tells the department to write its documents into the folder (`YYYY-MM-DD-<dept-id>-<slug>.md`), to add a line to the folder's `README.md`, and to put `initiative: <slug>` in its handoff. The CoS updates `status.md` from the handoffs, the decision records and the issues.
3. **Close**: when the CEO says it is done or dropped, the CoS writes the Summary, sets `state` and `updated`, and removes the line from `company/state.md`.
4. **Archive**: with the CEO's OK, the whole folder moves to `archive/initiatives/<slug>/` (steps in `schemas/document.md`, section "Archiving"), and its line moves to `## Archived`.

## Personal hqs

In a personal hq, `status.md` and the documents of an initiative are tracked by git: they hold structure, decisions and pointers only. Personal detail stays in `private/`.
