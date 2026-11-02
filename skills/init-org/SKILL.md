---
name: init-org
description: Setup wizard that generates a new organization hq repo (holding or company) from the ceo-of-agents templates. Asks groups of questions, shows a summary, then generates files. Run once, in an empty directory, only when the CEO explicitly invokes /ceo-of-agents:init-org.
argument-hint: "[optional: path to a file with all answers]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write Bash(git init *) Bash(git status *) Bash(git add *) Bash(git commit *) Bash(git remote add *) Bash(git -C * init *) Bash(git -C * add *) Bash(git -C * commit *) Bash(git -C * remote add *) Bash(git -C * fetch *) Bash(git -C * show *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(grep *) Bash(date *) Bash(python3 -c *)
---

# init-org: setup wizard

Reply to the CEO in the language the CEO writes in. Ask the questions in that language. Files you generate use the file language chosen in question 3.

You generate a new hq repo in the current directory from `${CLAUDE_PLUGIN_ROOT}/templates/`, `${CLAUDE_PLUGIN_ROOT}/catalog/`, `${CLAUDE_PLUGIN_ROOT}/gates/default.md` and `${CLAUDE_PLUGIN_ROOT}/schemas/`. Framework version: `0.1.1`.

## Rules

- Nothing is preselected. Never present an answer as the default that you will assume if the CEO stays silent. If the CEO does not answer a question, ask again.
- Ask one group of questions at a time (the numbered groups below), wait for the answers, then move on.
- Never push. Never run `git commit` without asking the CEO first.
- The only write outside the current directory is the policies repo directory the CEO named (holding only, question 10). The only reads outside the current directory and `${CLAUDE_PLUGIN_ROOT}` are the policy read check in question 9 (company only): `git -C <local> fetch` and `git -C <local> show <pin>:policy.yaml`.
- `mkdir` and `cp` write only into the target hq directory (the current directory) or the policies repo directory the CEO named. Never anywhere else.
- Every shell command in this skill is covered by `allowed-tools`, and every pattern there is used below. Use only those commands, with at least one argument each (for example `git status --short`).

## Step 0: check the directory

Run `ls -A`. If the directory holds anything other than `.git`, stop and tell the CEO what is there. Continue only if the CEO explicitly confirms generating into a non-empty directory. Never overwrite an existing file without a per-file confirmation.

## Non-interactive mode

If the CEO provides all answers in one message, or in a file passed as the argument, read them, map them to the question groups, ask only about what is missing or invalid, and skip the questions already answered. Still run validation, the policy check (question 9, company only) and show the full summary with a confirmation request before generating anything.

## Questions

### 1. Level
Ask: holding (the CEO as entrepreneur: registry of companies, policies, the most sensitive data) or company (one product, with its own code org and hq repo). Nothing is preselected.

### 2. Name and id
Ask for the org name and a short id used in codes (for example `ACME`). Validate the id: 2 to 8 characters, only capital letters A-Z and digits 0-9, starting with a letter. If invalid, explain and ask again. Do not invent an id from the name without the CEO choosing it; you may suggest one as a proposal only.

### 3. Languages
Ask for two separate settings: the language the chief of staff (CoS) uses in chat, and the language of every file in hq. You may recommend English for files (shared tooling and future collaborators read it more easily), but do not preselect it. Store language codes (`en`, `it`, `fr`, ...).

### 4. Departments
Nothing is preselected. Read the `Purpose` line of each of these files and show a numbered list with one line per entry:
`${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` for ids `engineering`, `design-brand`, `business`, `growth-social`, `legal`, `finance`, `tax`, `operations`.

Also offer: custom departments, and "none". For every custom department ask for: an id in kebab-case, a role name, a one-line purpose, its scope (what it covers), its triggers (when the chief of staff should route work to it), its exclusions (what it must not do or handle) and its single core job (one sentence). Scope, triggers and exclusions can have several items each; keep them as separate items. Custom departments are generated from `${CLAUDE_PLUGIN_ROOT}/templates/department/`. Do not invent any of these answers; if one is missing, ask again. Zero departments is valid. State that catalog entries are templates: the same entry chosen in another org creates an independent department with its own charter and memory. Department ids must be unique, kebab-case, letters, digits and hyphens.

For a holding, say that departments are optional like in any org (typical picks are advisory ones, but do not suggest any).

