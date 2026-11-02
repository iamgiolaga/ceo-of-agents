---
name: init-org
description: Setup wizard that generates a new organization hq repo (holding or company) from the ceo-of-agents templates. Asks nine groups of questions, shows a summary, then generates files. Run once, in an empty directory, only when the CEO explicitly invokes /ceo-of-agents:init-org.
argument-hint: "[optional: path to a file with all answers]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write Bash(git init:*) Bash(git status:*) Bash(git -C:*) Bash(git add:*) Bash(git commit:*) Bash(ls:*) Bash(mkdir:*) Bash(cp:*) Bash(grep:*) Bash(date:*) Bash(python3 -c:*)
---

# init-org: setup wizard

Reply to the CEO in the language the CEO writes in. Ask the questions in that language. Files you generate use the file language chosen in question 3.

You generate a new hq repo in the current directory from `${CLAUDE_PLUGIN_ROOT}/templates/`, `${CLAUDE_PLUGIN_ROOT}/catalog/`, `${CLAUDE_PLUGIN_ROOT}/gates/default.md` and `${CLAUDE_PLUGIN_ROOT}/schemas/`. Framework version: `0.1.0`.

## Rules

- Nothing is preselected. Never present an answer as the default that you will assume if the CEO stays silent. If the CEO does not answer a question, ask again.
- Ask one group of questions at a time (the numbered groups below), wait for the answers, then move on.
- Never push. Never run `git commit` without asking the CEO first.
- Do not read or write outside the current directory and `${CLAUDE_PLUGIN_ROOT}`, except the read-only policy check in question 9.

## Step 0: check the directory

Run `ls -A`. If the directory holds anything other than `.git`, stop and tell the CEO what is there. Continue only if the CEO explicitly confirms generating into a non-empty directory. Never overwrite an existing file without a per-file confirmation.

## Non-interactive mode

If the CEO provides all answers in one message, or in a file passed as the argument, read them, map them to the nine groups, ask only about what is missing or invalid, and skip the questions already answered. Still run validation, the policy check (question 9) and show the full summary with a confirmation request before generating anything.

## Questions

### 1. Level
Ask: holding (the CEO as entrepreneur: registry of companies, policies, the most sensitive data) or company (one product, with its own code org and hq repo). No default.

### 2. Name and id
Ask for the org name and a short id used in codes (for example `ACME-D3`). Validate the id: 2 to 8 characters, only capital letters A-Z and digits 0-9, starting with a letter. If invalid, explain and ask again. Do not invent an id from the name without the CEO choosing it; you may suggest one as a proposal only.

### 3. Languages
Ask for two separate settings: the language the chief of staff (CoS) uses in chat, and the language of every file in hq. You may recommend English for files (shared tooling and future collaborators read it more easily), but do not preselect it. Store language codes (`en`, `it`, `fr`, ...).

### 4. Departments
Nothing is preselected. Read the `Purpose` line of each of these files and show a numbered list with one line per entry:
`${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` for ids `engineering`, `design-brand`, `business`, `growth-social`, `legal`, `finance`, `tax`, `operations`.

Also offer: custom departments (the CEO gives an id in kebab-case and a one-line purpose; they are generated from `${CLAUDE_PLUGIN_ROOT}/templates/department/`), and "none". Zero departments is valid. State that catalog entries are templates: the same entry chosen in another org creates an independent department with its own charter and memory. Department ids must be unique, kebab-case, letters, digits and hyphens.

For a holding, say that departments are optional like in any org (typical picks are advisory ones, but do not suggest any).

### 5. Names
For each chosen department ask for a display name. The default is the role name (for example "Engineering"); a persona name is optional. Also ask for the CEO display name (optional, may stay empty). The CEO role id is `ceo`.

### 6. Approval gates
Read `${CLAUDE_PLUGIN_ROOT}/gates/default.md` and show its three-tier table (free, notice, ok) with the action ids. Ask whether the CEO accepts it as is or wants to move actions between tiers. Rules to enforce and to tell the CEO:
- Tier order is free < notice < ok.
- Advisory departments (legal, finance, tax) never perform `file-or-sign` or `make-payment` at all. No configuration can lower this; refuse any request that would.
- Principles: do not ask for OKs the table does not require; batch asks into the pending list; run exactly the approved action, nothing broader.

### 7. Connectors
For each department ask which connectors (MCP tool patterns, for example `mcp__github__*`) it may use. Nothing is granted by default: the answer "none" is valid. Then ask for forbidden connectors that no agent of this org may ever use (for example accounts of an employer). Explain that connectors are granted per department, never globally, and work and personal accounts must not be mixed.

