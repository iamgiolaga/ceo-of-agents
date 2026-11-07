---
name: weekly-brief
description: On-demand weekly brief for one org hq. Reads state, decision queue, recent decisions, inbox, metrics, initiatives and (read-only) the tracker, issues and PRs of registered product repos, runs a hygiene check (files over budget, old documents, long-open pending items, idle initiatives, contradictions, stale claims, orphans, missing links), writes company/briefs/YYYY-MM-DD-weekly.md with headline, changes, numbers with sources, risks, hygiene with a proposed archive list, what waits on the CEO and a proposed next week, and gives a short chat summary. Archives only what the CEO approves. Use only when the CEO asks for a briefing or weekly update; it never runs on a schedule.
user-invocable: false
allowed-tools: Read Write Edit Grep Glob Bash(git remote:*) Bash(git pull:*) Bash(git log:*) Bash(git status:*) Bash(git diff:*) Bash(git add:*) Bash(git commit:*) Bash(git mv:*) Bash(git -C * rev-list *) Bash(mkdir:*) Bash(ls:*) Bash(wc:*) Bash(date:*) Bash(gh project item-list:*) Bash(gh issue list:*) Bash(gh pr list:*)
---

# weekly-brief

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write the brief in the file language (`language.files`).

On demand only: no scheduled automation. Never invent numbers; every number carries a source and a date, and unknowns are written as unknown.

## Steps

1. Sync. Run `git remote`. If it prints nothing, skip pull and push and say once: "No remote: pull and push skipped". Otherwise run `git pull`; if it fails, say so in one line and continue with the local copy. Skip this step if the session already synced hq. Read `org.yaml`, `company/vision.md` and `company/strategy.md` (if present), `company/state.md`, `company/decision-queue.md`, `inbox/` (list and read the notes; do not process or delete them, that is the `intake` skill), `metrics/README.md`, `initiatives/README.md` (if present), and the latest file in `company/briefs/` if any.

2. Find what changed since the last brief: use the date of the latest brief, or, if none, 7 days ago. Read `git log --since=<date> --name-status` and the decision records created since then (`decisions/`). Also read the new handoffs in `inbox/`.

3. Product repos and tracker, read-only. Skip this step when `repos` in `org.yaml` is `[]` and `tracker` is `none`, or both are absent (an `org/2` file). Never write to GitHub from this skill.
   - Tracker (if not `none`): `gh project item-list <number> --owner <owner> --format json --limit 200`; count items by `tracker.status_field`.
   - For each registered repo (owner patterns `owner/*` and planned repos excluded; reads are free also on protected repos): `gh issue list -R <slug> --state open --limit 50`, `gh issue list -R <slug> --state closed --search "closed:>=<date from step 2>" --limit 50`, and `gh pr list -R <slug> --state open`.
   - Fallback: if a `gh` call fails (not installed, not signed in, no `project` scope, no access), write `not read: <reason>` for that source in the brief and in the chat summary, and suggest the exact command (for example `gh auth refresh -s project`). Never fill the gap with guesses or with older numbers presented as current.
   - Drift: an issue closed but still open on the tracker, work recorded in hq with no issue, a merged PR whose issue is still open. List it under Roadmap; do not fix it here.

4. Numbers only from `company/state.md` Key numbers and `metrics/README.md`, with source and as-of date. If a number is older than the period, show the last known value with its date and mark it stale. If a number is unknown, write `unknown (no source yet)`.

