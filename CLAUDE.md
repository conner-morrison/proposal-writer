# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a codebase**. It is a working folder for drafting **Upwork proposals**. The typical
task is: the user pastes a job description, and Claude writes a tailored proposal, a milestone
image, and an approach image.

There is no build, lint, test, or run step.

## Read the person profile first

**All personal information lives in the person profiles and nowhere else.** There is one profile
per person: `Mario.md` and `Zachary.md` today, more later. Identity, positioning, skills,
industries, portfolio with case-study links and verbatim metrics, working style, and voice. Read
the profile for whoever the proposal is for before drafting anything, and take every claim, link
and number from it. Never mix two people's facts.

**All proposal-writing instructions live in `guides/`.** `guides/general.md` is the default. This
file holds neither the profile nor the guide, so each stays a single source of truth.

Files in this folder:

| File | Holds |
| --- | --- |
| `Mario.md`, `Zachary.md` | Everything personal, one file per person: profile, portfolio, metrics, voice |
| `guides/*.md` | The proposal-writing guides. `general.md` is the default |
| `CLAUDE.md` | This file: what the repo is and where everything lives |
| `ui/index.html` | Front end: pick a guide, pick a person, paste a JD, get copy-ready output |
| `proposals/` | Local archive, one readable markdown file per proposal. Gitignored |
| `server.py` | Local server behind the UI. Start it with `./run-ui.sh` |
| `milestone-template.html` | Starting point for `milestones.jpg` |
| `approach-template.html` | Starting point for `my_approach.jpg` |
| `html-to-jpg.sh` | Renders either template to JPG |

**Proposals are archived locally.** Every proposal is written to `proposals/` as readable
markdown the moment it is posted back, named `<date>_<slug>_<person>_<id>.md` and carrying the
metadata, the screening answers, the questions and the original job description, so the file
stands alone. The `.jobs/<id>.json` record is the queue's working state; `proposals/` is the
durable copy. Both are gitignored, since they hold client names and rates and the repo is public.

Deleting a row in the history, or Clear all, removes the archived file too. The timed retention
purge does not: it trims the working list at 20:30 JST, it does not throw away finished work.

## How to write a proposal

The instructions moved out of this file. **Read `guides/general.md`** before drafting anything, and
follow it exactly. Additional guides will be added to `guides/` over time; use whichever one the
user names, and `general.md` when they name none.

Two inputs decide every proposal:

1. **Which guide** — from `guides/`, default `general.md`.
2. **Which person** — `Mario.md` or `Zachary.md`. Ask if the job description makes it ambiguous
   and the answer would materially change the proposal.

## Rules that apply to every guide

**Availability always matches what the client asked for.** Baseline is full time, 40 hours a week.
If the post wants full time, he's full time. If it wants 15 to 25 hours, that's what he offers. If
it's project by project or overflow work, that's what suits him. Never present availability as a
constraint, and never volunteer a number the post didn't ask about.

**Mirror the engagement model too.** Fixed price, hourly, retainer, milestone based, trial project:
take whatever the client named and present it as the way you prefer to work, with a reason that
benefits them. Never argue for a different model in a proposal.

**Phrase both so they read as professional and easy to say yes to,** not as compliance. The point
is to remove every reason to hesitate:

- Wants full time: "I've got full availability at 40 hours a week and can start Monday."
- Wants 15 to 25: "20 hours a week works well on my side, and it's enough to keep this moving
  without stalling your team."
- Overflow or per project: "Project by project suits me, and I can pick up work as it lands."
- Fixed price: "Happy to work fixed price per milestone, which keeps the cost predictable on your
  side and puts the risk on me."
- Timezone matters: "I'm in Miami, so 8:30 to 5:30 ET is my normal working day."

## The UI

`./run-ui.sh` starts a local server on port 8765 and serves `ui/index.html`. The page lets you
pick a guide, pick a person, paste a job description, and get a copy-ready proposal with a copy
button. It discovers guides from `guides/*.md` and people from single-word `.md` profiles in this
folder, so adding either is just adding a file.

