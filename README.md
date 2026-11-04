# ceo-of-agents

<!-- TOP SLOT: banner, tagline, badges and diagram go here (owned by design-brand). Body starts below. -->

A Claude Code plugin that gives you a chief of staff (CoS) and a small set of departments (engineering, design, legal, finance and so on), all living in one git repo called the **hq**. You are the CEO. The CoS frames your requests, routes work to departments, records every decision and keeps one list of what waits on you. Departments do the specialist work under explicit tool allowlists and approval gates.

Everything is plain markdown and YAML in git, so every decision, number and risk has one written home.

Status: v0.3.0, early. See the [design spec](docs/design.md) for the roadmap.

## 1. What we assume you have

- **Claude Code**, installed and signed in: the CLI, the desktop app's Code tab, or the VS Code extension.
- **git**.
- **A GitHub account**, to host the hq as a private repo (you can also start with no remote and add one later).
- **`gh` (GitHub CLI)**, optional: needed only if a department works on GitHub from the terminal (for example engineering opening pull requests).
- **An empty folder** for the hq.

Not needed: coding skills, a server, a database, an extra API key, hosting, or any scheduled job. Nothing runs unless you open a session.

## 2. Install

In a Claude Code session:

```
/plugin marketplace add iamgiolaga/ceo-of-agents
/plugin install ceo-of-agents@ceo-of-agents
```

Or from your shell:

```
claude plugin marketplace add iamgiolaga/ceo-of-agents
claude plugin install ceo-of-agents@ceo-of-agents
```

## 3. First run

1. Open the empty folder in Claude Code (terminal: `cd` into it and run `claude`; desktop app: open the folder in the Code tab).
2. Run the setup command. It is the only command you ever type:

   ```
   /ceo-of-agents:init-fleet
   ```

3. Answer the wizard. It asks, in order:
   1. **Purpose**: job, product, startup or company (company also asks: company or holding).
   2. **Name** of the org and a short id used in codes (for example `ACME`).
   3. **Languages**: one for chatting with you, one for files.
   4. **Departments**: pick from the catalog, define your own, or none. Nothing is preselected.
   5. **Names**: your CoS's name and, optionally, a persona name per department.
   6. **Approval gates**: keep the default table or change it.
   7. **Connectors**: which tools each department may use, and which no agent may ever use.
   8. **Models**: for the CoS, departments and workers.
   9. **Policy**: a holding's policy to follow (company), or a pointer to your employer's rules (job). A holding skips it.
   10. **Repo**: an optional git remote for the hq.
4. Check the summary and confirm. The wizard generates the hq:
   - `CLAUDE.md` (your CoS), `org.yaml` (setup, gates, models), `operating-model.md`;
   - `company/state.md` (state and the list of what waits on you), `company/decision-queue.md`;
   - `decisions/` with the first record (your setup answers), `inbox/`, `metrics/`;
   - one charter in `departments/<id>/` and one agent in `.claude/agents/<id>.md` per department, plus generic `reader` and `worker` agents.
5. Approve the permission prompt when the wizard writes into `.claude/agents/`, then approve the first commit. The wizard never pushes: push when you are ready.

## 4. Daily use

### Open a session

Open Claude Code in the hq folder. The CoS pulls the latest hq, processes department handoffs, and gives you a 3-5 line status with the codes of what waits on you.

### Talk in plain language

| You say | What happens |
|---|---|
| "I have an idea: a referral program for early users." | The CoS frames it, checks for duplicates, and routes it: a decision card, a task for a department, or a note. |
| "Decide whether we keep the free tier." | A decision card with its own code (for example `ACME-D3`): context, options, a recommendation. It goes on the pending list. |
| "Approve ACME-A2." or "ACME-D3: b." | The CoS runs exactly what you approved, or records your decision as a permanent record, and clears the item. |
| "Brief." | A dated brief in `company/briefs/`: what changed, numbers with sources, risks, what waits on you. |
| "Pass to engineering: why did the last release fail?" | The CoS forwards your text verbatim and returns the department's answer verbatim, then its own comment. |
| "Resume." | The CoS picks up from the state, the latest brief and the inbox, and proposes the next step. |

