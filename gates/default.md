# Default approval gates

Three tiers, ordered `free < notice < ok`. An org may change the table in `org.yaml`; a holding policy may only be tightened by a company.

## The table

| Tier | Rule | Action ids |
|---|---|---|
| free | Do it and mention it | `issues-and-labels`, `comments`, `drafts`, `open-pr`, `research`, `hq-write` |
| notice | One line before acting: what, where, content. Do not wait for a reply | `push-non-deploy-branch`, `hq-commit`, `dispatch-pushing-department` |
| ok | The CEO's explicit OK, as a narrow and exact request, batched into the pending list | `merge`, `deploy`, `publish`, `contact-people`, `spend-money`, `rotate-secrets`, `delete-data`, `org-or-repo-settings`, `change-brand-rules`, `change-policy-rules`, `file-or-sign`, `make-payment` |

## Actions in plain language

| Action id | Meaning |
|---|---|
| `issues-and-labels` | Create or edit tracker issues, project items, fields, labels, milestones |
| `comments` | Comment on issues, PRs and tracker items |
| `drafts` | Prepare drafts of documents, posts, emails or messages without sending or publishing them |
| `open-pr` | Open a pull request (the review and merge are the gate) |
| `research` | Read, search and analyze; no side effects outside hq |
| `hq-write` | Edit files in the org's hq working tree (committing is `hq-commit`) |
| `push-non-deploy-branch` | Push a branch that does not trigger a deploy or publish |
| `hq-commit` | The CoS commits and pushes to the hq main branch |
| `dispatch-pushing-department` | Start a department that will push code or content |
| `merge` | Merge a pull request into a default or protected branch |
| `deploy` | Release or promote to an environment, including a push that itself deploys or publishes |
| `publish` | Make anything public: posts, pages, packages, assets, announcements |
| `contact-people` | Send any message to a person or organization outside the org |
| `spend-money` | Commit funds: purchases, subscriptions, paid promotion |
| `rotate-secrets` | Rotate or revoke credentials and keys |
| `delete-data` | Delete or irreversibly change data, repos, branches of record |
| `org-or-repo-settings` | Change organization, repository, account or security settings |
| `change-brand-rules` | Change the identity, palette, typeface or voice rules |
| `change-policy-rules` | Change gates, policies or charters' approval rules |
| `file-or-sign` | File, sign, accept or submit anything legally or officially binding |
| `make-payment` | Pay, transfer or authorize a payment |

## Principles

1. Do not ask for OKs the table does not require.
2. Batch asks into the pending list (`A` items); do not interrupt per action.
3. Run exactly the approved action, nothing broader.
4. Tracking writes and PR creation are free; the review and merge are the control point.

## Advisory departments

Legal, finance and tax departments are advisory. They never perform `file-or-sign` or `make-payment` at all, in any tier: they prepare and recommend, and the CEO acts outside the agents. No org configuration or policy may lower this; those two actions stay in `ok` and the advisory departments do not get tools for them.

## Overriding the default in an org

An org copies the block below into `org.yaml` under `gates:` and moves action ids between the lists. Rules: every action id appears in exactly one list; ids come from this file; moving an action to a lower tier (for example `merge` from `ok` to `notice`) is a loosening and is allowed only if no holding policy sets a stricter minimum and the advisory rule above holds. Changing gates afterwards is itself `change-policy-rules` (tier `ok`).

```yaml
gates:
  free: [issues-and-labels, comments, drafts, open-pr, research, hq-write]
  notice: [push-non-deploy-branch, hq-commit, dispatch-pushing-department]
  ok: [merge, deploy, publish, contact-people, spend-money, rotate-secrets, delete-data, org-or-repo-settings, change-brand-rules, change-policy-rules, file-or-sign, make-payment]
```

## Tighten-only rule against a holding policy

When a company sets `policy` in `org.yaml`, the company CoS checks it at session start (read files only; no script). It reads only `policy.yaml` from the pinned commit of the holding's separate policies repo, read-only: an optional `git -C <local> fetch` (it may fail offline), then `git -C <local> show <pin>:policy.yaml`. It never reads a clone of the holding hq, and departments never read the policies repo. Compare with org.yaml:

1. Gates: for every action in the holding file, the company tier must be at or above the holding tier. An action absent from the company gates inherits the holding tier (fine).
2. Connectors: any holding `forbidden_connectors` entry present in any department's `connectors` is a loosening.
3. Language: holding `language.files` set and different from the company `language.files` is a loosening.
4. Models: `models.cos` more capable than `models.ceiling.cos`, or `models.departments` or any department `model` more capable than `models.ceiling.departments`, or a worker model (one tier below its parent) more capable than `models.ceiling.workers`, is a loosening.

Report in the session-start status either `Policy check (pin <short sha>): OK` or `Policy check: N loosening(s)` with one line each (for example `gate merge: company=notice, holding=ok`), and add an `A` item asking the CEO to tighten or to approve a pin or policy change. Never fix silently. If the pin cannot be read, say `Policy check skipped: <reason>`.
