# Brainstormed Guide

**Guide id:** `brainstormed`
**Use for:** any Upwork job where you want the proposal built from a read of the client, not just
a read of the requirements.

Two phases. First you brainstorm the client out of the job description. Then you write the
proposal from what you found. The person profile (`Mario.md`, `Zachary.md`, ...) supplies every
fact about us; this file supplies the method.

---

# Phase 1. Read the client out of the job description

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

# Phase 2. Write the proposal

Each numbered item is one paragraph, separated by a blank line.

**1. Attractive starter. No bold anywhere in it.**

- `Hi 👋` on its own line, or `Hi [name] 👋` when the post gives you a name. **Not bolded.**
- Then, immediately, the closest thing already built: "I've built ..." and the real project.
- Describe it in the client's terms, not ours. If they say listing tool, the sentence should
  contain their words, not our internal framing.
- Two or three sentences. This is proof, not a portfolio tour.

**2. The key point of their project. Bold the quoted phrase from the job description.**

Two or three sentences. No more.

- **Quote only the key part, not the whole sentence.** Find the few words that carry the point and
  bold those. A long quotation buries the thing you were pointing at.
- **Placement is optional.** It can open the paragraph, but it doesn't have to. Dropping it into
  the middle of your own sentence usually reads more naturally than leading with a quotation.
- **Show why that key point matters**, proved by something already built, not asserted. Brief
  approval is fine when the key point is genuinely a smart decision on their part, but skip the
  flattery and let the evidence carry it.
- **This is where Phase 1 point 3 gets used**: what they are proud of, suffering from, or willing
  to continue. One clause, not a sentence of its own.
  - **Write it as an announcement, never a request.** "Your findings and sample photos will
    shorten the first week" acknowledges what he's proud of and tells him it has value. "Send me
    your findings and sample photos" turns his contribution into a chore and spends the close on
    an ask that should have been the close's own.
  - The request, if one is needed at all, belongs in paragraph 8. Never in both.
- Cut anything that isn't the quote, the reason it matters, or the acknowledgement. Restating
  their brief back to them, explaining what you're about to explain, and telling them why you
  found the post interesting all belong on the floor.

**3. The solution, as our approach. A numbered list, never a block of prose. No bold anywhere in
this paragraph, including the word Approach.**

Lay it out exactly like this:

```
Approach
1. ...
2. ...
3. ...
```

- **Two to four steps**, depending on the size of the project. Three is usual. Four only when the
  work genuinely has four distinct phases; two when it honestly has two.
- One line per step, in the order they happen, so the client can follow the sequence at a glance.
- The reasoning that would have gone into a prose paragraph belongs inside the step lines, not
  around them.
- Vary the depth to fit the client: a careful client wants the checkpoint in each step, a direct
  one wants the step and nothing else.

**4. Bold sub-headline: `Main thing you can get`**

- **This is the only bolded sub-title in the whole proposal.** Nothing else gets one. Bolding a
  second or third heading dilutes this block until it stops standing out, which defeats the point
  of singling it out. The bold quotes in paragraph 2 are emphasis inside prose, not titles, and
  don't count against this.
- Do not import the habit from `general.md`, which bolds every block. That is a different guide.
- What the client gets out of hiring us specifically. Benefits, in their language.
- Frame it in their terms: their timeline, their budget, their risk, their team's workload.
- This is the block that separates us from every other bidder, so it must not read as generic.

**5. Their questions, answered.**

- Only when the post asks questions or demands specific inclusions.
- Label it `Answers to your questions`, **unbolded**.
- One item per question, each starting with `- `, a short reminder of the question ending in a
  colon, then a line break, then the answer:

```
Answers to your questions
- Why I'd be a good fit:
That measurement work is most of what I do.
- What I'd need from you:
The sample photos and your findings.
```

- **If they ask about similar projects, that is already answered in paragraph 1** and does not need
  its own item here. Either leave it out or point back to it in a few words. Repeating it wastes
  the client's attention on something they have already read.
- The client must be able to find their own question at a glance, because it is what they care
  about most.
- **This paragraph may push the proposal past 300 words, and that is correct.** Never drop one of
  their questions to protect a word count.

**6. Price and time.**

