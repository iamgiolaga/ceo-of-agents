# Policies

This repo holds the policy source for the companies of one holding. It is a small, separate repo: `policy.yaml` states the minimum rules every company org must respect, and this README explains the repo. Nothing else lives here.

## What must never go in this repo

This repo is shared with the CEO's clone of every company, so treat it as readable by all of them.

- No sensitive data: no tax, personal legal or finance detail, no personal data.
- No secrets, tokens, credentials or private URLs.
- No company details, numbers or decisions.
- No files other than `policy.yaml` and this `README.md`.

## Tighten only

Layering: framework defaults < these policies < company settings. A company may tighten a policy, never loosen it.

| Area | Tighten means | Example |
|---|---|---|
| Approval gates | Move an action to a stricter tier (free < notice < ok) | `merge` from notice to ok |
| Account separation | Add a restriction | Forbid one more connector |
| Language | Add a requirement | Files must be in a stated language |
| Models | Lower a ceiling | Cap workers to the cheapest tier |

## Create the repo

The holding setup wizard creates it. To do it by hand: make a new folder outside the holding hq, run `git init`, copy `policy.yaml` and `README.md` into it, edit `policy.yaml`, and commit. A remote is optional; add one with `git remote add origin <url>` if companies live on other machines or the repo should be backed up. Keep the remote private to the CEO's accounts.

## How companies use it

A company's `org.yaml` pins a commit of this repo:

```yaml
policy:
  repo: <git remote of this repo>
  local: <path to the CEO's local clone of this repo, read-only>
  pin: <commit sha>
```

At session start the company CoS runs `git -C <local> fetch` (optional, it may fail offline), then `git -C <local> show <pin>:policy.yaml`. It reads only that file, read-only, and reports any company setting that loosens a rule. It never fixes silently. Departments never read this repo.

## Update policies

- Changing `policy.yaml` is a commit in this repo that the CEO approves (gate `change-policy-rules`). The holding CoS prepares it; the CEO approves it.
- Companies do not follow changes on their own. Each company moves its pin to the new commit with a CEO-approved commit in that company's hq. The holding never writes to a company hq.
