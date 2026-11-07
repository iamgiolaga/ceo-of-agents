# {{DISPLAY_NAME}}: charter

Department `{{DEPT_ID}}` of {{ORG_NAME}} (`{{ORG_ID}}`). It is the CEO's own {{OWN_KIND}} `{{AGENT_NAME}}`, used as it is: its file lives outside this hq ({{OWN_LOCATION}}) and this org never edits it.

## Scope

Core job: {{DEPT_CORE_JOB}}

Use this department when:

{{DEPT_TRIGGERS}}

## Never does

- Never takes an action the approval gates reserve for the CEO.
- Never commits to the hq main branch.
- Never invents numbers.

Excluded from this department, and owned elsewhere:

{{DEPT_EXCLUSIONS}}

## How the chief of staff uses it

- An agent: dispatch it by its name, `{{AGENT_NAME}}`, with a self-contained brief that names this charter. A skill: run it yourself, then report as for any department's work.
- Its tools, model and connectors are the ones in its own file. This org grants it nothing (`connectors: []` in `org.yaml`); a grant goes through a decision card like for any department.
- The org's rules apply to its work: the approval gates in `org.yaml` and `CLAUDE.md`, this org's accounts only, and results that come back to the chief of staff, who records what matters in hq. If it does not leave an `inbox/` note itself, the chief of staff writes down its result.