**Bridge mode.** With no `ANTHROPIC_API_KEY` set, pressing "Write proposal" does not fail. It
queues the job and the running Claude Code session writes it. If you are that session, watch the
queue and service it:

```
curl -s localhost:8765/api/jobs/queued              # {"ids": [...]}
curl -s localhost:8765/api/jobs/next                # claim the oldest, marks it working
curl -s -X POST localhost:8765/api/job/<id>/note    -d '{"note":"reading the JD"}'
curl -s -X POST localhost:8765/api/job/<id>/message -d '{"role":"claude","text":"question?"}'
curl -s "localhost:8765/api/messages/since?seq=N"   # anything new, both roles
curl -s -X POST localhost:8765/api/job/<id>/result  -d '{"proposal":"**Hi** ..."}'
```

A job carries a `client` name from the UI when the user supplies one; use it in the greeting.

**Two kinds of question, and they do not go in the same place.**

- **Questions for the client** (which counties, is there a sandbox, who signs off) belong **in the
  proposal**, at the end, where they show you have thought past the brief. The guide for the
  selected mode says how many. They never go in the panel.
- **Questions for the user** go in the panel. These are the things only the user can settle:
  gaps or ambiguities in the person's background, whether a claim is safe to make, which project
  to lead with, rate and availability, tone and positioning calls. Anything where you had to
  guess about *your own side* rather than about the client's.

## The order of work on one job

Pressing **Write proposal** starts this sequence. It is the same in Auto and Manual mode, and
nothing in it is optional.

1. **Search GitHub** for one or two projects genuinely close to the job description. This comes
   before the analysis and before any drafting.
2. **Decide: send or carry on.** Repositories found means publish them to the `github` channel and
   hold, which shows the links above the status bar with an unticked box, presses Pause, and sets
   the status to *waiting for github reply*. Nothing found means send nothing and go straight to
   step 3.
3. **Analyse the job** the way the selected guide asks. Keep a running list of anything you cannot
   settle yourself, but do not post it yet.
4. **Write the proposal against the selected guide.** Whichever guide the request names, followed
   exactly: `general.md` unless told otherwise. The guide decides the shape, the length, the bold
   rules and the closing move.
5. **Keep adding to the list while writing.** Most of it surfaces here rather than in the analysis:
   a claim that turns out to need checking, a number only the user can set, a positioning call with
   two defensible answers.
6. **Post the proposal and the question list together.** The list goes up with the finished draft,
   not before it, so the user reads the questions knowing what the proposal already assumed.

The gate at step 2 releases on a reply naming the job, on a bare acknowledgement, or on a person
pressing Resume.

**Questions go up with the proposal, not ahead of it.** Every question states the assumption the
draft already shipped, which is only possible once the draft exists. **One round: all of them on
version 1, none on version 2.** If something surfaces during the rewrite, settle it and say so in
the note rather than opening a second round.

**Still never block.** Collecting questions does not mean waiting for answers. Decide every open
point yourself, ship the draft, and let the panel carry what you had to assume. The proposal is
complete and sendable as it stands; answers only ever improve it.

Post the list like this:

```
curl -s -X POST localhost:8765/api/job/<id>/questions -d '{"questions":[
  {"text":"Which counties hold most of your deal volume?",
   "assumption":"drafted platform-first rather than naming counties"}]}'
```

Each question shows in the UI with an ignore checkbox and an answer field. When the user presses
"Submit and rewrite", the job flips to `revising` and appears in `/api/jobs/answered`. Read the
answers off the job, skip anything flagged `ignored`, and post a revised proposal to `/result`.

**Screening questions from the job post** arrive in their own field and reach you as a separate
block in the prompt. Answer each one individually and post them back so each gets its own copy
button in the UI:

```
curl -s -X POST localhost:8765/api/job/<id>/screening_answers -d '{"answers":[
  {"question":"Have you scraped government sites before?","answer":"Yes. At ..."}]}'
```

Keep each answer short, specific, and in the same copy-ready form as the proposal. These are not
the same as your own open questions: the client wrote these and they get read before the cover
letter, so treat them as the more important half.

**One round of questions. Version 1 carries all of them, version 2 carries none.**

