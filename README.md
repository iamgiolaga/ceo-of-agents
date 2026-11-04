# ceo-of-agents

<p align="center">
  <img src="assets/banner.svg" width="100%" alt="ceo-of-agents, a plugin for Claude Code. You're the CEO. Your agents are the company.">
</p>

<p align="center">
  <strong>A Claude Code plugin: a chief of staff and departments that work from one git repo, behind approval gates.</strong>
</p>

<p align="center">
  <a href="#3-install"><img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-2DD4BF?style=flat-square&labelColor=0F172A"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/iamgiolaga/ceo-of-agents?style=flat-square&labelColor=0F172A&color=94A3B8"></a>
  <img alt="Version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fiamgiolaga%2Fceo-of-agents%2Fmain%2F.claude-plugin%2Fplugin.json&query=%24.version&label=version&style=flat-square&labelColor=0F172A&color=A78BFA">
  <img alt="Status: early" src="https://img.shields.io/badge/status-early-94A3B8?style=flat-square&labelColor=0F172A">
</p>

## What it is

- **You talk to one agent, your chief of staff (CoS).** It frames each request, routes it to a department agent (engineering, design, legal, finance and more) and pushes back when it should.
- **Everything is written down in a git repo you own, the hq:** the current state, what waits on you, and immutable decision records. It is plain markdown and YAML, so every decision, number and risk has one written home.
- **Nothing important happens without you.** Approval gates hold merges, publishing, spending and the like until you OK them by code.

Use it for your job, a product, a startup or a company. Status: early; see the [design spec](docs/design.md) for the roadmap.

<p align="center">
  <img src="assets/diagram.svg" width="100%" alt="How it works: you ask your chief of staff in plain language and get back a status and codes to approve. The chief of staff routes work to departments (engineering, design and brand, legal and finance, the last two advisory). Everything is written to the hq repo: state, decision records and approval gates (free, notice, ok).">
</p>

## Get started in 30 seconds

<p align="center">
  <img src="assets/quickstart.svg" width="100%" alt="Four steps: 1. You need Claude Code, git and a GitHub account. 2. Install the plugin with two commands inside Claude Code. 3. In an empty folder run /ceo-of-agents:init-fleet and say what the fleet is for. 4. Talk to your chief of staff in plain language and approve by code.">
</p>

**You need:** Claude Code (signed in), git, a GitHub account ([details](#2-what-we-assume-you-have)).

**1. Install** (inside Claude Code):

```
/plugin marketplace add iamgiolaga/ceo-of-agents
/plugin install ceo-of-agents@ceo-of-agents
```

**2. Start** (open Claude Code in an empty folder):

```
/ceo-of-agents:init-fleet
```

**3. Talk.** That is the only command you type. From then on, talk to your chief of staff in plain language.

Full steps: [Install](#3-install) · [First run](#4-first-run) · [Daily use](#5-daily-use)

## 1. The four purposes

| Purpose | What changes |
|---|---|
| **job** | Your own work at an employer. The employer's accounts used for the job count as this org's; your personal accounts stay out. An optional pointer to the employer's rules on data and AI. Never joins a holding. |
| **product** | One product. Suggested departments: engineering, design and brand, growth and social, business. Employer accounts stay out; can join a holding. |
| **startup** | A venture building a business. Suggested departments add legal and finance. Same account rules as product; can join a holding. |
| **company** | A company, or a **holding** that reads its companies' state read-only and gives you one list of what waits on you across all of them. A holding keeps shared policies (gates, model limits) in a separate repo that companies pin. |

Suggestions are only suggestions: you pick each department, or none.

## 2. What we assume you have

- **Claude Code** on your own machine, installed and signed in: the terminal, the desktop app, or an IDE extension such as VS Code or JetBrains.
- **git**.
- **A GitHub account**, to host the hq as a private repo (you can also start with no remote and add one later).
- **`gh` (GitHub CLI)**, optional: needed only if a department works on GitHub from the terminal (for example engineering opening pull requests).
- **An empty folder** for the hq.

Not needed: coding skills, a server, a database, an extra API key, hosting, or any scheduled job. Nothing runs unless you open a session.

## 3. Install

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

## 4. First run

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

## 5. Daily use

<p align="center">
  <img src="assets/exchange.svg" width="100%" alt="A typical exchange. You say: I have an idea, a referral program for early users. The chief of staff frames it, checks for duplicates, picks the route and runs it. You say: Decide whether we keep the free tier. It writes a decision card and adds ACME-D3 to your list. You say: ACME-D3, option b. It records the decision, clears the card and updates the state. You say: Pass to engineering, why did the last release fail? It forwards it, returns engineering's answer and adds its view.">
</p>

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

## 6. Update

Update the plugin from `/plugin` (Installed tab, **Update now**) or with `claude plugin update ceo-of-agents@ceo-of-agents`. Auto-update is off by default for third-party marketplaces like this one; you can turn it on in `/plugin`, Marketplaces tab.

Updating the plugin never touches your hq. When a release changes hq files, it ships a migration in [`migrations/`](migrations/README.md): ask your CoS to apply it, review the diff, approve the commit. Version 0.3.0 renamed the setup command from `init-org` to `init-fleet`; existing hqs follow [`migrations/0.2.0-to-0.3.0.md`](migrations/0.2.0-to-0.3.0.md).
