# Schema: decision record (`decisions/NNNN-<slug>.md`)

A decision record captures one answered decision. Records are immutable once written.

## Filename and numbering

`decisions/NNNN-<kebab-slug>.md`, where NNNN is four digits. Next number = highest existing + 1. The record number (NNNN) is separate from the card code (`ACME-D3`); the card is referenced in the `Card` line.

## Format (exact)

```
# NNNN. <Title>
- Date: YYYY-MM-DD
- Status: accepted            # accepted | superseded by NNNN | amended by NNNN
- Card: ACME-D3               # or: none
- Decided by: <ceo role id>
## Context
## Options
## Decision
## Consequences
## Links
```

## Field rules

- `Status` values: `accepted`, `superseded by NNNN`, `amended by NNNN`.
- `Card`: the D code of the card this record answers, or `none` (for example the setup record 0001).
- `Decided by`: the CEO role id from org.yaml (`ceo.role_id`).
- Options: lettered `(a)`, `(b)`, ... or bullets. Decision starts by naming the chosen option, then bullets. Keep each section short.

## Immutability

Never rewrite history. To change a decision, write a new record and update ONLY the `Status` line of the old record to `superseded by NNNN` or `amended by NNNN`. Nothing else in an old record may change. `decisions/README.md` is the index.

## Index: decisions/README.md

A table with exactly these columns:

```
| # | Decision | Date | Status |
|---|---|---|---|
| [0001](0001-setup.md) | Setup | 2026-01-15 | accepted |
```

The index Status mirrors the record's Status line.

## Minimal valid example

```markdown
# 0002. Flat monthly price for the beta
- Date: 2026-01-16
- Status: accepted
- Card: ACME-D3
- Decided by: ceo

## Context
The beta has no pricing; usage-based pricing was proposed by business.

## Options
- (a) Usage-based pricing from launch
- (b) Flat monthly price, revisit after 3 months

## Decision
(b). Flat monthly price; review after 3 months of data.

## Consequences
- Finance models revenue as testers x flat price.
- State.md Key numbers gets a pricing line once set.

## Links
- company/decision-queue.md (card removed in the same commit)
```

## Validation checklist

- Filename is four digits plus kebab slug; the number is unique and equals the number in the title.
- Header bullets present in order: Date, Status, Card, Decided by.
- The five H2 headings exist, in order.
- `Status` is one of the three allowed forms; a `superseded by` or `amended by` target record exists.
- `Card` code, when not `none`, no longer appears in decision-queue.md or state.md.
- A row exists in decisions/README.md with the same number, date and status.
- If the record is older than the current commit, only its Status line differs from its first committed version.
