---
name: portfolio-brief
description: Holding-only, on-demand portfolio brief. Pulls each registered company hq read-only, reads its company/state.md, composes one pending list across the holding and all companies (urgency, then level, then age), and writes company/briefs/YYYY-MM-DD-portfolio.md. Use when the CEO asks for a portfolio brief or a view across orgs. Refuses to run in a company hq.
allowed-tools: Read Write Edit Grep Glob Bash(git -C * pull --ff-only) Bash(git -C * log:*) Bash(git -C * status:*) Bash(git pull:*) Bash(git status:*) Bash(git add:*) Bash(git commit:*) Bash(ls:*) Bash(date:*)
---

# portfolio-brief (holding only)

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write the brief in the file language (`language.files`).

## Guard

Read `org.yaml`. If `org.level` is not `holding`, stop and say that this skill only runs in a holding hq. Do nothing else.

## Hard rules

- The holding is a registry. Never write to a company hq. Never commit in a company hq. Never run any git command in a company hq that changes it, other than the single `git -C <path> pull --ff-only` below. Read its files only through the Read tool or read-only git.
- Read only `<path>/company/state.md` of each company. Do not read its decisions, departments or inbox.
- Store no credentials. Pulls use the CEO's own git credentials already on the machine.
- The pending list is a view. Items are answered and recorded in the owning org by its own chief of staff, never here.

## Steps

1. Read `portfolio.yaml` (schema `portfolio/1`: `stale_after_days`, `orgs` with `id`, `name`, `path`, `remote`). Expand `~` in paths. If `orgs` is empty, say so and still write a brief with the holding's own items.

2. For each org: run `git -C <path> pull --ff-only`. If it fails (offline, diverged, missing path), record `pull failed: <reason>`, read the local copy if it exists, and mark the org. Then read `<path>/company/state.md`. If it is missing, record `state.md missing`.

3. Validate each state file: the frontmatter must have `schema: state/1`, `org_id`, `level`, `last_updated`, `framework_version`, `next_action`, `next_decision`, and the five H2 sections in order (see `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`). An unknown schema version: report `unknown schema <value>` for that org and do not guess its content; skip its items and say so. A known schema with problems: report the problem, use what parses.

4. Staleness: an org is stale if `last_updated` is older than `stale_after_days` days before today. Mark stale orgs clearly; their items stay in the list with the staleness shown.

5. Read the holding's own `company/state.md` (Waiting on the CEO and Open decisions).

6. Compose one pending list:
   - the holding's own items in "Waiting on the CEO";
   - every org's "Waiting on the CEO" items;
   - every org's "Open decisions" line carrying `[escalate: holding]` (if it is already in Waiting, list it once and mark it escalated).
   Keep each code exactly as the owning org wrote it (`ACME-D3`, `ACME-A2`). Order by urgency (high, normal, low; items without urgency count as normal), then level (holding before company), then age (oldest `since` first). For each escalated item, add the holding's advice next to the code: the holding's view across tax, personal legal and cash across orgs, drawn only from the holding's own departments and files; if there is nothing to add, write `no holding advice yet`. Do not put sensitive holding detail into the brief lines that the CEO might copy into a company.

7. Write `company/briefs/YYYY-MM-DD-portfolio.md` in the holding (today's date), sections:
   - `## Headline`
   - `## Organizations`: one status line per org: `ID name: last_updated YYYY-MM-DD, stale: yes|no, pull: ok|failed (<reason>), schema: state/1`.
   - `## Pending list`: the composed list, table `Code | Org | Urgency | Item | Since | Holding advice`.
   - `## Risks and key numbers by org`: risks and key numbers from each state (with their source and date as written).
   - `## Notes`: pull failures, unknown schemas, stale orgs.
   Open the pending list with this statement: "This list is a view. Answer each item in its owning org; the owning chief of staff records it there."

8. Update the holding's `company/state.md` `last_updated`. The brief and this edit are an hq commit with gate "notice": write one line to the CEO and commit in the holding with `docs: portfolio brief YYYY-MM-DD` and the attribution lines required by the session. Never push unless the CEO asks.

9. Chat summary in the chat language, at most 10 lines: orgs read, stale or failed ones, the top pending codes in order, and a reminder that the CEO answers each in the owning org. Give the brief's path.