### 5. Names
For each chosen department ask for a display name: either the role name (for example "Engineering") or a persona name. Ask, with no preselected answer. Also ask for the CEO display name (optional, may stay empty). The CEO role id is `ceo`.

### 6. Approval gates
Read `${CLAUDE_PLUGIN_ROOT}/gates/default.md` and show its three-tier table (free, notice, ok) with the action ids. Ask whether the CEO accepts it as is or wants to move actions between tiers. Rules to enforce and to tell the CEO:
- Tier order is free < notice < ok.
- Advisory departments (legal, finance, tax) never perform `file-or-sign` or `make-payment` at all. No configuration can lower this; refuse any request that would.
- Principles: do not ask for OKs the table does not require; batch asks into the pending list; run exactly the approved action, nothing broader.

### 7. Connectors
For each department ask which connectors (MCP tool names or patterns, for example `mcp__github__*`) it may use. Nothing is granted unless the CEO names it: the answer "none" is valid.

For the advisory departments (legal, finance, tax) accept only read-only connector tools:
- Only single tool names (for example `mcp__x__get_record`). Refuse server wildcards such as `mcp__x__*`, because a wildcard can include write tools.
- For each tool, ask the CEO to confirm that it only reads (get, list, search, read).
- Refuse any tool that files, pays, sends, publishes or writes, with this one line: "Advisory departments never file, pay, send or publish, so they only get read-only connector tools." Ask for another tool or "none".

Other departments may get single tools or server patterns. Then ask for forbidden connectors that no agent of this org may ever use (for example accounts of an employer). Explain that connectors are granted per department, never globally, and work and personal accounts must not be mixed.

### 8. Model tiers
Show the tier list `[opus, sonnet, haiku]`, most to least capable. Ask which tier the CoS should use and which tier the departments should use (a per-department override is allowed; ask, no preselected answer). Explain the rule, which is fixed and is not a question: workers run one tier below their parent and never use a more capable model than their parent (`workers: one-down` in `org.yaml`). If the parent is the least capable tier, workers use the same tier. Every org gets two generic worker agents, `reader` and `worker`, which run one tier below the departments tier. Show the resulting worker model for the CoS, for the generic workers and for any department with an override in the summary.

### 9. Holding policy (company only; skip for a holding)
Ask whether this company follows a holding policy. It is optional. If yes, ask for:
- the policies repo git remote (a small repo that holds only `policy.yaml` and a README). It may be a git remote URL, or `""` when the policies repo has no remote yet (the CoS reads only `local` and `pin` anyway),
- the CEO's local clone path of that policies repo (read-only for this org),
- the pin (a commit sha).

If given, verify read-only, reading only the policy file. Optionally fetch first (it may fail offline; that is not an error):
```
git -C <local> fetch --quiet
git -C <local> show <pin>:policy.yaml
```
If it cannot be read, report the reason and ask for a corrected value or to continue without a policy. If it can be read, parse it (schema `policy/1`; see `${CLAUDE_PLUGIN_ROOT}/schemas/policy.yaml`) and run the tighten-only comparison against the answers so far, immediately:
1. Gates: for every action in the policy file, the company tier must be at or above the policy tier. An action absent from the company gates inherits the policy tier (fine).
2. Connectors: any policy `forbidden_connectors` entry present in any department's connectors is a loosening.
3. Language: policy `language.files` set and different from the company file language is a loosening.
4. Models: `models.cos`, `models.departments` or any department `model` more capable than `models.ceiling.departments`, or a worker model (one tier below its parent, including the generic `reader` and `worker`) more capable than `models.ceiling.workers`, is a loosening.

Report every loosening, one line each (for example `gate merge: company=notice, holding=ok`), before generating. A company may only tighten. Ask the CEO to adjust the answers; never silently fix them. Read nothing else in the policies repo.

### 10. Repositories
Ask these as questions, with no preselected answer. Both remotes are optional; "none" is valid.
- The hq git remote URL. If given, it is added after init (`git remote add origin <url>`); never pushed. Tell the CEO that, while there is no remote, the CoS skips pull and push and says so in its status line.
- Holding only: where to create the policies repo. Ask for an absolute path outside this hq directory (the CEO chooses it; do not propose one). Check with `ls -A <path>` that it does not exist or is empty; otherwise ask for another path. Then ask for the policies repo remote URL (optional; if given it is added with `git -C <path> remote add origin <url>`; never pushed). Explain that the policies repo must hold no sensitive data: only `policy.yaml` and `README.md`.

