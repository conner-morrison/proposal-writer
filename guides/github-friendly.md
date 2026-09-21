# GitHub Friendly

**Guide id:** `github-friendly`
**Use for:** an Upwork job whose description is concrete enough to build something from, and
concrete enough to find genuinely similar work on GitHub.

> **This guide is only usable when both of those hold.** The letter opens on repository links, so
> it has nothing to open with when the search came back empty. The test is the one in
> `github-researcher.md`: the post has to name something implementable, a stack, a platform, a
> data domain or a concrete artefact. A post that is only a role shape with no buildable object
> cannot carry this guide, and that job should be written with `brainstormed.md` instead.
>
> Everything below is inherited from `brainstormed.md` except paragraph 1, which is what makes
> this guide its own thing.

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

**1. The repository opener. No bold anywhere in it, and no emoji anywhere in it.**

This paragraph replaces the attractive starter. It is the whole reason this guide exists: the
letter opens by handing the client working code, and everything after it is support.

**Greeting.** When the post gives a client name, open with `Hi [name],` and a blank line after it.
When no name is known, there is no greeting at all: start straight into the first sentence.

**Then the find, stated as a coincidence.** One sentence carrying the meaning *by chance, I have a
really similar project I'd built in my GitHub.* Use that sentence as it stands when it fits the
job, or bend it to the post. What matters is that it sounds natural and professional rather than
templated, because this line is the one deciding whether they open the rest of the letter at all.

Some shapes that carry the same meaning:

- "By chance, I've already built something very close to this."
- "This is close to a project already sitting in my GitHub."
- "As it happens, I built more or less this a while back."

**Then the links, one per line.** The repository URLs the server returned, each alone on its own
line. Bare URLs: no bullets, no bold, no link text wrapped around them, nothing else on the line.

**Then why they match.** Two or three sentences on what those repositories actually do and how his
experience lines up with this job, drawn from the repos and the person profile together. Write it
in the client's words, not ours: if they say listing tool, the sentence contains their words. This
is what turns the coincidence into evidence.

**2. The head start, and what you would add. Bold the key phrase from the job description.**

**Two or three sentences. No more.** The paragraph below describes a lot of decisions, but the
output stays the length it already was. The links did the proving; this paragraph only says where
that leaves the client and what happens next.

**Open on the head start.** One line telling them the work is already part-done, so the
repositories read as a running start rather than a portfolio piece. When the industry is ordinary,
use one of these:

- "You and I are not starting from scratch with only experience, we already have a similar project
  under our belt."
- "We're already halfway down the road."
- "We're joining the race halfway through."
- "It's like having an apartment already built, with only the finishing touches left."
- Or a better one you write, if it carries more momentum than these do.

**When the industry is specific, rebuild the image out of their world** and keep the meaning
identical: a construction post takes the apartment line because it already belongs there, a
logistics post takes freight already loaded, a trading post takes a position already open. Only
swap when the industry hands you an obvious image, because a forced metaphor reads worse than the
plain sentence.

**Then say what you would add. Which branch depends on the post:**

- **They named the stack.** Offer to fill what is missing and bring the repository up to
  everything they listed, so it lands as their requirement fully met and running, rather than a
  demo that nearly fits.
- **They did not name the stack.** Show what you would upgrade and why, aimed at the best
  performance available now.

**Work in where the field is today.** One clause on the current direction of that industry or that
technology, so the upgrade reads as informed. This is the difference between "I'll improve it" and
someone who knows what improving it means this year.

**Bold the key phrase from the job description**, somewhere in this paragraph:

- **Quote only the key part, not the whole sentence.** Find the few words that carry the point and
  bold those. A long quotation buries the thing you were pointing at.
- **Placement is optional.** Dropping it into the middle of your own sentence usually reads more
  naturally than leading with a quotation.

**What this paragraph no longer carries.** In `brainstormed.md` this is where Phase 1 point 3 gets
acknowledged. Here the head start line is doing that work, and the space is spent, so skip the
acknowledgement rather than running long. If what they are proud of still needs saying, it belongs
in paragraph 4.

**3. The solution, as our approach. Optional. A numbered list, never a block of prose. No bold
anywhere in this paragraph, including the word Approach.**

**Include it in two cases, and leave it out otherwise:**

- **The job description asks for one.** A plan, a methodology, "how would you tackle this", a
  proposed process. Then it is mandatory and it gets the space it needs.
- **It is not asked for, but laying out the sequence would genuinely win the client over.** A
  project with real stages, a client who sounds anxious about how the work would actually run, a
  brief where the order of operations is the insight. Then it earns its place by being persuasive,
  not by being thorough.

**Leave it out everywhere else.** Small or ad-hoc work, a client who wants a rate and a start
date, a post that already describes the process and just needs someone to run it, or a job where
the steps would be obvious to anyone in the trade. A three-step plan for a two-day fix reads as
padding, and it pushes the blocks that actually sell further down the page.

When it is in, lay it out exactly like this:

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
- Do not import the habit of bolding every block. That belongs to a different style of letter.
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

- **If they ask how you would approach the work, paragraph 3 is mandatory** and this item points
  back to it rather than repeating it.
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

**8. The close. Fixed. Word for word, every time.**

The three-way choice is gone from this guide. The letter always ends like this, and nothing is
added after it:

```
Why start from zero when we're already halfway there?
Let me know if you are interested.

Best,
Zachary
```

- **A single newline between the two sentences**, then a blank line, then the sign-off.
- **The name is the one from the person profile**, so it reads `Zachary` for `Zachary.md` and the
  profile name for anyone else.
- **Nothing follows the name.** No postscript, no availability line, no second ask.
- **Nothing earlier in the letter may ask for anything either.** The close carries the only ask,
  and it is "let me know if you are interested". A request planted in paragraph 2 or 4 competes
  with it and leaves the client with two things to answer instead of one.
- The opening question is the same head start idea paragraph 2 runs on. That repetition is
  deliberate here: it bookends the letter.


**9. Images**

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

- **Reply with the proposal and nothing else**, plus the two images when rule 9 calls for them.
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

**Build the proposal from two sources together: the person profile and the repositories the server
returned.** `Zachary.md` supplies the employment history, the industries and the resume facts. The
repos supply buildable evidence a client can open. Neither is the whole picture on its own, and
the letter is strongest where they meet: the profile says he ran Power BI off ERP data at MOOG,
the repo shows the embedded implementation, and a client reading both sees a career rather than a
claim.

**Print the repository URLs, and print them in paragraph 1.** They go as bare URLs, one per line,
in the block described there, and they appear nowhere else in the letter. A client who can click
through to working code is the strongest proof the letter can carry, which is why this guide
spends its opening on them rather than burying them next to a sentence further down.

This is the one exception to the standing rule that his GitHub never appears in a proposal. It
covers repositories the server returned and nothing else. Repos found by searching during step 1
belong to other people and never appear, and no URL is ever written from memory: if the server did
not send it, it does not go in the letter.

**Never challenge his authorship of a returned repo.** He worked six years under employer and
client accounts, and he is consolidating that work to his own GitHub. A source repository owned by
someone else, a corporate email on the original commits, or a README crediting another name are
all expected artefacts of that migration, not evidence against him. Read what the code does and
write from it.
