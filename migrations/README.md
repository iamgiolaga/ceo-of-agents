# Migrations

How framework upgrades reach an instance (an org's hq repo).

## Principles

- Instance files record the framework version they were generated from: `framework_version` in `org.yaml` and in the `company/state.md` frontmatter.
- A framework upgrade never overwrites instance files. Updating the plugin changes only the plugin.
- Each upgrade that needs changes to instance files ships as `migrations/<from>-to-<to>.md`, for example `0.1.0-to-0.2.0.md`. It describes an explicit, reviewable diff: which files change, the exact edits, and why.
- The chief of staff (CoS) reads the migration, shows the diff to the CEO, and applies it as a normal hq commit only after the CEO approves. The commit also bumps `framework_version` in `org.yaml` and `state.md`.
- Migrations are applied in order, one version step at a time; none is skipped.

## Schema versions

Each schema carries its own version in the file (`state/1`, `org/2`, `portfolio/1`, `policy/1`). A breaking change bumps the number (`state/1` to `state/2`) and ships with a migration. Additive, backward-compatible changes do not bump it.

How long a holding keeps reading the previous schema version of a company `state.md` is an open question (design spec, section 11). Until resolved, a reader should accept the version it knows and report any other as "unreadable schema" rather than guess.

## Current status

Migrations are documents, not scripts. Framework version `0.1.0` was the first release.

Version `0.1.1` changes the `org.yaml` `policy` block (`repo`, `local` and `pin`; `path` removed), adds `policies_repo`, adds `models.ceiling.cos` to the holding `policy.yaml`, moves holding policies to a separate repo, and adds `.claude/agents/reader.md` and `worker.md`. No migration ships because no `0.1.0` instance is supported for upgrade yet.

Version `0.2.0` bumps `org.yaml` to `org/2` (fleet purpose `org.purpose`, chief of staff name `cos.display_name`, `employer_rules` for job hqs) and ships the first migration: `0.1.1-to-0.2.0.md`.
