# Department catalog

The catalog holds starting templates for departments. Each entry has two files:

- `charter.md`: scope, what the department never does, inputs, outputs, gates, handoff.
- `agent.md`: a Claude Code subagent template with an explicit `tools:` allowlist. Spawning is limited by type: legal, finance and tax have no `Agent` tool; engineering has `Agent(reader, worker)`; every other department has `Agent(reader)`. The type list is enforced in direct `claude --agent` sessions only. When the CoS dispatches a department as a subagent the list is ignored, so the department must still spawn only those types. The `reader` and `worker` agents come from `templates/workers/`.

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

## How to read it

- Entries are templates, not defaults. Nothing is preselected; the setup wizard asks and zero departments is a valid answer.
- Picking the same entry in two orgs creates two independent departments, each with its own charter, agent file and memory. Nothing is shared between them.
- The wizard fills the placeholders (`{{DEPT_ID}}`, `{{AGENT_NAME}}` (the department's agent name; its agent file is named after it), `{{DISPLAY_NAME}}`, `{{ORG_NAME}}`, `{{ORG_ID}}`, `{{MODEL}}`, `{{WORKER_MODEL}}`, `{{OTHER_ACCOUNTS_EXAMPLE}}` (the account example, set by the org's purpose)). Every department starts with no connectors; the CoS adds one to the `tools:` list only after a decision card grants it.
- Once generated, the files belong to the org and can be edited freely. Gates in a generated hq live in `org.yaml`; advisory departments never file, sign or pay.
- Each agent file may name generic categories of optional external plugins. Nothing is vendored or installed by the framework; the CEO decides whether to add any.
- For a department not in the catalog, use `templates/department/`.

## Suggestions by purpose

Suggestions only. The wizard shows the line for the chosen purpose next to the list above; nothing is preselected and the CEO still picks each department or none. This table is the single source the wizard reads.

| Purpose and level | Suggested departments |
|---|---|
| `job` (company level) | `operations` (recurring obligations and work tools); `engineering` (only if the job is technical); custom departments that mirror the CEO's own work streams. Not suggested: `business`, `growth-social`, `legal`, `finance`, `tax` (they speak for the employer or cover the employer's own functions). |
| `product` (company level) | `engineering`, `design-brand`, `growth-social`, `business` |
| `startup` (company level) | `engineering`, `business`, `design-brand`, `growth-social`, `legal`, `finance` |
| `company` (company level) | `engineering`, `business`, `legal`, `finance`, `tax`, `operations` |
| `company` (holding level) | None. Departments are optional for a holding; do not suggest any. |
