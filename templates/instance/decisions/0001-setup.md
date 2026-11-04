# 0001. Initial setup of {{ORG_NAME}}

- Date: {{DATE}}
- Status: accepted
- Card: none
- Decided by: {{CEO_ROLE_ID}}

## Context

{{ORG_NAME}} (`{{ORG_ID}}`) was set up with ceo-of-agents {{FRAMEWORK_VERSION}}. The setup wizard asked {{SETUP_QUESTION_COUNT}} question groups; rows marked not applicable were skipped. The answers below are the starting configuration. They live in `org.yaml`, which stays the source of truth for the current values.

## Options

Each question offered the framework's listed choices or a custom answer. The answers chosen are listed under Decision.

## Decision

| # | Question | Answer |
|---|---|---|
| 1 | Purpose and level | {{PURPOSE}} / {{LEVEL}} |
| 2 | Org name and id | {{ORG_NAME}} / {{ORG_ID}} |
| 3 | What the org is about | see `company/vision.md`; stage {{STAGE}} in `company/strategy.md` |
| 4 | Chat language / file language | {{CHAT_LANGUAGE}} / {{FILE_LANGUAGE}} |
| 5 | Departments | {{SETUP_DEPARTMENTS}} |
| 6 | Names or personas (CoS, departments, CEO) | {{SETUP_PERSONAS}} |
| 7 | Approval gates | {{SETUP_GATES}} |
| 8 | Models (CoS / departments / workers) | {{MODEL_COS}} / {{MODEL_DEPARTMENTS}} / one-down (CoS workers: {{MODEL_WORKERS}}) |
| 9 | Holding policy (companies) or employer rules (job) | {{SETUP_POLICY}} |
| 10 | Repositories | {{SETUP_REPOS}} |

## Consequences

- hq was generated with the structure described in `CLAUDE.md` and `operating-model.md`.
- Changing any of these answers later is a new decision record plus the matching edit in `org.yaml`.
- Every department starts with no connectors. A connector is granted later through a decision card with a one-line reason.
- No connector is forbidden in `org.yaml` at setup. At the first session, and on every new machine or fresh clone, the CoS asks which visible connectors belong to another account and records them in `accounts.local.yaml`, which git does not track.
- Gates can only be moved to a stricter tier where a holding policy applies.

## Links

- `org.yaml`
- `company/vision.md`
- `operating-model.md`