5. Hygiene. A fixed check that keeps the hq lean and findable. It reports and proposes; it never archives, trims or rewrites anything on its own. Thresholds: a document is old when its `as_of` is more than 90 days before today; a pending item is long-open when its `since` date is more than 14 days before today; an initiative is idle when its `state` is `active` and both its `updated` date and the last commit in its folder (`git log -1 --format=%cs -- initiatives/<slug>`) are more than 14 days before today. Documents are the files in `departments/` and `initiatives/` other than charters, `status.md` and `README.md`; never look in `archive/`.
   - Boot files over budget: measure them as the `session-start` skill does (step 4), against `${CLAUDE_PLUGIN_ROOT}/schemas/boot-set.md`.
   - Old documents: Grep the frontmatter for `status: current` and `as_of:`, and list the current documents whose `as_of` is old. Count the documents with no lifecycle frontmatter, naming at most three.
   - Long-open pending items: the items in "Waiting on the CEO" whose `since` date is old, except the archive item of step 7. An item with no `since` date takes the date of the first commit that added its code (`git log -S '<code>' --format=%cs --reverse -- company/state.md`, first line).
   - Idle initiatives: from `initiatives/README.md` and the `status.md` of each current initiative. Also list the initiatives closed (`done` or `dropped`) but not yet archived.
   - Lint, four checks:
     a. Contradictions: two current documents, or a current document and `company/state.md`, `company/strategy.md` or a decision record, that state different facts about the same thing.
     b. Stale claims: a current document overtaken by a newer document or a later decision record, or whose `source_commit` is behind the default branch of its repo (`git -C <clone> rev-list --count <sha>..HEAD`, only when the repo has a clone path under `repo_paths` in `accounts.local.yaml`; otherwise skip that part). Propose `status: superseded` with `superseded_by`, or a refresh by the department that owns the document.
     c. Orphans: a document not listed in its folder's `README.md` (Grep its file name in the index). A folder with documents but no `README.md` is reported once.
     d. Missing cross-references: a document or a `status.md` that names a decision record, an initiative, an issue or another document without linking it, and a decision record that cites an initiative whose `status.md` does not link back. Decision records are immutable: the fix goes on the other side.
     Checks c and d run over all documents with Grep. Checks a and b run on the documents added or changed since the last brief (step 2), against the current documents on the same subject, found through the indexes; a full pass runs only when the CEO asks for it. When more than a few documents must be read, hand the reading to a `reader` worker with the list of paths and these four checks, and use its findings, not file dumps.
   - Archive list: superseded documents, the folders of closed initiatives, and old documents the CEO may no longer need, one line each with the reason. Nothing moves yet.

6. Write `company/briefs/YYYY-MM-DD-weekly.md` (today's date, `date +%F`; create `company/briefs/` if missing). Exactly these sections, in this order (`## Roadmap` only when step 3 ran), under a title `# Weekly brief YYYY-MM-DD: <org name>`:
   - `## Headline`: one or two sentences, measured against "Current focus" in `company/strategy.md` when it is set.
   - `## What changed`: 3 to 6 bullets (decisions recorded with record numbers, work done, initiatives opened or closed, handoffs received).
   - `## Key numbers`: table `Metric | Value | Source | As of`.
   - `## Roadmap`: only when step 3 ran. Tracker items by status, issues closed in the period, open PRs (an open PR waits on the CEO's merge OK), and drift. Counts carry their source (the Project or `gh issue list -R <slug>`) and today's date.
   - `## Risks`: from state.md Risks plus new ones, each with impact and owner.
   - `## Hygiene`: the findings of step 5, one line each with the fix proposed and who does it, then `Proposed for the archive:` and the archive list. At most 15 lines: the most useful first, then "and N more". If there is nothing to report, the single line `- nothing to report`.
   - `## Waiting on the CEO`: every open item from state.md, by code (`<ORG_ID>-A<n>`, `<ORG_ID>-D<n>`), with a one-line meaning, in urgency order (high, normal, low, then oldest first). For each decision give the question and the recommendation or `needs analysis by <dept-id>`; point to the queue for details.
   - `## Proposed next week`: a short list of proposed priorities that serve the current focus, each marked as a proposal for the CEO to accept or change.
   Keep it under about one page. Do not include sensitive detail (tax, personal legal, personal finance) that state.md keeps out.

7. Update `company/state.md`: set `last_updated` to today. If the review shows drift between state.md and reality (stale lines, items done but still listed), fix those lines only when you can verify them; otherwise list the drift in the brief. Add no CEO code here, with one exception: when the archive list is not empty and no archive item is open, add `- <ORG_ID>-A<n> [low]: approve the archive list in company/briefs/YYYY-MM-DD-weekly.md, section Hygiene; archive steps in the plugin's schemas/document.md, Archiving (since YYYY-MM-DD)` and increment `next_action`.

8. The brief and state edits are an hq commit: gate "notice". Write one line to the CEO and commit with `docs: weekly brief YYYY-MM-DD` and the attribution lines required by the session, or leave the changes uncommitted if the CEO prefers. Never push unless the CEO asks.

9. Chat summary in the chat language, at most 10 lines: the headline, the top changes, one plain line on the cleanup check (for example "Cleanup: 2 old documents, 1 stalled piece of work, 3 files I propose to archive"), and the pending codes in urgency order, then ask which decisions to take now (answers go through the `record-decision` skill) and whether the archive list is approved, all of it or which lines (nothing is deleted: archived files move to `archive/` and stay in the history). Give the path of the brief.

10. Archive, only after the CEO's OK on the list, all of it or named lines: move exactly the approved paths as in `${CLAUDE_PLUGIN_ROOT}/schemas/document.md`, section "Archiving" (`git mv` into `archive/` with the same path, `status: archived`, indexes and links updated), remove the archive A item, and commit with notice. Archiving removes nothing from git, so it is an hq write; the CEO's OK on the list is still required. Lines the CEO turns down stay where they are.
