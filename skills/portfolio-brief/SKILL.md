---
name: portfolio-brief
description: Holding-only, on-demand portfolio brief. Fetches each registered company hq read-only (no change to its working tree), reads its company/state.md from the fetched default branch, composes one pending list across the holding and all companies (urgency, then level, then age), and writes company/briefs/YYYY-MM-DD-portfolio.md. Use when the CEO asks for a portfolio brief or a view across orgs. Refuses to run in a company hq. Skips job hqs (org.purpose job) without reading their state.
allowed-tools: Read Write Edit Grep Glob Bash(git -C * fetch *) Bash(git -C * show *) Bash(git -C * status *) Bash(git -C * branch *) Bash(git -C * symbolic-ref *) Bash(git add *) Bash(git commit *) Bash(ls *) Bash(date *)
---

# portfolio-brief (holding only)

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write the brief in the file language (`language.files`).

## Guard

Read `org.yaml`. If `org.level` is not `holding`, stop and say that this skill only runs in a holding hq. Do nothing else.

## Hard rules

- The holding is a registry. Never write to a company hq. Never commit in a company hq. Never run any git command in a company hq that changes its working tree, its index, its branches or its commits. The only git commands allowed there are `fetch` (it updates only remote-tracking refs, never the working tree), `show`, `status`, `branch --show-current` and `symbolic-ref`. Read its state only with `git show` on the fetched ref (or on the local default branch when there is no remote). A dirty clone or a clone on another branch never blocks the brief and is never touched.
- Read only `<path>/company/state.md` of each company, plus the single key `org.purpose` from its `org.yaml` (same ref) to skip job hqs. Do not read or quote any other key of `org.yaml`, nor its decisions, departments or inbox.
- Run one git command per Bash call, as `git -C <absolute path> <subcommand>`. Do not use `cd`, shell variables, `&&`, `;` or pipes: the `allowed-tools` patterns match a single command, and a compound command is refused.
- Store no credentials. Fetches use the CEO's own git credentials already on the machine.
- The pending list is a view. Items are answered and recorded in the owning org by its own chief of staff, never here.

## Steps

1. Read `portfolio.yaml` (schema `portfolio/1`: `stale_after_days`, `orgs` with `id`, `name`, `path`, `remote`; `remote` may be `""` for a company with no remote). Expand `~` in paths. If `orgs` is empty, say so and still write a brief with the holding's own items.

2. For each org, read it without touching its working tree (use `ls` to check the path exists; if it is missing, record `path missing` and go on):
   - `git -C <path> fetch origin`. If it fails (offline, no remote, never fetched), record `fetch failed: <reason>` and continue with the last fetched ref; if there is no remote-tracking ref at all, record `never fetched`.
   - Default branch: `git -C <path> symbolic-ref --short refs/remotes/origin/HEAD` (gives `origin/<default>`). If it fails, use `origin/main`.
   - Purpose check, before reading state (also in the no-remote fallback below, on the ref chosen there): `git -C <path> show <ref>:org.yaml`, and read only `org.purpose`. If it is `job`: skip the org entirely (do not read its state; no items, no risks). Its Organizations line is `ID name: skipped (job hq, never part of a portfolio; remove it from portfolio.yaml)` and a Notes line says the same. If `org.yaml` cannot be read or has no `org.purpose` (schema `org/1`), treat the org as `company` and go on.
   - State: `git -C <path> show origin/<default>:company/state.md`. If it fails, record `state.md missing`.
   - No remote fallback: if there is no remote-tracking ref (the entry has `remote: ""`, the clone has no remote, or it was never fetched), read the local default branch instead. Find it with `git -C <path> symbolic-ref --short HEAD` (the checked-out branch; use `main` if that fails), then run `git -C <path> show <default>:company/state.md`. Record the read as `read: local <default> (no remote, may include unpushed changes)`. This is the only wording for a local read. Still read-only: `show` never touches the working tree.
   - Clone checks, read-only: `git -C <path> status --porcelain` (any output means `clone: dirty`, else `clean`) and `git -C <path> branch --show-current` (record `branch: <name>` only when it differs from `<default>`). These are information only: the brief reads `origin/<default>` (or the local default branch in the no-remote fallback) anyway.

3. Validate each state file: the frontmatter must have `schema: state/1`, `org_id`, `level`, `last_updated`, `framework_version`, `next_action`, `next_decision`, and the five H2 sections in order (see `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`). An unknown schema version: report `unknown schema <value>` for that org and do not guess its content; skip its items and say so. A known schema with problems: report the problem, use what parses.

4. Staleness: an org is stale if `last_updated` is older than `stale_after_days` days before today. Mark stale orgs clearly; their items stay in the list with the staleness shown.

5. Read the holding's own `company/state.md` (Waiting on the CEO and Open decisions).

6. Compose one pending list:
   - the holding's own items in "Waiting on the CEO";
   - every org's "Waiting on the CEO" items;
   - every org's "Open decisions" line carrying `[escalate: holding]` (if it is already in Waiting, list it once and mark it escalated).
   Keep each code exactly as the owning org wrote it (`ACME-D3`, `ACME-A2`). Order by urgency (high, normal, low; items without urgency count as normal), then level (holding before company), then age (oldest `since` first). For each escalated item, add the holding's advice next to the code: the holding's view across tax, personal legal and cash across orgs, drawn only from the holding's own departments and files; if there is nothing to add, write `no holding advice yet`. Do not put sensitive holding detail into the brief lines that the CEO might copy into a company.

7. Write `company/briefs/YYYY-MM-DD-portfolio.md` in the holding (today's date), sections:
   - `## Headline`: write it last, after the `## Pending list` table is composed. Compute every count it states (total items, high-urgency items, items per org) from the rows of that final table, not from the source states or from memory. Re-count the rows and compare with the Headline numbers before writing the file; fix any mismatch.
   - `## Organizations`: one status line per org (a skipped job hq gets the `skipped (job hq, never part of a portfolio; remove it from portfolio.yaml)` variant instead): `ID name: last_updated YYYY-MM-DD, stale: yes|no, fetch: ok|failed (<reason>)|never, clone: clean|dirty, schema: state/1`, with `, branch: <name>` added only when the clone is on a branch other than the default. Add `, read: local <default> (no remote, may include unpushed changes)` when the local fallback was used; otherwise the state shown is the one on `origin/<default>`.
   - `## Pending list`: the composed list, table with exactly these columns: `Code | Org | Urgency | Item | Since | Holding advice`. `Holding advice` is filled only for items marked `[escalate: holding]` (the holding CoS's advice on tax, personal legal or cash across orgs, or `pending: <what analysis is needed>`); every other item has `—` there. The holding's own Waiting-on-the-CEO items are included (`Org` = the holding id).
   - `## Risks and key numbers by org`: risks and key numbers from each state (with their source and date as written), one labelled subsection per registered org plus one for the holding itself (labelled as the holding).
   - `## Notes`: fetch failures or never-fetched orgs (the state shown may be old), dirty clones, clones on a non-default branch (local changes are not in the brief), unknown schemas, stale orgs.
   Open the pending list with this statement: "This list is a view. Answer each item in its owning org; the owning chief of staff records it there."

8. Get today's date with `date +%F`. Update the holding's `company/state.md` `last_updated`. The brief and this edit are an hq commit with gate "notice": write one line to the CEO and commit in the holding with `docs: portfolio brief YYYY-MM-DD` and the attribution lines required by the session. Never push unless the CEO asks.

9. Chat summary in the chat language, at most 10 lines: orgs read, stale or failed ones, the top pending codes in order, and a reminder that the CEO answers each in the owning org. Give the brief's path.
