# Analyzer Rule

**What this file is.** The rules for analysing a job that arrives from the **search** feed. The
machinery around it — when it fires, where the result goes — is workflow and lives in `CLAUDE.md`.
This file holds only the judgement: what to look at, and what to conclude.

---

## When it runs

**Automatically, the moment a job arrives with `source: search`.** Nothing else triggers it. Jobs
from the `upwork` and `vollna` alerts are not analysed, and nothing about writing a proposal is
involved: the analysis happens before anyone decides whether to bid.

**The whole of this file applies to the general vollna search and to nothing else.** That means the
analysis, the stack marks, the Telegram message, **and the power to drop a job instead of writing
it.** A row qualifies when its body carries `type: job-decision` or a `source` of
`general-vollna-search`, `vollna-search` or `job-decision`; the server normalises those to
`source: search` and flags the row, and a job created from such a row now carries the `source`
forward so the distinction survives.

**A job from any other feed is not acted on at all, in either direction.** It is neither triaged
nor written. An alert row reaches the queue because the server keeps every message on the `jobs`
channel as a row, so its presence means a message arrived rather than that anybody chose it.
**Leave it queued and say what landed.** A person asking for it is what starts the work.

**The one exception is something that is not a job post at all**, such as a notification email
pasted in by mistake. There is no client and nothing to answer, so say that plainly and post it as
a drop whatever the feed. That is not a stack judgement; it is the absence of a job.

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

Three things, in this order. The first decides whether the job survives at all.

### 1. The stack, and whether one of our engineers can do it

Read the job description and work out what building it would actually take. Then mark the job with
every role that genuinely applies:

| Mark | The job is really asking for |
| --- | --- |
| `Data` | pipelines, ETL, warehouses, SQL, dashboards, reporting, data quality, migrations |
| `AI` | LLM and agent work, RAG, prompt engineering, model APIs, AI features in a product |
| `ML` | training or evaluating models, statistics, forecasting, classification, computer vision |
| `Full` | web and mobile applications, APIs, frontend, backend, integrations, infrastructure |
| `Crypto` | cryptocurrency and blockchain: exchanges, wallets and custody, on-chain integrations, smart contracts, tokens, DeFi, web3 |

**A job can carry several marks, and most interesting ones do.** A Snowflake migration with an
LLM layer on top is `Data` and `AI`. A React dashboard over a warehouse is `Full` and `Data`. A
crypto exchange with an order book and a Node backend is `Crypto` and `Full`. Mark what the work
needs, not what the post's title claims.

**`Crypto` goes on anything touching cryptocurrency or a blockchain**, and it goes on *alongside*
the other marks rather than instead of them: the backend of an exchange is still `Full`, and an
on-chain analytics pipeline is still `Data`. The mark records that the domain is crypto, which is
what decides the person.

**A dropped row is deleted, not hidden.** It leaves the queue the moment the analysis drops it,
on the user's instruction of 2026-10-13. Hiding it was the first attempt and left the directory
filling with rows nobody would read again.

**Two consequences, and they are the price of the drop being final.** A wrong call cannot be
reversed with a `redo`, because there is no row left to redo; the post has to arrive again. And the
written analysis goes with the file, so the reasoning for the drop is not kept. **Be sure before
marking a row dropped** — an empty stack is a deletion, not a label. **Clear all** beside Refresh
empties the rest of the queue in one action.

**If none of the five apply, drop it.** Design-only briefs, copywriting, virtual assistants,
sales and lead-generation roles, bookkeeping, video editing: there is no engineer here who can do
them, so the row is marked dropped and nothing further happens to it. No Telegram message is sent
for a dropped job.

Judge the work, not the vocabulary. A post that says "AI-powered" and means a Zapier webhook is
`Full`, not `AI`. A post that never says "machine learning" but asks for a forecast is `ML`.

### 2. Whose job it is, and the marks decide it

**The stack chooses the person. There is no judgement left in this step.** The rule, from the
user on 2026-10-13:

> **1. `Crypto` present is Zachary, whatever else is on the job.**
> **2. Otherwise `Data` present and `AI` absent is Zachary. Everything else is Connor.**

Crypto is Zachary's domain outright. Beyond that, data-led work is his, and the moment a job wants
AI it is Connor's:

| Stack marks | Person |
| --- | --- |
| anything with `Crypto` on it | **Zachary** |
| `Data` | **Zachary** |
| `Data` + `ML` | **Zachary** |
| `Data` + `Full` | **Zachary** |
| `Data` + `ML` + `Full` | **Zachary** |
| **everything else, including any set with `AI` and no `Crypto`** | **Connor** |

**`Data` + `AI` is Connor, not Zachary** — the `AI` mark decides it, however much data work the
job also wants. **But `Crypto` + `AI` is Zachary**, because rule 1 is checked first and was given
with no exception attached to it.

