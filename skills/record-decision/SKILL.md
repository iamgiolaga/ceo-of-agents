---
name: record-decision
description: Record a decision the CEO took, either by answering a decision card by code (for example ACME-D3) or by deciding in chat. Creates the immutable decision record, updates the index, the queue and the pending list, handles supersession, dispatches follow-ups, and commits with notice. Use when the CEO answers a card, says "decision", or confirms a direction.
argument-hint: "[card code, e.g. ACME-D3, optional]"
allowed-tools: Read Grep Glob Edit Write Bash(git pull:*) Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(ls:*) Bash(date:*)
---

# record-decision

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. Record format: `${CLAUDE_PLUGIN_ROOT}/schemas/decision-record.md`; card format: `${CLAUDE_PLUGIN_ROOT}/schemas/decision-card.md`; state format: `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`.

## Hard rule

Never record a decision the CEO did not take. An answer must come from the CEO in this conversation. A recommendation, a draft, or silence is not a decision. If the CEO's words are ambiguous or only partly answer the card, ask one clarifying question before writing anything. If the CEO only says "ok" to a long list, confirm which codes and options you understood.

## Steps

1. Identify the decision. Read `org.yaml`, `company/state.md`, `company/decision-queue.md` and `decisions/README.md`. Match the CEO's answer to a card by code (`<ORG_ID>-D<n>`) and to an option, or, for a chat decision with no card, state it in one line and confirm it. Answers to several cards in one message become one record per card.

2. Check for existing and conflicting records: Grep `decisions/` for the topic. If the new decision replaces or changes an earlier one, plan the supersession (step 6). If a card is only partly answered, keep it in the queue with the answered part noted and record only what was decided.

3. Next number: highest `NNNN` in `decisions/` plus 1, four digits, never reused. Filename `decisions/NNNN-<kebab-slug>.md`. Create it:
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

4. Update `decisions/README.md`: add a row `| [NNNN](NNNN-<slug>.md) | <Title> | YYYY-MM-DD | accepted |` to the `| # | Decision | Date | Status |` index.

5. Update the queue and the lists:
   - Remove the answered card from `company/decision-queue.md`. If the queue becomes empty, write `_No open decisions._`.
   - Remove the `<ORG_ID>-D<n>` item from "Waiting on the CEO" in `company/state.md`, and its line from "Open decisions".
   - If the decision changes facts (products, numbers with source and date, risks), update those sections. A consciously accepted risk goes in Risks with a link to the record.
   - Set `last_updated` to today. Do not change `next_action` or `next_decision`; codes are never reused.

6. Supersession and amendment: records are immutable. Never edit the body of an old record. If the new record supersedes or amends an earlier one, change only the old record's status line to `Status: superseded by NNNN` or `Status: amended by NNNN`, and update that row's Status in the index. Mention the old record in the new record's Links.

7. Follow-ups: for each consequence that needs work, either
   - add an A item to "Waiting on the CEO" when only the CEO can do it (`- <ORG_ID>-A<n> [urgency]: <exact action> (since YYYY-MM-DD)`, increment `next_action`), or
   - dispatch a department with a self-contained brief (goal, files, constraints, definition of done, what to return; end it with: "If you spawn sub-agents, do not set a more capable model than your own"), or leave a note for it. Respect the gate table: a dispatch to a department that will push is "notice" (one line before); anything at the "ok" tier needs the CEO's explicit OK and goes in the pending list first.
   - If the decision touches a rule that needs a later check (gates, brand, policy), say which item will carry it.

8. Commit. The gate for `hq-commit` is "notice": write one line to the CEO (what, where; for example "Committing to hq main: record 0007 for ACME-D3, queue and state updated."), then commit with a message like `docs: record decision NNNN <slug>` and the attribution lines required by the session. Do not wait for an OK. Never push unless the CEO asks.

9. Report in chat language, briefly: record created (number and title), what moved in the queue and pending list, follow-ups with codes, and anything superseded.

## Notes

- Company with an `[escalate: holding]` card: the answer is recorded here only. Never write to the holding repo.
- If the CEO asks to undo an earlier decision, that is a new decision: record it as a new record that supersedes the old one.
