---
name: hq-version
description: Compare this hq's framework version with the installed ceo-of-agents plugin version and, after the CEO's OK, apply the pending migrations in order. Use at session start in a ceo-of-agents hq, and when the CEO approves an hq update.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git status:*) Bash(git diff:*) Bash(git add:*) Bash(git mv:*) Bash(git commit:*) Bash(git remote:*) Bash(git push:*) Bash(ls:*) Bash(date:*)
---

# hq-version: check the hq against the plugin, then migrate

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. A department agent never does.

Why a skill: the installed plugin version and the migration notes live in the plugin folder. Only plugin skills reach that folder, through `${CLAUDE_PLUGIN_ROOT}`; a project `CLAUDE.md` cannot, and the install path differs per machine and per version.

## Check

Run at session start. It is read-only, except for one A item.

1. Installed version: `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. If the file is unreadable, the version is unknown.
2. hq version: `framework_version` in `org.yaml` and in the `company/state.md` frontmatter. If they differ, report both and use the lower one. If it is missing, the version is unknown.
3. Compare `major.minor.patch` as numbers, not as text.

Then:

- Equal: report nothing.
- Behind: build the chain of migrations. Start at the hq version and look for `${CLAUDE_PLUGIN_ROOT}/migrations/<from>-to-<to>.md` (use `ls` on the folder). Follow each file's `<to>` as the next `<from>`, until the installed version. For a one-line description of each step, use "Current status" in `${CLAUDE_PLUGIN_ROOT}/migrations/README.md`. If a step is missing, say from which version no migration exists and that this part must be done by hand with the CEO. Never guess edits. Put one line in the status, for example: `hq on 0.5.0, plugin 0.7.0: 2 updates to apply (0.5.0-to-0.6.0: product repos and roadmap; 0.6.0-to-0.7.0: agents named after personas, version check).`
  Then add one A item to "Waiting on the CEO", unless an open A item for the hq update already exists, in the exact line format of `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`: `- <ORG_ID>-A<n> [normal]: approve updating hq from <hq> to <installed> (migrations <list>, in the plugin's migrations/ folder) (since YYYY-MM-DD)`. Increment `next_action`. If an open item has an older target, update its text instead of adding another.
- Ahead: say `hq on X is newer than the installed plugin Y: update the plugin (/plugin, Installed tab, Update now).` and continue.
- Unknown: say `Version check skipped: <reason>` and continue.

Never edit any other hq file during the check.

## Apply

Only after the CEO approves the A item. Applying a migration is an hq commit, but it always needs the CEO's OK: never apply one silently.

For each migration in order, one at a time:

1. Run `git status --short`. If it shows this session's own hq edits (for example the A item), commit them first with notice; if it shows anything else, stop and ask. The hq `framework_version` must equal the migration's `<from>`.
2. Read the migration file in full, then the hq files it edits.
3. Apply the edits exactly as written. Where the migration says to ask the CEO (for example an agent-name clash), ask one plain question and wait. Writes into `.claude/` may raise a permission prompt. If it is denied, do not work around it: stop and list the missing edits.
4. Run its "Check after applying" section. Fix what fails, or stop and report.
5. Show a short summary: one line per changed file (from `git status --short`) and one or two plain lines on what it means for the CEO.
6. Commit with notice (one line to the CEO first): `chore: migrate hq to <to>` with the attribution lines required by the session. Then push if `git remote` is not empty.

After the last migration: remove the A item, set `last_updated` in `company/state.md`, commit with notice, and say the hq is up to date.

On any failure: stop, name the migration and the failed check, and leave the working tree as it is (never reset). Add nothing silently.
