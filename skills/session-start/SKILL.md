---
name: session-start
description: Start-of-session routine of the chief of staff in a ceo-of-agents hq. Syncs the hq, reads the boot files, checks the plugin version and the size of the boot files, runs the checks that apply to this org (clone paths, holding policy, portfolio, private data), processes the inbox and gives a short status. Use at the start of every chief of staff session.
user-invocable: false
allowed-tools: Read Grep Glob Edit Write Bash(git remote:*) Bash(git pull:*) Bash(git status:*) Bash(git rev-list:*) Bash(git -C * fetch *) Bash(git -C * show *) Bash(git -C * symbolic-ref *) Bash(git -C * status *) Bash(ls:*) Bash(wc:*) Bash(date:*)
---

# session-start: the chief of staff's start of session

Reply to the CEO in the chat language set in `org.yaml` (`language.chat`); write every file in the file language (`language.files`).

Only the chief of staff (CoS) runs this skill. A department agent never does: it skips the CoS session start.

Why a skill: this routine runs once per session, so it does not need to sit in `CLAUDE.md`, which every session and every agent loads. `CLAUDE.md` keeps the identity, the gates, the house rules and the map; procedures like this one load on demand.

Run the steps in order. A step marked "only when" is skipped silently when its condition is false.

## Steps

1. **Pull.** If `git remote` is empty, skip pull and push and say once in the status: "No remote: pull and push skipped". Otherwise `git pull` the hq (the CEO may work from several computers; the remote main branch is the reference). If the pull fails, say so in the status and continue with the local copy.

2. **Read.** `org.yaml`, `company/vision.md`, `company/strategy.md`, `company/state.md`, `company/decision-queue.md`, `accounts.local.yaml` (if present), and list `inbox/`.

3. **Plugin version.** Use the `hq-version` skill to compare this hq's `framework_version` (in `org.yaml` and `company/state.md`) with the installed plugin version. If the hq is behind, say so in one line of the status, list the migrations to apply in order, and add one A item asking the CEO's OK (unless one is already open). Apply them only after that OK, with the same skill: it shows a short summary of what changes, then commits with notice. Never migrate silently. If the hq is ahead of the plugin or a version is unknown, say so in one line and continue.

4. **Boot files.** Measure the boot files against the budgets in `${CLAUDE_PLUGIN_ROOT}/schemas/boot-set.md`: their size with `wc -c` on the files that exist, and the long lines of `company/state.md` with Grep (pattern `^.{301,}`). If everything is within budget, say nothing. Otherwise add one line to the status that names each offending item, for example: `Boot files over budget: company/state.md 12.0 KB (budget 8 KB); 2 lines over 300 characters in company/state.md ("Acme app: ...", "Launch plan: ..."). I can move the detail to linked notes.` Quote at most three long lines by their first words, then "and N more". Propose the trim; do it only when the CEO agrees. Add no A item for it.

5. **Repos on this machine** (only when `repos` in `org.yaml` lists a repo other than the hq itself, role `hq`). If such a repo is not marked `planned: true` and has no entry under `repo_paths` in `accounts.local.yaml`, ask the CEO for its local clone path with the `product-repos` skill (section "Clone paths"). Clone paths differ per computer, so git does not track `accounts.local.yaml`: never commit it.

6. **Policy check (tighten-only)** (only when `policy` in `org.yaml` is not `null`). Read the pinned holding policy read-only. Read `local` and `pin` from the `policy:` block in `org.yaml`, then run `git -C <local> fetch` (optional; it may fail offline) and `git -C <local> show <pin>:policy.yaml`. `local` is a clone of the holding's separate policies repo. Read only `policy.yaml`, nothing else, and never a clone of the holding hq. No other agent reads it. Ceilings and all other limits come only from the policies repo `policy.yaml`, never from `org.yaml`: `org.yaml` has no `models.ceiling`, so never report a missing ceiling there. Compare the policy with `org.yaml`:
   - Gates: for every action in the holding file, this org's tier must be equal or stricter (free < notice < ok). An action absent here inherits the holding tier (fine).
   - Connectors: any holding `forbidden_connectors` entry present in this org's connectors is a loosening.
   - Language: if the holding sets `language.files` and it differs from this org's `language.files`, it is a loosening.
   - Models: `models.cos` more capable than `models.ceiling.cos`, or `models.departments` or any department `model` more capable than `models.ceiling.departments`, or a worker model (one tier below its parent, or the parent's own tier for a department with `workers: same`) more capable than `models.ceiling.workers`, is a loosening.

   Report the result in the status: `Policy check (pin <short sha>): OK`, or `Policy check: N loosening(s)` with one line each (for example `gate merge: company=notice, holding=ok`). For each loosening add an A item asking the CEO to tighten the setting or to approve a pin or policy change. Never fix silently. If the policies repo or the pin cannot be read, say only `Policy check skipped: <reason>`. Do not report a gap from `org.yaml` in that case, and add no A item (a skipped check is not a loosening).

7. **Portfolio pending list** (only when `org.level` is `holding`). Read `portfolio.yaml`. For each org in `orgs`, read its pending items read-only, one `git -C <absolute path> <subcommand>` per call (no `cd`, no pipes), and never change its clone (no pull, checkout or commit). If the org has a remote in `portfolio.yaml`, run `git -C <path> fetch origin` (a failure is not an error: note it and use the last fetched ref) and find the default branch with `git -C <path> symbolic-ref --short refs/remotes/origin/HEAD` (if that fails, `origin/main`). If it has `remote: ""` or no remote-tracking ref at all, skip the fetch and read the local default branch: `git -C <path> symbolic-ref --short HEAD` (if that fails, `main`), and mark the org `read: local <branch> (no remote, may include unpushed changes)`. Run `git -C <path> show <ref>:org.yaml` and read only `org.purpose`: if it is `job` or `personal`, skip the org (a job or personal hq never belongs in a portfolio; say so once). Otherwise run `git -C <path> show <ref>:company/state.md` and take its "Waiting on the CEO" items and its "Open decisions" lines marked `[escalate: holding]`, with their codes exactly as written. Check the clone with `git -C <path> status --porcelain`. In the status, after the holding's own codes, add one line per org with its pending codes, and flag in one line each an org that is stale (`last_updated` older than `stale_after_days` in `portfolio.yaml`), dirty (non-empty `status --porcelain`) or unreachable (path missing, or `state.md` unreadable), and note a failed fetch as `fetch failed: state may be old`. This is a list only; the full cross-org analysis stays in the `portfolio-brief` skill.

8. **Private data on this computer** (only when `org.purpose` is `personal`). If `private/` is missing or empty, say once in the status: "`private/` is empty on this computer: personal data does not travel with git. If you keep it on another computer, copy it here yourself." Never copy, sync or push it yourself.

9. **Process the inbox.** Handle each handoff with the `intake` skill, then delete the processed notes in the same commit.

10. **Status.** Reply in the chat language with a 3-5 line status (what is new, what is blocked, which decisions wait) and the codes of the pending list, plus the one-line results of the steps above that have something to say. While `decisions/` holds only the setup record 0001, open the status with one line from the vision. Then ask what to do.

## Rules

- Read-only except: `accounts.local.yaml` (step 5), A items in `company/state.md` (steps 3 and 6), and what the `intake` skill writes (step 9).
- Never commit `accounts.local.yaml` or anything under `private/`.
- No scheduled automation and no hooks: this routine runs when the CEO opens a session.
