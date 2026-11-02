# Policies

This folder is the policy source for the companies registered in `portfolio.yaml`. `policy.yaml` states the minimum rules every company org must respect.

## Tighten only

Layering: framework defaults < these policies < company settings. A company may tighten a policy, never loosen it.

| Area | Tighten means | Example |
|---|---|---|
| Approval gates | Move an action to a stricter tier (free < notice < ok) | `merge` from notice to ok |
| Account separation | Add a restriction | Forbid one more connector |
| Language | Add a requirement | Files must be in a stated language |
| Models | Lower a ceiling | Cap workers to the cheapest tier |

## How companies use it

A company's `org.yaml` pins this folder:

```yaml
policy:
  source: <this hq's git remote>
  local: <path to the CEO's local clone>
  path: policies/
  pin: <commit sha>
```

At session start the company CoS reads `policies/policy.yaml` at the pinned commit, read-only, and reports any company setting that loosens a rule. It never fixes silently. Departments never read this folder.

## Changing policies and pins

- Changing `policy.yaml` is a commit the CEO approves (gate `change-policy-rules`).
- Companies pin a commit. Moving a company's pin to a newer commit is a CEO-approved commit in that company's hq. This holding never writes to a company hq.