**No marks means no person**, because a row with no marks is dropped and a dropped row is never
written.

**The server applies this for you.** `person_for_stack()` resolves the marks and the analysis
endpoint records the answer on the row, so a job created from that row starts as the right person
without the decision being made twice:

```
curl -s -X POST localhost:8765/api/queue/<seq>/analysis \
  -d '{"analysis":"...","stack":["Data","ML"]}'      # row.person becomes "Zachary"
```

**In `person_mode: auto` the row's person wins over the dropdown**, which was only ever a default.
In `manual` the user's pick stands and this rule does not apply — they chose, and the server
refuses to change it. This also means **the person table in `decision-maker.md` does not run for
an analysed search row**: the marks have already answered it. That table is for a job with no
analysis behind it, such as a hand-pasted post.

### 3. The client's name, from the feedback they have been left

The work-history section carries reviews written **to the client** by freelancers who worked for
them, and those reviews routinely name the person: *"It was a great working experience with
Chris"*, *"Really nice to work with Mr. Cooper"*, *"Thanks, Chris."*

Read every `to client` line, collect the names, and take the one that recurs. Put it in the row's
client name field so the greeting can use it. Where the reviews are all `(no text)` or say only
"Great client", leave it empty rather than guessing: a proposal addressed to the wrong person is
worse than one addressed to nobody.

### 4. Then send it to Telegram, to the jobs bot

For every job that survived step 1, send one message carrying the **title**, the **URL**, the
producer's **decision**, the **tech stack** marks, **the person those marks chose**, the **client's
name** where step 3 found one, and the **job description**. That is the message the phone is for:
enough to judge a job away from the desk.

**Nothing is sent before this point, and a row merely waiting to be analysed sends nothing at
all.** The analysis is what produces the three things a notification is for — dropped or not,
whose job it is, and who the client is — so there is nothing to say until it exists. An alarm for
an unanalysed row was tried on 2026-10-13 and removed the same day for exactly that reason.

**It goes to its own bot.** Job info is sent with `TELEGRAM_JOBS_BOT_TOKEN` and
`TELEGRAM_JOBS_CHAT_ID` from `.env`, which is the *Hungry* bot. The other token,
`TELEGRAM_BOT_TOKEN`, belongs to a different bot and carries only the finished-proposal and
boost-due alarms. Two bots so the phone tells a job worth reading from a proposal worth sending
without either being opened. Never send job info on the proposal bot.

**Cut the work history out of the description first.** The feed appends it to the end of the
description text, so sending the description raw sends fifty contracts with it and buries the job
in the client's past. The message stops at the `Work history (N past contracts):` header. The
history belongs on the queue card, behind its button, where it can be read deliberately.

Nothing is sent for a dropped job.

### 5. If the decision is bid, write the proposal

A surviving job whose `decision` is `bid` goes straight into the proposal flow: claim it and
follow `CLAUDE.md` from the repository search onwards. The analysis is the gate, so once it is
passed there is nothing to wait for.

**Do not stop to ask, and do not report the analysis and wait.** Three conditions and the write
starts: the row is from the general vollna search, it was not dropped, and the decision is `bid`.
All three are known the moment the analysis is posted, so the proposal follows in the same breath.
**Working one job at a time means sequential, not a question between every step** — the
one-at-a-time rule is about never having two things in flight, not about pausing for permission.
This is written down because on 2026-10-13 seq 562 met all three conditions and the analysis was
reported back with a "which do you want?" instead of a proposal.

Concerns found during the analysis do not stop it either. They go in the note to the user
alongside the finished draft, the way every other assumption does.

`skip` and `manual check` stop here. They stay on the queue with their marks and their analysis,
and a person decides whether to spend a Connect.

### 6. A dropped job sends nothing, on either bot

**No job info on Hungry, and no proposal-done alarm on Night Fury.** The second half matters
because a dropped row still gets a `/result` posted to it — the UI needs something in the box, and
what goes there is the refusal and the reason. That is not a finished proposal, so no alarm goes
out for it: a phone buzzing "Proposal done" for work nobody can do is worse than silence, since it
pulls someone to the desk for nothing.

**Say so when posting the result,** which is what suppresses it:

```
curl -s -X POST localhost:8765/api/job/<id>/result \
  -d '{"proposal":"Not one to bid on. ...","dropped":true}'
```

The server also suppresses the alarm when the job's own queue row is marked dropped, but that link
only exists once a row has been pressed into a job. **Send the flag; do not rely on the fallback.**

## What to produce

**The card shows status only, not the reasoning.** It reads `analysing…` while the job is waiting
and `analysed` once it is done, and the conclusion is carried by the stack marks beside the title.
Printing the full analysis there made every search row several lines tall and buried both the
marks and the job itself.

So the written analysis is for the record and for Telegram rather than for the card. Lead with the
conclusion, then the reasoning that is not already in the feed's own `reason` line.
