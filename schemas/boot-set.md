# Schema: the boot set and its budget

The boot set is what the chief of staff (CoS) reads at every session start, before any work. Every byte of it is paid in every session, so it has a budget. Everything else in the hq (analyses, notes, decision records, briefs) is read on demand and costs nothing until it is needed.

## Files and budgets

Sizes in KB of 1024 bytes, measured with `wc -c`. A missing file counts as 0.

| File | Budget | What keeps it small |
|---|---|---|
| `CLAUDE.md` | 24 KB | Identity, gates, house rules and the map only; procedures live in plugin skills loaded on demand. A fresh render is 15 to 21 KB, depending on purpose, departments and repos |
| `org.yaml` | 6 KB | Facts only; no prose |
| `company/vision.md` | 4 KB | Stable; changes only through a decision record |
| `company/strategy.md` | 4 KB | The stage and a short current focus |
| `company/state.md` | 8 KB | One line per item, each under 300 characters; details in a linked note |
| `company/decision-queue.md` | 10 KB | Open cards only; answered cards leave with `record-decision` |
| `accounts.local.yaml` | 2 KB | Clone paths only |
| Whole boot set | 40 KB | The sum of the files above |

`inbox/` is listed at session start, not read; its notes are read by the `intake` skill and deleted once processed.

## Line budget

Every line of `company/state.md` is under 300 characters, frontmatter included. An item that needs more keeps its one line (what, status, date) and links a note (for example `departments/<id>/YYYY-MM-DD-<slug>.md`) for the detail.

## Check

The `session-start` skill measures the files with `wc -c` and finds long lines in `company/state.md` with the pattern `^.{301,}`. When something is over budget it adds one line to the status that names each offending file with its size and budget, and quotes at most three long lines by their first words. It proposes moving the detail to linked notes and does it only when the CEO agrees. It adds no A item and never trims on its own.

The budgets are guidance for the CoS, not limits enforced by a tool: an hq may be over budget for a while, and the status line says so until it is not.
