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

**All proposal-writing instructions live in `guides/`,** and which one writes a given job is
decided by `decision-maker.md` rather than fixed. This file holds neither the profile nor the
guide, so each stays a single source of truth.

Files in this folder:

| File | Holds |
| --- | --- |
| `Mario.md`, `Zachary.md` | Everything personal, one file per person: profile, portfolio, metrics, voice |
| `guides/*.md` | The proposal-writing guides. `decision-maker.md` picks one per job |
| `github-researcher.md` | The rules for the repository search: judging a job, querying, what to send |
| `decision-maker.md` | Reading the client out of the post, then choosing which guide writes it |
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

The instructions moved out of this file. **Read `decision-maker.md` first** to read the client
and choose the guide, then read that guide and follow it exactly. The choice is
`github-friendly` when the repository search returned something and `article-based` when it did
not; `brainstormed.md` stays in the folder and is used only when the user names it outright.

Two inputs decide every proposal:

1. **Which guide** — decided per job by `decision-maker.md`, not taken from the dropdown.
   `github-friendly` when the repository search returned something, `article-based` otherwise.
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

1. **Read the job description and search GitHub** for one or two projects genuinely close to it.
   This comes before the full analysis and before any drafting.
2. **Post the job id and the URLs found** to the relay's `github` channel. The UI shows them above
   the status bar as a checklist with unticked boxes.
3. **Drop those URLs from working context.** Once they are on the server they belong to the
   server. Do not carry the ones you found into the analysis or into the draft, and do not quote
   them back later: they were other people's repositories, and the only URLs that reach a proposal
   are the ones the server sends back at step 5.
4. **Hold at the gate.** Arming it presses Pause and sets the status line to *waiting for github
   reply*. Do not draft while the gate is closed. **Nothing found means no publish, no gate, no
   pause** — go straight to step 6.
5. **The server answers with GitHub URLs, and those are Zachary's own repositories.** This is the
   point of the whole exchange: the search goes out, and what comes back is his matching work.
   Read what those repos actually contain, because they are the material the past-work half of the
   proposal is built from.
6. **Read the client out of the post, then pick the guide, but only in Auto.** The job carries
   `guide_mode`. **`manual` means the person chose it and you must write with what they picked**,
   whatever the decision would have said; the server rejects a guide change on such a job. In
   `auto`, decide it. Both halves are in `decision-maker.md`:
   the nine-point read, then the choice. Repositories came back means `github-friendly`; anything
   else means `article-based`. **The dropdown is only a default, and this decision overrides it.**
   Record the choice so the UI and the archive name the guide that actually wrote the letter:
   `POST /api/job/<id>/guide -d '{"guide":"github-friendly"}'`.
7. **Write the proposal against that guide, followed exactly.** The guide decides the shape, the
   length, the bold rules, the closing move, and whether the repository URLs are printed.
8. **Post the proposal and the question list together.** The list goes up with the finished draft,
   not before it, so the user reads the questions knowing what the proposal already assumed. Keep
   adding to that list while writing — most of it surfaces during the draft rather than during the
   analysis: a claim that needs checking, a number only the user can set, a positioning call with
   two defensible answers.

The gate at step 4 releases on a done ping from the server, on a reply naming the job, on a bare
acknowledgement, or on a person pressing Resume.

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

**One box in the UI, two readings, decided by the tick beside it.** The field under the job
description carries a checkbox. **Ticked** means what the user typed is the client's screening
questions and the job arrives with it in `screening`: answer each one and post them back, exactly
as above. **Unticked** means the text is the user talking to you about this proposal, and it
arrives in `notes` instead. Read `notes` the way you would read a message typed into the Claude
Code chat: it is an instruction about how to write this one, so follow it while drafting and
**never answer it inside the proposal**. It is not the client and the client never sees it.

Reply to it only when it asks you something, or when it forced a call the user should see. **Keep
the reply short.** Lead with the answer itself, the number or the decision, and give at most a
sentence or two of reason. The panel is read at a glance, and a long answer buries the part that
was actually asked for.

**Post it in the same step as the proposal**, alongside `/result` and `/questions`. The page stops
watching for late arrivals after a couple of minutes, and a reply sent well after the draft can
miss the window and leave the panel empty.

