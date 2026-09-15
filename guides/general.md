# General Proposal Guide

**Guide id:** `general`
**Use for:** any Upwork job description, any person.

This is the default guide for writing a proposal. The person profile (`Mario.md`, `Zachary.md`, ...)
supplies every fact; this file supplies the shape.

## Delivery format

When the user pastes a job description, **reply with the proposal and both images, and nothing
else.** No preamble, no "here is why this works," no scoring or gap analysis afterward. Output the
Unicode-bold proposal in a single fenced code block, then attach `milestones.jpg` and
`my_approach.jpg`. Offer commentary only if asked.

**The proposal is not saved to a file.** It lives in the reply and nowhere else. Draft it, count
it, convert it, send it. Do not write `proposal-<slug>.md` or any other copy, and do not keep past
proposals around.

**The two images always carry these exact names, and every new job description overwrites them.**
There is one `milestones.jpg` and one `my_approach.jpg` in the folder at any time, both matching
the most recent proposal. Never write `milestones-<slug>.jpg` or keep old copies around.

## Follow-up questions after the job description

Job posts often come with screening questions, and clients ask more in chat. When the user pastes
one, **answer it in the same copy-ready form as a proposal**: a single fenced code block, Unicode
sans-serif bold on any sub-headline, no markdown asterisks, no em dashes, contractions throughout.

- **Lead with the answer.** No throat-clearing, no restating the question back at them.
- **Short blocks, one idea each**, so it's scannable in a chat window. Bold sub-headlines when
  there's more than one part to the answer, plain prose when it's a single point.
- **No `Hi` opener and no sign-off** unless the answer is clearly a standalone
  message rather than a reply in an existing thread.
- **No 2000-character cap**, that's a proposal rule. Keep it as short as the question allows,
  usually well under half a proposal.
- Same evidence rules apply: real links, real numbers from the person profile, nothing invented. If a
  question asks about something that isn't in the person profile, say so plainly and bridge to the nearest
  real experience rather than bluffing.
- **No images** unless the question is about process or timeline and one would genuinely help.

## The milestone image (ships with every proposal)

A 1600x900 JPG built from the proposal's own milestones, so the client can grasp the plan without
reading. Content rules:

- **One card per milestone**, each with two labelled blocks: **YOU GET** (the deliverable) and
  **HOW YOU MEASURE** (the check that proves it landed). Every milestone needs both.
- **No dates and no money.** No week numbers, no durations, no rates, no totals. Number the
  milestones 1, 2, 3 and let the proposal text carry the schedule.
- **Keywords and short phrases, not sentences.** A client should read the whole image in about
  fifteen seconds, and it still has to carry everything they need to judge the plan.
- Keep bullets short enough not to wrap. Fix the "YOU GET" list to a set height so the
  "HOW YOU MEASURE" blocks line up across all three cards.
- Close with a one-line spine at the bottom right: the single promise the plan rests on.

## The approach image (also ships with every proposal)

A second 1600x900 JPG, `my_approach.jpg`, showing how the work would run on this specific job.
Content rules:

- **Five stages across the top**, each with two keyword bullets, drawn from the proposal's own
  approach and tailored to the job. Not a generic SDLC.
- **A communication band is mandatory and must be visually prominent.** This is the point of the
  image, not a footnote: update cadence, demo rhythm, preferred channel, and how blockers are
  raised. Dark band, full width, directly under the stages.
- **A closing principles row** carrying the positioning from the person profile.
- Same rule as the milestone image: keywords and short phrases, readable in fifteen seconds, but
  complete enough to judge how he works.

**How to build both.** Copy `milestone-template.html` and `approach-template.html`, swap the copy
for this job, then run `./html-to-jpg.sh <file>.html milestones.jpg` and
`./html-to-jpg.sh <file>.html my_approach.jpg`. That script renders the page in headless Chrome
and converts the PNG to JPG through a canvas in a second Chrome pass, because this machine has no
Pillow, ImageMagick, or netpbm. Read each rendered file back before sending: overflowing cards
silently push the footer out of frame, bullets that wrap make the columns ragged, and a short
section leaves dead space at the bottom of the frame.

