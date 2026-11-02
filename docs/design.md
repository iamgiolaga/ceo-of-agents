# ceo-of-agents: design spec (draft v0)

Status: v0.1.0 implemented (phase 0). Sections updated where implementation diverged.

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
  catalog/           department catalog (charter + agent template each)
  skills/            init-org, intake, record-decision, weekly-brief, portfolio-brief
  schemas/           state.md, org.yaml, portfolio.yaml, policy.yaml, handoff, decision card, decision record
  gates/             default approval-gate table
  migrations/        vN-to-vN+1 diffs
```

There is no `agents/` dir: Claude Code auto-registers every `.md` under a plugin's `agents/` as a live subagent, so templates with placeholders cannot live there.

**Instance (hq) layout**

```
<org>-hq/
  CLAUDE.md                     CoS instructions (generated)
  org.yaml                      level, id, language, models, gates, policy pin
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
  portfolio.yaml                holding only
  policies/policy.yaml          holding only
```

A holding instance is an org like any other whose specific job is to be a registry: `portfolio.yaml` lists references to company hqs, which may live in separate code orgs. It also holds `policies/` (`policies/policy.yaml`). Its departments are chosen at setup like in any org, and may be none.

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
framework_version: 0.1.0
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
    remote: <git remote>        # for pull
```

The holding CoS runs `git pull --ff-only` on each registered hq and reads `state.md` read-only. On pull failure it reads the local copy and marks the org "pull failed". It never writes to a company hq. Staleness is visible from `last_updated` against `stale_after_days`. Reads use the CEO's own git credentials (the CEO is a member of every org); the holding stores no credentials and nothing is shared between orgs.

### Downward: holding to company

Policy layering: framework defaults < holding policies < company overrides. A company may tighten a holding policy, never loosen it.

| Policy area | "Tighten" means | Example |
|---|---|---|
| Approval gates | Move an action to a stricter tier | "Merge" from notice to explicit OK |
| Account separation | Add a restriction | Forbid a connector the holding allows |
| Language | Add a requirement | Files must be in a stated language |
| Models | Lower a ceiling | Cap workers to the cheapest tier |

The holding's policy lives in `policies/policy.yaml` (schema `policy/1`): minimum gate tiers, forbidden connectors, required file language, model ceilings. A company hq references it from `org.yaml`:

```yaml
policy:
  source: <holding hq remote>
  local: <path>                 # CEO's local clone of the holding hq, read-only
  path: policies/
  pin: <commit sha>
```

At session start the company CoS runs `git -C <local> show <pin>:policies/policy.yaml` and compares four areas: gates (company tier at least as strict as the holding minimum), connectors (no holding-forbidden connector granted to any department), language (file language matches the required one), models (no company model above the holding ceilings). It reports `Policy check: OK` or one line per loosening, and adds an `A` item. It never fixes silently. If the policy is unreadable it says "skipped: <reason>". Moving the pin is an explicit commit the CEO approves.

### Aggregated CEO pending list

Codes are namespaced per org: `ACME-D12` (decision), `ACME-A3` (action). The holding CoS composes one list across all orgs in its brief, ordered by urgency and level. Items are resolved in the owning org: the CEO answers there, and the owning CoS records it. The holding list is a view, never a second source.

### Escalation

When a company decision touches money, personal liability or the portfolio, the company CoS marks the card `escalate: holding`. The holding sees it on its next read of `state.md`, adds context (tax, personal legal, cash across orgs) and puts its advice in the holding brief next to the namespaced code. The CEO carries it into the owning org when answering the card. The holding never writes to a company hq, so the decision is still recorded only where it belongs.

## 6. Setup wizard

`/ceo-of-agents:init-org` runs in an empty directory and asks:

1. Level: holding or company.
2. Org name and short id (used in codes).
3. Language for chat with the CEO, and language for files.
4. Departments: nothing is preselected. Pick from the catalog, define custom ones, or none.
5. Names or personas per agent (optional; default is the role name).
6. Approval-gate table: accept defaults or edit.
7. Allowed connectors per department.
8. Model tiers for the CoS, departments and workers.
9. For a company: holding policy source and pin (optional). If a policy is given, the tighten-only check runs before anything is generated.

