# Migrations

How framework upgrades reach an instance (an org's hq repo).

## Principles

- Instance files record the framework version they were generated from: `framework_version` in `org.yaml` and in the `company/state.md` frontmatter.
- A framework upgrade never overwrites instance files. Updating the plugin changes only the plugin.
- Each upgrade that needs changes to instance files ships as `migrations/<from>-to-<to>.md`, for example `0.1.0-to-0.2.0.md`. It describes an explicit, reviewable diff: which files change, the exact edits, and why.
- The chief of staff (CoS) reads the migration, shows the diff to the CEO, and applies it as a normal hq commit only after the CEO approves. The commit also bumps `framework_version` in `org.yaml` and `state.md`.
- Migrations are applied in order, one version step at a time; none is skipped.
- From `0.7.0`, the CoS checks the version at session start with the hidden `hq-version` procedure and proposes the migrations (an older hq gets the check through `intake`). It still applies them only after the CEO's OK.

## Schema versions

Each schema carries its own version in the file (`state/1`, `org/4`, `portfolio/1`, `policy/1`). A breaking change bumps the number (`state/1` to `state/2`) and ships with a migration. Additive, backward-compatible changes do not bump it.

How long a holding keeps reading the previous schema version of a company `state.md` is an open question (design spec, section 11). Until resolved, a reader should accept the version it knows and report any other as "unreadable schema" rather than guess.

## Current status

Migrations are documents, not scripts. Framework version `0.1.0` was the first release.

Version `0.1.1` changes the `org.yaml` `policy` block (`repo`, `local` and `pin`; `path` removed), adds `policies_repo`, adds `models.ceiling.cos` to the holding `policy.yaml`, moves holding policies to a separate repo, and adds `.claude/agents/reader.md` and `worker.md`. No migration ships because no `0.1.0` instance is supported for upgrade yet.

Version `0.2.0` bumps `org.yaml` to `org/2` (fleet purpose `org.purpose`, chief of staff name `cos.display_name`, `employer_rules` for job hqs) and ships the first migration: `0.1.1-to-0.2.0.md`.

Version `0.3.0` renames the setup wizard to `init-fleet` and hides the four CoS procedures from the `/` menu; no schema changes. Migration: `0.2.0-to-0.3.0.md` (wording in `CLAUDE.md` and `operating-model.md`, the account-separation line for custom departments).

Version `0.4.0` adds three working rules: a reason for every elevated grant (department review in `init-fleet`, and a paragraph in `CLAUDE.md` for departments added later), task-splitting rules for the CoS, and blocked and failure hygiene in the worker and department agent files. No schema changes. Migration: `0.3.0-to-0.4.0.md`.

Version `0.5.0` adds `company/vision.md` and `company/strategy.md`, moves machine-specific forbidden connectors to an untracked `accounts.local.yaml`, rewrites the wizard's gates question in plain language, and drops its connectors question (departments start with none; the CoS checks other accounts' connectors at the first session). No schema changes. Migration: `0.4.0-to-0.5.0.md`.

Version `0.6.0` bumps `org.yaml` to `org/3`: a registry of product repos (`repos:`) and an optional roadmap tracker (`tracker:`, a GitHub Project), with local clone paths per machine in `accounts.local.yaml`. A standing rule keeps issues and the tracker current; `intake`, `record-decision` and `weekly-brief` gain tracker steps, and the engineering catalog gains tracker hygiene. Migration: `0.5.0-to-0.6.0.md`.

Version `0.7.0` bumps `org.yaml` to `org/4`: each department gets an `agent` name, its persona in lowercase or its id, which names its agent file and is used to route and open it. A new hidden skill, `hq-version`, checks the hq against the installed plugin at session start and proposes the pending migrations. Migration: `0.6.0-to-0.7.0.md`.

Version `0.8.0` drops the CoS's first-session question about connectors of other accounts: no more per-computer `forbidden_connectors` in `accounts.local.yaml` and no more deny rules written to `.claude/settings.local.json`. `accounts.local.yaml` keeps only `repo_paths`. The written account-separation rule, departments with no connectors by default and the optional `accounts.forbidden_connectors` in `org.yaml` stay. No schema changes. Migration: `0.7.0-to-0.8.0.md`.

Version `0.8.1` makes one copy of the plugin, installed at project scope in the hq folder, the supported install: the README install and update steps use project scope and say how to remove a second copy at another scope, `init-fleet` accepts the `.claude/settings.json` that install writes, and `hq-version` points to a stale second install when the hq is newer than the loaded plugin. No schema changes. Migration: `0.8.0-to-0.8.1.md` (version bump only).

Version `0.9.0` changes the setup wizard and the generated hq: chat language asked first, multi-line answers kept verbatim, a commands question for custom departments, an `attribution` setting for commits and pull requests, repos that do not exist yet (`planned: true`), "later" answers that become action items, the per-department option "top model, workers included" (`workers: same`), and a pending list across companies at the start of a holding session. No schema changes: both new keys in `org.yaml` are optional. Migration: `0.8.1-to-0.9.0.md`.

Version `0.10.0` adds the fleet purpose `personal` (company level only, never in a holding portfolio, no holding policy or employer rules, no product repos or roadmap questions), three advisory catalog entries offered only for it (`health`, `money`, `paperwork`), and a git-ignored `private/` folder for personal data in a personal hq. No schema changes: `personal` and the three catalog ids are new allowed values. Migration: `0.9.0-to-0.10.0.md` (version bump; a holding also gets two one-line edits in `CLAUDE.md` so it skips personal hqs).
