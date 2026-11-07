---
name: init-fleet
description: Setup wizard that generates a new organization hq repo (holding or company) from the ceo-of-agents templates. Asks groups of questions, shows a summary, then generates files. Run once, in an empty directory, only when the CEO explicitly invokes /ceo-of-agents:init-fleet.
argument-hint: "[optional: path to a file with all answers]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write Bash(git init *) Bash(git status *) Bash(git add *) Bash(git commit *) Bash(git remote add *) Bash(git -C * init *) Bash(git -C * add *) Bash(git -C * commit *) Bash(git -C * remote add *) Bash(git -C * fetch *) Bash(git -C * show *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(grep *) Bash(date *) Bash(python3 -c *) Bash(ruby -ryaml *) Bash(ruby -rjson *)
---

# init-fleet: setup wizard

Reply to the CEO in the chat language, which is settled before question 1 (see "Before question 1: chat language"). Ask the questions in that language. Files you generate use the file language chosen in question 4. Keep technical ids (action ids, file names, patterns) out of the questions; they go into the files.

You generate a new hq repo in the current directory from `${CLAUDE_PLUGIN_ROOT}/templates/`, `${CLAUDE_PLUGIN_ROOT}/catalog/`, `${CLAUDE_PLUGIN_ROOT}/gates/default.md` and `${CLAUDE_PLUGIN_ROOT}/schemas/`. Framework version: `0.12.0`. <!-- x-release-please-version -->

## Rules

- Nothing is preselected. Never present an answer as the default that you will assume if the CEO stays silent. If the CEO does not answer a question, ask again.
- Optional questions accept "later" (or any clear equivalent in the chat language). "Later" is an explicit answer; silence is not, so the rule "Nothing is preselected" still holds.
  - Optional, deferrable: the CEO display name (question 6), the employer rules pointer (question 9, job), the holding policy (question 9, purpose product, startup or company at company level), the hq remote (question 10), the policies repo remote (question 10, holding), the product repos and the roadmap board (question 10, not asked for a holding or a personal hq), the attribution question (question 10).
  - Required, never deferrable (ask again): purpose, level, org name and id, the three answers to question 3 ("not decided yet" is how to leave one open), chat and file languages, the departments answer ("none" is valid), the CoS name, the gates answer, the models answer, and a holding's policies repo path.
  - A deferred answer is written as its empty value (`""`, `null`, no remote, `[]`, `none`, no `attribution` key), shown as "deferred" in the summary, written as `deferred (<ORG_ID>-A<n>)` in the matching setup-record cell (inside the existing cell text, no newline, no `|`), and becomes exactly one A item (generation step 12). The A item names the question in plain words and the exact file and field to fill.
- Free-text answers may span several lines or be a bulleted list. Say so when you ask a free-text question (for example "a short list is fine"). Keep the CEO's words: never summarise, merge or shorten an answer. You may only fix obvious typos and turn line breaks into markdown bullets. Show the result in the summary.
- During setup this wizard writes every hq file itself, in the main session: one coherent writer keeps the generated files consistent, and sub-agents may lack the `.claude/` write permissions. This rule wins over any user-level or project instruction (for example in `~/.claude/CLAUDE.md`) that says to delegate hands-on work to sub-agents. If such an instruction is present, tell the CEO in one line at the start, in the chat language, that the wizard writes the files itself during setup; then proceed exactly as without it.
- Ask one group of questions at a time (the numbered groups below), wait for the answers, then move on.
- Use plain words. Introduce a term only when the CEO needs it to answer.
- Never push. Never run `git commit` without asking the CEO first.
- The only write outside the current directory is the policies repo directory the CEO named (holding only, question 10). The only reads outside the current directory and `${CLAUDE_PLUGIN_ROOT}` are the policy read check in question 9 (company level, purpose product, startup or company): `git -C <local> fetch` and `git -C <local> show <pin>:policy.yaml`, and the file of an agent or skill the CEO brings in question 5, read once and read-only, only when the CEO gives its path.
- `mkdir` and `cp` write only into the target hq directory (the current directory) or the policies repo directory the CEO named. Never anywhere else.
- Do not ask about granting connectors (external services reached through MCP servers). Every department starts with none (least privilege); the CEO asks the CoS to grant one later, through a decision card. Connectors of other accounts are not asked either: the written account-separation rule in `CLAUDE.md` keeps them out. The one exception is the optional step after question 1, which may read the services the CEO picks as this org's, read-only, to pre-fill answers; it grants nothing to any agent.
- Do not call GitHub (`gh`) and do not create GitHub Projects or change any GitHub setting. Product repos and the tracker are recorded as the CEO gives them; the CoS uses them later.
- Every shell command in this skill is covered by `allowed-tools`, and every pattern there is used below. Use only those commands, with at least one argument each (for example `git status --short`).

## Step 0: check the directory

Run `ls -A`. The plugin is installed at project scope in this directory, which writes `.claude/settings.json`; if `.claude` is present, also run `ls -A .claude`. If the directory holds anything other than `.git` and `.claude/settings.json`, stop and tell the CEO what is there. Continue only if the CEO explicitly confirms generating into a non-empty directory. Never overwrite an existing file without a per-file confirmation.

## Non-interactive mode

If the CEO provides all answers in one message, or in a file passed as the argument, read them, map them to the question groups (the chat language comes from the message or the answers file), ask only about what is missing or invalid, and skip the questions already answered. Still run validation, the policy check (question 9, company level, purpose product, startup or company), the department review and show the full summary with a confirmation request before generating anything.

## Questions

### Before question 1: chat language
This step is not a numbered group and does not count in `{{SETUP_QUESTION_COUNT}}`.
- If the CEO wrote any text with the command (words after `/ceo-of-agents:init-fleet`, or an answers file passed as the argument), use that text's language as the chat language from the very first question. Show it in the summary for confirmation.
- Otherwise the first message asks only the chat language, in one short line that does not assume a language, for example: `Language? Lingua? Idioma? Langue? Sprache? (reply in the language you want me to use)`. Then ask everything in that language.
- Non-interactive mode: the chat language comes from the message or the answers file.

### 1. Purpose and level
Ask, nothing preselected: "What is this fleet for?" with the five values and their one-line meanings:
- `job`: the CEO's own work at an employer.
- `product`: one product the CEO builds.
- `startup`: a startup the CEO is founding or running.
- `company`: a company the CEO runs; at holding level, the CEO's affairs as an entrepreneur across their orgs.
- `personal`: the CEO's own personal life, for example health, money and paperwork.

Then, only if the purpose is `company`, ask the level: holding (the CEO as entrepreneur: registry of companies, policies, the most sensitive data) or company (one company, with its own code org and hq repo). Nothing is preselected. For `job`, `product`, `startup` and `personal` the level is `company` and is not asked; say so in one line.

For `job`, also say, once: a job hq is never registered in a holding portfolio and never pins a holding policy; the employer's connectors used for this job are this org's accounts and may be granted to departments later, through the CoS; check the employer's rules on data and AI tools before putting work content into this hq or any remote.

For `personal`, also say, once: a personal hq is never registered in a holding portfolio, never pins a holding policy and has no employer rules; personal data (documents, records, figures) lives only in `private/`, a folder of this hq that git ignores, so it stays on this computer and git never carries it to another one (copy it yourself if you need it elsewhere); the departments suggested for it only advise: they prepare and remember, the professional (a doctor, an accountant, a lawyer) decides, and they never file, sign or pay.

