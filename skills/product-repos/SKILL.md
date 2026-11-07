---
name: product-repos
description: Keep the product repos registry and the roadmap board of a ceo-of-agents hq. Registers a repo or a GitHub Project board in org.yaml, handles repos that do not exist yet, asks for local clone paths on this computer, and holds the gh rules. Use when the CEO names a new repo or board, when a planned repo may now exist, when a clone path is missing, or before the first gh call of a session.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git remote:*) Bash(git status:*) Bash(git diff:*) Bash(git add:*) Bash(git commit:*) Bash(git push:*) Bash(ls:*) Bash(date:*) Bash(gh auth status:*) Bash(gh repo view:*) Bash(gh project view:*) Bash(gh project field-list:*)
---

# product-repos: the repos registry and the roadmap board

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. Departments read the registry in `org.yaml` and follow the rules in `CLAUDE.md`; they never edit it.

The registry: `repos:` in `org.yaml` (GitHub slug, role, visibility, issues home, whether it is protected, and `planned: true` for a repo that does not exist yet) and `tracker:` (a GitHub Project, or `none`). Field rules: `${CLAUDE_PLUGIN_ROOT}/schemas/org.yaml`. Local clone paths are per computer, under `repo_paths` in `accounts.local.yaml`, which git does not track. A holding and a personal hq keep `repos: []` and `tracker: none`.

## Register a repo or a board

The registry is a list of facts, not a decision: no decision card and no new record.

1. Ask only what is missing, in plain words: the address as `owner/name`, what it is in a word or two (code, site, docs, ...), public or private, and whether it already exists on GitHub. Validate the address: one `/`; the owner uses only letters, digits and `-`; the name only letters, digits, `-`, `_` and `.`.
2. Protected or not: for a repo other than the hq, ask one plain question, with nothing preselected: "Do other people work on this project and see what your agents write there (issues, comments, pull requests)? If yes, or if you are not sure, your agents will always ask you before writing there." Yes or "not sure" gives `protected: true`; no gives `protected: false`. The hq (role `hq`) is always `protected: false` and is never asked about.
3. A repo that does not exist yet gets `planned: true` (see "Planned repos").
4. The first repo of the list also needs an issues home: the repo that holds issues touching several repos (one of the listed repos, or the hq itself when it has a GitHub remote, then added with role `hq`, private). Exactly one item has `issues_home: true`.
5. A board: its address (`https://github.com/orgs/<owner>/projects/<number>` or `https://github.com/users/<owner>/projects/<number>`) and the name of its status field (often "Status"). Write `kind: github-project`, `owner`, `number` (an integer) and `status_field`.
6. Confirm the entry to the CEO in one line, edit `org.yaml`, and commit with notice (`chore: register <slug>`). Push if `git remote` is not empty.
7. For a repo that exists and is not the hq, ask for its clone path on this computer (see "Clone paths").

## Protected repos

A repo with `protected: true` gets no write from any agent without the CEO's explicit OK (see "Approval gates" in `CLAUDE.md`). The flag changes only on the CEO's word: "free <repo>" sets it to `false`, "protect <repo>" sets it to `true`; confirm in one line and commit with notice. The hq is never protected.

Owner patterns, only when the CEO asks for one (never propose it): an item with slug `<owner>/*` covers every repo of that owner that has no item of its own, with one `protected` value for all of them; an exact item for a repo of that owner is the exception and wins over the pattern. A pattern item has `issues_home: false`, no `planned` key and no clone path; for `visibility` take the CEO's answer for that owner's repos, and `public` when they are mixed or the CEO is not sure.

## Planned repos

A repo marked `planned: true` does not exist yet. Before the first write to it, check once with `gh repo view <slug>`. While it does not exist, skip each issue or tracker write for it with one line (this is not a failure) and make sure an A item asks the CEO to create it with the exact command, for example `gh repo create <slug> --private` (add one unless it is already open). Once it exists, remove `planned: true` from `org.yaml` with notice, clear the A item, and ask for its clone path.

## Clone paths

Ask once per computer for each registered repo other than the hq that is not planned, is not an owner pattern and has no entry under `repo_paths` in `accounts.local.yaml`: its local clone path on this machine, or "not cloned here". Write the answers to `repo_paths:` in that file, creating it if missing (each slug maps to a path, or to `null` when not cloned here; then agents reach it with `gh -R <slug>` only). Never commit `accounts.local.yaml`.

## Tools

Use `gh` with `-R <slug>` for a repo and `gh project <subcommand> --owner <owner>` for the tracker. If `gh` is missing, not signed in, or lacks the `project` scope (`gh auth status` shows it), say so once, add an A item with the exact command for the CEO (for example `gh auth refresh -s project`) unless one is already open, and carry on without tracker writes. Never guess what the tracker holds.

Issue and tracker writes themselves follow the `intake` skill (issue route) and the `record-decision` skill.
