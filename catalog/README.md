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
- The wizard fills the placeholders (`{{DEPT_ID}}`, `{{DISPLAY_NAME}}`, `{{ORG_NAME}}`, `{{ORG_ID}}`, `{{MODEL}}`, `{{WORKER_MODEL}}`) and replaces `{{CONNECTORS}}` with `, mcp__<name>__*` entries granted to that department only, or removes it.
- Once generated, the files belong to the org and can be edited freely. Gates in a generated hq live in `org.yaml`; advisory departments never file, sign or pay.
- Each agent file may name generic categories of optional external plugins. Nothing is vendored or installed by the framework; the CEO decides whether to add any.
- For a department not in the catalog, use `templates/department/`.
