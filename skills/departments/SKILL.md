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
2. A new department can be built in four ways, the same as at setup. Ask in plain words which one the CEO wants, unless the request already says it; the first is the plain path and needs no further question:
   - **the catalog entry as is**: `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` and `agent.md`;
   - **the catalog entry plus changes**: the same files, plus a "Changes for this org" section (`${CLAUDE_PLUGIN_ROOT}/templates/department/changes.md`) at the end of both, and the `tools:` line with the abilities added or dropped. Everything else, including running commands where the catalog has it, stays from the catalog. The rules are those of question 5 in the `init-fleet` skill ("Changing a catalog department"): a one-line reason per ability added, and an advisory entry never gains commands or helpers. `adapted: true` in `org.yaml`. The same applies to changing an existing catalog department later;
   - **fully custom**: `${CLAUDE_PLUGIN_ROOT}/templates/department/` with its scope, triggers, exclusions, single core job, and whether it runs commands (with the reason);
   - **the CEO's own agent or skill**: registered as it is, never rewritten, copied or moved: a charter from `${CLAUDE_PLUGIN_ROOT}/templates/department/own-charter.md`, an item with `from_catalog: own`, `kind`, `location` and no `model`, and a routing row. It can sit next to the others, replace one (the replaced department is removed in the same decision), or be the only one. If the CEO gives its file path, read it once, read-only, and show its tools; it brings its own tools, and this org grants it nothing.

   Ask the CEO for what is missing; never invent it. Then draft the display name and agent name (the persona in lowercase, or the id; a brought-in one keeps its own name; unique, never `reader`, `worker` or another department's id), the model tier (not for a brought-in one) and, if wanted, "top model, workers included" (`workers: same`). For a change to an existing department: the exact lines that change in its charter, its agent file and `org.yaml`.
3. Overlap check: compare what the new or changed department covers with every other department (charter scopes, changes sections, the core job and triggers of brought-in ones). For each piece of work two of them cover, add one plain line with a suggestion to the card, for example "Engineering and Security both cover security reviews: drop it from Engineering, or keep both and route security work to Security." Warnings only: they never block the card.
4. Review the draft as a whole (scope, tools, connectors, model) and give a one-line reason for each elevated grant: any connector, `Edit`, `Write`, `Bash` or `Agent`. Drop a grant that has no reason, and say so.
5. Account checks for a connector:
   - never one listed in `accounts.forbidden_connectors` in `org.yaml`;
   - only a connector of this org's own accounts (see "Account separation" in `CLAUDE.md`);
   - an advisory department gets only read-only connector tools, named one by one, never a whole server (`mcp__<server>__*`).
6. Write the decision card (`company/decision-queue.md`, own D code) with the draft, the reasons and a recommendation, and add it to "Waiting on the CEO".

A reply from the CEO to a denied permission is not a grant by itself: do not widen an allowlist on the strength of it; the grant goes through the card.

## After the CEO decides

Record the decision with the `record-decision` skill, then apply exactly what was decided:

- New department: `departments/<id>/charter.md` and `.claude/agents/<agent>.md` rendered from the catalog entry or the custom template, or only the charter for the CEO's own agent or skill (placeholders as in the `init-fleet` skill's placeholder reference), an item in `departments:` in `org.yaml` (`connectors: []` unless the decision grants one), and a row in the routing table of `CLAUDE.md`. Writes into `.claude/` may raise a permission prompt.
- Grant: add the connector to the department's `connectors:` in `org.yaml` and to the `tools:` list of its agent file. For the CEO's own agent or skill, record it in `org.yaml` only and tell the CEO that its own file decides what it can use.
- `workers: same` gained or lost: also update the worker model lines in its agent file.
- Removal: delete its charter folder and agent file, its item in `org.yaml` and its routing row. Git keeps the history.

Then commit with notice, as for any hq change.
