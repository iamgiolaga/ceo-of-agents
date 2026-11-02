---
name: weekly-brief
description: On-demand weekly brief for one org hq. Reads state, decision queue, recent decisions, inbox and metrics, writes company/briefs/YYYY-MM-DD-weekly.md with headline, changes, numbers with sources, risks, what waits on the CEO and a proposed next week, and gives a short chat summary. Use only when the CEO asks for a briefing or weekly update; it never runs on a schedule.
allowed-tools: Read Write Edit Grep Glob Bash(git pull:*) Bash(git log:*) Bash(git status:*) Bash(git diff:*) Bash(ls:*) Bash(date:*)
---

# weekly-brief

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write the brief in the file language (`language.files`).

On demand only: no scheduled automation. Never invent numbers; every number carries a source and a date, and unknowns are written as unknown.

## Steps

1. `git pull` (if there is a remote; if it fails, say so and continue with the local copy). Read `org.yaml`, `company/state.md`, `company/decision-queue.md`, `inbox/` (list and read the notes; do not process or delete them, that is `/ceo-of-agents:intake`), `metrics/README.md`, and the latest file in `company/briefs/` if any.

2. Find what changed since the last brief: use the date of the latest brief, or, if none, 7 days ago. Read `git log --since=<date> --name-status` and the decision records created since then (`decisions/`). Also read the new handoffs in `inbox/`.

3. Numbers only from `company/state.md` Key numbers and `metrics/README.md`, with source and as-of date. If a number is older than the period, show the last known value with its date and mark it stale. If a number is unknown, write `unknown (no source yet)`.

4. Write `company/briefs/YYYY-MM-DD-weekly.md` (today's date, `date +%F`; create `company/briefs/` if missing). Exactly these sections, under a title `# Weekly brief YYYY-MM-DD: <org name>`:
   - `## Headline`: one or two sentences.
   - `## What changed`: 3 to 6 bullets (decisions recorded with record numbers, work done, handoffs received).
   - `## Key numbers`: table `Metric | Value | Source | As of`.
   - `## Risks`: from state.md Risks plus new ones, each with impact and owner.
   - `## Waiting on the CEO`: every open item from state.md, by code (`<ORG_ID>-A<n>`, `<ORG_ID>-D<n>`), with a one-line meaning, in urgency order (high, normal, low, then oldest first). For each decision give the question and the recommendation or `needs analysis by <dept-id>`; point to the queue for details.
   - `## Proposed next week`: a short list of proposed priorities, each marked as a proposal for the CEO to accept or change.
   Keep it under about one page. Do not include sensitive detail (tax, personal legal, personal finance) that state.md keeps out.

5. Update `company/state.md`: set `last_updated` to today. If the review shows drift between state.md and reality (stale lines, items done but still listed), fix those lines only when you can verify them; otherwise list the drift in the brief. Do not add or remove CEO codes here.

6. The brief and state edits are an hq commit: gate "notice". Write one line to the CEO and commit with `docs: weekly brief YYYY-MM-DD` and the attribution lines required by the session, or leave the changes uncommitted if the CEO prefers. Never push unless the CEO asks.

7. Chat summary in the chat language, at most 10 lines: the headline, the top changes, and the pending codes in urgency order, then ask which decisions to take now (answers go through `/ceo-of-agents:record-decision`). Give the path of the brief.
