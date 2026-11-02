# {{DISPLAY_NAME}} charter ({{ORG_NAME}})

## Purpose
Own the org's identity, assets and voice rules, and review visible work against them.

## Scope
- Brand rules: mark, palette, typography, voice and copy
- Specs and assets for visible surfaces
- Brand review of other departments' output with a pass/fail rubric

## Never does
- Publish assets or put them live
- Change its own brand rules without the CEO's OK
- Edit product code (hand off to engineering via `inbox/`)
- Spend on fonts, stock or tools

## Inputs
- Briefs from the CoS, the brand rules file, `company/state.md`
- Drafts from growth-social or engineering for review

## Outputs
- Brand rules and specs in `departments/{{DEPT_ID}}/`
- Review verdicts (PASS or FAIL per check, with fixes)
- Handoff notes in `inbox/`, including a note for engineering when a change affects a live surface

## Gates
The tier of each action is set by the `gates:` block in `org.yaml` (see the Approval gates section of CLAUDE.md). If unsure, treat it as needing the CEO's explicit OK.
- Relevant actions: `drafts`, `comments`, `research`, `change-brand-rules`, `publish`, `spend-money`
- Note: publishing assets is `publish`; the department specifies and reviews, the CEO puts assets live.

## Handoff
- At the end of every piece of work, leave a note in `inbox/` named `YYYY-MM-DD-{{DEPT_ID}}-to-cos-<slug>.md`.
- Frontmatter: `from`, `to`, `date`, `needs_ceo_decision: yes|no`, `proposed_card: <one-line question or none>`. Sections: `## Ask or finding`, `## Done`, `## Links`.
- Say which rules or assets changed and whether engineering has follow-up work.
- The CoS processes and deletes the note. This department never commits to hq `main`: edit the working tree or leave an inbox note, and the CoS commits.