### After question 1: services you already use (optional)
This step is not a numbered group and does not count in `{{SETUP_QUESTION_COUNT}}`. Ask it once, for every purpose and level, in plain words, for example: "Do you want me to look at the services you already connected (chat, docs, code) to fill in names, channels and repos for you?"
- No, or no answer (the CEO goes on to something else): continue exactly as without this step and never ask again. This is the one question where no answer counts as an answer (no), unlike "Nothing is preselected" above. Non-interactive mode: no, unless the answers say yes.
- Yes: list the services connected in this session (from the tools named `mcp__<server>__<tool>`), one line each, with a plain name taken from the server name. If none is connected, say so in one line and continue. Ask, per service and with nothing preselected, whether it belongs to this org: "this org's", "another account's" or "skip". A service the CEO does not mark as this org's is never read, not even to list what it holds.
- Read only the services marked as this org's, read-only: use only their tools that list, search or read, never one that creates, sends, edits, deletes or changes a setting, and only to find names: the org, its teams and products, channels, docs spaces, platforms, and repository addresses. Do not read message or document contents beyond what names these things. Never keep personal data or secrets. A permission prompt may appear for a read; if it is denied, do not retry it and do not work around it.
- Show what was found as proposals, grouped by where each would go, each with the service it came from: the org name (question 2); hints for the answers to question 3 (the CEO writes the answers; a hint is never written as an answer); relevance notes for departments (question 5); product repos (question 10, where each repo still gets its own questions); and channels, spaces and platforms for the charters of the departments the CEO picks. The CEO confirms, edits or drops each item. Only confirmed items are used, each in its own question; nothing read is written to the hq beyond them.
- Reading grants nothing: every department still starts with `connectors: []`, and no agent file gets a tool of any service. A department that needs a service later asks the chief of staff, through a decision card.

### 2. Name and id
Ask for the org name and a short id used in codes (for example `ACME`). Validate the id: 2 to 8 characters, only capital letters A-Z and digits 0-9, starting with a letter. If invalid, explain and ask again. Do not invent an id from the name without the CEO choosing it; you may suggest one as a proposal only.

