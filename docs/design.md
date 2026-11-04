# ceo-of-agents: design spec (draft v0)

Status: v0.5.0 implemented. v0.1.1 implemented phase 0 plus review fixes. Sections updated where implementation diverged. v0.1.1 applied these fixes: restricted spawning with `reader` and `worker` agents, read-only connectors for advisory departments, a separate policies repo, a portfolio brief that never pulls, no preselected choices in the wizard, an optional hq remote, and fully filled custom departments. v0.2.0 adds schema `org/2`: the chief of staff's name (`cos.display_name`) and the fleet purpose (`org.purpose`: job, product, startup, company), which drives suggested departments, account rules and holding eligibility. v0.3.0 renames the setup wizard to `init-fleet`, the only command the CEO types; the four CoS procedures (`intake`, `record-decision`, `weekly-brief`, `portfolio-brief`) are hidden from the `/` menu (`user-invocable: false`) and invoked by the CoS from plain-language requests. Custom departments get the same purpose-aware account-separation line as catalog departments. v0.4.0 adds three working rules: a department review in `init-fleet` with a one-line reason for every elevated grant (also when a department is added later), task-splitting rules for the CoS, and blocked and failure hygiene for workers and departments. v0.5.0 makes the wizard ask what the org is about (generating `company/vision.md` and `company/strategy.md`), rewrites the gates question in plain language, drops the connectors question (every department starts with none; the CoS checks connectors of other accounts at the first session and writes them to an untracked `accounts.local.yaml`), and makes every CoS procedure check for a remote before pulling.

## 1. Problem

One person, many organizations. A solo founder may run a product company, a second venture, and their own affairs as an entrepreneur (accounting, tax, personal legal, portfolio, personal brand). Context for each lives in separate places, shared context has no structure, and the CEO checks many queues to learn what needs them.

AI agents help, but unstructured they have predictable failures: decisions are made in chat and forgotten, numbers are invented, outward-facing actions happen without approval, and work and personal accounts get mixed. The framework gives each organization a written, auditable structure and gives the CEO one place to look.

