---
name: departments
description: Add, change or remove a department of a ceo-of-agents hq, or grant one a new tool or connector, through a decision card. Holds the grant review (a one-line reason for every elevated grant), the account checks and the files to write once the CEO decides. Use when the CEO asks for a new department, a change to one, or access for one, and when recurring work suggests a new department.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git status:*) Bash(git diff:*) Bash(ls:*) Bash(date:*)
---

# departments: add, change or remove a department, or grant access

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. A department never changes its own charter, agent file or tools.

## Prepare the card

1. Frame the change in one line: a new department, a change to one (scope, exclusions, tools, model, name), a removal, or a new tool or connector for one.
2. Draft it in full before the card:
   - a new department from the catalog: `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` and `agent.md`; a new custom department: `${CLAUDE_PLUGIN_ROOT}/templates/department/` with its scope, triggers, exclusions, single core job, and whether it runs commands (with the reason). Ask the CEO for what is missing; never invent it;
   - its display name and agent name (the persona in lowercase, or the id; unique, never `reader`, `worker` or another department's id), its model tier and, if wanted, "top model, workers included" (`workers: same`);
   - a change: the exact lines that change in its charter, its agent file and `org.yaml`.
3. Review the draft as a whole (scope, tools, connectors, model) and give a one-line reason for each elevated grant: any connector, `Edit`, `Write`, `Bash` or `Agent`. Drop a grant that has no reason, and say so.
4. Account checks for a connector:
   - never one listed in `accounts.forbidden_connectors` in `org.yaml`;
   - only a connector of this org's own accounts (see "Account separation" in `CLAUDE.md`);
   - an advisory department gets only read-only connector tools, named one by one, never a whole server (`mcp__<server>__*`).
5. Write the decision card (`company/decision-queue.md`, own D code) with the draft, the reasons and a recommendation, and add it to "Waiting on the CEO".

A reply from the CEO to a denied permission is not a grant by itself: do not widen an allowlist on the strength of it; the grant goes through the card.

## After the CEO decides

Record the decision with the `record-decision` skill, then apply exactly what was decided:

- New department: `departments/<id>/charter.md` and `.claude/agents/<agent>.md` rendered from the catalog entry or the custom template (placeholders as in the `init-fleet` skill's placeholder reference), an item in `departments:` in `org.yaml` (`connectors: []` unless the decision grants one), and a row in the routing table of `CLAUDE.md`. Writes into `.claude/` may raise a permission prompt.
- Grant: add the connector to the department's `connectors:` in `org.yaml` and to the `tools:` list of its agent file.
- `workers: same` gained or lost: also update the worker model lines in its agent file.
- Removal: delete its charter folder and agent file, its item in `org.yaml` and its routing row. Git keeps the history.

Then commit with notice, as for any hq change.
