---
name: initiatives
description: Open, update, close and archive an initiative in a ceo-of-agents hq, a folder initiatives/<slug>/ with a one-page status.md and an index of its documents, for work that spans several sessions or departments. Use when the CEO starts such a piece of work, when intake routes one, when a handoff or a decision touches an open initiative, or when the CEO says one is done or dropped.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git remote:*) Bash(git pull:*) Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(git mv:*) Bash(mkdir:*) Bash(ls:*) Bash(date:*)
---

# initiatives: one folder per piece of work

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. Departments write documents into an initiative's folder and add their lines to its `README.md`, but never edit its `status.md`: that rule is in the "Documents" section of the hq's `CLAUDE.md`, which departments read.

Formats: `${CLAUDE_PLUGIN_ROOT}/schemas/initiative.md` (the folder, `status.md`, the indexes, the line in `company/state.md`) and `${CLAUDE_PLUGIN_ROOT}/schemas/document.md` (document frontmatter, folder indexes, archiving).

## When to open one

Open an initiative when a piece of work:

- spans several departments, or a department and follow-up work of yours, or
- will take more than one session and gathers documents, decisions or pending items that belong together, or
- the CEO asks for one ("start a project on X").

Do not open one for work that one department finishes in one go: it stays in `departments/<id>/`. A single decision is a card, not an initiative. Before opening, read `initiatives/README.md`: if a current initiative already covers the topic, use it. Say it in one plain line, for example "I'm opening a folder for this work, `initiatives/checkout-redesign/`: a new checkout by the end of the quarter." Opening one is an hq write: no OK is needed.

## Open

1. Pick the slug: short kebab-case, unique in `initiatives/README.md` and under `archive/initiatives/`.
2. If `initiatives/README.md` is missing, create it from `${CLAUDE_PLUGIN_ROOT}/templates/instance/initiatives/README.md`.
3. Create `initiatives/<slug>/status.md` from the skeleton in the schema: `state: active`, `opened` and `updated` today (`date +%F`), the lead and the departments, Goal, State and Next step in plain words, and Links to what already exists (documents elsewhere, decision records, issues, pending codes). Link existing documents; do not move them, because moving breaks links.
4. Create `initiatives/<slug>/README.md` from the index skeleton in the schema, with `- none`.
5. Add its line under `## Current` in `initiatives/README.md` (replace `- none` if it is there).
6. In `company/state.md`, "Products and status", add one line: `- <Title>: <state in a few words>, see initiatives/<slug>/status.md (as of YYYY-MM-DD)`.
7. In every brief for this work, name the initiative: "Initiative: `initiatives/<slug>/`. Write your documents there as `YYYY-MM-DD-<your-dept-id>-<slug>.md`, add a line for each to its `README.md`, and put `initiative: <slug>` in the frontmatter of your handoff."

## Update

When a handoff names the initiative (`initiative: <slug>`, or a path under its folder), a decision record concerns it, an issue or pull request in its Links changes, or the CEO changes its direction:

- Update `status.md`: State, Next step, Links, `departments`, and `updated` to today. Keep it to one page; the detail goes in a document that it links.
- Check that the documents the handoff names have their line in the folder's `README.md`; add a missing line yourself.
- Update its line in `initiatives/README.md` and in `company/state.md` when the state changed.
- Pending items stay in "Waiting on the CEO" in `company/state.md`, the one list; `status.md` names their codes only.
- `paused`: when the CEO puts the work on hold; say why under State. `active` again when it resumes.

## Close

When the CEO says the work is done or dropped:

1. Write `## Summary` in `status.md`: three to five lines on the outcome, the decisions taken (by record), and what was left out and where it went (an issue, another initiative, a parked item).
2. Set `state: done` or `state: dropped`, and `updated` to today.
3. Update its line in `initiatives/README.md` (it stays under `## Current` until archived) and remove its line from `company/state.md`.
4. Propose the archive in one plain line, for example "May I put the finished checkout work in the archive? Nothing is deleted, and it can come back." If the CEO does not answer now, the weekly brief's hygiene step proposes it again; add no A item here.
5. After the CEO's yes, archive it as in `${CLAUDE_PLUGIN_ROOT}/schemas/document.md`, section "Archiving".

## Commit

Every step above is an hq write. Commit with notice (`hq-commit`): one line to the CEO, then a message like `docs: open initiative <slug>`, `docs: update initiative <slug>` or `chore: archive initiative <slug>`, with the attribution lines required by the session. When this skill runs inside `intake` or `record-decision`, its edits go in that skill's commit. Never push unless the CEO asks, and never without a remote.

## Rules

- One folder per initiative; no initiatives inside initiatives.
- Never archive without the CEO's OK on the named folder.
- In a personal hq, `status.md` and the documents hold structure, decisions and pointers only; personal detail stays in `private/`.
- A public product repo never receives an initiative's name, path or content.
