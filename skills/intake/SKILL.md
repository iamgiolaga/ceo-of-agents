---
name: intake
description: Process handoff notes in inbox/ and new CEO requests or ideas in a ceo-of-agents hq. Updates state.md, adds decision cards and action items with namespaced codes, flags escalations to the holding, deletes processed notes in the same hq commit. Use at session start when inbox/ has notes, or when the CEO brings a new idea, request or finding.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git remote:*) Bash(git pull:*) Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(git rm:*) Bash(ls:*) Bash(date:*)
---

# intake: process handoffs and new requests

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. A department agent must not process or delete `inbox/` notes, nor edit `company/state.md` or `company/decision-queue.md`; it leaves a handoff instead.

Formats are fixed: `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`, `${CLAUDE_PLUGIN_ROOT}/schemas/decision-card.md`, `${CLAUDE_PLUGIN_ROOT}/schemas/handoff.md`.

## Inputs

1. Handoff notes: every file in `inbox/` except `README.md` (`inbox/YYYY-MM-DD-<from>-to-<to>-<slug>.md`, frontmatter `from`, `to`, `date`, `needs_ceo_decision`, `proposed_card`, sections `Ask or finding`, `Done`, `Links`).
2. A new request, idea or finding the CEO states in chat.

## Steps

1. Sync. Run `git remote`. If it prints nothing, skip pull and push and say once: "No remote: pull and push skipped". Otherwise run `git pull`; if it fails, say so in one line and continue with the local copy. Skip this step if the session already synced hq.

2. Orient. Read `org.yaml`, `company/vision.md` and `company/strategy.md` (if present), `company/state.md`, `company/decision-queue.md` and `ls inbox/`. Note the org id, the level and the next codes (`next_action`, `next_decision`). Search `decisions/` and the queue for duplicates and conflicts with the topic (Grep). If a topic is already decided, say so and cite the record rather than reopening it, unless the new input is a reason to supersede it. If a request does not serve the vision or the current focus, say so in one line, then follow the CEO.

3. For a new CEO request (no note): restate it in one line. Classify it into exactly one primary route:
   - Decision: a clear choice is needed, so add a card.
   - Action: something only the CEO can do (an exact click, link, signature), so add an A item.
   - Department task: delegate with full context (a self-contained brief; the department leaves a handoff at the end). Keep it one task unless it must be split:
     - split only where a part has a different owner, needs different permissions, can really run in parallel, must wait for another part (a hard prerequisite), or is an independent review;
     - write each dependency into the briefs, for example "starts after engineering's PR is open";
     - a split never adds an approval and never skips one: an action that needs an OK still needs it in whichever part runs it;
     - a review brief stands on its own, without the author's context, and names who receives the verdict.
   - Reasoning session: vague or strategic; propose a conversation first and record only what comes out of it.
   - Later: does not fit now; park it as a low-urgency item rather than dropping it.
   State the route in one short line, then execute. Do not ask for OKs the gate table does not require.

4. For each handoff note, read it fully, then:
   - Update `company/state.md` where facts changed: Products and status, Key numbers (only with source and date; never invent a number), Risks (with owner). Sensitive detail (tax, personal legal, personal finance) stays out of state.md; keep it in the department folder.
   - If `needs_ceo_decision: yes`, or the finding needs a CEO choice: add a decision card to `company/decision-queue.md` with the next code `<ORG_ID>-D<next_decision>`, fields `status: open`, `since`, `urgency`, exactly one of `proposed_by: <dept-id|cos>` or `needs analysis by: <dept-id>` (never both), `escalate: no` (company level, purpose not job; omit the line in a holding or a job hq), and sections Context, Options (lettered), Recommendation. Increment `next_decision`. Add the matching line to "Open decisions" and to "Waiting on the CEO" (`- <ORG_ID>-D<n> [urgency]: decide <question>, see decision queue (since YYYY-MM-DD)`).
   - If something only the CEO can do is needed: add `- <ORG_ID>-A<n> [urgency]: <exact action: where, what, link> (since YYYY-MM-DD)` to "Waiting on the CEO" and increment `next_action`.
   - Codes are namespaced, monotonic and never reused. Never reuse a code of a removed item.
   - Remove "Waiting on the CEO" items the note shows are already done.

5. Escalation (company level, purpose not job; the `escalate:` line does not exist in a holding or a job queue): if a decision touches money, personal liability or the portfolio, set `escalate: holding` on the card and append ` [escalate: holding]` to its line in "Open decisions". The holding reads it on its next portfolio brief. Never write to the holding repo. Tell the CEO the card is flagged and that the answer is still recorded here.

6. Finish state.md: set `last_updated` to today (`date +%F`), keep the five H2 sections in order, `- none` for empty ones. Keep each line to the formats in the schema.

7. Delete each processed note (`git rm` or remove the file) in the same hq commit as the updates. Git history keeps them. Do not delete a note you could not fully process; say why.

8. Commit. The gate for `hq-commit` is "notice": write one line to the CEO before committing (what, where, content; for example "Committing to hq main: 2 notes processed, ACME-D4 added, state.md updated."), then commit on the current branch with a message like `chore: process inbox (<codes>)` and the attribution lines required by the session. Do not wait for an OK. Never push unless the CEO asks; a push is a separate notice-tier action, and never happens without a remote.

9. Reply with a short summary in the chat language: notes processed, new codes (A and D, with one-line meaning), escalations, and anything blocked or ambiguous. Cite codes, do not paste cards. If nothing was in the inbox and the CEO gave no request, say so in one line.

## Rules

- hq is the single source of truth: whatever the CEO says that matters ends up written down before you reply.
- One card = one D code, shown in both `decision-queue.md` and `state.md`.
- Do not record a decision the CEO has not taken. Intake adds questions, not answers; answers go through the `record-decision` skill.
- Keep recommendations honest: the card names who proposes (`proposed_by:`), or says `needs analysis by: <dept-id>` instead. In `state.md` the matching "Open decisions" line reads `proposed by <dept-id|cos>` or `needs analysis by <dept-id>`.
- If a note is malformed (missing frontmatter), process what is clear and list what you assumed.
