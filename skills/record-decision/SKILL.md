---
name: record-decision
description: Record a decision the CEO took, either by answering a decision card by code (for example ACME-D3) or by deciding in chat. Creates the immutable decision record, updates the index, the queue and the pending list, handles supersession, creates or updates issues and tracker fields in registered product repos, dispatches follow-ups, and commits with notice. Use when the CEO answers a card, says "decision", or confirms a direction.
user-invocable: false
argument-hint: "[card code, e.g. ACME-D3, optional]"
allowed-tools: Read Grep Glob Edit Write Bash(git remote:*) Bash(git pull:*) Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(ls:*) Bash(date:*) Bash(gh issue list:*) Bash(gh issue create:*) Bash(gh issue edit:*) Bash(gh issue comment:*) Bash(gh issue close:*) Bash(gh project view:*) Bash(gh project field-list:*) Bash(gh project item-list:*) Bash(gh project item-add:*) Bash(gh project item-edit:*)
---

# record-decision

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. Record format: `${CLAUDE_PLUGIN_ROOT}/schemas/decision-record.md`; card format: `${CLAUDE_PLUGIN_ROOT}/schemas/decision-card.md`; state format: `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`.

## Hard rule

Never record a decision the CEO did not take. An answer must come from the CEO in this conversation. A recommendation, a draft, or silence is not a decision. If the CEO's words are ambiguous or only partly answer the card, ask one clarifying question before writing anything. If the CEO only says "ok" to a long list, confirm which codes and options you understood.

## Steps

1. Sync. Run `git remote`. If it prints nothing, skip pull and push and say once: "No remote: pull and push skipped". Otherwise run `git pull`; if it fails, say so in one line and continue with the local copy. Skip this step if the session already synced hq.

2. Identify the decision. Read `org.yaml`, `company/state.md`, `company/decision-queue.md` and `decisions/README.md`. Match the CEO's answer to a card by code (`<ORG_ID>-D<n>`) and to an option, or, for a chat decision with no card, state it in one line and confirm it. Answers to several cards in one message become one record per card.

3. Check for existing and conflicting records: Grep `decisions/` for the topic. If the new decision replaces or changes an earlier one, plan the supersession (step 7). If a card is only partly answered, keep it in the queue with the answered part noted and record only what was decided.

4. Next number: highest `NNNN` in `decisions/` plus 1, four digits, never reused. Filename `decisions/NNNN-<kebab-slug>.md`. Create it:
   ```
   # NNNN. <Title>
   - Date: YYYY-MM-DD
   - Status: accepted
   - Card: <ORG_ID>-D<n>          (or: none)
   - Decided by: <ceo role id from org.yaml>
   ## Context
   ## Options
   ## Decision
   ## Consequences
   ## Links
   ```
   Context and Options come from the card (the card's `proposed_by: <dept-id|cos>` or `needs analysis by: <dept-id>` line is not copied; name the proposer in Context if relevant; keep them short; quote the CEO only where it captures intent). Decision names the chosen option first, then the specifics. Consequences list what changes and any accepted risk. Links point to the card code, related records, issues or files. Date is today (`date +%F`).

5. Update `decisions/README.md`: add a row `| [NNNN](NNNN-<slug>.md) | <Title> | YYYY-MM-DD | accepted |` to the `| # | Decision | Date | Status |` index.

6. Update the queue and the lists:
   - Remove the answered card from `company/decision-queue.md`. If the queue becomes empty, write `_No open decisions._`.
   - Remove the `<ORG_ID>-D<n>` item from "Waiting on the CEO" in `company/state.md`, and its line from "Open decisions".
   - If the decision changes facts (products, numbers with source and date, risks), update those sections. A consciously accepted risk goes in Risks with a link to the record.
   - If the decision sets or changes what the org focuses on now, update "Current focus" in `company/strategy.md` (if present) and cite the record (`see decision NNNN`). A change to `company/vision.md` needs a decision that says so explicitly.
   - Set `last_updated` to today. Do not change `next_action` or `next_decision`; codes are never reused.

7. Supersession and amendment: records are immutable. Never edit the body of an old record. If the new record supersedes or amends an earlier one, change only the old record's status line to `Status: superseded by NNNN` or `Status: amended by NNNN`, and update that row's Status in the index. Mention the old record in the new record's Links.

8. Follow-ups: for each consequence that needs work, either
   - add an A item to "Waiting on the CEO" when only the CEO can do it (`- <ORG_ID>-A<n> [urgency]: <exact action> (since YYYY-MM-DD)`, increment `next_action`), or
   - dispatch a department, by its agent name (`agent` in `org.yaml`, or its id when `agent` is missing), with a self-contained brief (goal, files, constraints, definition of done, what to return; end it with: "If you spawn sub-agents, do not set a more capable model than your own"), or leave a note for it. Respect the gate table: a dispatch to a department that will push is "notice" (one line before); anything at the "ok" tier needs the CEO's explicit OK and goes in the pending list first.
   - If the decision touches a rule that needs a later check (gates, brand, policy), say which item will carry it.

9. Issues and tracker. Skip this step entirely when `repos` in `org.yaml` is `[]` or absent (an `org/2` file); skip only the Project part when `tracker` is `none` or absent. These writes are free: do them, then report them.
   - For each consequence that is work in a registered repo, find its issue (`gh issue list -R <slug> --search "<words>"`) or create one (`gh issue create -R <slug> --title "<title>" --body "<body>"`) in that repo, or in the issues home (`issues_home: true`) when the work spans repos. The body holds acceptance criteria. Link the decision: in a private repo (or an issues home that is the hq) write `<ORG_ID>-D<n>` and record `NNNN`; in a repo with `visibility: public` write no internal names, codes or hq content.
   - Update issues the decision changes (`gh issue edit`, `gh issue comment`) and close the ones it makes obsolete, with a one-line comment saying why (`gh issue close -R <slug> <number> --comment "<why>"`).
   - Add each new issue to the tracker and set `tracker.status_field` to match the decision (`gh project item-list` to find an existing item; `gh project item-add`, `gh project view`, `gh project field-list` and `gh project item-edit` to add and set, as in the `intake` skill's issue route).
   - Put every issue URL in the new record's Links before the commit (the record is immutable once committed).
   - If `gh` fails (not installed, not signed in, no `project` scope), say so, add an A item with the exact command for the CEO (for example `gh auth refresh -s project`) unless one is already open, list the intended issue changes in the report, and commit the rest.

10. Commit. The gate for `hq-commit` is "notice": write one line to the CEO (what, where; for example "Committing to hq main: record 0007 for ACME-D3, queue and state updated."), then commit with a message like `docs: record decision NNNN <slug>` and the attribution lines required by the session. Do not wait for an OK. Never push unless the CEO asks, and never without a remote.

11. Report in chat language, briefly: record created (number and title), what moved in the queue and pending list, issues created, updated or closed and the status set (with links), follow-ups with codes, and anything superseded.

## Notes

- Company with an `[escalate: holding]` card: the answer is recorded here only. Never write to the holding repo.
- If the CEO asks to undo an earlier decision, that is a new decision: record it as a new record that supersedes the old one.
