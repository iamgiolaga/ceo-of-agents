---
name: weekly-brief
description: On-demand weekly brief for one org hq. Reads state, decision queue, recent decisions, inbox, metrics and (read-only) the tracker, issues and PRs of registered product repos, writes company/briefs/YYYY-MM-DD-weekly.md with headline, changes, numbers with sources, risks, what waits on the CEO and a proposed next week, and gives a short chat summary. Use only when the CEO asks for a briefing or weekly update; it never runs on a schedule.
user-invocable: false
allowed-tools: Read Write Edit Grep Glob Bash(git remote:*) Bash(git pull:*) Bash(git log:*) Bash(git status:*) Bash(git diff:*) Bash(git add:*) Bash(git commit:*) Bash(ls:*) Bash(date:*) Bash(gh project item-list:*) Bash(gh issue list:*) Bash(gh pr list:*)
---

# weekly-brief

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write the brief in the file language (`language.files`).

On demand only: no scheduled automation. Never invent numbers; every number carries a source and a date, and unknowns are written as unknown.

## Steps

1. Sync. Run `git remote`. If it prints nothing, skip pull and push and say once: "No remote: pull and push skipped". Otherwise run `git pull`; if it fails, say so in one line and continue with the local copy. Skip this step if the session already synced hq. Read `org.yaml`, `company/vision.md` and `company/strategy.md` (if present), `company/state.md`, `company/decision-queue.md`, `inbox/` (list and read the notes; do not process or delete them, that is the `intake` skill), `metrics/README.md`, and the latest file in `company/briefs/` if any.

2. Find what changed since the last brief: use the date of the latest brief, or, if none, 7 days ago. Read `git log --since=<date> --name-status` and the decision records created since then (`decisions/`). Also read the new handoffs in `inbox/`.

3. Product repos and tracker, read-only. Skip this step when `repos` in `org.yaml` is `[]` and `tracker` is `none`, or both are absent (an `org/2` file). Never write to GitHub from this skill.
   - Tracker (if not `none`): `gh project item-list <number> --owner <owner> --format json --limit 200`; count items by `tracker.status_field`.
   - For each registered repo: `gh issue list -R <slug> --state open --limit 50`, `gh issue list -R <slug> --state closed --search "closed:>=<date from step 2>" --limit 50`, and `gh pr list -R <slug> --state open`.
   - Fallback: if a `gh` call fails (not installed, not signed in, no `project` scope, no access), write `not read: <reason>` for that source in the brief and in the chat summary, and suggest the exact command (for example `gh auth refresh -s project`). Never fill the gap with guesses or with older numbers presented as current.
   - Drift: an issue closed but still open on the tracker, work recorded in hq with no issue, a merged PR whose issue is still open. List it under Roadmap; do not fix it here.

4. Numbers only from `company/state.md` Key numbers and `metrics/README.md`, with source and as-of date. If a number is older than the period, show the last known value with its date and mark it stale. If a number is unknown, write `unknown (no source yet)`.

5. Write `company/briefs/YYYY-MM-DD-weekly.md` (today's date, `date +%F`; create `company/briefs/` if missing). Exactly these sections, in this order (`## Roadmap` only when step 3 ran), under a title `# Weekly brief YYYY-MM-DD: <org name>`:
   - `## Headline`: one or two sentences, measured against "Current focus" in `company/strategy.md` when it is set.
   - `## What changed`: 3 to 6 bullets (decisions recorded with record numbers, work done, handoffs received).
   - `## Key numbers`: table `Metric | Value | Source | As of`.
   - `## Roadmap`: only when step 3 ran. Tracker items by status, issues closed in the period, open PRs (an open PR waits on the CEO's merge OK), and drift. Counts carry their source (the Project or `gh issue list -R <slug>`) and today's date.
   - `## Risks`: from state.md Risks plus new ones, each with impact and owner.
   - `## Waiting on the CEO`: every open item from state.md, by code (`<ORG_ID>-A<n>`, `<ORG_ID>-D<n>`), with a one-line meaning, in urgency order (high, normal, low, then oldest first). For each decision give the question and the recommendation or `needs analysis by <dept-id>`; point to the queue for details.
   - `## Proposed next week`: a short list of proposed priorities that serve the current focus, each marked as a proposal for the CEO to accept or change.
   Keep it under about one page. Do not include sensitive detail (tax, personal legal, personal finance) that state.md keeps out.

6. Update `company/state.md`: set `last_updated` to today. If the review shows drift between state.md and reality (stale lines, items done but still listed), fix those lines only when you can verify them; otherwise list the drift in the brief. Do not add or remove CEO codes here.

7. The brief and state edits are an hq commit: gate "notice". Write one line to the CEO and commit with `docs: weekly brief YYYY-MM-DD` and the attribution lines required by the session, or leave the changes uncommitted if the CEO prefers. Never push unless the CEO asks.

8. Chat summary in the chat language, at most 10 lines: the headline, the top changes, and the pending codes in urgency order, then ask which decisions to take now (answers go through the `record-decision` skill). Give the path of the brief.
