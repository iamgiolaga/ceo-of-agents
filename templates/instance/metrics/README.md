# Metrics

Rule: never invent a number. Every number carries its source and the date it was read. If a value is unknown, write `unknown (no source yet)`.

## Definitions

| Metric | Definition | Source | How to read | Last checked |
|---|---|---|---|---|
| _none yet_ | | | | |

Columns:
- **Metric**: the name used everywhere else (state, briefs).
- **Definition**: what exactly is counted, over which period.
- **Source**: where the value is read from (a dashboard, an export, an API), precise enough for someone else to reproduce it.
- **How to read**: meaning and caveats (for example "proxy for usage", "cumulative, not activity").
- **Last checked**: date the value was last read (YYYY-MM-DD).

## Notes

- Add source caveats here (broken collector, preferred alternative).
- A stale number is shown with its last known value and date, never refreshed by guessing.