## Summary and confirmation

After the last group, show a compact summary: level, name and id, languages, departments (id, source, display name, model, connectors), gate changes versus the framework table, forbidden connectors, model tiers (CoS, departments, and the derived worker model of the generic `reader` and `worker` agents), policy and the result of the check, the hq remote (or none) and, for a holding, the policies repo path and remote. For a holding, also show the policy ceilings `models.ceiling.departments` and `models.ceiling.workers` (proposed as described under `{{CEILING_DEPARTMENTS}}` and `{{CEILING_WORKERS}}` in the placeholder reference; the CEO confirms or changes them) and say they are written to the policies repo. Ask for explicit confirmation. Also ask whether to write `.claude/settings.json` enabling the plugin for this repo (optional; yes or no, ask, do not assume). On any correction go back to the affected group and show the summary again.

## Generation

Only after confirmation.

Before generating, tell the CEO that the wizard writes into `.claude/` (`.claude/agents/*.md` and optionally `.claude/settings.json`), which Claude Code protects, so a permission prompt may appear and must be approved. For headless runs, start Claude Code with `--allowedTools "Edit(.claude/**)"` (`Write(...)` path rules are not accepted as allow rules; `Edit(path)` covers writes). Generate every file directly with your own tools; do not delegate file writes to sub-agents, which may lack the permissions.

1. List `${CLAUDE_PLUGIN_ROOT}/templates/instance/` and copy every file to the same relative path in the current directory, rendering as below.
2. Placeholders: render every `{{NAME}}` using the "Placeholder reference" below. Every placeholder used in `templates/` and `catalog/` is listed there.
3. Conditional blocks: render them as described under "Conditional markers" below.
4. Holding-only files: see "Holding-only files" below.
5. `{{DEPARTMENTS_TABLE}}` and `{{GATES_TABLE}}`: see the reference below (column specs are fixed there).
6. `org.yaml`: fill every field (`models.workers` stays the literal `one-down`), including `departments` (id, from_catalog, display_name, model, connectors), the `gates` lists, `accounts.forbidden_connectors`, `policies_repo` (holding: local and remote; company: `null`) and `policy` (company with a policy: repo, local, pin; otherwise `null`). It must follow `${CLAUDE_PLUGIN_ROOT}/schemas/org.yaml`.
7. Per department:
   - catalog department: copy `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` to `departments/<id>/charter.md` and `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/agent.md` to `.claude/agents/<id>.md`;
   - custom department: do the same from `${CLAUDE_PLUGIN_ROOT}/templates/department/` (`charter.md`, `agent.md`), filling the purpose, scope, triggers, exclusions and core job the CEO gave.
   Render the department placeholders from the reference below. Make sure the department file name equals the `name:` in its frontmatter.
   Not rendered: `catalog/README.md` (framework documentation, never copied). Catalog and department templates are used only for the departments chosen.
