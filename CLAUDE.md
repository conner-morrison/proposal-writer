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
| `server.py` | Local server behind the UI. Start it with `./run-ui.sh` |
| `milestone-template.html` | Starting point for `milestones.jpg` |
| `approach-template.html` | Starting point for `my_approach.jpg` |
| `html-to-jpg.sh` | Renders either template to JPG |

Proposals are never saved to disk. They live in the reply only.

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

**Never block on either.** Write the best proposal you can from the JD alone, decide every open
point yourself, and post the result. Then post the user-facing ones as a question list:

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

**Ask as few questions as possible.** Three is a lot. Only raise something where a different
answer would materially change the proposal, and always state the assumption you shipped with. If
a question would be more useful asked of the client than of the user, it belongs in the proposal
instead.

Post the proposal back as **markdown**; the page converts it to Unicode bold itself. Jobs are
mirrored to `.jobs/<id>.json`. Build `milestones.jpg` and `my_approach.jpg` as usual and send them
in chat, since the output box is text only. With an API key set, the same button calls the API
directly and the queue is unused.