- Include only when the post asks for it, or when Phase 1 point 8 shows it would help.
- Judge which form fits: exact price and period, price only, period only, or milestones with no
  figures. A client who admits they don't know what this costs needs a number. A client who wants
  discovery first should not be quoted a build price.
- Combine the estimate with our reasoning, so it reads as judgement rather than a guess:
  "roughly G for D, H for E, so X in total, because in my experience the part that takes longest
  here is ..."
- **No bolded label on this block either.** It carries weight through position and content.
- The order matters. Leading with the number reads as a quote; leading with the reasoning reads as
  advice. The test is what the client asked of you:
  - **Reasoning first** when they admit they don't know what the work costs, or asked for someone
    with more expertise than them. They want to be walked to the number, and arriving at it after
    the breakdown makes it a conclusion rather than a demand.
  - **Number first** when they named a budget, set a range, or are purely price-comparing against
    other bids and need the figure findable in a scan.
- Word it professionally and acceptably. This is the paragraph that decides whether they hire us.

**7. Tech stack.**

- Only when it helps or is asked for. Skip it when it would burn twenty words a non-technical
  client cannot use.
- Say plainly that we are comfortable with the stack this project needs, with the years behind it.
- Do not list everything. Leave out a few of the less important tools even when they are genuinely
  ours. A short list reads as focus; an exhaustive one reads as a resume.
- Only ever name what the person profile supports.

**8. Ending. Short. Two sentences is usually plenty.**

Three ways to close. **Pick whichever leads this client furthest toward the next step, and never
default to one shape across every proposal.** If the post already names a next step, that outranks
the other two.

---

**Option 1. Propose a verification step.**

The purpose is to prove the approach on a small scope, using what they already have, before either
side commits. **Present it as part of the service**, the step that assures them the proposal
actually holds against their requirement.

- **Why the word "free" is there.** The whole offer rests on the client risking nothing on either
  side of the exchange. They hand over one small thing they already have, and they pay nothing to
  find out whether the approach works. Say both halves out loud, because an unstated price is
  still a question in their head, and a question is a reason not to reply.
- **The ask must cost them no effort either.** It has to be something already sitting on their
  machine: existing photos, a report they already run, a file they already have. Nothing to
  prepare, nothing to produce, nothing to think about. If they'd have to make something for you,
  the offer has stopped being free in the only sense that matters to them.
- **Say it with certainty, not as a favour.** You are running it free because you already know it
  holds, not because you are discounting to win the work. "Send me three and I'll run them free
  and tell you what fails" reads as confidence. "I'd be happy to do a free sample for you" reads
  as pleading. Same word, opposite effect.
- **If you need nothing from them:** say you'll run the test free on their agreement, and what it
  will show.
- **If you need something:** ask for the smallest thing that would expose the hard part.

One shape that works often, though not the only one:

1. Ask for a small, bounded sample of their own hardest material. Name the number, and frame it as
   their worst case, so they pick what would break it rather than what flatters it.
2. Promise a specific diagnostic back, free and said so, of a kind only someone who understands
   the problem could offer.
3. Say why it tells them more than the proposal does, so it reads as confidence.

The model, for a client whose problem is garment photos:

> "Send me three of your hardest garments, the ones you'd expect to break it, and I'll run them
> free and tell you which the check would reject and why. That'll tell you more about whether I'm
> the right person than anything else I can write here."

**The unit changes with the job, and so can the shape.** Three counties for a scraper, one property
for an analytics audit, the messiest document for an extraction pipeline, one "this number looks
wrong" case for a lineage job, the slowest page for a performance job. Never copy the garment
sentence into a job that isn't about garments.

**When that shape doesn't fit the job or the approach you proposed, build a different verification
that does.** Run the first rule against their existing data and report where it disagrees.
Reconcile one month against their own books. Stand up one integration end to end and show the
output. Replay one week of their history. The test should be the first step of the approach in
paragraph 3, shrunk to something they can judge in days.

---

**Option 2. The single best question.**

Use this when there is a genuinely open decision only they can make, and knowing the answer would
make the solution materially closer to what they actually need. Draft three, then test each:

1. Can the person reading actually answer it?
2. Does asking it prove something a rival could not have known to ask?
3. Does it make replying easier rather than harder?

Fold the survivor into the closing sentence.

---

**Option 3. Take the next step they named.**

