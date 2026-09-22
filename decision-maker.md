# Decision Maker

**What this file is.** The prompt for reading the client out of a job description, before any
drafting. It is the analysis half of the work, kept apart from the guides so every guide can use
the same read.

Taken from Phase 1 of `guides/brainstormed.md` on 2026-09-21, where it was the first half of that
guide. Both copies exist today; if they ever disagree, this file is the one to fix.

---

# Read the client out of the job description

Work these nine points out before writing a word. **Use them as reference, never state them as
labels in the proposal.**

> **Two kinds of point here, and they have different rules.**
>
> **Points 1, 2, 4 and 9 are judgement.** Read between the lines. Tone, structure, word choice,
> what they bothered to explain and what they assumed you'd know. Inferring a client's personality
> from how they write is the entire value of this phase, and waiting for proof of it would leave
> you with nothing. Commit to a read.
>
> **Points 3, 5, 6, 7 and 8 are evidence only. Do not generate what the text does not support.**
> These are claims about the person's actual situation, what they hold, what they asked and what
> they will pay. Invent one and the proposal answers a client who isn't there: you thank them for
> research they never mentioned, or quote against a budget they never named. If the post doesn't
> support it, write "unknown" and move on. Quote the line behind each conclusion, at least to
> yourself.

**1. What kind of client is this?** *(judgement)*

*Personality, read from how they write:*
- Aggressive, or measured
- Direct, or circling
- Collaborative and committed, or hands-off and delegating everything to the freelancer
- Careful and risk-averse, or relaxed
- How transparent: do they volunteer budget, constraints, prior failures, internal politics?

*Technical awareness:* do they name technologies precisely, vaguely, or not at all? Do they say
outright that they are not technical? Do they use a term slightly wrong, which tells you more than
either extreme?

**2. Was the job description written by AI or by hand?** *(judgement)*

Handwritten posts have typos, uneven bullets, first-person asides, signed names, and specific
detail nobody would invent. AI-written posts are evenly structured, complete, generically worded,
and often longer than the job warrants. A handwritten post means a person is reading proposals, so
write to a person. An AI-written post often means volume screening, so front-load the match.

**3. What is this client confident about, interested in, proud of, suffering from, and willing to
do next?** *(evidence only)*

This is the highest-value point in the whole phase. Examples of the shape:
- Josh was **proud** of years of his own research and ideas, and **willing** to keep going for
  several more tasks after this one.
- The vet PMS client was **suffering** from an undocumented platform, and **confident** in their
  backend lead, which is why they fenced the integration layer off.

What someone is proud of is what you should acknowledge. What they are suffering from is what you
should solve. What they are willing to do next is what you should aim the close at.

**4. What is the key point of the project, the thing they most want implemented?** *(judgement)*

The single item where success or failure is decided. Usually it is the thing they wrote most
carefully, or repeated, or added a qualifier to. This becomes paragraph 2 of the proposal.

**5. What can they provide?** *(evidence only)*

Data, sample files, prior findings, access, a domain expert, a point of contact, an existing
codebase. If they offered something, using it is free goodwill and most bidders will ignore it.

**6. What kind of person are they looking for?** *(evidence only)*

Contractor, partner, specialist, team lead, bench resource, someone to think for them, someone to
execute a settled plan. Match the register to this.

**7. What questions do they ask?** *(evidence only)*

List every question and every instruction to include something. Missing one is usually fatal, and
some posts plant an instruction deliberately to test attention.

**8. What time and budget do they estimate?** *(evidence only)*

Their number, their range, their silence. Note whether they anchored, admitted they don't know, or
said they are benchmarking against other bids.

**9. Anything else specific to this job.** *(judgement)*

Compliance, a named deadline, a rejection list, an ownership demand, a mandatory video, a
non-negotiable stack. Whatever is unusual about this post and no other.

---

# Then pick the guide

The read above decides which guide writes the letter. **The guide is chosen here, not taken from
the dropdown.** Whatever the UI was set to is a default, and this decision overrides it.

The test is the one thing the whole workspace is built around: is this post concrete enough that a
genuinely similar project can be found on GitHub?

| The post | The guide |
| --- | --- |
| Concrete enough to find similar work on GitHub, and the search actually returned repositories | `github-friendly` |
| Anything else | `article-based` |

**Decide it on the outcome, not the hope.** The question is settled by the time the github gate
releases: repositories came back, or they did not. A post that looked searchable but returned
nothing goes to `article-based` like any other, because `github-friendly` opens on repository
links and has nothing to open with.

**Record the choice** so the UI and the archived copy show the guide that actually wrote the
letter:

```
curl -s -X POST localhost:8765/api/job/<id>/guide -d '{"guide":"github-friendly"}'
```

**Say which one you picked and why, in one line**, when you report the job. A silent switch away
from what the user selected in the dropdown is the kind of thing that should never be a surprise.

**Only decide when the job says you may.** Every job carries `guide_mode`. **`manual` means the
person picked the guide themselves and this whole section is skipped**: write with what they
chose. The server enforces it and will reject a guide change on a manual job. `auto` is where the
table above applies.
