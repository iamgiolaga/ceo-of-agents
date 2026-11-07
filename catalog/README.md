# Department catalog

The catalog holds starting templates for departments. Each entry has two files:

- `charter.md`: scope, what the department never does, inputs, outputs, gates, handoff.
- `agent.md`: a Claude Code subagent template with an explicit `tools:` allowlist. Spawning is limited by type: the advisory entries (legal, finance, tax, health, money, paperwork) have no `Agent` tool and no `Bash`; engineering has `Agent(reader, worker)`; every other department has `Agent(reader)`. The type list is enforced in direct `claude --agent` sessions only. When the CoS dispatches a department as a subagent the list is ignored, so the department must still spawn only those types. The `reader` and `worker` agents come from `templates/workers/`.

| Id | Department | Advisory |
|---|---|---|
| `engineering` | Engineering | no |
| `design-brand` | Design and brand | no |
| `business` | Business | no |
| `growth-social` | Growth and social | no |
| `legal` | Legal | yes |
| `finance` | Finance and accounting | yes |
| `tax` | Tax | yes |
| `operations` | Operations | no |
| `health` | Health (personal only) | yes |
| `money` | Money (personal only) | yes |
| `paperwork` | Paperwork (personal only) | yes |

## How to read it

- Entries are templates, not defaults. Nothing is preselected; the setup wizard asks and zero departments is a valid answer.
- Picking the same entry in two orgs creates two independent departments, each with its own charter, agent file and memory. Nothing is shared between them.
- The wizard fills the placeholders (`{{DEPT_ID}}`, `{{AGENT_NAME}}` (the department's agent name; its agent file is named after it), `{{DISPLAY_NAME}}`, `{{ORG_NAME}}`, `{{ORG_ID}}`, `{{MODEL}}`, `{{WORKER_MODEL}}`, `{{WORKER_TIER}}` (how its workers relate to the department's tier: one tier down, or the same tier for a department set to top model, workers included), `{{OTHER_ACCOUNTS_EXAMPLE}}` (the account example, set by the org's purpose)). Every department starts with no connectors; the CoS adds one to the `tools:` list only after a decision card grants it.
- Once generated, the files belong to the org and can be edited freely. Gates in a generated hq live in `org.yaml`; advisory departments never file, sign or pay.
- Each agent file may name generic categories of optional external plugins. Nothing is vendored or installed by the framework; the CEO decides whether to add any.
- For a department not in the catalog, use `templates/department/`.
- `health`, `money` and `paperwork` are offered only in a personal hq (`org.purpose: personal`). They keep personal detail in the hq's git-ignored `private/` folder and put only pointers in tracked files and handoffs.

## Suggestions by purpose

Suggestions only. The wizard shows the line for the chosen purpose next to the list above; nothing is preselected and the CEO still picks each department or none. This table is the single source the wizard reads.

Org chart reason: wherever `design-brand` is suggested, the wizard shows this reason with it: its first task can be to draw the org chart of this org (you, your chief of staff, each department and how work flows between them), a picture that helps you understand and explain the org you just set up. For `job` it adds that the chart is for you, not something that speaks for your employer. When `design-brand` is picked, the chief of staff proposes the org chart as its first task at the first session, and runs it only if you say yes.

| Purpose and level | Suggested departments |
|---|---|
| `job` (company level) | `operations` (recurring obligations and work tools); `design-brand` (org chart reason; the chart is for the CEO, not a deliverable that speaks for the employer); `engineering` (only if the job is technical); custom departments that mirror the CEO's own work streams. Not suggested: `business`, `growth-social`, `legal`, `finance`, `tax` (they speak for the employer or cover the employer's own functions). |
| `product` (company level) | `engineering`, `design-brand` (also for the org chart reason), `growth-social`, `business` |
| `startup` (company level) | `engineering`, `business`, `design-brand` (also for the org chart reason), `growth-social`, `legal`, `finance` |
| `company` (company level) | `engineering`, `business`, `legal`, `finance`, `tax`, `operations`, `design-brand` (org chart reason) |
| `company` (holding level) | None. Departments are optional for a holding; do not suggest any. |
| `personal` (company level) | `health`, `money`, `paperwork` (advisory: they prepare and remember, the professional decides); custom departments for other areas of the CEO's life. Not suggested: `legal`, `finance`, `tax` (they cover a company's functions; `money` and `paperwork` cover the personal side), `engineering`, `design-brand`, `business`, `growth-social`, `operations` (they work for an organization). |