8. Create `departments/` only if there is at least one department. `company/briefs/.gitkeep` and `inbox/` come from the template.
9. Generic workers, for every org (also with zero departments): render `${CLAUDE_PLUGIN_ROOT}/templates/workers/reader.md` to `.claude/agents/reader.md` and `${CLAUDE_PLUGIN_ROOT}/templates/workers/worker.md` to `.claude/agents/worker.md`, with `{{MODEL_WORKERS}}`.
10. Holding only, the policies repo, at the absolute path the CEO gave in question 10: `mkdir -p <path>`, `git -C <path> init --quiet`, render `${CLAUDE_PLUGIN_ROOT}/templates/policies-repo/README.md` and `policy.yaml` into `<path>` (with `{{CEILING_DEPARTMENTS}}` and `{{CEILING_WORKERS}}`). Show `git -C <path> status --short`, then ask the CEO before its first commit. If approved: `git -C <path> add -A`, then `git -C <path> commit -m "chore: initialize policies"` with the attribution lines required by the session. If a remote was given: `git -C <path> remote add origin <url>`. Never push. Write nothing else outside the hq.
11. Decision `decisions/0001-setup.md`, from the template, following `${CLAUDE_PLUGIN_ROOT}/schemas/decision-record.md`: record all answers in Context and Decision (level, name and id, languages, departments with models and connectors, gate changes, forbidden connectors, model tiers, policy pin and check result, remotes, and for a holding the policies repo path). `Card: none`, `Decided by: ceo`. Add its row to `decisions/README.md`.
12. `company/state.md`: empty schema-valid state from the template (`schema: state/1`, the five fixed H2 sections, `- none` in empty sections, `next_action: 1`, `next_decision: 1`). If the policy check reported loosenings the CEO chose to keep, seed one A item per kept loosening, in the exact "Waiting on the CEO" line format of `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`: `- <ORG_ID>-A<n> [high]: <exact action> (since YYYY-MM-DD)` with urgency `high`, `since` = today (`date +%F`), and the text an exact action, for example `In org.yaml move \`merge\` from notice back to ok, or approve a holding policy change; see decision 0001`. Number them from 1 and set `next_action` to the last number plus one (`2` for a single item). Never use `normal` or omit the `since` date. Also keep the rest of `state.md` consistent: Risks and Open decisions stay `- none` unless the CEO says otherwise (the A item is the only record, and decision 0001 holds the details).
13. If the CEO agreed, write `.claude/settings.json` enabling the plugin, for example:
    ```json
    { "enabledPlugins": { "ceo-of-agents@ceo-of-agents": true } }
    ```
    Check the marketplace name in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/marketplace.json` before writing it. Otherwise skip this file.

## Placeholder reference

Render with plain string replacement. Values are single-line unless stated. Never leave a `{{...}}` behind. The org-wide placeholders also apply to `templates/workers/` and `templates/policies-repo/`.

### Org-wide (all files under `templates/instance/`)

| Placeholder | Value |
|---|---|
| `{{ORG_NAME}}` | Org name as given (question 2) |
| `{{ORG_ID}}` | Org id (question 2), for example `ACME` |
| `{{LEVEL}}` | `company` or `holding` |
| `{{CHAT_LANGUAGE}}` | Chat language code (question 3), for example `en` |
| `{{FILE_LANGUAGE}}` | File language code (question 3) |
| `{{CEO_ROLE_ID}}` | `ceo` |
| `{{CEO_DISPLAY_NAME}}` | CEO display name without quotes, or an empty string. The template already wraps it in quotes (`display_name: "..."`) |
| `{{FRAMEWORK_VERSION}}` | `0.1.1` |
| `{{DATE}}` | Today, `YYYY-MM-DD` (`date +%F`) |
| `{{MODEL_COS}}` | Tier chosen for the CoS (question 8) |
| `{{MODEL_DEPARTMENTS}}` | Tier chosen for departments (question 8; a department may override) |
| `{{MODEL_WORKERS}}` | The tier one below `models.departments` (`{{MODEL_DEPARTMENTS}}`) in `models.tiers`; the same tier if `{{MODEL_DEPARTMENTS}}` is the last. Used in `templates/workers/*` and in prose (`CLAUDE.md`, `decisions/0001-setup.md`). `org.yaml` keeps the literal rule `workers: one-down`, never a model name |
| `{{DEPARTMENTS_TABLE}}` | Markdown table `Agent id \| Name \| Role \| Use for`, one row per department: `Agent id` = the department id (`name` in its agent file), `Name` = display name (persona or role name), `Role` = the catalog role name (for example Business; the one in the agent file's intro line) or, for a custom department, the custom department's role name as given when it was defined, `Use for` = a short routing phrase of at most 12 words derived from the charter's `Purpose` line (never the full sentence). Used inside the `departments` condition only (for none, the `no-departments` block applies) |
| `{{GATES_TABLE}}` | Markdown table `Tier \| Rule \| Action ids`, exactly three rows (free, notice, ok) in that order. `Rule` is the short rule from `${CLAUDE_PLUGIN_ROOT}/gates/default.md` (free: do it and mention it; notice: one line before acting; ok: the CEO's explicit OK). `Action ids` are the final action ids of that tier, in backticks, comma-separated |
| `{{DEPARTMENTS_YAML}}` | `[]` for no departments. Otherwise the value starts with a newline and is a block list indented two spaces under `departments:`; each item has `id`, `from_catalog` (catalog id or `custom`), `display_name`, `model`, `connectors` (inline list such as `[mcp__github__*]`, or `[]`) |
| `{{GATES_FREE}}` `{{GATES_NOTICE}}` `{{GATES_OK}}` | Final action ids of that tier as an inline YAML list: `[a, b, c]` (`[]` if the tier is empty). Each action id is in exactly one tier |
| `{{FORBIDDEN_CONNECTORS}}` | Inline YAML list of forbidden connector patterns, `[mcp__x__*, mcp__y__*]`, or `[]` |
| `{{POLICY_YAML}}` | Company only. `null` when there is no holding policy. Otherwise the value starts with a newline and is a mapping indented two spaces under `policy:` with keys `repo`, `local`, `pin` (question 9) |
| `{{POLICIES_REPO_YAML}}` | Holding: the value starts with a newline and is a mapping indented two spaces under `policies_repo:` with keys `local` (absolute path, question 10) and `remote` (the URL, or `""` when none). Company: `null` |
| `{{CEILING_DEPARTMENTS}}` | Holding only, rendered into the policies repo `policy.yaml`. Most capable model a company department may use. Proposed: the holding's own department model (`{{MODEL_DEPARTMENTS}}`). Show it in the summary; the CEO confirms or changes it; it must be a name from `models.tiers` |
| `{{CEILING_WORKERS}}` | Holding only, same file. Most capable model a company worker may use. Proposed: the tier one below `{{CEILING_DEPARTMENTS}}` (the same if it is the last). A name from `models.tiers`, never `one-down` |
| `{{SETUP_QUESTION_COUNT}}` | Number of question groups asked (questions 1 to 10). A holding skips question 9, which stays in the table as a row marked not applicable and is not counted. Custom department follow-ups belong to question 4 and do not add groups. Counted by groups that apply to the level, also in non-interactive mode. Holding: 9. Company: 10 |
| `{{SETUP_DEPARTMENTS}}` | Cell text for `decisions/0001-setup.md`: `id (model)` for each department, comma-separated, or `none` |
| `{{SETUP_PERSONAS}}` | `id: display name` for each department whose display name differs from the role name, plus `CEO: <name>` if given; `none` if there is nothing |
| `{{SETUP_GATES}}` | `framework table` or `framework table with changes: <action> <from> -> <to>; ...` |
| `{{SETUP_CONNECTORS}}` | `id: patterns` per department with connectors, `;`-separated, plus `forbidden: patterns` if any; `none` if there is nothing |
| `{{SETUP_REPOS}}` | Cell text for `decisions/0001-setup.md`: `hq remote: <url or none>` and, for a holding, `; policies repo: <path>, remote: <url or none>` |
| `{{SETUP_POLICY}}` | `none` for a company without policy, `not applicable (holding)` for a holding, otherwise `<repo> @ <short pin> (check: OK)` or `<repo> @ <short pin> (check: N loosening(s) kept)` |

Table cell values (`SETUP_*`) must not contain `|` or newlines.

### Per department (`catalog/<id>/*` and `templates/department/*`)

| Placeholder | Value |
|---|---|
| `{{DEPT_ID}}` | Department id (kebab-case) |
| `{{DISPLAY_NAME}}` | Display name (question 5). The agent intro renders as "You are {{DISPLAY_NAME}}, the {{ROLE_NAME}} department of {{ORG_NAME}}." If the display name equals the role name it reads "You are Business, the Business department of Acme."; this repetition is accepted, keep it |
| `{{ROLE_NAME}}` | The department's role name, for example "Customer Support" (the catalog role or the custom role from question 4). Always the role name, even when a persona name is chosen as the display name |
| `{{ORG_NAME}}`, `{{ORG_ID}}` | As above |
| `{{MODEL}}` | The department's model tier |
| `{{WORKER_MODEL}}` | The tier one below `{{MODEL}}` in `models.tiers` (the same tier if it is already the last) |
| `{{DEPT_SCOPE}}` | Custom departments only. The scope items as markdown bullet lines, each starting with `- `, one per line (multi-line value) |
| `{{DEPT_TRIGGERS}}` | Custom departments only. The triggers as bullet lines, each starting with `- ` |
| `{{DEPT_EXCLUSIONS}}` | Custom departments only. The exclusions as bullet lines, each `- <thing> (owner: <department or CEO>)`. If the CEO gave no owner, ask which department or the CEO owns it |
| `{{DEPT_CORE_JOB}}` | Custom departments only. The single core job: one single-line sentence ending with a period, containing no `: ` |
| `{{DEPT_TRIGGERS_LINE}}` | Custom departments only. The trigger items on one line, comma-separated noun phrases, derived from the same bullets as `{{DEPT_TRIGGERS}}` (no extra question). No `: `, no trailing period. Used in the one-line YAML `description:` of the agent file |
| `{{DEPT_EXCLUSIONS_LINE}}` | Custom departments only. The exclusion items on one line, same format as `{{DEPT_TRIGGERS_LINE}}`, derived from the same bullets as `{{DEPT_EXCLUSIONS}}` without the `(owner: ...)` parts. No `: `, no trailing period |
| `{{CONNECTORS}}` | Empty string when the department has no connectors; otherwise `, mcp__x__*, mcp__y__*` (leading comma and space), appended to the `tools:` list in the agent file. For legal, finance and tax only the read-only single tool names confirmed in question 7 |

### Conditional markers

Two comment styles exist, handle both. Markdown files (`.md`) use `<!-- IF x -->` ... `<!-- END IF -->`. YAML files (`org.yaml`) use `# IF x` ... `# END IF`. Each marker sits on its own line; blocks are not nested. In `org.yaml` the `# IF holding` block holds `policy: null` and `policies_repo: {{POLICIES_REPO_YAML}}`; the `# IF company` block holds `policy: {{POLICY_YAML}}` and `policies_repo: null`. Exactly one of the two blocks survives. Keep the content when the condition is true, drop the whole block when it is false, and always delete the marker lines.

| Condition | True when |
|---|---|
| `holding` | level is holding |
| `company` | level is company |
| `policy` | level is company and a holding policy source was given |
| `departments` | at least one department was chosen |
| `no-departments` | no department was chosen |

### Holding-only files

`portfolio.yaml` is skipped entirely for a company: do not create it. For a holding, create it; it stays `orgs: []`. The holding hq has no `policies/` directory: its policies live in the separate policies repo (generation step 10).

## Post-generation checks

Run them and fix what fails; report the results:
- `grep -rnE '\{\{|<!-- (IF|END IF)|# (IF|END IF)|<[A-Z]|\.\.\.' . --exclude-dir=.git` finds nothing, in the hq and, for a holding, in the policies repo directory. Check every hit. A hit is a leftover and must be fixed, unless it is legitimate text the CEO wrote (for example an ellipsis inside a quoted answer); then list it in the report as excluded and why.
- `org.yaml` parses. Try `python3 -c "import yaml,sys; yaml.safe_load(open('org.yaml'))"`; if that fails (for example no `yaml` module), check it carefully by reading and say explicitly in the final report that YAML was checked by reading only.
- Every expected `.claude/agents/<id>.md` exists (one per department in `org.yaml`), plus `.claude/agents/reader.md` and `.claude/agents/worker.md`. If any is missing, stop and tell the CEO clearly, listing the missing files and the likely cause (`.claude/` write permission, see Generation); never report success with missing agent files.
- Mandatory, never skipped: compare `company/state.md` against `${CLAUDE_PLUGIN_ROOT}/schemas/state.md` item by item: frontmatter keys and values, the 5 H2 headings in exact order, the line formats, and `- none` in every empty section. List the result of each item in the final report. A skipped or partial check is reported as a failure, not as done.
- Advisory department agent files (legal, finance, tax, from the catalog) have no `Agent` in `tools:`, and their connectors are single read-only tool names.
- `.claude/agents/reader.md` and `worker.md` have `model:` equal to `{{MODEL_WORKERS}}` as rendered.
- Every `.claude/agents/*.md` has an explicit `tools:` list in its frontmatter, and its `name` equals its file name.
- The files in `departments/` match the departments in `org.yaml`, and the display names appear in `CLAUDE.md`.

## Git

If there is no `.git`, run `git init --quiet`. If the CEO gave an hq remote, run `git remote add origin <url>`. Show `git status --short`. Ask the CEO before the first commit. If approved, run `git add -A`, then commit everything with `git commit -m` and the message `chore: initialize <org name> hq with ceo-of-agents 0.1.1` and the attribution lines required by the session. Never push. Tell the CEO how to push on their own (and how to add a remote if none was given). For a holding, say the same for the policies repo.

## End

Tell the CEO in chat language: what was generated (file count, departments, the generic `reader` and `worker` agents and their model), any open A items, the policies repo path (holding), that the CoS skips pull and push while there is no hq remote, and how to start: open Claude Code in this directory and say what is on their mind; the CoS (from `CLAUDE.md`) takes it from there. Mention `/ceo-of-agents:intake`, `/ceo-of-agents:record-decision`, `/ceo-of-agents:weekly-brief`, and for a holding `/ceo-of-agents:portfolio-brief`.
