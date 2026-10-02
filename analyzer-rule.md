# Analyzer Rule

**What this file is.** The rules for analysing a job that arrives from the **search** feed. The
machinery around it — when it fires, where the result goes — is workflow and lives in `CLAUDE.md`.
This file holds only the judgement: what to look at, and what to conclude.

---

## When it runs

**Automatically, the moment a job arrives with `source: search`.** Nothing else triggers it. Jobs
from the `upwork` and `vollna` alerts are not analysed, and nothing about writing a proposal is
involved: the analysis happens before anyone decides whether to bid.

The job is flagged `analysis_wanted` on arrival and appears in `/api/queue/analyzing`. The
analysis is posted back to `/api/queue/<seq>/analysis` and shows on the queue card.

## What the feed already tells you

Each search job arrives carrying the producer's own verdict, so start from it rather than
repeating it:

- `decision` — `bid`, `skip`, or `manual check`
- `reason` — the rule that produced it, e.g. "spent $323136 (>= $100K) and pays $75.61/hr (>= $20)"
- `clientName` — sometimes, with a mention count
- the full job description, title and Upwork link

The producer decides on client spend and hourly rate alone. Everything it cannot see is what the
analysis is for.

---

## What to analyse

> **Not written yet.** Describe here what the analysis should look at and what it should
> conclude. Until this section is filled in, the analyzer has no rules to follow and should say so
> rather than inventing criteria.

## What to produce

Keep it short enough to read on a queue card without opening anything. Lead with the conclusion,
then the reasoning that is not already in the feed's own `reason` line.