### 3. What the org is about
Ask three short questions in one group, in plain words. The answers anchor the CoS: they become `company/vision.md` and `company/strategy.md`, which the CoS reads at every session start. Do not ask about goals, success metrics or milestones (a holding's personal goals, below, are the one exception). Each answer is required; "not decided yet" is a valid answer and is written as given. Answers may be several lines or a short list (say so when you ask). They are kept as given (a list stays a list) and shown back in the summary for the CEO to confirm. The questions depend on the purpose and level:

| Purpose and level | A (becomes `{{VISION_WHAT}}`) | B (becomes `{{VISION_WHY}}`) | C, the stage (pick one; becomes `{{STAGE}}`) |
|---|---|---|---|
| `product`, `startup`, `company` at company level | What does the org do, and for whom? | Why does it exist? | idea, building, live |
| `job` | What is your role, and which team or people do you work with and for? | What does good work look like in this job? | new in the role, settled, in transition |
| `company` at holding level | As an entrepreneur, what do you want your orgs to achieve for you (personal goals)? | Where should your portfolio go (portfolio direction)? | starting, growing, steady |
| `personal` | What part of your life should this fleet look after? | What would make it worth it? | setting up, running |

Nothing is preselected for the stage; if the CEO does not pick one, ask again.

### 4. File language (chat language already set)
Show the chat language as already set (the CEO may still change it here) and ask the language of every file in hq. You may recommend English for files (shared tooling and future collaborators read it more easily), but do not preselect it. Store language codes (`en`, `it`, `fr`, ...).

### 5. Departments
Nothing is preselected. Read the `Purpose` line of each of these files and show a numbered list with one line per entry:
`${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` for ids `engineering`, `design-brand`, `business`, `growth-social`, `legal`, `finance`, `tax`, `operations`, and, only for purpose `personal`, `health`, `money`, `paperwork`. The personal entries are never listed for another purpose: they hold personal life data, which only a personal hq keeps (in `private/`).

After the list, show the suggestion line for the chosen purpose (and level) from `${CLAUDE_PLUGIN_ROOT}/catalog/README.md`, section "Suggestions by purpose", labelled as suggestions. Then, except for a holding, add one short relevance note per catalog entry based on the answers to question 3: why it seems relevant or not (for example "engineering: you said you are building an app"). Notes explain; they never preselect. Wherever the suggestion line lists `design-brand`, its note also gives the org chart reason from that file, in plain words, for example "design and brand: its first task can be to draw your org chart: you, your chief of staff, each department and how work flows between them"; for `job` add "a picture for you, not something that speaks for your employer". Nothing is preselected and the CEO still picks each department or none.

Then ask one plain question that covers the four ways to build the org, with nothing preselected, for example: "Which departments do you want? Pick numbers from the list, or say none. In the same answer you can also change one you pick, write your own from scratch, or bring agents or skills you already have." Each choice maps to one way:

1. **Take the proposal as is**: the CEO names catalog entries. Nothing more is asked about them.
2. **Proposal plus changes**: the CEO names a catalog entry and wants to change it (see "Changing a catalog department" below).
3. **Fully custom**: the CEO writes a department from scratch (see "Custom departments" below).
4. **Bring your own**: the CEO plugs in agents or skills they already have (see "Bringing your own agents or skills" below).

Ways can be mixed, and "none" is valid. A CEO who only picks numbers sees no other question in this group.

#### Changing a catalog department

For each catalog entry the CEO wants to change, show in plain words what it covers (its charter's Scope items), what it never does, and what it can do (read and write files; run commands, for engineering; hand work to helper agents; search the web), then ask what to add or remove, in one question: things to cover, things to drop (and who covers them then), things it must never do (and who does them instead), and abilities to add or drop. Keep every answer as given. Rules:
- Everything the CEO does not change stays from the catalog: its rules, its gates and its tools, including running commands where the catalog entry has it.
- Each ability added needs a one-line reason, asked in plain words ("what does it need that for?"); it is the reason for the grant. Abilities that can be added: running commands (`Bash`), handing work to the hands-on helper (`Agent(worker)`, only together with `Bash`), web search (`WebSearch`, `WebFetch`). Abilities that can be dropped: `Bash`, `Agent(...)`, `WebSearch`, `WebFetch`. Reading and writing files stay: every department writes its outputs and its handoff.
- An advisory entry (legal, finance, tax; in a personal hq also health, money, paperwork) never gains commands or helpers, and nothing can make it file, sign or pay. Say so in one line if asked, and do not record it.
- Connectors are not offered here: every department starts with none.

#### Custom departments

For every custom department ask for: an id in kebab-case, a role name, a one-line purpose, its scope (what it covers), its triggers (when the chief of staff should route work to it), its exclusions (what it must not do or handle) and its single core job (one sentence, because it feeds a one-line field; say so). Scope, triggers and exclusions can have several items each (a short list is fine); keep them as separate items, each exactly as given. Also ask, in plain words and with nothing preselected: "Does this department need to run commands (scripts, command-line tools, git)?" If yes, ask what for, in one line; that line is the reason for the grant and is kept as given. Custom departments are generated from `${CLAUDE_PLUGIN_ROOT}/templates/department/`. Do not invent any of these answers; if one is missing, ask again. Zero departments is valid. State that catalog entries are templates: the same entry chosen in another org creates an independent department with its own charter and memory. Department ids must be unique, kebab-case, letters, digits and hyphens.

#### Bringing your own agents or skills

For each agent or skill the CEO brings, ask, in plain words and with nothing preselected: its name as Claude Code knows it (for example `reviewer`, or `some-plugin:reviewer`); whether it is an agent or a skill; where it lives (a file path, "my own agents", or the plugin it comes from); what it is for, in one sentence; when the chief of staff should use it (a short list is fine); what it must not do, and who does that instead; and whether it replaces one of the listed departments. Its file is never rewritten, copied or moved: the org registers it as it is (routing table, charter, gates, account rules).
- If the CEO gives a file path, read that file once, read-only, and show its tools and its model in plain words. If its tools include a connected service, say in one line that the agent brings it with it and that this org's rules still apply to it (this org's accounts only). Setup grants it nothing and changes nothing in the file.
- Replacing a department: the replaced catalog entry is not generated. Propose the replaced department's id as the id of the brought-in one, so routing keeps the same name; the CEO may pick another.
- Own agents or skills can sit next to generated departments, replace some of them, or be the only departments.
- Its id follows the department id rules; its name must differ from every other department's agent name and id and from `reader` and `worker`. If it clashes, the brought-in name cannot change (its file is not edited), so ask the CEO to rename the other department.

#### Overlap check

After the departments are chosen (all four ways), compare what each one covers: the catalog Scope items (with the changes the CEO made), the custom scopes, and the purpose and triggers of each brought-in agent or skill. For each piece of work that two of them cover, say so in one plain line with a suggestion, for example: "Engineering and Security both cover security reviews. You can drop it from Engineering, or keep both and I will send security work to Security." It is a warning only: never block, and keep both if the CEO says so. Say nothing when nothing overlaps.

For a holding, say that departments are optional like in any org (typical picks are advisory ones, but do not suggest any).

For `personal`, say in one line that the suggested entries (health, money, paperwork) only advise: no commands, no delegation, and later only read-only connectors. Custom departments are offered as for any purpose, with the same questions, the commands question included.

### 6. Names
Ask for the chief of staff's display name: either the role name "Chief of staff" or a persona name. It is required, with no preselected answer; ask again if it is missing. For each chosen department ask for a display name: either the role name (for example "Engineering") or a persona name. Ask, with no preselected answer. Also ask for the CEO display name (optional, may stay empty). The CEO role id is `ceo`.

Then derive each department's agent name. Do not ask for it, except in the two cases below. A brought-in agent or skill keeps its own name as its agent name: it is not derived, and it may contain `:` (for example `some-plugin:reviewer`). The agent name is how the CEO talks to a department directly (`claude --agent <name>`), and it is the `name` of the department's agent file. Say it once, in plain words, when you show the result.
- Derivation. If the display name equals the role name (ignoring case), the agent name is the department id. Otherwise it is the persona slug: remove accents, lowercase, keep letters and digits, turn every other run of characters into one hyphen, and drop a leading or trailing hyphen ("Mike" gives `mike`, "Anna Maria" gives `anna-maria`, "Zoë" gives `zoe`). It must match `^[a-z][a-z0-9-]*$`. If nothing usable is left (for example a name in a non-Latin script), ask the CEO for a short name in Latin letters.
- Clashes. An agent name must differ from every other department's agent name and id, and from `reader` and `worker`. For each clash, ask one plain question, with nothing preselected, for example: "Your engineering and support departments would both be called `mike`. Pick another name for one of them, or I call one of them `mike-support`: which one?" The second option is always `<agent>-<department id>` for the department the CEO names. Check again after each answer.

### 7. Approval gates
Open with this purpose line: "This decides what agents may do on their own and what they must ask you first."

Read `${CLAUDE_PLUGIN_ROOT}/gates/default.md` (the table and "Actions in plain language") and show the actions in three groups, in plain words, with no action ids, tier names or file names in the visible text:
- "On their own, and they tell you after" (tier `free`);
- "They tell you in one line first, without waiting for you" (tier `notice`);
- "Only with your explicit OK" (tier `ok`).

Under each group, one line per action: its meaning, said simply, and its example from the Example column. Then add one line: "Whatever needs your OK goes on one list that you clear by code, and an OK covers exactly what was asked, nothing more."

Show the advisory rule only if an advisory department (legal, finance, tax, health, money or paperwork) was picked in question 5, and name only the ones picked, for example: "Your legal department only advises: it never signs, files or pays, whatever this table says." Do not mention departments the CEO did not pick.

Then offer three answers, nothing preselected:
1. Accept as shown.
2. Make something stricter: the CEO names actions and the group each moves to.
3. Make something looser: before recording it, warn in one line that agents will then do that action with less warning or none. Signing or filing anything binding, and payments, always need the CEO's OK (`file-or-sign` and `make-payment` stay in `ok`; see `gates/default.md`, "Advisory departments"): do not offer them, and refuse a request to move them.

Internally, the tiers are ordered `free` < `notice` < `ok`; moving an action toward `ok` is stricter. Record the final lists with the action ids in `org.yaml` only. Every action stays in exactly one list. If a holding policy applies, question 9 checks the result.

### 8. Model tiers
Show the tier list `[opus, sonnet, haiku]`, most to least capable. Ask which tier the CoS should use and which tier the departments should use (a per-department override is allowed; ask, no preselected answer). Explain the rule, which is fixed and is not a question: workers run one tier below their parent and never use a more capable model than their parent (`workers: one-down` in `org.yaml`). If the parent is the least capable tier, workers use the same tier. Every org gets two generic worker agents, `reader` and `worker`, which run one tier below the departments tier. After the fixed rule, offer one per-department option, nothing preselected: "top model, workers included". The department runs on the most capable tier (the first in `models.tiers`) and its workers run on that same tier instead of one below. It keeps its ability to delegate. The rule that workers never use a more capable model than their parent still holds (the same tier is not more capable). In `org.yaml` such a department has `model: <first tier>` and `workers: same`. Show the resulting worker model for the CoS, for the generic workers and for any department with an override or with "top model, workers included" in the summary.

### 9. Holding policy (company level, purpose product, startup or company) or employer rules (job); skip for a holding and for personal
For a job hq there is no holding policy question: a job hq is never governed by a holding. Instead ask for an optional pointer to the employer's rules on data, AI tools and accounts (a URL or a path; "none" is valid). It is stored as `employer_rules` in `org.yaml`. Never read or copy its content during setup.

For a personal hq, skip this group entirely: it is never governed by a holding and has no employer rules (`policy: null`, `employer_rules: null`). The rest of this section applies when the purpose is `product`, `startup` or `company` at company level.

Ask whether this company follows a holding policy. It is optional. If yes, ask for:
- the policies repo git remote (a small repo that holds only `policy.yaml` and a README). It may be a git remote URL, or `""` when the policies repo has no remote yet (the CoS reads only `local` and `pin` anyway),
- the CEO's local clone path of that policies repo (read-only for this org),
- the pin (a commit sha).

If given, verify read-only, reading only the policy file. Optionally fetch first (it may fail offline; that is not an error):
```
git -C <local> fetch --quiet
git -C <local> show <pin>:policy.yaml
```
If it cannot be read, report the reason and ask for a corrected value or to continue without a policy. If it can be read, parse it (schema `policy/1`; see `${CLAUDE_PLUGIN_ROOT}/schemas/policy.yaml`) and run the tighten-only comparison against the answers so far, immediately:
1. Gates: for every action in the policy file, the company tier must be at or above the policy tier. An action absent from the company gates inherits the policy tier (fine).
2. Language: policy `language.files` set and different from the company file language is a loosening.
3. Models: `models.cos` more capable than `models.ceiling.cos`, or `models.departments` or any department `model` more capable than `models.ceiling.departments`, or a worker model (one tier below its parent, including the generic `reader` and `worker`; for a department with `workers: same`, its own tier) more capable than `models.ceiling.workers`, is a loosening.

Report every loosening, one line each (for example `gate merge: company=notice, holding=ok`), before generating. A company may only tighten. Ask the CEO to adjust the answers; never silently fix them. Read nothing else in the policies repo.

### 10. Repositories and attribution
Ask these as questions, with no preselected answer. Both remotes are optional; "none" is valid.
- The hq git remote URL. If given, it is added after init (`git remote add origin <url>`); never pushed. Tell the CEO that, while there is no remote, the CoS skips pull and push and says so in its status line.
- Holding only: where to create the policies repo. Ask for an absolute path outside this hq directory (the CEO chooses it; do not propose one). Check with `ls -A <path>` that it does not exist or is empty; otherwise ask for another path. Then ask for the policies repo remote URL (optional; if given it is added with `git -C <path> remote add origin <url>`; never pushed). Explain that the policies repo must hold no sensitive data: only `policy.yaml` and `README.md`.
- Personal only, after the hq remote question: say in one line that a remote receives only the tracked files (structure, decisions, pointers), never `private/`, which stays on this computer.
- Job only, after the hq remote question: ask where the remote lives, a personal account or an employer account. It is the CEO's choice; propose nothing and impose nothing. Remind the CEO to check the employer's rules on where work content may be stored. Record the answer only in decision 0001 (`{{SETUP_REPOS}}`), not in `org.yaml`.

Then, company level only and not for a personal hq (a holding and a personal hq get `repos: []` and `tracker: none` without asking), two more questions in the same group. Say what they are for in one line: "With these, your chief of staff and departments keep your product's issues and roadmap up to date as they work." "None" is a valid answer to each, and both can be added later by telling the CoS.

- Product repos: "Which GitHub repositories hold your product (its code, website, docs)?" For each, ask its address as `owner/name` (for example `acme/acme-app`; the owner may be a GitHub organization or a personal account, and repos may mix both), what it is in a word or two (code, site, docs, ...), and whether it is public or private. Then ask, for each repo and with nothing preselected: "Do other people work on this project and see what your agents write there (issues, comments, pull requests)? If yes, or if you are not sure, your agents will always ask you before writing there." Yes or "not sure" records it as protected (`protected: true`), no as not protected (`protected: false`). Then ask whether the repo already exists on GitHub. If the CEO says it does not exist yet (the wizard never calls GitHub, so it takes the CEO's word), confirm in one line, for example "I will record <slug> as planned; your chief of staff will ask you to create it before it writes any issue there", and record it with `planned: true`. This also applies to the repo chosen as issues home. Validate the address: one `/`; the owner uses only letters, digits and `-`; the name only letters, digits, `-`, `_` and `.`; ask again if invalid. Do not ask for local folders: they differ per computer, so the CoS asks for them at the first session on each machine. When at least one repo other than the hq is given (existing or planned), say once, in one line, where to put it on this computer: next to this hq folder, inside the same parent folder, never inside the hq folder, with an example built from the current directory (for an hq in `/home/me/acme/acme-hq`, the repo `acme/app` goes to `/home/me/acme/app`). When no repo other than the hq is given, say nothing about folders. If at least one repo is given, ask where issues that touch several repos should go: one of the listed repos, or this hq when it has a GitHub remote (then the hq is added to the list with role `hq`, private, not protected and not asked about, its address taken from the remote URL). Without an hq remote, the choice is among the listed repos. Nothing is preselected, also with a single repo.
- Roadmap board: "Do you track this product's work on a GitHub Project board?" If yes, ask for its address (`https://github.com/orgs/<owner>/projects/<number>` or `https://github.com/users/<owner>/projects/<number>`) and the name of the field that holds each card's status (often "Status"); take the owner and number from the address. A board owned by a personal account can hold issues from repos of different owners. If the CEO wants a board but has none yet, say the setup does not create one: they create it in GitHub, then tell the CoS its address, and answer "none" for now.
- Whenever the CEO gives a board, or says they will create one, list the built-in workflows to switch on in GitHub (the board's menu, then Workflows), in plain words: "Auto-add to project" (new issues of a chosen repo join the board; set it once per repo), "Auto-add sub-issues to project" (smaller tasks split out of an issue join the board too), "Item added to project" (sets a status on new cards), "Item closed" (moves closed cards to Done), "Pull request linked to issue" (moves the card when work starts), "Pull request merged" (moves the card to Done), "Auto-close issue" (closes the issue when its card reaches Done). Say that the agents also update the board themselves; these workflows catch what they miss. The CEO switches them on; the setup changes nothing in GitHub.

Last, for every level, one more plain question, with no preselected answer: "How should commits and pull requests made in this hq be signed?" Three answers:
- (a) Claude Code's default: a co-author line naming the Claude model on commits, and a "Generated with Claude Code" line on pull requests.
- (b) Your own text: one text for commits and one for pull requests, or the same for both; the CEO writes it (kept as given).
- (c) None.

It is optional ("later" is valid). It is written to the `attribution` key of `.claude/settings.json` (generation step 13): (a) no `attribution` key, because Claude Code's default applies when the key is absent; (b) `"attribution": { "commit": "<text>", "pr": "<text>" }` with JSON string escapes (`\n` for line breaks); (c) `"attribution": { "commit": "", "pr": "" }`. Use empty strings, not `false`: older Claude Code versions reject `false` and then skip the whole settings file.

## Department review

Skip this if no department was chosen. Otherwise, before the summary, re-read each department draft as a whole: scope (and for a custom department its triggers, exclusions and core job), tools and model. If the parts do not fit together, go back to the affected question.

Every elevated grant needs a one-line reason tied to the department's scope. Elevated grants are any connector, `Edit`, `Write`, `Bash` and `Agent`.
- Template tools carry their reason: `Edit` and `Write` because every department writes its outputs and its `inbox/` handoff; `Agent(...)` because the department delegates to the generic workers it lists; `Bash` (engineering) because it runs repo checks and git on branches; `Bash` of a custom department because of the CEO's answer to the commands question (question 5), kept as the reason. An ability added to a changed catalog department carries the reason the CEO gave for it.
- A brought-in agent or skill keeps the tools of its own file; this org grants it nothing, so there is nothing to review here. If its file was read, show its tools in the summary.
- No connector is granted at setup: every department starts with none. A connector granted later goes through a decision card with its own reason (see `CLAUDE.md`).
- Drop any grant that has no reason before the summary, and tell the CEO which grants were dropped.
- Grants come only from the confirmed answers. Approving a permission prompt during setup, or replying after a denied one, grants nothing to any agent.

## Summary and confirmation

After the last group, show a compact summary: the chat language (ask to confirm it), purpose, level, name and id, what the org is about (the three answers to question 3), the CoS name, languages, departments (id, agent name, source, display name, model; the source is "catalog", "catalog, changed" with the changes listed, "custom" or "your own agent" / "your own skill" with where it lives and what it replaces; a brought-in one shows no model, its own file decides it; for a department with "top model, workers included" also its derived worker model; for a custom department "runs commands: yes (<reason>)" or "runs commands: no"; no connectors, see the line below), the overlap warnings if any, gate changes versus the framework table (in plain words), model tiers (CoS, departments, and the derived worker model of the generic `reader` and `worker` agents), policy and the result of the check (for a job hq: the employer rules pointer or none; for a personal hq: not applicable), the hq remote (or none), for a job hq where the remote lives, for a personal hq one line that personal data goes only in the git-ignored `private/` folder, at company level (not personal) the product repos (address, what it is, public or private, issues home, and whether your agents ask before writing there) and the roadmap board (address and status field, or none), planned repos (marked planned), for a holding the policies repo path and remote, the attribution answer (Claude Code default, custom text, none, or deferred), the services read after question 1 (names only, or "none") with each confirmed fact and where it goes, and every deferred answer (shown as "deferred"). For a holding, also show the policy ceilings `models.ceiling.cos`, `models.ceiling.departments` and `models.ceiling.workers` (proposed as described under `{{CEILING_COS}}`, `{{CEILING_DEPARTMENTS}}` and `{{CEILING_WORKERS}}` in the placeholder reference; the CEO confirms or changes them) and say they are written to the policies repo. Add one line: every department starts with no connectors (the CEO asks the CoS when one needs a connector). Show multi-line answers as given. Ask for explicit confirmation. If `.claude/settings.json` already enables the plugin (the project-scope install writes it), say it stays as it is and do not ask about it. Otherwise also ask whether to write `.claude/settings.json` enabling the plugin for this repo (optional; yes or no, ask, do not assume). On any correction go back to the affected group and show the summary again.

## Generation

Only after confirmation.

Before generating, tell the CEO that the wizard writes into `.claude/` (`.claude/agents/*.md` and optionally `.claude/settings.json`), which Claude Code protects, so a permission prompt may appear and must be approved. For headless runs (`claude -p`) these writes can be denied even with `acceptEdits` or `--allowedTools "Edit(.claude/**)"`: path rules do not lift the `.claude/` protection. If a write into `.claude/` is denied, do not retry or work around it. Finish everything else, then list the missing files in the final report and tell the CEO to run the wizard in an interactive session, or to approve the prompt, or to place the files from the templates by hand. Generate every file directly with your own tools; do not delegate file writes to sub-agents, which may lack the permissions.

1. List `${CLAUDE_PLUGIN_ROOT}/templates/instance/` and copy every file to the same relative path in the current directory, rendering as below. Two exceptions: `gitignore` is written as `.gitignore` (it lists two per-computer files that git must never track: `accounts.local.yaml`, with the local clone paths, and `.claude/settings.local.json`, Claude Code's local settings; for a personal hq it also lists `private/`), and `ignore` is written as `.ignore` (it lists `archive/`, which search tools that follow `.ignore` files then skip; git still tracks it). `archive/README.md` and `initiatives/README.md` (the index of initiatives, empty at setup) are copied like any other file. The wizard writes neither file and does not create `private/`: the CoS creates `accounts.local.yaml` when it first asks for a clone path, and `private/` is created when the first personal file is saved.
2. Placeholders: render every `{{NAME}}` using the "Placeholder reference" below. Every placeholder used in `templates/` and `catalog/` is listed there.
3. Conditional blocks: render them as described under "Conditional markers" below.
4. Holding-only files: see "Holding-only files" below.
5. `{{DEPARTMENTS_TABLE}}` and `{{GATES_TABLE}}`: see the reference below (column specs are fixed there).
6. `org.yaml`: fill every field (`models.workers` stays the literal `one-down`), including `departments` (id, agent, from_catalog, display_name, model, `workers: same` right after `model` only for a "top model, workers included" department, `connectors: []`), the `gates` lists, `repos` (a planned repo gets `planned: true`) and `tracker` (question 10; a holding: `[]` and `none`), `org.purpose`, `cos.display_name`, `employer_rules` (job: the pointer or `null`; otherwise `null`), `policies_repo` (holding: local and remote; otherwise `null`) and `policy` (company level, purpose product, startup or company, with a policy: repo, local, pin; otherwise `null`; always `null` for job and personal). A personal hq has `repos: []` and `tracker: none`. It must follow `${CLAUDE_PLUGIN_ROOT}/schemas/org.yaml`.
7. Per department:
   - catalog department: copy `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/charter.md` to `departments/<id>/charter.md` and `${CLAUDE_PLUGIN_ROOT}/catalog/<id>/agent.md` to `.claude/agents/<agent>.md` (`agent` = `departments[].agent`);
   - custom department: do the same from `${CLAUDE_PLUGIN_ROOT}/templates/department/` (`charter.md`, `agent.md`), filling the purpose, scope, triggers, exclusions and core job the CEO gave;
   - changed catalog department: copy the catalog files as for a catalog department, then append `${CLAUDE_PLUGIN_ROOT}/templates/department/changes.md` to the end of both the charter and the agent file, and edit the agent file's `tools:` line: the catalog tools plus the abilities added, minus the abilities dropped, in the catalog order with additions at the end. Nothing else in the catalog files changes;
   - brought-in agent or skill: render `${CLAUDE_PLUGIN_ROOT}/templates/department/own-charter.md` to `departments/<id>/charter.md`. No agent file is written: its own file stays where it is, unchanged.
   - every department, whatever its source: render `${CLAUDE_PLUGIN_ROOT}/templates/department/index.md` to `departments/<id>/README.md`, the one-line index of the documents the department writes there (`- none` at setup).
   Render the department placeholders from the reference below, and the conditional blocks (the custom department template has a `personal` block). Confirmed channels, spaces and platforms from the services step (after question 1) go at the end of the `## Inputs` list of the charter of the department they serve, one bullet each: `- <name> (<service>, confirmed at setup)`. A brought-in department's charter has no such list; mention them in the summary only. The charter stays at `departments/<id>/charter.md`. Make sure the department file name equals the `name:` in its frontmatter and `agent` in `org.yaml`.
   Not rendered: `catalog/README.md` (framework documentation, never copied). Catalog and department templates are used only for the departments chosen.
8. Create `departments/` only if there is at least one department. `company/briefs/.gitkeep` and `inbox/` come from the template.
9. Generic workers, for every org (also with zero departments): render `${CLAUDE_PLUGIN_ROOT}/templates/workers/reader.md` to `.claude/agents/reader.md` and `${CLAUDE_PLUGIN_ROOT}/templates/workers/worker.md` to `.claude/agents/worker.md`, with `{{MODEL_WORKERS}}`.
10. Holding only, the policies repo, at the absolute path the CEO gave in question 10: `mkdir -p <path>`, `git -C <path> init --quiet`, render `${CLAUDE_PLUGIN_ROOT}/templates/policies-repo/README.md` and `policy.yaml` into `<path>` (with `{{CEILING_COS}}`, `{{CEILING_DEPARTMENTS}}` and `{{CEILING_WORKERS}}`). Show `git -C <path> status --short`, then ask the CEO before its first commit. If approved: `git -C <path> add -A`, then `git -C <path> commit -m "chore: initialize policies"` with the attribution lines required by the session. If a remote was given: `git -C <path> remote add origin <url>`. Never push. Write nothing else outside the hq.
11. Decision `decisions/0001-setup.md`, from the template, following `${CLAUDE_PLUGIN_ROOT}/schemas/decision-record.md`: record all answers in Context and Decision (purpose, level, name and id, the CoS name, languages, departments with models, gate changes, model tiers, policy pin and check result, remotes, and for a holding the policies repo path). `Card: none`, `Decided by: ceo`. Add its row to `decisions/README.md`.
12. `company/state.md`: empty schema-valid state from the template (`schema: state/1`, the five fixed H2 sections, `- none` in empty sections, `next_action: 1`, `next_decision: 1`). Seed "Waiting on the CEO" in this order, numbered from 1, in the exact line format of `${CLAUDE_PLUGIN_ROOT}/schemas/state.md`, with `since` = today (`date +%F`):
    1. One `[high]` item per policy loosening the CEO chose to keep: `- <ORG_ID>-A<n> [high]: <exact action> (since YYYY-MM-DD)`, for example `In org.yaml move \`merge\` from notice back to ok, or approve a holding policy change; see decision 0001`.
    2. One `[normal]` item per planned repo: `- <ORG_ID>-A<n> [normal]: create the GitHub repo <slug> (<visibility>): run gh repo create <slug> --<visibility>, then tell the CoS (since YYYY-MM-DD)`.
    3. One `[low]` item per deferred answer: `- <ORG_ID>-A<n> [low]: answer the setup question deferred at setup: <the question in plain words>; <exact file and field>` (since YYYY-MM-DD), for example `answer the setup question deferred at setup: the hq remote URL; when you have it, tell the CoS, who runs git remote add origin <url>` or `answer the setup question deferred at setup: the CEO display name; it goes to org.yaml ceo.display_name`. The same code goes into the matching setup-record cell as `deferred (<ORG_ID>-A<n>)`.

    Set `next_action` to the last number plus 1 (1 if there is no item). If there is no item, the section is `- none`. Never omit the `since` date. Risks and Open decisions stay `- none` unless the CEO says otherwise (the A items are the only record, and decision 0001 holds the details).
13. `.claude/settings.json` is merged, never replaced. If it exists (the project-scope install writes `enabledPlugins`), keep every existing key and add or replace only `attribution` (answers b and c; for answer a or a deferred answer, change nothing). If it does not exist, write it with `enabledPlugins` (only if the CEO agreed, for example `{ "enabledPlugins": { "ceo-of-agents@ceo-of-agents": true } }`; check the marketplace name in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/marketplace.json` first) and `attribution` (only for answers b and c). If neither applies, do not create the file.
14. `company/vision.md` and `company/strategy.md` come from the template with the answers to question 3.

## Placeholder reference

Render with plain string replacement. Values are single-line unless stated (`{{VISION_WHAT}}`, `{{VISION_WHY}}` and the department list placeholders may be multi-line). Never leave a `{{...}}` behind. The org-wide placeholders also apply to `templates/workers/` and `templates/policies-repo/`.

### Org-wide (all files under `templates/instance/`)

| Placeholder | Value |
|---|---|
| `{{ORG_NAME}}` | Org name as given (question 2) |
| `{{ORG_ID}}` | Org id (question 2), for example `ACME` |
| `{{PURPOSE}}` | `job`, `product`, `startup`, `company` or `personal` (question 1) |
| `{{LEVEL}}` | `company` or `holding` |
| `{{COS_DISPLAY_NAME}}` | CoS display name (question 6) without quotes; the `org.yaml` template wraps it in quotes. In `CLAUDE.md` it renders "You are **<name>**, the chief of staff (CoS) of ...". If the name equals the role name the repetition is accepted, as for departments |
| `{{EMPLOYER_RULES}}` | `null`, or the pointer in double quotes (job only; question 9). Not job: `null` |
| `{{CHAT_LANGUAGE}}` | Chat language code (question 4), for example `en` |
| `{{FILE_LANGUAGE}}` | File language code (question 4) |
| `{{CEO_ROLE_ID}}` | `ceo` |
| `{{CEO_DISPLAY_NAME}}` | CEO display name without quotes, or an empty string. The template already wraps it in quotes (`display_name: "..."`) |
| `{{FRAMEWORK_VERSION}}` | `0.12.0` <!-- x-release-please-version --> |
| `{{DATE}}` | Today, `YYYY-MM-DD` (`date +%F`) |
| `{{MODEL_COS}}` | Tier chosen for the CoS (question 8) |
| `{{MODEL_DEPARTMENTS}}` | Tier chosen for departments (question 8; a department may override) |
| `{{MODEL_WORKERS}}` | The tier one below `models.departments` (`{{MODEL_DEPARTMENTS}}`) in `models.tiers`; the same tier if `{{MODEL_DEPARTMENTS}}` is the last. Used in `templates/workers/*` and in prose (`CLAUDE.md`, `decisions/0001-setup.md`). `org.yaml` keeps the literal rule `workers: one-down`, never a model name |
| `{{DEPARTMENTS_TABLE}}` | Markdown table `Agent \| Name \| Role \| Id \| Use for` (header row exactly `| Agent | Name | Role | Id | Use for |`), one row per department: `Agent` = the agent name (`name` in its agent file, `departments[].agent`), `Name` = display name (persona or role name), `Role` = the catalog role name (for example Business; the one in the agent file's intro line) or, for a custom department, the custom department's role name as given when it was defined, or, for a brought-in one, `Own agent` or `Own skill`, `Id` = the department id, `Use for` = a short routing phrase of at most 12 words derived from the charter's `Purpose` line, or for a custom or brought-in department from its core job (never the full sentence). Used inside the `departments` condition only (for none, the `no-departments` block applies) |
| `{{GATES_TABLE}}` | Markdown table `Tier \| Rule \| Action ids`, exactly three rows (free, notice, ok) in that order. `Rule` is the short rule from `${CLAUDE_PLUGIN_ROOT}/gates/default.md` (free: do it and mention it; notice: one line before acting; ok: the CEO's explicit OK). `Action ids` are the final action ids of that tier, in backticks, comma-separated |
| `{{DEPARTMENTS_YAML}}` | `[]` for no departments. Otherwise the value starts with a newline and is a block list indented two spaces under `departments:`; each item has `id`, `agent` (the agent name, right after `id`), `from_catalog` (catalog id, `custom` or `own`), `adapted: true` (right after `from_catalog`; only for a changed catalog department), `kind` and `location` (right after `from_catalog`; only for `own`: `agent` or `skill`, and where it lives in double quotes), `display_name`, `model` (omitted for `own`: its own file decides), `workers: same` (right after `model`; only for a "top model, workers included" department, omitted for the others), `connectors: []` (every department starts with none) |
| `{{GATES_FREE}}` `{{GATES_NOTICE}}` `{{GATES_OK}}` | Final action ids of that tier as an inline YAML list: `[a, b, c]` (`[]` if the tier is empty). Each action id is in exactly one tier |
| `{{VISION_WHAT}}` | Answer A to question 3, verbatim as confirmed in the summary. May be multi-line: a list stays a markdown list, one `- ` item per line; a single sentence stays one line |
| `{{VISION_WHY}}` | Answer B to question 3, verbatim as confirmed in the summary. May be multi-line: a list stays a markdown list, one `- ` item per line; a single sentence stays one line |
| `{{STAGE}}` | The stage picked in question 3, for example `building` |
| `{{POLICY_YAML}}` | Company level, purpose product, startup or company only. `null` when there is no holding policy. Otherwise the value starts with a newline and is a mapping indented two spaces under `policy:` with keys `repo`, `local`, `pin` (question 9) |
| `{{POLICIES_REPO_YAML}}` | Holding: the value starts with a newline and is a mapping indented two spaces under `policies_repo:` with keys `local` (absolute path, question 10) and `remote` (the URL, or `""` when none). Otherwise `null` |
| `{{CEILING_COS}}` | Holding only, rendered into the policies repo `policy.yaml`. Most capable model a company CoS may use. Proposed: the holding's own CoS model (`{{MODEL_COS}}`). Show it in the summary; the CEO confirms or changes it; it must be a name from `models.tiers` |
| `{{CEILING_DEPARTMENTS}}` | Holding only, same file. Most capable model a company department may use. Proposed: the holding's own department model (`{{MODEL_DEPARTMENTS}}`). Show it in the summary; the CEO confirms or changes it; it must be a name from `models.tiers` |
| `{{CEILING_WORKERS}}` | Holding only, same file. Most capable model a company worker may use. Proposed: the tier one below `{{CEILING_DEPARTMENTS}}` (the same if it is the last). A name from `models.tiers`, never `one-down` |
| `{{SETUP_QUESTION_COUNT}}` | Number of question groups asked (questions 1 to 10). A holding skips question 9, which stays in the table as a row marked not applicable and is not counted. Custom department follow-ups belong to question 5 and do not add groups. A personal hq skips question 9 the same way. Counted by groups that apply to the level and purpose, also in non-interactive mode. Holding: 9. Personal: 9. Company: 10 (purposes job, product, startup and company; a job hq answers question 9 as employer rules) |
| `{{SETUP_DEPARTMENTS}}` | Cell text for `decisions/0001-setup.md`: `id (model)` for each department, comma-separated, or `none`. A custom department with `Bash`: `id (model, runs commands)`. A "top model, workers included" department: `id (model, workers on <model>)`. Both: `id (model, runs commands, workers on <model>)`. A changed catalog department adds `changed` (for example `engineering (opus, changed)`). A brought-in one: `id (own agent <name>)` or `id (own skill <name>)`, plus `, replaces <id>` when it replaces a catalog entry |
| `{{SETUP_PERSONAS}}` | Starts with `CoS: <cos display name>`, then `id: display name (agent <agent>)` for each department whose display name differs from the role name, then `CEO: <name>` if given |
| `{{SETUP_GATES}}` | `framework table` or `framework table with changes: <action> <from> -> <to>; ...` |
| `{{SETUP_SERVICES}}` | Services read in the step after question 1, by plain name, comma-separated (for example `chat, docs`), or `none` (also when the CEO said no or did not answer). Names only: no channel, repo or other fact |
| `{{SETUP_REPOS}}` | Cell text for `decisions/0001-setup.md`: `hq remote: <url or none>`; for a holding append `; policies repo: <path>, remote: <url or none>`; for a job hq append `, hosted on: <the CEO's answer: personal account, employer account, or not decided>`; at company level, except for a personal hq, append `; product repos: <slug (role, visibility), ...; or none>; issues home: <slug or none>; tracker: <owner> project <number> or none`; at every level append `; attribution: <one of: Claude Code default, custom, none, deferred (<ORG_ID>-A<n>)>`. Each repo is shown as `slug (role, visibility, protected)` or `slug (role, visibility, not protected)`; a planned repo adds `, planned`. The hq is always `not protected`. A deferred answer is written inside its part as `deferred (<ORG_ID>-A<n>)` |
| `{{REPOS_YAML}}` | `org.yaml` `repos:` value (question 10). `[]` for none and always for a holding and a personal hq. Otherwise the value starts with a newline and is a block list indented two spaces under `repos:`; each item has `slug` (`owner/name`), `role`, `visibility` (`public` or `private`), `issues_home` (`true` for exactly one item, `false` for the others), `protected` (`true` or `false` from the answer; always `false` for the hq) and, only for a planned repo, `planned: true` as the last key (omit the key for existing repos). No local paths |
| `{{TRACKER_YAML}}` | `org.yaml` `tracker:` value (question 10). `none` for none and always for a holding and a personal hq. Otherwise the value starts with a newline and is a mapping indented two spaces under `tracker:` with `kind: github-project`, `owner` (login), `number` (integer) and `status_field` (in double quotes) |
| `{{SETUP_POLICY}}` | `none` for a company without policy, `not applicable (holding)` for a holding, `not applicable (personal)` for a personal hq, `not applicable (job); employer rules: <pointer or none>` for a job hq, otherwise `<repo> @ <short pin> (check: OK)` or `<repo> @ <short pin> (check: N loosening(s) kept)` |
| `{{ADVISORY_DEPARTMENTS}}` | The advisory catalog ids as prose, used where `CLAUDE.md` and the department templates name the advisory departments. Personal: `health, money, paperwork, legal, finance, tax`. Any other purpose: `legal, finance, tax` |

Table cell values (`SETUP_*`) must not contain `|` or newlines.

### Per department (`catalog/<id>/*` and `templates/department/*`)

| Placeholder | Value |
|---|---|
| `{{DEPT_ID}}` | Department id (kebab-case) |
| `{{AGENT_NAME}}` | The department's agent name (question 6): the persona in lowercase kebab-case, or the department id when the display name is the role name. Used for `name:` in the agent file, the agent file name and `Agent file:` in a custom charter |
| `{{DISPLAY_NAME}}` | Display name (question 6). The agent intro renders as "You are {{DISPLAY_NAME}}, the {{ROLE_NAME}} department of {{ORG_NAME}}." If the display name equals the role name it reads "You are Business, the Business department of Acme."; this repetition is accepted, keep it |
| `{{ROLE_NAME}}` | The department's role name, for example "Customer Support" (the catalog role or the custom role from question 5). Always the role name, even when a persona name is chosen as the display name |
| `{{ORG_NAME}}`, `{{ORG_ID}}`, `{{ADVISORY_DEPARTMENTS}}` | As above |
| `{{OTHER_ACCOUNTS_EXAMPLE}}` | Purpose not job: `for example an employer's`. Purpose job: `for example the CEO's personal accounts; the employer's accounts used for this job are this org's accounts` |
| `{{MODEL}}` | The department's model tier |
| `{{WORKER_MODEL}}` | The tier one below `{{MODEL}}` in `models.tiers` (the same tier if it is already the last). For a department with `workers: same`, equal to `{{MODEL}}` |
| `{{WORKER_TIER}}` | `one tier down` normally; `on your own tier (top model, workers included)` for a department with `workers: same`. Used in catalog and custom agent files, in sentences like "workers that run {{WORKER_TIER}} at `{{WORKER_MODEL}}`" |
| `{{DEPT_SCOPE}}` | Custom departments only. The scope items as markdown bullet lines, each starting with `- `, one per line, each kept as given (multi-line value) |
| `{{DEPT_TRIGGERS}}` | Custom and brought-in departments only. The triggers as bullet lines, each starting with `- ` |
| `{{DEPT_EXCLUSIONS}}` | Custom and brought-in departments only. The exclusions as bullet lines, each `- <thing> (owner: <department or CEO>)`. If the CEO gave no owner, ask which department or the CEO owns it |
| `{{DEPT_TOOLS}}` | Custom departments only. The `tools:` value of the agent file: `Read, Grep, Glob, Edit, Write, Agent(reader)` when the CEO answered no to the commands question; `Read, Grep, Glob, Edit, Write, Bash, Agent(reader)` when yes |
| `{{DEPT_COMMANDS}}` | Custom departments only. One single-line sentence for the agent body. No: `You do not run commands (you have no \`Bash\` tool).` Yes: `You may run commands (scripts, command-line tools, git) for: <the CEO's reason>. Never commit to or push the hq main branch.` The reason is kept as given and the sentence ends with a period |
| `{{DEPT_CORE_JOB}}` | Custom and brought-in departments only. The single core job: one single-line sentence ending with a period, containing no `: ` |
| `{{DEPT_TRIGGERS_LINE}}` | Custom departments only. The trigger items on one line, as a comma-separated list of noun phrases, derived from the same bullets as `{{DEPT_TRIGGERS}}` (no extra question). It must read after "Use for " (so turn a situation into a noun phrase: "a customer email arrives" becomes "incoming customer emails"), for example `incoming customer emails, refund requests`. No `: `, no trailing period. Used in the one-line YAML `description:` of the agent file |
| `{{FROM_CATALOG}}` | Changed catalog departments only (`changes.md`). The catalog id, for example `engineering` |
| `{{ADAPT_SCOPE_ADDED}}` | Changed catalog departments only. One `- ` bullet per item to cover, kept as given, or `- none` |
| `{{ADAPT_SCOPE_REMOVED}}` | Changed catalog departments only. One bullet per item dropped, `- <item> (owner: <department or CEO>)`, or `- none`. If the CEO gave no owner, ask which department or the CEO covers it |
| `{{ADAPT_EXCLUSIONS_ADDED}}` | Changed catalog departments only. One bullet per new exclusion, `- <thing> (owner: <department or CEO>)`, or `- none` |
| `{{ADAPT_TOOLS}}` | Changed catalog departments only. One bullet per ability added or dropped, `- added <tool>: <the CEO's reason>` or `- dropped <tool>`, or `- none`. When `Bash` is added, its bullet reads `- added Bash: <reason>. Never commit to or push the hq main branch.` |
| `{{OWN_KIND}}` | Brought-in departments only (`own-charter.md`). `agent` or `skill` |
| `{{OWN_LOCATION}}` | Brought-in departments only. Where it lives, as the CEO said it (a path, "the CEO's own agents", or "plugin <name>"), single line |
| `{{DEPT_EXCLUSIONS_LINE}}` | Custom departments only. The exclusion items on one line, same format as `{{DEPT_TRIGGERS_LINE}}` (noun phrases that read after "Not for ", for example `legal advice, payments`), derived from the same bullets as `{{DEPT_EXCLUSIONS}}` without the `(owner: ...)` parts. No `: `, no trailing period |

### Conditional markers

Two comment styles exist, handle both. Markdown files (`.md`) use `<!-- IF x -->` ... `<!-- END IF -->`. YAML files (`org.yaml`) and `gitignore` use `# IF x` ... `# END IF`. Each marker sits on its own line; blocks are not nested. In `org.yaml` four blocks exist: `# IF portfolio-company` holds `policy: {{POLICY_YAML}}`, `policies_repo: null` and `employer_rules: null`; `# IF job` holds `policy: null`, `policies_repo: null` and `employer_rules: {{EMPLOYER_RULES}}`; `# IF personal` holds `policy: null`, `policies_repo: null` and `employer_rules: null`; `# IF holding` holds `policy: null`, `policies_repo: {{POLICIES_REPO_YAML}}` and `employer_rules: null`. Exactly one of the four blocks survives. Keep the content when the condition is true, drop the whole block when it is false, and always delete the marker lines.

| Condition | True when |
|---|---|
| `holding` | level is holding |
| `job` | purpose is job |
| `not-job` | purpose is not job |
| `personal` | purpose is personal |
| `not-personal` | purpose is not personal |
| `product-repos` | level is company and purpose is not personal (the hq may list product repos and a roadmap tracker) |
| `portfolio-company` | level is company and purpose is product, startup or company (a company that a holding may register and govern) |
| `policy` | level is company, purpose is product, startup or company, and a holding policy source was given |
| `departments` | at least one department was chosen |
| `no-departments` | no department was chosen |

### Holding-only files

`portfolio.yaml` is skipped entirely for a company: do not create it. For a holding, create it; it stays `orgs: []`. The holding hq has no `policies/` directory: its policies live in the separate policies repo (generation step 10).

## Post-generation checks

Run them and fix what fails; report the results:
- `grep -rnE '\{\{|<!-- (IF|END IF)|# (IF|END IF)|<[A-Z]|[^(]\.\.\.|^\.\.\.' . --exclude-dir=.git` finds nothing (the pattern skips `Agent(...)`, which is standard text in `CLAUDE.md`), in the hq and, for a holding, in the policies repo directory. Check every hit. A hit is a leftover and must be fixed, unless it is legitimate text the CEO wrote (for example an ellipsis inside a quoted answer); then list it in the report as excluded and why.
- `org.yaml` is consistent with `${CLAUDE_PLUGIN_ROOT}/schemas/org.yaml`: purpose and level agree (holding requires purpose company; job, product, startup and personal require level company), a job or personal hq has `policy: null`, a personal hq has `repos: []` and `tracker: none`, and `employer_rules` is non-null only for a job hq. `repos` is `[]` or a list where exactly one item has `issues_home: true` and no item holds a path; every item has `protected: true` or `protected: false`, and the item with role `hq` has `protected: false`; `planned` is either absent or `true`, and each planned repo has exactly one A item in `company/state.md` with its `gh repo create` command; every deferred answer has exactly one A item and its `deferred (<ORG_ID>-A<n>)` cell mark; `tracker` is `none` or a `github-project` mapping with an integer `number`; a holding has `repos: []` and `tracker: none`.
- For purpose job: `grep -rn "for example an employer's" CLAUDE.md .claude/agents` finds nothing. For purpose not job: `grep -rn "used for this job" CLAUDE.md .claude/agents` finds nothing.
- `org.yaml` parses. Try PyYAML first: `python3 -c "import yaml,sys; yaml.safe_load(open('org.yaml'))"`. If that fails (no python3 or no `yaml` module), use Ruby's YAML, present on stock macOS: `ruby -ryaml -e 'YAML.load_file(ARGV[0])' org.yaml`. If both fail, check it carefully by reading. The final report says which validator was used, or that YAML was checked by reading only.
- Every expected `.claude/agents/<agent>.md` exists (one per department in `org.yaml`, except `from_catalog: own`, which has none), plus `.claude/agents/reader.md` and `.claude/agents/worker.md`. If any is missing, stop and tell the CEO clearly, listing the missing files and the likely cause (`.claude/` write permission, see Generation); never report success with missing agent files.
- Mandatory, never skipped: compare `company/state.md` against `${CLAUDE_PLUGIN_ROOT}/schemas/state.md` item by item: frontmatter keys and values, the 5 H2 headings in exact order, the line formats, and `- none` in every empty section. List the result of each item in the final report. A skipped or partial check is reported as a failure, not as done.
- Advisory department agent files (legal, finance, tax, health, money, paperwork, from the catalog) have no `Agent` and no `Bash` in `tools:`.
- Catalog entries `health`, `money` and `paperwork` appear only in a personal hq.
- `.claude/agents/reader.md` and `worker.md` have `model:` equal to `{{MODEL_WORKERS}}` as rendered.
- Every `.claude/agents/*.md` has an explicit `tools:` list in its frontmatter, and its `name` equals its file name (for a department, also `departments[].agent` in `org.yaml`). The frontmatter of each parses as YAML (a `: ` inside an unquoted `description:` breaks it), with the same validator order: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" <file>`, else `ruby -ryaml -e 'YAML.load(File.read(ARGV[0]).split("---")[1])' <file>`, else by reading. If that fails for a custom department, fix the rendered value, never leave it.
- A custom department's agent file lists `Bash` in `tools:` if and only if the CEO answered yes to the commands question.
- For a department with `workers: same`: its `model` is the first tier in `models.tiers`, and its agent file names that tier as its workers' model.
- If `.claude/settings.json` exists, it parses as JSON: `python3 -c "import json,sys; json.load(open('.claude/settings.json'))"`; if python3 fails, `ruby -rjson -e 'JSON.parse(File.read(ARGV[0]))' .claude/settings.json`; say which one was used, or that it was checked by reading only. It keeps `enabledPlugins` if it had it, and its `attribution` matches the answer (absent for answer a and for deferred).
- Agent names are unique, match `^[a-z][a-z0-9-]*$` (a brought-in one: any name without spaces), and none equals another department's id, `reader` or `worker`.
- A changed catalog department has `adapted: true` in `org.yaml`, a "Changes for this org" section at the end of both its charter and its agent file, and a `tools:` line equal to the catalog one plus the abilities added and minus the ones dropped; an advisory one still has no `Agent` and no `Bash`.
- A brought-in department has `from_catalog: own`, `kind`, `location`, no `model`, a charter rendered from `own-charter.md`, and no file in `.claude/agents/`; the setup wrote nothing outside the hq for it.
- Every `Agent(...)` entry in the `tools:` of any agent file names an existing `.claude/agents/<name>.md`.
- The files in `departments/` match the departments in `org.yaml`, and the display names appear in `CLAUDE.md`.
- No department has a connector: every department in `org.yaml` has `connectors: []`, no `.claude/agents/*.md` lists an `mcp__` tool, and `accounts.forbidden_connectors` is `[]`. This holds also when services were read after question 1.
- Every line a charter got from the services step ends with `confirmed at setup` and was confirmed in the summary; the setup record names the services read, or `none`.
- `company/vision.md` and `company/strategy.md` exist and hold the confirmed answers to question 3.
- `.gitignore` lists `accounts.local.yaml` and `.claude/settings.local.json`, and neither file exists in the hq (the wizard writes neither). For a personal hq it also lists `private/`; for any other purpose it does not.
- `.ignore` exists and lists `archive/`, `archive/README.md` exists, and `.gitignore` does not list `archive/`.
- `initiatives/README.md` exists, and every department in `org.yaml` has `departments/<id>/README.md` next to its charter.
- `CLAUDE.md` is within its budget in `${CLAUDE_PLUGIN_ROOT}/schemas/boot-set.md` (check with `ls -l CLAUDE.md`); if it is over, say so in the report.

## Git

If there is no `.git`, run `git init --quiet`. If the CEO gave an hq remote, run `git remote add origin <url>`. Show `git status --short`. Ask the CEO before the first commit. If approved, run `git add -A`, then commit everything with `git commit -m` and the message `chore: initialize <org name> hq with ceo-of-agents <framework version>` (for example `ceo-of-agents 0.12.0`) and the attribution lines required by the session. Never push. Tell the CEO how to push on their own (and how to add a remote if none was given). For a holding, say the same for the policies repo. <!-- x-release-please-version -->

## End

Tell the CEO in chat language: what was generated (file count, departments, the generic `reader` and `worker` agents and their model), any open A items (name the deferred answers and the planned repos to create), the policies repo path (holding), that the CoS skips pull and push while there is no hq remote, that departments start with no connectors (the CEO asks the CoS when one needs a connector), for a personal hq that personal data goes only in `private/` (git-ignored, on this computer only; copy it yourself to use it on another computer), that, if product repos other than the hq were given, they go next to the hq folder, never inside it, and the CoS asks at the first session where they are cloned on this computer (and asks again on any other computer or fresh clone), that the CEO can open a department directly with `claude --agent <agent>`, using its agent name (for example `claude --agent mike`), and how to start: open Claude Code in this directory and say what is on their mind; the CoS (from `CLAUDE.md`) takes it from there. Give three or four plain-language examples, such as describing an idea, "decide X", "brief", and with departments "pass to <department>: <text>". Do not list the CoS procedures (`session-start`, `intake`, `record-decision`, `weekly-brief`, `hq-version`, `departments`, `product-repos`, `initiatives`, `portfolio-brief`) as commands: they are hidden from the `/` menu and the CoS invokes them on its own. `/ceo-of-agents:init-fleet` is the only command the CEO types.