### 8. Model tiers
Show the tier list `[opus, sonnet, haiku]`, most to least capable. Ask which tier the CoS should use and which tier the departments should use by default (a per-department override is allowed). Explain the rule, which is fixed and is not a question: workers run one tier below their parent and never use a more capable model than their parent (`workers: one-down` in `org.yaml`). If the parent is the least capable tier, workers use the same tier. Show the resulting worker model for the CoS (and for any department with an override) in the summary.

### 9. Holding policy (company only; skip for a holding)
Ask whether this company follows a holding policy. It is optional. If yes, ask for:
- the policy source remote (the holding hq git remote),
- the CEO's local clone path of the holding hq,
- the path inside it (normally `policies/`),
- the pin (a commit sha).

If given, verify read-only, reading only the policy file:
```
git -C <local> show <pin>:<path>policy.yaml
```
If it cannot be read, report the reason and ask for a corrected value or to continue without a policy. If it can be read, parse it (schema `policy/1`; see `${CLAUDE_PLUGIN_ROOT}/schemas/policy.yaml`) and run the tighten-only comparison against the answers so far, immediately:
1. Gates: for every action in the holding file, the company tier must be at or above the holding tier. An action absent from the company gates inherits the holding tier (fine).
2. Connectors: any holding `forbidden_connectors` entry present in any department's connectors is a loosening.
3. Language: holding `language.files` set and different from the company file language is a loosening.
4. Models: `models.cos`, `models.departments` or any department `model` more capable than `models.ceiling.departments`, or a worker model (one tier below its parent) more capable than `models.ceiling.workers`, is a loosening.

Report every loosening, one line each (for example `gate merge: company=notice, holding=ok`), before generating. A company may only tighten. Ask the CEO to adjust the answers; never silently fix them. Read nothing else in the holding repo.

## Summary and confirmation

After the last group, show a compact summary: level, name and id, languages, departments (id, source, display name, model, connectors), gate changes versus the default, forbidden connectors, model tiers (CoS, departments, and the derived worker model), policy and the result of the check. For a holding, also show the policy ceilings `models.ceiling.departments` and `models.ceiling.workers` (derived as described under `{{CEILING_DEPARTMENTS}}` and `{{CEILING_WORKERS}}` in the placeholder reference) and let the CEO change them. Ask for explicit confirmation. Also ask whether to write `.claude/settings.json` enabling the plugin for this repo (optional, default no; ask, do not assume). On any correction go back to the affected group and show the summary again.

## Generation

Only after confirmation.

Before generating, tell the CEO that the wizard writes into `.claude/` (`.claude/agents/*.md` and optionally `.claude/settings.json`), which Claude Code protects, so a permission prompt may appear and must be approved. For headless runs, start Claude Code with `--allowedTools "Edit(.claude/**)"` (`Write(...)` path rules are not accepted as allow rules; `Edit(path)` covers writes). Generate every file directly with your own tools; do not delegate file writes to sub-agents, which may lack the permissions.

1. List `${CLAUDE_PLUGIN_ROOT}/templates/instance/` and copy every file to the same relative path in the current directory, rendering as below.
2. Placeholders: render every `{{NAME}}` using the "Placeholder reference" below. Every placeholder used in `templates/` and `catalog/` is listed there.
3. Conditional blocks: render them as described under "Conditional markers" below.
4. Holding-only files: see "Holding-only files" below.
5. `{{DEPARTMENTS_TABLE}}` and `{{GATES_TABLE}}`: see the reference below (column specs are fixed there).
6. `org.yaml`: fill every field (`models.workers` stays the literal `one-down`), including `departments` (id, from_catalog, display_name, model, connectors), the `gates` lists, `accounts.forbidden_connectors` and, if given, `policy` (source, local, path, pin). It must follow `${CLAUDE_PLUGIN_ROOT}/schemas/org.yaml`.
7. Per department:
   - catalog department: copy `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` to `departments/<id>/charter.md` and `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/agent.md` to `.claude/agents/<id>.md`;
   - custom department: do the same from `${CLAUDE_PLUGIN_ROOT}/templates/department/` (`charter.md`, `agent.md`), filling the purpose the CEO gave.
   Render the department placeholders from the reference below. Make sure the department file name equals the `name:` in its frontmatter.