When the post describes what happens next, a demo walkthrough, a paid test task, a code challenge,
a call, a video, go at it directly and with appetite. They have told you the path, so walking it
beats inventing one. Be specific about what you'd show or do, not merely willing.

---

**Rules across all three.** One ask only. Never stack an offer with a question, or either with a
request for a call: three asks in a paragraph that should carry one resolve to none of them. The
close should read like a person wrote it to another person, warm, direct, and easy to act on. If
nothing above fits, ask for fifteen minutes.

**9. Sign off**

`Best,` and the name from the person profile, on separate lines. Nothing after it.

**10. Images**

Ship `milestones.jpg` and `my_approach.jpg` **only when the engagement is multi-week and the
client is buying a plan.** Skip them when the job is a few days or less, when the model is bench
or hourly rather than milestone-based, or when the proposal's own argument is that scope isn't
known yet, because a confident milestone chart contradicts asking for discovery.

---

# Basic rules

**1. Tone: sound like a person. Write like someone typing a message, not a consultancy
producing a document.**
No em dashes. Contractions throughout. Match the register to the client you found in Phase 1: a
direct client gets directness back, a careful one gets reassurance, a collaborative one gets
"we" rather than "I" where it fits.

The structure below is fixed. The **voice inside it is not**, and getting the voice wrong is the
single most common way these proposals fail. A client reads forty of these. The polished,
perfectly balanced ones all sound like the same machine wrote them, because increasingly one did.
Sounding like a real person who read the post is now the differentiator.

### The tells that give it away

These are taken from our own shipped proposals. Each is a habit to break, not a style to admire.

**a. The X-not-Y antithesis.** The worst offender by far. "A draft with an opinion, not a
decision." "Refined against replies instead of revenue." "Maintained daily rather than rebuilt
weekly." "Structured data, not a digest." One shipped letter carried nine of these. It is the
most recognisable AI sentence shape in existence. **Cap: one per proposal, and only if it is
genuinely the clearest way to say the thing.** Usually the fix is to delete the "not Y" half,
because the "X" half already said it.

**b. The closing epigram.** Ending a paragraph on a neat aphorism: "Steering meetings that end in
decisions." "That's the difference between weekly refinement and weekly opinion." "A bot learns
to be agreeable rather than effective." Nobody talks like this. It reads as performance. End
paragraphs on the plain point instead, even when the clever line is available, **especially**
when the clever line is available.

**c. Rule of three.** "Activity, stage conversion and agent version." "Their timeline, their
budget, their risk." Real people list two things, or four, or one. Three balanced items is a
rhythm you fall into when you are generating rather than remembering. Vary it.

**d. Every sentence load-bearing.** Both shipped letters are 100% signal, every clause doing
work. Humans don't write like that. A real message has a throwaway line, an aside, a short
reaction. That texture is what makes the dense parts land.

**e. Abstract nouns doing the verb's job.** "An archaeology exercise." "The measurement layer."
"Commercial calls with the record attached." Say who does what to what.

**f. No visible reaction.** Nothing in either letter shows a human had a thought while reading
the post. No "honestly", no "this is the part I'd worry about", no sign of interest or
scepticism. It reads as output, because it is.

### What to do instead

- **React to something specific in their post, in your own words.** One line, early. "The bit
  about the pre-build pool ageing quietly is the part I'd worry about first." It costs eight
  words and it proves a person read it.
- **Use "I" and mean it.** "I've done this", "I'd start by", "I think", "in my experience", "I
  ran into this exact thing at MOOG". Confidence does not require impersonality.
- **Let one sentence be short and flat.** "That part is straightforward." "Standard stuff." "I've
  seen this go wrong twice."
- **Say the mildly awkward true thing** where it helps: "That timeline is tight but doable."
  "Worth saying I'd push back on doing the scraper first." Nothing signals a human like a small
  honest reservation, and it makes the confident claims believable.
- **Allow a hedge.** "I'd guess", "probably", "depends what's in there". A proposal with zero
  uncertainty in it reads as generated, because a person who actually knows the work knows what
  they cannot know yet from a job post.
- **Vary sentence length hard.** Long, long, short. The rhythm is most of the effect.

### The check before you post