## Hard constraints (non-negotiable)

- **Under 2000 characters.** Total. This is the binding constraint and it forces ruthless word
  choice. Draft, then cut. Count before delivering.
- **No em dashes anywhere.** Use commas, colons, periods, or parentheses.
- **No placeholders.** Ship a finished proposal, never `[insert X]` or "add your rate here."
  Fill every slot from the profile, the portfolio, and the job description.
- **Bold sub-headlines on every block** so the client can skim it in seconds.
- **Seam the blocks together.** Each sub-headline should carry a thread from the block above it,
  so the proposal reads as one argument rather than a stack of disconnected sections. The past
  work should set up the read of their problem, and the key point should set up the toolchain.
- **Always deliver a paste-ready version, in the chat only.** Upwork does not render markdown, so
  `**bold**` pastes as literal asterisks. Draft with markdown bold, then convert every bold span to
  Unicode sans-serif bold (the same style used on the Upwork profile: capitals from U+1D5D4,
  lowercase from U+1D5EE, digits from U+1D7EC) and output that converted text in a fenced code
  block, with no commentary inside the block. **Write no files for the proposal**, not `.md` and
  not `.txt`. Do the 2000-character check on the markdown draft, since Unicode bold inflates the
  count in editors that measure UTF-16 code units.
- **Tone:** professional, confident, friendly. Impressive without bragging. Warm without filler.
  **It has to sound like a person typed it.** The client is reading forty of these and the
  polished ones all sound machine-written. Specifically: cap "not X, but Y" / "rather than" /
  "instead of" constructions at one per proposal, never end a paragraph on a neat aphorism, break
  up rule-of-three lists, and let at least one sentence be short and plain. React to something
  specific in their post in your own words, use "I" freely, and allow one honest reservation
  ("that timeline is tight but doable"). A proposal with zero uncertainty in it reads as
  generated. Full detail in `guides/brainstormed.md` under "Sound like a person".
- **Use contractions.** Write "I've", "I'm", "it's", "don't", "you'll", never "I have built",
  "I am", "it is", "do not", "you will". The long form reads stiff and formal. This applies to the proposal, the images, and any follow-up answer. The stack
  headline, when the stack line is used at all, is therefore **I'm fully comfortable with**, not
  "I am fully comfortable with".
- **Open with `**Hi** 👋` on its own line,** then a blank line, then the opening proof block
  described in Required structure.
- **Always sign off with `Best,` and the name on separate lines** as the final two lines, name
  taken from the selected person profile. Nothing after it.
- **The opening must stop the scroll and carry evidence at the same time.** Never open with "I am
  a full-stack developer with N years of experience," and never with "I've built a similar
  project." Clients stop reading both instantly. The sub-headline names the match in their terms,
  the sentence under it names the real project that proves it.

## Read the job description first, and prove it

Before drafting, work out three things. **Use them as reference, do not state them as labels in
the proposal:**

1. What they are actually trying to build.
2. What the single most important key to this job is (the thing that decides success or failure).
3. What kind of person they are looking for (contractor, partner, specialist, team lead).

Then, in the first two sentences, reference something only a careful reader would catch: their
project name, a technical constraint, a business goal, a stack decision. Those two sentences are
the opening proof block, so the reference has to sit inside the evidence rather than replace it.

## Required structure

**1. Open on the proof, with their problem inside it**

The first block is the closest thing he has actually built, not an abstract insight, because only
the opening lines show in the client's results list and an insight with no proof behind it reads
as cleverness. But it must not open like every other bidder either: "I've built a similar project"
and "I'm a great fit for this" are what forty other people wrote this morning.

So the sub-headline names the match in the client's own terms, and the first sentence carries the
evidence:

> **I've done this exact job, on different documents**
> At International Aircraft Associates I scraped part information out of PDFs into a maintained
> structured matrix, on Python and SQL pipelines that replaced a manual process. Deed records are
> the same shape of problem: documents in, clean rows out.

