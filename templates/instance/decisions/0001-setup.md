# 0001. Initial setup of {{ORG_NAME}}

- Date: {{DATE}}
- Status: accepted
- Card: none
- Decided by: {{CEO_ROLE_ID}}

## Context

{{ORG_NAME}} (`{{ORG_ID}}`) was set up with ceo-of-agents {{FRAMEWORK_VERSION}}. The setup wizard asked nine questions; the answers below are the starting configuration. They live in `org.yaml`, which stays the source of truth for the current values.

## Options

Each question offered the framework defaults or a custom answer. The answers chosen are listed under Decision.

## Decision

| # | Question | Answer |
|---|---|---|
| 1 | Level | {{LEVEL}} |
| 2 | Org name and id | {{ORG_NAME}} / {{ORG_ID}} |
| 3 | Chat language / file language | {{CHAT_LANGUAGE}} / {{FILE_LANGUAGE}} |
| 4 | Departments | {{SETUP_DEPARTMENTS}} |
| 5 | Names or personas | {{SETUP_PERSONAS}} |
| 6 | Approval gates | {{SETUP_GATES}} |
| 7 | Connectors per department | {{SETUP_CONNECTORS}} |
| 8 | Models (CoS / departments / workers) | {{MODEL_COS}} / {{MODEL_DEPARTMENTS}} / one-down (CoS workers: {{MODEL_WORKERS}}) |
| 9 | Holding policy source and pin | {{SETUP_POLICY}} |

## Consequences

- hq was generated with the structure described in `CLAUDE.md` and `operating-model.md`.
- Changing any of these answers later is a new decision record plus the matching edit in `org.yaml`.
- Gates can only be moved to a stricter tier where a holding policy applies.

## Links

- `org.yaml`
- `operating-model.md`