**On the first write, search GitHub before writing anything.** When a job is written for the
first time (the **Write proposal** button, never a rewrite), the repository search is the *first*
step, ahead of the job analysis and ahead of any drafting. Both modes: a job typed into Manual
gets the same search as one ticked off the Auto queue.

**The sequence, in order:**

1. **Search GitHub** for one or two repositories genuinely close to what the job describes.
2. **Publish the result** to the relay's `github` channel — the job id, the job title, and the
   URLs found.
3. **If repositories were found, stop and wait.** Arm the gate, which makes the UI show the
   Pause button as pressed with Resume available, and the status line read *waiting for github
   reply*. Do not draft while the gate is closed.
4. **If the description could not carry a search, send nothing and keep going.** No publish, no
   gate, no pause: write the proposal immediately. The channel only ever hears about jobs that
   produced repositories, so a message arriving there always carries something to look at.

```
# 2. found one or two
curl -s -X POST localhost:8765/api/relay/publish -H 'content-type: application/json' -d '{
  "channel":"github",
  "body":{"type":"github_refs","job":"<id>","title":"<job title>","upworkUrl":"<if any>",
          "repos":[{"url":"https://github.com/owner/name","why":"one line on the overlap"}]}}'

# 3. then hold, and wait for the channel to answer
curl -s -X POST localhost:8765/api/job/<id>/await_github -d '{}' -H 'content-type: application/json'
```

**Judging whether the description can carry a search.** It qualifies when it names something
implementable: a stack, a platform, a data domain, or a concrete artefact ("Apify actor for CRE
listings", "GA4 and GTM audit", "NFL power ratings in Sheets"). It does not when it is only a role
shape with no buildable object ("we need an operations lead", "an analyst to support reporting").
A forced keyword match is worse than none, and it would also stall the write behind a pointless
gate. When it does not qualify, the job is simply written with nothing sent to the channel.

**The gate releases three ways:** a reply on the channel naming the job id, a bare acknowledgement
when exactly one job is waiting, or a person pressing Resume. A bare acknowledgement while several
jobs wait is ignored rather than guessed at.

**Two rules on what comes back.** Repositories found this way belong to other people, so they are
build references and never portfolio: the saved rule is no GitHub links in proposals. And say
plainly in the `why` what actually overlaps, since a repo that merely shares a keyword is noise
the channel does not need.


**The profile is a summary, not an inventory.** Nobody writes every project of their career into a
markdown file, and the user only sends jobs the person is genuinely confident in. Job selection is
itself the evidence. A gap in `Zachary.md` or `Mario.md` is a gap in the document, not in the
person, so **never ask whether he can do something the post requires, and never hedge because the
profile doesn't happen to mention it.** Write it with confidence.

**Decide it yourself. Ask only what is sensitive**, meaning something you genuinely cannot settle
and getting it wrong would cost real money or credibility:

1. **Price and rate**: a business decision only the user can make.
2. **Anything only the user can do**: record a video, share a repo, confirm availability.
3. **A specific fact that would be publicly falsified**: a named client, a live URL, a
   certification, a language fluency the post will test on a call.
4. **A real either/or in positioning** where both readings are defensible and the user's
   preference decides the proposal.

**Never ask about:** whether he has a tool or platform the post names, which past project to lead
with, whether to ship images, whether to include the stack line, or how to phrase something. Those
are all yours to decide, and the guides already answer them.

Every question states the assumption already shipped in the draft, so an unanswered question still
leaves a complete proposal.

**After the answers come back, rewrite and post the final version with no new questions.** If
something surfaces during the rewrite, decide it yourself and say so in the note rather than
opening a second round. Questions raised after a proposal has been posted are a failure of the
analysis step, not a second chance at it. A question that would be better asked of the client belongs in the
proposal, not the panel.

Post the proposal back as **markdown**; the page converts it to Unicode bold itself. Jobs are
mirrored to `.jobs/<id>.json`. Build `milestones.jpg` and `my_approach.jpg` as usual and send them
in chat, since the output box is text only. With an API key set, the same button calls the API
directly and the queue is unused.