You never type the CoS's procedures: they ship with the plugin, hidden from the `/` menu, and the CoS uses them on its own.

### Approvals and gates

Every action has a tier, set in `org.yaml`:

| Tier | Rule | Examples (default table) |
|---|---|---|
| free | Done and mentioned | Drafts, research, opening a pull request |
| notice | One line before acting | Committing to the hq, pushing a branch |
| ok | Your explicit OK | Merge, deploy, publish, spend money, contact people |

Asks that need your OK are batched on the pending list with a code, so you can clear several in one pass.

### Direct session with one department

For long work inside one department, skip the CoS and open that department directly, from the hq folder:

```
claude --agent <department-id>
```

The department leaves a handoff in `inbox/`; the CoS processes it at your next CoS session. Decisions taken there become official only when the CoS records them.

### Several computers

The hq is a git repo. Clone it on each computer and install the plugin there too. The CoS pulls at the start of every session and pushes after its commits, so the remote stays the reference.

## 5. The four purposes

| Purpose | What changes |
|---|---|
| **job** | Your own work at an employer. The employer's accounts used for the job count as this org's; your personal accounts stay out. An optional pointer to the employer's rules on data and AI. Never joins a holding. |
| **product** | One product. Suggested departments: engineering, design and brand, growth and social, business. Employer accounts stay out; can join a holding. |
| **startup** | A venture building a business. Suggested departments add legal and finance. Same account rules as product; can join a holding. |
| **company** | A company, or a **holding** that reads its companies' state read-only and gives you one list of what waits on you across all of them. A holding keeps shared policies (gates, model limits) in a separate repo that companies pin. |

Suggestions are only suggestions: you pick each department, or none.

## 6. Where it runs

| Surface | Support |
|---|---|
| Claude Code on your own machine: the CLI, the desktop app's Code tab, VS Code, JetBrains (through its terminal) | Full |
| Claude Code on the web (claude.ai/code) | Partial. Marketplace plugins are not loaded there, so the setup and the CoS procedures are unavailable. The hq's `CLAUDE.md` and `.claude/agents/` still load. |
| Claude chat apps and Cowork | Not suited: no repo and no `CLAUDE.md` |

If you are not used to the terminal, use the **Code tab of the Claude desktop app**.

Sources, checked 2026-11-04: [Discover plugins](https://code.claude.com/docs/en/discover-plugins.md), [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md), [Plugin platform support](https://claude.com/docs/plugins/platform-support.md).

## 7. Update

Update the plugin from `/plugin` (Installed tab, **Update now**) or with `claude plugin update ceo-of-agents@ceo-of-agents`. Auto-update is off by default for third-party marketplaces like this one; you can turn it on in `/plugin`, Marketplaces tab.

Updating the plugin never touches your hq. When a release changes hq files, it ships a migration in [`migrations/`](migrations/README.md): ask your CoS to apply it, review the diff, approve the commit. Version 0.3.0 renamed the setup command from `init-org` to `init-fleet`; existing hqs follow [`migrations/0.2.0-to-0.3.0.md`](migrations/0.2.0-to-0.3.0.md).

## Plugin layout

```
.claude-plugin/   plugin.json, marketplace.json
skills/           init-fleet (setup) and the CoS procedures: intake, record-decision, weekly-brief, portfolio-brief
templates/        hq, department, worker and policies-repo templates
catalog/          starting department catalog (charter + agent each)
schemas/          state, org, portfolio, policy, handoff, decision card/record
gates/            default approval-gate table
migrations/       how upgrades reach existing hqs
docs/             design spec
```

To try a local copy: `claude --plugin-dir <path-to-this-repo>`.

## License

MIT, see [LICENSE](LICENSE).