8. Create `departments/` only if there is at least one department. `company/briefs/.gitkeep` and `inbox/` come from the template.
9. Decision `decisions/0001-setup.md`, from the template, following `${CLAUDE_PLUGIN_ROOT}/schemas/decision-record.md`: record all answers in Context and Decision (level, name and id, languages, departments with models and connectors, gate changes, forbidden connectors, model tiers, policy pin and check result). `Card: none`, `Decided by: ceo`. Add its row to `decisions/README.md`.
10. `company/state.md`: empty schema-valid state from the template (`schema: state/1`, the five fixed H2 sections, `- none` in empty sections, `next_action: 1`, `next_decision: 1`). If the policy check reported loosenings the CEO chose to keep, seed one A item per kept loosening, in the exact "Waiting on the CEO" line format of `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`: `- <ORG_ID>-A<n> [high]: <exact action> (since YYYY-MM-DD)` with urgency `high`, `since` = today (`date +%F`), and the text an exact action, for example `In org.yaml move \`merge\` from notice back to ok, or approve a holding policy change; see decision 0001`. Number them from 1 and set `next_action` to the last number plus one (`2` for a single item). Never use `normal` or omit the `since` date. Also keep the rest of `state.md` consistent: Risks and Open decisions stay `- none` unless the CEO says otherwise (the A item is the only record, and decision 0001 holds the details).
11. If the CEO agreed, write `.claude/settings.json` enabling the plugin, for example:
    ```json
    { "enabledPlugins": { "ceo-of-agents@ceo-of-agents": true } }
    ```
    Check the marketplace name in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/marketplace.json` before writing it. Otherwise skip this file.

## Placeholder reference

Render with plain string replacement. Values are single-line unless stated. Never leave a `{{...}}` behind.

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
| `{{FRAMEWORK_VERSION}}` | `0.1.0` |
| `{{DATE}}` | Today, `YYYY-MM-DD` (`date +%F`) |
| `{{MODEL_COS}}` | Tier chosen for the CoS (question 8) |
| `{{MODEL_DEPARTMENTS}}` | Tier chosen as the default for departments |
| `{{MODEL_WORKERS}}` | The concrete model one tier below `{{MODEL_COS}}` in `models.tiers` (the same tier if `{{MODEL_COS}}` is the last). Used only in prose (`CLAUDE.md`, `decisions/0001-setup.md`). `org.yaml` keeps the literal rule `workers: one-down`, never a model name |
| `{{DEPARTMENTS_TABLE}}` | Markdown table `Agent id \| Name \| Role \| Use for`, one row per department: `Agent id` = the department id (`name` in its agent file), `Name` = display name (persona or role name), `Role` = the catalog role name (for example Business; the one in the agent file's intro line) or, for a custom department, the custom department's role name as given when it was defined, `Use for` = a short routing phrase of at most 12 words derived from the charter's `Purpose` line (never the full sentence). Used inside the `departments` condition only (for none, the `no-departments` block applies) |
| `{{GATES_TABLE}}` | Markdown table `Tier \| Rule \| Action ids`, exactly three rows (free, notice, ok) in that order. `Rule` is the short rule from `${CLAUDE_PLUGIN_ROOT}/gates/default.md` (free: do it and mention it; notice: one line before acting; ok: the CEO's explicit OK). `Action ids` are the final action ids of that tier, in backticks, comma-separated |
| `{{DEPARTMENTS_YAML}}` | `[]` for no departments. Otherwise the value starts with a newline and is a block list indented two spaces under `departments:`; each item has `id`, `from_catalog` (catalog id or `custom`), `display_name`, `model`, `connectors` (inline list such as `[mcp__github__*]`, or `[]`) |
| `{{GATES_FREE}}` `{{GATES_NOTICE}}` `{{GATES_OK}}` | Final action ids of that tier as an inline YAML list: `[a, b, c]` (`[]` if the tier is empty). Each action id is in exactly one tier |
| `{{FORBIDDEN_CONNECTORS}}` | Inline YAML list of forbidden connector patterns, `[mcp__x__*, mcp__y__*]`, or `[]` |
| `{{POLICY_YAML}}` | Company only. `null` when there is no holding policy. Otherwise the value starts with a newline and is a mapping indented two spaces under `policy:` with keys `source`, `local`, `path`, `pin` |
| `{{CEILING_DEPARTMENTS}}` | Holding only (`policies/policy.yaml`). Most capable model a company department may use. Derived default: the holding's own department model (`{{MODEL_DEPARTMENTS}}`). Show it in the summary and let the CEO change it; it must be a name from `models.tiers` |
| `{{CEILING_WORKERS}}` | Holding only. Most capable model a company worker may use. Derived default: the tier one below `{{CEILING_DEPARTMENTS}}` (the same if it is the last). A name from `models.tiers`, never `one-down` |
| `{{SETUP_DEPARTMENTS}}` | Cell text for `decisions/0001-setup.md`: `id (model)` for each department, comma-separated, or `none` |
| `{{SETUP_PERSONAS}}` | `id: display name` for each department whose display name differs from the role name, plus `CEO: <name>` if given; `none` if there is nothing |
| `{{SETUP_GATES}}` | `framework default` or `framework default with changes: <action> <from> -> <to>; ...` |
| `{{SETUP_CONNECTORS}}` | `id: patterns` per department with connectors, `;`-separated, plus `forbidden: patterns` if any; `none` if there is nothing |
| `{{SETUP_POLICY}}` | `none` for a company without policy, `not applicable (holding)` for a holding, otherwise `<source> @ <short pin> (check: OK)` or `(check: N loosening(s) kept)` |

Table cell values (`SETUP_*`) must not contain `|` or newlines.

### Per department (`catalog/<id>/*` and `templates/department/*`)

| Placeholder | Value |
|---|---|
| `{{DEPT_ID}}` | Department id (kebab-case) |
| `{{DISPLAY_NAME}}` | Display name (question 5). The agent intro renders as "You are {{DISPLAY_NAME}}, the <Role> department of {{ORG_NAME}}." With the default (display name equal to the role name) it reads "You are Business, the Business department of Acme."; this repetition is accepted, keep it. In a custom department's agent file replace the literal `<Role>` with the custom department's role name |
| `{{ORG_NAME}}`, `{{ORG_ID}}` | As above |
| `{{MODEL}}` | The department's model tier |
| `{{WORKER_MODEL}}` | The tier one below `{{MODEL}}` in `models.tiers` (the same tier if it is already the last) |
| `{{CONNECTORS}}` | Empty string when the department has no connectors; otherwise `, mcp__x__*, mcp__y__*` (leading comma and space), appended to the `tools:` list in the agent file |

### Conditional markers

Markdown: `<!-- IF x -->` ... `<!-- END IF -->`. YAML: `# IF x` ... `# END IF`. Each marker sits on its own line; blocks are not nested. Keep the content when the condition is true, drop the whole block when it is false, and always delete the marker lines.

| Condition | True when |
|---|---|
| `holding` | level is holding |
| `company` | level is company |
| `policy` | level is company and a holding policy source was given |
| `departments` | at least one department was chosen |
| `no-departments` | no department was chosen |

### Holding-only files

`portfolio.yaml` and `policies/` (`README.md`, `policy.yaml`) are skipped entirely for a company: do not create them and do not render their placeholders (`{{CEILING_DEPARTMENTS}}`, `{{CEILING_WORKERS}}` exist only there). For a holding, create them; `portfolio.yaml` stays `orgs: []`.

## Post-generation checks

Run them and fix what fails; report the results:
- `grep -rnE '\{\{|<!-- (IF|END IF)|# (IF|END IF)' .` finds nothing (ignore `.git`).
- `org.yaml` parses. Try `python3 -c "import yaml,sys; yaml.safe_load(open('org.yaml'))"`; on ImportError try `ruby -ryaml -e 'YAML.load_file(ARGV[0])' org.yaml`; if neither is available, check it carefully by reading and say explicitly in the final report that YAML was checked by reading only.
- Every expected `.claude/agents/<id>.md` exists (one per department in `org.yaml`). If any is missing, stop and tell the CEO clearly, listing the missing files and the likely cause (`.claude/` write permission, see Generation); never report success with missing agent files.
- `company/state.md` matches `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`: frontmatter fields, exact H2 headings in order.
- Every `.claude/agents/*.md` has an explicit `tools:` list in its frontmatter, and its `name` equals its file name.
- The files in `departments/` match the departments in `org.yaml`, and the display names appear in `CLAUDE.md`.

## Git

If there is no `.git`, run `git init`. Show `git status`. Ask the CEO before the first commit. If approved, commit everything with the message `chore: initialize <org name> hq with ceo-of-agents 0.1.0` and the attribution lines required by the session. Never push. Tell the CEO how to add a remote and push on their own.

## End

Tell the CEO in chat language: what was generated (file count, departments), any open A items, and how to start: open Claude Code in this directory and say what is on their mind; the CoS (from `CLAUDE.md`) takes it from there. Mention `/ceo-of-agents:intake`, `/ceo-of-agents:record-decision`, `/ceo-of-agents:weekly-brief`, and for a holding `/ceo-of-agents:portfolio-brief`.