It generates `CLAUDE.md`, `org.yaml`, `operating-model.md`, the `company/` files with empty schema-valid state, one charter and one agent file per department (file names use the department id), `decisions/README.md`, `inbox/README.md`, `metrics/README.md` and an initial decision record (`0001`) capturing the setup answers. A holding also gets `portfolio.yaml` and `policies/`. Optionally it writes `.claude/settings.json` enabling the plugin, only with the CEO's OK. It never pushes and asks before the first commit.

**Starting department catalog**

Catalog entries are templates, not defaults: each org decides its own structure. Picking the same entry in two orgs creates two independent departments with separate charters and memory.

| Department | Purpose | Default tool allowlist idea | Default gate notes |
|---|---|---|---|
| Engineering | Code, CI, releases, security | Read, edit, shell, delegation; repo access for the org only | Open PRs free; merge, deploy, secret rotation need OK |
| Design and brand | Identity, assets, tone of voice, brand review | Read, edit, design-tool connector, delegation | Brand-rule changes need OK; publishing needs OK |
| Business | Model, pricing, market, competitors, discovery | Read, edit, web search and fetch | Contacting people or spending needs OK |
| Growth and social | Editorial calendar, post drafts | Read, edit, web search | Drafts only; publishing needs OK |
| Legal | Privacy, terms, policies, accuracy of claims. Advisory | Read, edit, web search | Never signs or files; routes to a professional on request |
| Finance and accounting | Bookkeeping views, cash, invoices review. Advisory | Read, edit; no payment tools | No payments or transfers; spending needs OK |
| Tax | Tax position, deadlines, document checklists. Advisory | Read, edit, web search; no filing tools | Never files or signs; deadlines surface as `A` items |
| Operations | Admin, vendors, tooling, calendars of obligations | Read, edit, scoped connectors | Subscriptions and vendor contact need OK |

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

Principles: do not ask for OKs the table does not require; batch the asks into the pending list; run the exact approved action, nothing broader. Advisory departments (legal, finance, tax) never do `file-or-sign` or `make-payment` at all; no config can lower them.

## 8. Models and cost

| Role | Default tier | Notes |
|---|---|---|
| CoS | Top | Plans, decides, judges, talks to the CEO |
| Department | Configurable, default top | Vertical specialist; orchestrates its own workers |
| Workers | One tier down from their parent | Bulk reading, drafting, code, commands |

Rules: workers never escalate to a more capable model than their parent. Departments delegate to workers and do not hand work back up. The CoS does small things itself when writing the brief would cost more than the work. Every result is verified (diff read, check run) before it is built on or reported. Briefs to workers are self-contained: goal, files, constraints, definition of done, what to return.

## 9. Separation and privacy

- Each department has an explicit `tools:` allowlist; connectors are granted per department, not globally.
- Never mix accounts: credentials and connectors for org A are not used for org B, and work-employer accounts are never used for any org's affairs.
- The holding holds the most sensitive data (tax, personal legal, finances). Its repo stays private.
- Upward, cross-org reads happen only through the holding CoS, read-only, through `state.md`. Sensitive detail stays out of `state.md`.
- Downward, the only cross-org read is the company CoS reading `policies/` at the pinned commit. Departments never read it. Nothing else in the holding repo is read.
- Numbers always carry source and date. If unknown, say so. Never invent a metric.

## 10. Roadmap

| Phase | Scope |
|---|---|
| 0 | Extract the framework from the reference instance, with no behavior change there |
| 1 | Build a holding instance from the wizard |
| 2 | Link the holding and the reference instance, read-only |
| 3 | Publish the framework |

Migrating the reference instance onto the framework happens only after v0 exists.

## 11. Open questions

1. `state.md` schema versioning: `schema: state/1` exists; the announcement and compatibility policy (how breaking changes are announced, how long older versions are read) is still open (see `migrations/README.md`).
2. More than one human per org (a partner, a read-only professional): out of scope for v0. To keep the door open, "CEO" is a role with an id in `org.yaml`, not a hard-coded person.
3. License: resolved, MIT.
4. Migration UX: how much of an upgrade can be applied automatically while still arriving as a reviewable diff?
5. Policy enforcement: v0: the CoS reads files at session start; a validator script stays open.
6. Pending-list staleness: v0: `stale_after_days` in `portfolio.yaml` (default 14) flags stale orgs; open: what to do beyond flagging.
7. Holding policy repo separation: a holding may later publish policies from a separate repo, so company sessions need no clone of the private holding repo.
8. Whether `allowed-tools` patterns for `git -C` in skills behave as intended (unverified).