Read the draft back and ask: **would a smart freelancer type this, or would they say it out
loud?** If a line is one you would never say to the client on a call, rewrite it as the thing you
would say. Then count the "rather than" / "instead of" / "not X, but Y" constructions. More than
one, cut the rest.

None of this means casual to the point of sloppy. It stays professional, specific and confident.
It just has to sound like it came from a person, because the client's alternative is forty
letters that don't.

**2. Short by default, longer only when earned.**
Do not explain at length where a sharp line does the job. Expand when the client is careful, asks
for detail, or lacks the technical background to fill gaps themselves. For a non-technical client
who is otherwise direct and confident, shrink the technical content and add a little more
explanation of the business consequence.

**3. Length: 200 to 300 words.**
Exceed it only for mandatory content, above all their own questions.

**4. Detect their technical level and write to it.**
Technical client: full technical vocabulary, precise strategy, real depth. They are judging
whether we know the domain.
Non-technical client: cover the same technique in business language. Where a mechanism has to be
conveyed, explain it by the phenomenon rather than the implementation, using a plain analogy that
carries the same principle. Never make them feel behind.

**5. Frame value in their terms, not ours.**
Where it matters, and always in paragraphs 4 and 6, express the benefit as their timeline, their
budget, their risk, their team's time. "Cheap now, impossible to retrofit later" beats a
description of the architecture.

**6. Client-centric, never boastful.**
Do not list achievements and do not push our ideas at them. Build from a real understanding of
their position, their situation and their need, so the proposal reads as though it was written
for them alone and makes continuing the conversation the obvious next move. Every claim about us
should exist to answer something they said.

---

# Working with the UI

**Questions first, then the proposal.** Finish Phase 1, post the question list, and only then
start writing. The questions belong to the analysis, not to the draft, so they reach the user
while the proposal is still being written rather than arriving attached to something that already
looks finished.

**Never block on them.** Write while they sit in the panel. Decide every open point yourself and
ship. Answers that arrive in time get folded into version 1, which then needs no rewrite at all;
answers that don't arrive change nothing, because every question shipped with the assumption
already in the draft.

- **Their screening questions** arrive in their own field. Answer each one separately and post
  them back to `/api/job/<id>/screening_answers` so each gets its own copy button. These are read
  before the cover letter, so treat them as the more important half.
- **Our open questions** go to `/api/job/<id>/questions`, each with the assumption already shipped
  in the draft. Questions for the client belong in the proposal, never here.
- **The profile is a summary, not an inventory.** Nobody records every project of their career in
  a markdown file, and the user only sends jobs the person is genuinely confident in, so the job
  having been sent is itself the evidence. A gap in the profile is a gap in the document, not in
  the person. **Never ask whether he can do something the post requires, and never soften a claim
  because the profile doesn't happen to mention it.** Write it confidently and move on.
- **Cover as much as you can yourself, and ask only what is sensitive.** Price and rate, anything
  only the user can physically do, a specific fact that would be publicly falsified such as a
  named client or a language the post will test on a call, and a genuine either/or in positioning.
  Never ask which project to lead with, whether to ship images, whether to include a stack line,
  or how to word something. Those are yours.
- **One round only.** Version 1 carries every question; version 2 carries none. Sweep the full
  checklist in `CLAUDE.md` before posting the first draft: profile gaps, claim safety, which
  project leads, price, availability, tone, deliverables, ambiguity in the post, client asks the
  profile can't satisfy, and anything only the user can do. Raising a second round after the
  answers arrive means the first sweep was lazy.
- When answers come back, skip anything flagged ignored, rewrite, and post the final version with
  no new questions. Anything that surfaces during the rewrite gets decided and noted, not asked.

---

# Delivery format

- **Reply with the proposal and nothing else**, plus the two images when rule 10 calls for them.
  Commentary only if asked.
- One fenced code block, markdown bold converted to Unicode sans-serif bold (capitals U+1D5D4,
  lowercase U+1D5EE, digits U+1D7EC), because Upwork renders markdown as literal asterisks.
- **Write no files.** The proposal lives in the reply.
- Count characters on the markdown draft, not the converted text.

# Evidence

Never invent a URL, a client name, or a metric. Every number comes from the person profile exactly
as written there. Where the profile records no outcome metric, cite scope and system detail
instead. Availability always matches what the client asked for, and the engagement model mirrors
theirs, per the rules in `CLAUDE.md`.
