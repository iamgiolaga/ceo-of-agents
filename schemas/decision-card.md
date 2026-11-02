# Schema: decision card (`company/decision-queue.md`)

A decision card is one pending question for the CEO. Every card has its own D code. Answered cards are removed from the queue by the record-decision skill and become decision records (see decision-record.md).

## File structure

```
# Decision queue
<one-line intro>

<one card per open decision, or the single line: _No open decisions._>
```

## Card format (exact)

```
## ACME-D3: <question>
- status: open
- since: YYYY-MM-DD
- urgency: high | normal | low
- proposed_by: <dept-id|cos>        # or: needs analysis by <dept-id>
- escalate: no                      # company only: no | holding
### Context
### Options
- (a) ...
- (b) ...
### Recommendation
```

## Field rules

| Field | Rule |
|---|---|
| Heading | `## <ORG_ID>-D<n>: <question>`; the code is unique and never reused |
| `status` | `open` (answered cards are removed, not marked) |
| `since` | `YYYY-MM-DD` |
| `urgency` | `high`, `normal` or `low` |
| `proposed_by` | a department id or `cos`; or replace the line with `- needs analysis by: <dept-id>` when nobody has proposed an option yet |
| `escalate` | `no` or `holding`; present for company orgs only (omit at holding level) |
| Context | enough that the CEO can decide without opening other files |
| Options | lettered `(a)`, `(b)`, ...; at least two |
| Recommendation | names who proposes it, or says `needs analysis by <dept-id>` |

Use either `proposed_by: <dept-id|cos>` or the line `- needs analysis by: <dept-id>`; never both.

## Minimal valid example

```markdown
# Decision queue
Open decisions for the CEO. Answer in chat; the CoS records the answer with record-decision.

## ACME-D3: Adopt usage-based pricing for the beta?
- status: open
- since: 2026-01-10
- urgency: normal
- proposed_by: business
- escalate: holding
### Context
The beta has 40 testers and no pricing. Usage-based pricing affects revenue forecasts across orgs.
### Options
- (a) Usage-based pricing from launch
- (b) Flat monthly price, revisit after 3 months
### Recommendation
(b), proposed by business: simpler to explain and to test.
```

## Validation checklist

- Heading code uses the org id and `D`, and matches a line in state.md "Open decisions" and "Waiting on the CEO".
- No two cards share a code; a code is never reused after the card is answered.
- All field lines present in the stated order; `status` is `open`.
- `urgency` is one of the three allowed values; `since` is a valid date.
- Exactly one of `proposed_by` or `needs analysis by` is given.
- Context, Options and Recommendation H3 headings exist, in order; Options has at least two lettered items.
- An empty queue is exactly `_No open decisions._`.