Upwork's strongest published example does the same thing in one breath: "I noticed you're looking
for someone to label and categorize image datasets," then immediately "I've completed similar
projects for two AI startups, including a 50,000-image classification project with a 98.7%
accuracy rate."

Rules for this block:
- One or two portfolio links that genuinely resemble their ask, not a catalog of everything.
- State the outcome for that client, concretely.
- Keep it to two or three sentences.
- The sub-headline must be specific to this job. Never a generic claim of similarity.
- The scroll-stopping idea that used to open the proposal moves to the block after this one, under
  a sub-headline that carries the thread forward ("The part that makes it finishable").

**2. Proof you read the JD**
- Pay one specific, earned compliment: name the exact feature or tech choice they made, use a
  professional approval word (strategic, smart, efficient, forward-thinking), then state the direct
  benefit it buys them (saves time, scales cleanly, better UX).
- Name the hardest part of their project out loud (tight deadline, messy data migration,
  compliance, latency, cost per token) and show you know how to handle it.

**3. A clear, tailored solution**
- Three simple steps, specific to their build, under an **Approach** heading. Not a generic SDLC.
- One improvement or alternative tool they did not ask for. This is where deep expertise shows.
  Head this block **Key point you can get**, never "One improvement" or "Suggestion".
- **The stack line is conditional, not automatic.** Include it only when the post enumerates
  technologies. Cut it when it doesn't.

  **Include it when** the client listed languages, frameworks, databases or named tools, because
  they will scan for those tokens coming back and the absence reads as a gap. It is strongest with
  niche tools: anyone can write "data pipelines," but Stape, CCXT, Analytics Canvas, SAP Ariba or
  Pentaho prove you have been in the room. When you include it, mirror their exact words in their
  order, and don't pad with adjacent tools they didn't mention.

  **Cut it when** the client is non-technical or wrote a short post with no technologies in it.
  They can't evaluate the line, it costs fifteen words of a limited budget, and it is the most
  resume-like thing in the whole proposal. Upwork's own guidance is that a proposal is not a
  resume. Spend those words on the outcome instead.

  Note the cost either way: every tool you list is fair game on the call. Only name what the person
  profile supports or what he is genuinely ready to be questioned on.

  When it is included, introduce it with **I'm fully comfortable with**, never the word "Stack".

**4. Transparent timeline and process**
- A realistic estimate in days or weeks.
- Update cadence and preferred channel (Upwork chat or Slack).
- Milestones, so they know when working software appears.

## Every proposal must also

- **Emphasize the one thing** the client has to solve or implement for this job to succeed. Make
  that the spine of the proposal, not a footnote.
- **Ask exactly three professional questions.** Sharp, specific to their build, the kind that show
  you have already thought past the brief.
- **Close by moving them to the next step.** A short call or a reply that saves them time and gives
  them a clearer picture. This close matters more than anything else in the proposal.

## Evidence rules

1. **Never invent a URL, a client name, or a hard metric.** Only the links in the person profile are
   real, and every number must come from that profile exactly as written there. Do not round
   figures, convert them into percentages, or invent a "reduced X by 20%" style claim. A fabricated
   percentage is the fastest way to lose a client who checks.
   Some projects publish no outcome metrics at all; the person profile marks which. For those, cite scope
   and system detail instead of results, and never fill the gap with a number.
2. **When a portfolio project genuinely matches,** lead with it: case-study link, plus the live URL
   when seeing the running product helps. Pull the specifics from the case study, not from
   imagination.
3. **When nothing in the portfolio matches,** write from capability and approach instead: the
   architecture to use, the decisions to make, the relevant industry or system type.
   Original framing is fine. Fictional case studies and invented numbers are not.
4. **When the profile lines up with the role,** use it directly. When it does not line up cleanly,
   build the bridge: the transferable system type, the adjacent industry, the reason the business
   framing matters for this exact problem.
5. **Match the job's own vocabulary.** If the post says "AI agent," write "AI agent," not
   "agentic orchestration layer."
