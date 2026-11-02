# ceo-of-agents

A Claude Code framework that gives a solo founder (the CEO) an AI organization. A chief-of-staff agent frames, routes, records and challenges. Department agents, picked at setup, do the specialist work under explicit tool allowlists. Everything lives in plain files in a git repo (an "hq"), so every decision, number and risk has one written home.

Organizations come in two levels: a holding (the CEO as entrepreneur) and one company per product. The holding reads company hqs read-only and composes a single list of what waits on the CEO.

## Status

v0.1.1, early. Design and schemas are in place; see the roadmap in the design spec.

## Install

```
claude plugin marketplace add <owner>/<repo>
claude plugin install ceo-of-agents@ceo-of-agents
```

To test locally: `claude --plugin-dir <path-to-this-repo>`.

## Quick start

Create an empty directory, start Claude Code in it and run `/ceo-of-agents:init-org`. The wizard asks for level, name, languages, departments, gates, connectors and models, then generates the hq. A holding also creates a separate policies repo that its companies pin.

Run `init-org` interactively. If you run it headless, the plugin directory and (for a holding) the policies repo path are outside the current directory, so pass them with `--add-dir`. Writing `.claude/agents/*` may also need interactive approval.

## Plugin layout

```
.claude-plugin/   plugin.json, marketplace.json
templates/        instance, department, worker and policies-repo templates
catalog/          starting department catalog (charter + agent each)
skills/           init-org, intake, record-decision, weekly-brief, portfolio-brief
schemas/          state, org, portfolio, policy, handoff, decision card/record
gates/            default approval-gate table
migrations/       how upgrades ship
docs/             design spec
```

## The problem

- A founder who runs several organizations carries their context in their head or scattered across chats.
- Each org's context is siloed, so the CEO checks many queues and re-explains the same things.
- Agents without structure act too freely, forget decisions and invent numbers.

## Read the design

See [docs/design.md](docs/design.md).

## License

MIT, see [LICENSE](LICENSE).