The pattern was proven in one running instance (the reference instance, the author's first product org). This spec generalizes it.

## 2. Goals and non-goals

**Goals**
- One entry point per org: a chief of staff (CoS) the CEO talks to.
- Departments as vertical specialists with charters and explicit tool allowlists.
- A git repo per org as the single source of truth.
- One aggregated list of what waits on the CEO, across all orgs.
- Cheap by design: the top-tier model plans, cheaper models execute.
- Safe by default: a configurable approval-gate table.

**Non-goals**
- No hosted service. Everything runs locally in Claude Code against files the CEO owns.
- No scheduled automation by default. Rhythms (weekly brief, reviews) run on demand.
- Agents never take outward-facing or irreversible actions without passing the gate.
- Finance, tax and legal departments are advisory. They never file, sign or submit anything and are not a substitute for professionals.
- Not a project-management tool. Issue trackers stay where they are; hq links to them.

## 3. Core concepts

| Term | Meaning |
|---|---|
| Framework | The versioned, reusable part: templates, catalog, skills, schemas, wizard |
| Instance | One org's hq repo, generated from the framework and owned by the CEO |
| Level | `holding` (the CEO as entrepreneur) or `company` (one per product, with its own code org and hq repo) |
| Purpose | What the fleet is for: job (the CEO's own work at an employer), product, startup or company. Set by the first wizard question; drives suggested departments, account rules and holding eligibility (see 6) |
| Chief of staff (CoS) | The CEO's single point of contact per org. Frames, routes, records, challenges. Owns hq. Does no deep execution |
| Department | A vertical specialist agent with a charter, a tool allowlist and a model tier |
| Charter | A short file stating a department's scope, what it never does, its inputs and outputs, and its gates |
| Handoff | A note a department leaves in `inbox/` for the CoS at the end of its work |
| Decision card | A pending question: context, options, recommendation, and who proposes it (or "needs analysis by <department>") |
| Decision record | A numbered, immutable file in `decisions/` recording an answered card |
| Approval gate | A rule saying which actions are free, need notice, or need the CEO's explicit OK |
| CEO pending list | The one list of what waits on the CEO: actions (`A`) and decisions (`D`), with codes. Lives in `company/state.md` under "Waiting on the CEO" |

## 4. Framework vs instance

The framework is a versioned Claude Code plugin. An instance is an hq repo per org. Framework upgrades never overwrite instance files. An upgrade ships as a migration: an explicit, reviewable diff the CEO (via the CoS) applies as a normal commit. Instance files record the framework version they were generated from.

**Plugin layout**

```
ceo-of-agents/
  .claude-plugin/    plugin.json, marketplace.json
  templates/
    instance/        CoS CLAUDE.md template and all hq files, with placeholders
    department/      custom department: charter + agent
    workers/         reader and worker agent templates, one pair per instance
    policies-repo/   policy.yaml and README.md for the holding's separate policies repo
  catalog/           department catalog (charter + agent template each)
  skills/            init-fleet, intake, record-decision, weekly-brief, portfolio-brief
  schemas/           state.md, org.yaml, portfolio.yaml, policy.yaml, handoff, decision card, decision record
  gates/             default approval-gate table
  migrations/        vN-to-vN+1 diffs
```

There is no `agents/` dir: Claude Code auto-registers every `.md` under a plugin's `agents/` as a live subagent, so templates with placeholders cannot live there.

**Instance (hq) layout**

```
<org>-hq/
  CLAUDE.md                     CoS instructions (generated)
  org.yaml                      level, purpose, id, CoS name, language, models, gates, policy pin (company) or policies_repo (holding)
  operating-model.md            how the CEO works with this org
  company/
    state.md                    living snapshot, fixed schema (see 5)
    decision-queue.md           open decision cards
    briefs/                     dated briefs
  decisions/README.md           index of decision records
  decisions/NNNN-<slug>.md      numbered decision records
  inbox/                        handoffs, deleted once processed
  departments/<dept>/charter.md
  metrics/README.md             metric definitions, sources, dates
  .claude/agents/<dept>.md      department agents with tool allowlists
  .claude/agents/reader.md      read-only worker (bulk reading, research)
  .claude/agents/worker.md      hands-on worker (for departments with Bash)
  portfolio.yaml                holding only
```

A holding instance is an org like any other whose specific job is to be a registry: `portfolio.yaml` lists references to company hqs, which may live in separate code orgs. It does not keep its policies in the hq: they live in a separate small policies repo (see 5), whose path is recorded in `org.yaml` as `policies_repo`. Its departments are chosen at setup like in any org, and may be none.

## 5. Cross-org context

This is the core value. The mechanism is deliberately simple: files, git, read-only reads. Nothing is copied, synced or automated.

### Upward: company to holding

Each instance exposes `company/state.md` as its standard interface, with a fixed schema.

```yaml
---
schema: state/1
org_id: ACME
level: company
last_updated: 2026-01-15
framework_version: 0.5.0
next_action: 1
next_decision: 1
---
```

Fixed sections, in order: Products and status; Key numbers (each with source and date); Risks; Open decisions; Waiting on the CEO. Line formats live in `schemas/state.md`.

Codes are written namespaced in every file (`ACME-D12`, `ACME-A3`), are monotonic per org and never reused; `next_action` and `next_decision` hold the next numbers. Every decision card carries its own D code.

The holding keeps `portfolio.yaml`:

```yaml
schema: portfolio/1
stale_after_days: 14
orgs:
  - id: ACME
    name: Acme
    path: ~/work/acme-hq        # local clone
    remote: <git remote>        # the hq remote
```

The holding CoS never pulls. For each registered hq it runs `git -C <path> fetch`, then `git -C <path> show origin/<default-branch>:company/state.md`, so the clone's working tree is never touched. The Organizations line records when a clone is dirty, on another branch or not fetched (the last fetched copy is then read, and marked). It never writes to a company hq. Staleness is visible from `last_updated` against `stale_after_days`. Reads use the CEO's own git credentials (the CEO is a member of every org); the holding stores no credentials and nothing is shared between orgs.

A job hq (`org.purpose: job`) is never registered; the portfolio brief skips one if listed, reading only `org.purpose` from its `org.yaml`.

### Downward: holding to company

Policy layering: framework defaults < holding policies < company overrides. A company may tighten a holding policy, never loosen it. A job hq never pins a policy.

| Policy area | "Tighten" means | Example |
|---|---|---|
| Approval gates | Move an action to a stricter tier | "Merge" from notice to explicit OK |
| Account separation | Add a restriction | Forbid a connector the holding allows |
| Language | Add a requirement | Files must be in a stated language |
| Models | Lower a ceiling | Cap workers to the cheapest tier |

The holding keeps its policy in a separate small policies repo, not in its hq. The repo has only `policy.yaml` (schema `policy/1`: minimum gate tiers, forbidden connectors, required file language, model ceilings for the CoS, departments and workers) and `README.md` at its root, and no sensitive data, because it is shared with every company's CEO clone. The holding `org.yaml` records it as `policies_repo` (`local` path, `remote` or `""`). Changing a policy is a commit in that repo approved by the CEO (`change-policy-rules`, tier ok). A company hq pins a commit of it in `org.yaml`:

```yaml
policy:
  repo: <policies repo remote>
  local: <path>                 # CEO's local clone of the policies repo, read-only
  pin: <commit sha>
```

At session start the company CoS runs an optional `git -C <local> fetch` (it may fail offline), then `git -C <local> show <pin>:policy.yaml`, and compares four areas: gates (company tier at least as strict as the holding minimum), connectors (no holding-forbidden connector granted to any department), language (file language matches the required one), models (`models.cos` not above `models.ceiling.cos`, no company department above `models.ceiling.departments`, no worker above `models.ceiling.workers`). It reports `Policy check: OK` or one line per loosening, and adds an `A` item. It never fixes silently. If the policy is unreadable it says "skipped: <reason>". Moving the pin is an explicit commit the CEO approves. The company never needs a clone of the holding hq.

### Aggregated CEO pending list

Codes are namespaced per org: `ACME-D12` (decision), `ACME-A3` (action). The holding CoS composes one list across all orgs in its brief, ordered by urgency and level. Items are resolved in the owning org: the CEO answers there, and the owning CoS records it. The holding list is a view, never a second source.

### Escalation

When a company decision touches money, personal liability or the portfolio, the company CoS marks the card `escalate: holding`. The holding sees it on its next read of `state.md`, adds context (tax, personal legal, cash across orgs) and puts its advice in the holding brief next to the namespaced code. The CEO carries it into the owning org when answering the card. The holding never writes to a company hq, so the decision is still recorded only where it belongs.

## 6. Setup wizard

`/ceo-of-agents:init-fleet` runs in an empty directory and asks:

1. Purpose and level: what the fleet is for (job, product, startup, company); level (holding or company) is asked only for company, and job, product and startup are company-level hqs.
2. Org name and short id (used in codes).
3. What the org is about: what it does and for whom, why it exists, and its stage (for a job: role and team, what good work looks like; for a holding: personal goals and portfolio direction). The answers become `company/vision.md` and `company/strategy.md`, which the CoS reads at session start.
4. Language for chat with the CEO, and language for files.
5. Departments: nothing is preselected, with relevance notes from question 3. Pick from the catalog, define custom ones, or none. For every custom department the wizard asks scope, triggers, exclusions and the single core job, so no placeholder is left in its files.
6. Names or personas per agent, including the chief of staff's name (the role name or a persona, the CEO's choice; the CoS name is required).
7. Approval gates, in plain words with one example per action (ids stay in `org.yaml`): accept, make something stricter, or make something looser after a warning.
8. Model tiers for the CoS, departments and workers.
9. For a company with purpose not job: the holding's policies repo (remote), the local clone and the pin (optional). If a policy is given, the tighten-only check runs before anything is generated. For a job hq: an optional pointer to the employer's rules on data, AI tools and accounts. A holding skips this question.

The wizard asks nothing about connectors. Every department starts with none (least privilege) and gets one later only through a decision card with a one-line reason; advisory departments (legal, finance, tax) get read-only connector tools only, named one by one (no server wildcard). At the first session, and on every new machine or fresh clone, the CoS lists the connectors visible in the session, asks the CEO which belong to another account, and writes them to the untracked `accounts.local.yaml` and to deny rules in `.claude/settings.local.json`. `accounts.forbidden_connectors` in `org.yaml` starts empty; connectors that mean the same account on every machine are added there later through a decision.

The wizard also offers an optional remote for the hq, added with `git remote add` and never pushed. Without a remote, the CoS skips pull and push and says once "No remote: pull and push skipped". A holding additionally creates its policies repo at a path the CEO gives (outside the hq; the only write outside the current directory): `git init`, renders `policy.yaml` and `README.md` from `templates/policies-repo/`, asks before its first commit, and offers an optional remote the same way. For a job hq the wizard also asks where the remote lives (a personal or an employer account) without imposing one, and reminds the CEO of the employer's rules.

It generates `CLAUDE.md`, `org.yaml`, `operating-model.md`, the `company/` files with empty schema-valid state, one charter and one agent file per department (file names use the department id), `decisions/README.md`, `inbox/README.md`, `metrics/README.md` and an initial decision record (`0001`) capturing the setup answers. It also generates `.claude/agents/reader.md` and `.claude/agents/worker.md`. A holding also gets `portfolio.yaml` and the separate policies repo. Optionally it writes `.claude/settings.json` enabling the plugin, only with the CEO's OK. It never pushes and asks before the first commit.

**Fleet purpose**

| Purpose | Level | Account rule | Holding |
|---|---|---|---|
| job | company (not asked) | The employer's accounts and connectors used for this job are this org's accounts; the CEO's personal accounts and other orgs' accounts are kept out | Never registered, never pins a policy; an optional `employer_rules` pointer instead |
| product | company (not asked) | Employer accounts kept out | May be registered, may pin a policy |
| startup | company (not asked) | Employer accounts kept out | May be registered, may pin a policy |
| company | asked: company or holding | Employer accounts kept out | Company: may be registered, may pin a policy. Holding: is the registry |

Suggested departments per purpose are in `catalog/README.md`, section "Suggestions by purpose". They are suggestions only; nothing is preselected.

**Starting department catalog**

Catalog entries are templates, not defaults: each org decides its own structure. Picking the same entry in two orgs creates two independent departments with separate charters and memory.

| Department | Purpose | Default tool allowlist idea | Default gate notes |
|---|---|---|---|
| Engineering | Code, CI, releases, security | Read, edit, shell, may spawn `reader` and `worker`; repo access for the org only | Open PRs free; merge, deploy, secret rotation need OK |
| Design and brand | Identity, assets, tone of voice, brand review | Read, edit, design-tool connector, may spawn `reader` | Brand-rule changes need OK; publishing needs OK |
| Business | Model, pricing, market, competitors, discovery | Read, edit, web search and fetch | Contacting people or spending needs OK |
| Growth and social | Editorial calendar, post drafts | Read, edit, web search | Drafts only; publishing needs OK |
| Legal | Privacy, terms, policies, accuracy of claims. Advisory | Read, edit, web search; read-only connectors; no Agent tool | Never signs or files; routes to a professional on request |
| Finance and accounting | Bookkeeping views, cash, invoices review. Advisory | Read, edit; read-only connectors; no payment tools; no Agent tool | No payments or transfers; spending needs OK |
| Tax | Tax position, deadlines, document checklists. Advisory | Read, edit, web search; read-only connectors; no filing tools; no Agent tool | Never files or signs; deadlines surface as `A` items |
| Operations | Admin, vendors, tooling, calendars of obligations | Read, edit, scoped connectors, may spawn `reader` | Subscriptions and vendor contact need OK |

## 7. Approval gates

Default table (`gates/default.md`), configurable per org: `org.yaml` holds `gates: {free, notice, ok}` lists of stable action ids.

| Tier | Action ids |
|---|---|
| free | `issues-and-labels`, `comments`, `drafts`, `open-pr`, `research`, `hq-write` |
| notice | `push-non-deploy-branch`, `hq-commit`, `dispatch-pushing-department` |
| ok | `merge`, `deploy`, `publish`, `contact-people`, `spend-money`, `rotate-secrets`, `delete-data`, `org-or-repo-settings`, `change-brand-rules`, `change-policy-rules`, `file-or-sign`, `make-payment` |

Tier order: free < notice < ok.

| Tier | Rule | Examples |
|---|---|---|
| Free | Do it, mention it | Issues and labels, comments, drafts, opening PRs, research, writing in hq (CoS) |
| With notice | One line before acting (what, where, content) | Pushes to a non-deploying branch, hq commits, dispatching a department that will push |
| Explicit CEO OK | Narrow, exact request, batched | Merge, deploy, publish, contacting people, spending money, rotating secrets, deleting data, org or repo settings, changing brand or policy rules |

Principles: do not ask for OKs the table does not require; batch the asks into the pending list; run the exact approved action, nothing broader. Advisory departments (legal, finance, tax) never do `file-or-sign` or `make-payment` at all; no config can lower them. Changing a holding policy is `change-policy-rules` (tier `ok`): a CEO-approved commit in the policies repo.

## 8. Models and cost

| Role | Tier | Notes |
|---|---|---|
| CoS | Top | Plans, decides, judges, talks to the CEO |
| Department | Chosen per org (from the tier list) | Vertical specialist; orchestrates its own workers |
| Workers | One tier down from their parent (the lowest tier stays itself) | Bulk reading, drafting, code, commands |

Every instance ships two worker agents in `.claude/agents/`, generated from `templates/workers/`. `reader` has Read, Grep, Glob, WebSearch and WebFetch only: read-only research and bulk reading, returning conclusions, not dumps. `worker` adds Edit, Write and Bash and is for departments that already have Bash. Neither has the Agent tool or any connector, and neither spawns agents or escalates. Both run on `{{MODEL_WORKERS}}`, one tier below `models.departments`.

Who may spawn what: engineering `Agent(reader, worker)`; other non-advisory departments `Agent(reader)`; advisory departments (legal, finance, tax) no Agent tool at all. When an advisory department needs bulk reading, the CoS dispatches a `reader` for it. Known limit: the `Agent(type)` allowlist is enforced only when the department runs as the main thread of `claude --agent`. When the CoS dispatches a department as a subagent, any type list is ignored, so the rule there is that departments spawn only `reader` or `worker`, and advisory departments carry no Agent tool so nothing can be spawned from them.

Rules: workers never escalate to a more capable model than their parent. Departments delegate to workers and do not hand work back up. The CoS does small things itself when writing the brief would cost more than the work. Every result is verified (diff read, check run) before it is built on or reported. Briefs to workers are self-contained: goal, files, constraints, definition of done, what to return.

## 9. Separation and privacy

- Each department has an explicit `tools:` allowlist; connectors are granted per department, not globally.
- Never mix accounts: credentials and connectors for org A are not used for org B. Use only this org's accounts: in a job hq (`org.purpose: job`) the employer's accounts used for that job are this org's accounts and the CEO's personal accounts are kept out; in every other org other accounts (for example an employer's) are never used.
- Advisory departments (legal, finance, tax) get read-only connector tools only, named one by one.
- The holding holds the most sensitive data (tax, personal legal, finances). Its repo stays private.
- Upward, cross-org reads happen only through the holding CoS, read-only, through `state.md`. Sensitive detail stays out of `state.md`.
- Downward, the only cross-org read is the company CoS reading `policy.yaml` from the pinned commit of the holding's separate policies repo. Departments never read it. A company never needs a clone of the holding hq, which stays private. The policies repo holds no sensitive data and is shared with every company's CEO clone.
- Numbers always carry source and date. If unknown, say so. Never invent a metric.

## 10. Roadmap

| Phase | Scope |
|---|---|
| 0 | Extract the framework from the reference instance, with no behavior change there |
| 1 | Build a holding instance from the wizard |
| 2 | Link the holding and the reference instance, read-only |
| 3 | Publish the framework |

Migrating the reference instance onto the framework happens only after v0 exists. v0.1.1 applied the review fixes to phase 0 (see the status line at the top).

## 11. Open questions

1. `state.md` schema versioning: `schema: state/1` exists; the announcement and compatibility policy (how breaking changes are announced, how long older versions are read) is still open (see `migrations/README.md`).
2. More than one human per org (a partner, a read-only professional): out of scope for v0. To keep the door open, "CEO" is a role with an id in `org.yaml`, not a hard-coded person.
3. License: resolved, MIT.
4. Migration UX: how much of an upgrade can be applied automatically while still arriving as a reviewable diff?
5. Policy enforcement: v0: the CoS reads files at session start; a validator script stays open.
6. Pending-list staleness: v0: `stale_after_days` in `portfolio.yaml` (default 14) flags stale orgs; open: what to do beyond flagging.
7. Holding policy repo separation: resolved in v0.1.1. The holding keeps policies in a separate small repo with no sensitive data; companies pin a commit of it and need no clone of the holding hq.
8. Whether `allowed-tools` patterns for `git -C` in skills behave as intended (unverified).