The reply gets its own panel in the UI with a copy button, and like the screening answers it is
editable there:

```
curl -s -X POST localhost:8765/api/job/<id>/notes_reply \
  -d '{"reply":"Led on the Salesforce work as you asked. Left the rate at $75 since the post named no band."}'
```

A job carries at most one of the two, so check `notes` as well as `screening` when you claim a
job. Both are archived to `proposals/` with the finished letter.

**That same panel is where client research goes**, whether a note was typed or not. When the post
names their team, company or product, run it down to a domain and report it there, per **Find out
who they are** in `decision-maker.md`. With no note to answer the panel titles itself *For you*,
and it is never shown to the client.

**One round of questions. Version 1 carries all of them, version 2 carries none.**

**On the first write, search GitHub before writing anything.** When a job is written for the
first time (the **Write proposal** button, never a rewrite), the repository search is the *first*
step, ahead of the job analysis and ahead of any drafting. Both modes: a job typed into Manual
gets the same search as one ticked off the Auto queue.

**The sequence, in order:**

1. **Search GitHub** for one or two repositories genuinely close to what the job describes.
2. **Publish the result** to the relay's `github` channel — the job id, the job title, and the
   URLs found.
3. **Forget the URLs you sent.** They are on the server now, and nothing you found in the search
   is allowed into the proposal.
4. **If repositories were found, stop and wait.** Arm the gate, which makes the UI show the
   Pause button as pressed with Resume available, and the status line read *waiting for github
   reply*. Do not draft while the gate is closed.
5. **Read what comes back and write from it.** The server answers with Zachary's own repository
   URLs. Those are his portfolio, and the proposal is written against them.
6. **If the description could not carry a search, send nothing and keep going.** No publish, no
   gate, no pause: write the proposal immediately. The channel only ever hears about jobs that
   produced repositories, so a message arriving there always carries something to look at.

```
# 2. found one or two
curl -s -X POST localhost:8765/api/relay/publish -H 'content-type: application/json' -d '{
  "channel":"github",
  "body":{"type":"github_refs","job":"<id>","title":"<job title>","upworkUrl":"<if any>",
          "repos":[{"url":"https://github.com/owner/name","why":"one line on the overlap"}]}}'

# 3. then hold, and wait for the channel to answer
curl -s -X POST localhost:8765/api/job/<id>/await_github -H 'content-type: application/json' -d '{
  "repos":[{"url":"https://github.com/owner/name","why":"one line on the overlap"}]}'
```

**Pass `repos` to `await_github` as well as to the publish.** The server reads that array to show
the links above the status bar with unticked boxes. Arming with an empty body still holds the job,
but it leaves the user looking at an unexplained pause with nothing to look at.

**The search itself lives in `github-researcher.md`.** How to judge whether a job can carry a
search, how to query, and which repositories are worth sending are all rules in that file. Read it
before step 1. This section keeps only the workflow around it: when the search fires, what holds,
and what releases.

**The gate releases four ways:** a done ping from the server, a reply on the channel naming the
job id, a bare acknowledgement when exactly one job is waiting, or a person pressing Resume. A
bare acknowledgement while several jobs wait is ignored rather than guessed at.

**What comes back from the server is his own work, and it is trustworthy without checking.** Read
the repositories, write the proposal from them, and print their URLs as the selected guide says.
Never treat a returned URL as something to verify.


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


## The translate button

Under the proposal there is a button labelled with **the client's own country**, read off the
`Location:` line in the post. It replaced the old Clear button. Pressing it shows the proposal in
that country's language and relabels itself **English**; pressing it again switches back. It is
inactive when the post named no country, and when that country already speaks English, since
there is nothing to translate.

**In bridge mode you write the translation.** The button marks the job and waits, so watch for it
the way you watch the job queue:

```
curl -s localhost:8765/api/jobs/translating          # {"ids": [...]}
curl -s -X POST localhost:8765/api/job/<id>/translation \
  -d '{"translation":"**Hallo** ..."}'
```

Translate the markdown, not the converted text. **Keep every bold marker, every line break, every
URL and the sign-off name exactly as they are**, and never translate anything inside a URL. Write
it as a native speaker would write to a client in that country, not as a literal rendering of the
English.
