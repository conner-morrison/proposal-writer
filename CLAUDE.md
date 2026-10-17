# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a codebase**. It is a working folder for drafting **Upwork proposals**. The typical
task is: the user pastes a job description, and Claude writes a tailored proposal, a milestone
image, and an approach image.

There is no build, lint, test, or run step.

## Read the person profile first

**All personal information lives in the person profiles and nowhere else.** There is one profile
per person, all of them in `profiles/`: `Mario.md`, `Zachary.md` and `Connor.md` today, more
later. Identity, positioning, skills,
industries, portfolio with case-study links and verbatim metrics, working style, and voice. Read
the profile for whoever the proposal is for before drafting anything, and take every claim, link
and number from it. Never mix two people's facts.

**All proposal-writing instructions live in `guides/`,** and which one writes a given job is
decided by `decision-maker.md` rather than fixed. This file holds neither the profile nor the
guide, so each stays a single source of truth.

Files in this folder:

| File | Holds |
| --- | --- |
| `profiles/Mario.md`, `Zachary.md`, `Connor.md` | Everything personal, one file per person: profile, portfolio, metrics, voice |
| `profiles/connor-work-pool.md` | Connor's 134 works: 124 repositories plus 10 repo-less projects from his portfolio sites. His 6 live websites are already among those, so they are described there but not counted again |
| `profiles/zachary-github.md` | Zachary's 74 repositories across his two accounts, each one described from its README |
| `profiles/` | Every profile, and the resumes and exports they were built from. **Gitignored** |
| `guides/*.md` | The proposal-writing guides. `decision-maker.md` picks one per job |
| `github-researcher.md` | The rules for the repository search: judging a job, querying, what to send |
| `decision-maker.md` | Reading the client out of the post, then choosing which guide writes it |
| `CLAUDE.md` | This file: what the repo is and where everything lives |
| `ui/index.html` | Front end: pick a guide, pick a person, paste a JD, get copy-ready output |
| `.claude/commands/queue-worker.md` | `/queue-worker` — turns a session into the queue worker: analyse arrivals, write the `bid` ones, one at a time |
| `.claude/agents/queue-analyst.md` | Triage one row. **Haiku**, because it is rule-driven and most rows drop |
| `.claude/agents/proposal-writer.md` | Write one proposal end to end for the queue. **Opus**, because a paying stranger reads it |
| `.claude/agents/manual-writer.md` | Write the proposal a person clicked for. **Opus**. Carries no rules of its own, so the project is its single source |
| `proposals/` | Local archive, one markdown file per proposal, plus the images. **Gitignored** |
| `server.py` | Local server behind the UI. Start it with `./run-ui.sh` |
| `milestone-template.html` | Starting point for `proposals/milestones.jpg` |
| `approach-template.html` | Starting point for `proposals/my_approach.jpg` |
| `html-to-jpg.sh` | Renders either template to JPG |

**Proposals are archived locally.** Every proposal is written to `proposals/` as readable
markdown the moment it is posted back, named `<date>_<slug>_<person>_<id>.md` and carrying the
metadata, the screening answers, the questions and the original job description, so the file
stands alone. The `.jobs/<id>.json` record is the queue's working state; `proposals/` is the
durable copy. Both are gitignored, since they hold client names and rates and the repo is public.

Deleting a row in the history, or Clear all, removes the archived file too. The timed retention
purge does not: it trims the working list at 20:30 JST, it does not throw away finished work.

## The project ships, the data does not

**This repo is public, and it holds the tool rather than anybody's proposals.** Somebody else
should be able to clone it, drop their own people into `profiles/`, and have a working proposal
writer. So the split is between the project and the data, and it is not negotiable:

| | Where | Git |
| --- | --- | --- |
| **The project** — guides, rules, `decision-maker.md`, `github-researcher.md`, `analyzer-rule.md`, `CLAUDE.md`, `server.py`, the UI, the templates, the shell scripts | the root, `guides/`, `ui/` | **pushed** |
| **The people** — every profile, plus the resumes, LinkedIn exports and sample files they were built from | `profiles/` | **ignored** |
| **The work** — finished proposals, `milestones.jpg`, `my_approach.jpg`, the per-job HTML they were rendered from | `proposals/` | **ignored** |
| **The machinery's state** — the job queue, the relay threads, the worker's credentials | `.jobs/`, `.queue/`, `.threads/`, `.env` | **ignored** |

**Three rules follow from it.**

1. **A new profile goes in `profiles/`,** never at the root. The server discovers people by
   globbing `profiles/*.md` for single-word names, so adding a person is still just adding a file —
   it is simply a file in that folder. A hyphenated name there is supporting material rather than a
   person, which is how `connor-work-pool.md` sits beside `Connor.md` without becoming a fourth
   person in the dropdown.
2. **Images are written into `proposals/`.** `milestones.jpg` and `my_approach.jpg` are per-job
   output, so they belong with the proposal they illustrate and are ignored along with it. The two
   templates they are rendered from are project files and stay at the root.
3. **Never add a single file to `.gitignore` to fix a leak.** Add the pattern, or move the file
   into one of the two ignored folders. Naming files one at a time is how a confidential client
   tender reached the public remote on 2026-10-09.

**Nothing personal is ever written to a pushed path.** If a task seems to need one, it is the task
that is wrong.

## Whose work is whose

**Two people, two pools, and they must never be mixed.** Every repository name below belongs to one
of them, and a claim from one person's pool inside the other person's proposal is a false claim.

| Person | Their pool | Indexed in |
| --- | --- | --- |
| **Zachary** | `github.com/zacharywing303-art` (63 repos, the current one) and `github.com/ZWingman22` (11 repos, 2020 to 2022) | `profiles/zachary-github.md` |
| **Connor** | `github.com/connorodea` (124 of his own), plus six sites: `odeaworks.com`, `connorodea.com`, `juricratic.com`, `lockrooms.com`, `nexserp.com`, `preecursor.com` | `profiles/connor-work-pool.md` |
| **Mario** | no GitHub flow at all | — |

**The confusable part is the naming.** Zachary's current account names everything with a single
generic word, so `systems`, `learning`, `model`, `fully` and `touch` are his, and they tell you
nothing about their contents without the pool file. Connor's are descriptive, so `ShopifyScraper`
and `clawd-hub` are plainly his. **If a repository name is a bare common noun it is Zachary's; if
it reads like a product it is Connor's.** When in doubt, check the file rather than guess.

**Neither account is ever linked wholesale.** Print at most one repository URL, and only when the
selected guide says to.

## How to write a proposal

The instructions moved out of this file. **Read `decision-maker.md` first** to read the client
and choose the guide, then read that guide and follow it exactly. The choice is
`github-friendly` when the repository search returned something and `article-based` when it did
not; `brainstormed.md` stays in the folder and is used only when the user names it outright.

Two inputs decide every proposal:

1. **Which person** — a profile in `profiles/`. **Decided first**, because whose pool the
   repository search runs against depends on it. **An analysed search row has already decided it
   from its stack marks** — `Crypto` is Zachary outright, otherwise `Data` with no `AI` is
   Zachary and everything else is Connor, per `analyzer-rule.md` step 2 — and the server records
   that on the row. Like the guide it has two modes: the job carries
   `person_mode`, and `manual` means the user picked and you must write for whoever they chose.
   In `auto` the dropdown is only a default and `decision-maker.md` decides. Ask in the panel only
   when it is genuinely ambiguous and the answer would materially change the proposal.
2. **Which guide** — decided per job by `decision-maker.md`, not taken from the dropdown.
   `github-friendly` when the repository search returned something, `article-based` otherwise.
   **Decided last**, since the choice turns on what the search returned.

Both are recorded back so the UI and the archive name what actually wrote the letter:
`POST /api/job/<id>/person` and `POST /api/job/<id>/guide`. The server rejects either change on a
job whose matching mode is `manual`.

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

**One door in, and it is the queue.** Every job is created from a queue row: `/api/generate`
takes a `queue_seq` and nothing else, and the raw-`jd` shape it used to accept was removed on
2026-10-13. A row carries the posting, the Upwork link, the real title and the client name as
*fields*, so a job built from one gets all four — which is what the old shape could not do, since
it carried only flattened prose.

Rows reach the queue two ways, and there is no third:

| Route | How | Analysed? |
| --- | --- | --- |
| **The relay** | the server's own `relay_pull` long-polls the `jobs` channel and keeps every message as a row | only when the body says `source: search` |
| **A paste** | `POST /api/queue/paste -d '{"jd":"...","url":"..."}'` returns a `seq`, which the UI then generates from | never: a person pasting a post has already judged it |

A pasted row is handed back to the writer **verbatim**. Clients plant application instructions in
the posting, so nothing is prepended or appended to a paste — its link travels as a field on the
row instead. Pasted rows take seqs from 900000 up so they can never collide with a relay seq.

**What the relay allocated this project, and what it says to it.** The server is the only thing
that talks to the relay. Three endpoints cover it:

```
curl -s localhost:8765/api/relay/status                  # worker id, channels, last poll
curl -s -X POST localhost:8765/api/relay/enrol -d '{}'   # enrol this machine as a worker
curl -s -X POST localhost:8765/api/relay/publish  -d '{"channel":"github","body":{...}}'
```

- **The worker id is read off the live poll**, not a file: `/messages` names the caller on every
  answer, so a restart knows it again within one 25-second cycle. `connected` is true once it has.
- **Channels can only be observed**, since the relay exposes no way to list them. The map is
  seeded at boot from the channels recorded on stored queue rows and report threads, so the
  status is useful immediately rather than blank until the next job lands.
- **A notice is the relay talking to this project** rather than handing it work. `/messages`
  returns a `notices` array alongside `messages`, and until 2026-10-13 it was read by nothing —
  every notice the relay ever sent was dropped. Notices now become report threads, which is where
  an instruction message already goes, so they are read on the Report page.
- **Enrolment is a one-time handshake whose result lives on the relay**, keyed to `RELAY_WORKER`
  and `RELAY_TOKEN` in `.env`. It is harmless to repeat and answers `already` when it is. This is
  the one thing `proposal_bridge.py` did that was worth keeping; the endpoint enrols and can do
  nothing else, which is why the bridge itself is not missed.

**Bridge mode.** With no `ANTHROPIC_API_KEY` set, pressing "Write proposal" does not fail. It
queues the job and the running Claude Code session writes it. **This is unrelated to the
`proposal_bridge.py` relay bridge, which was deleted on 2026-10-13** — "bridge mode" only means
the writer is a Claude Code session rather than the API. If you are that session, watch the queue
and service it:

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

## Check the description is whole, before anything else

**A job description that ends mid-sentence is blocking.** Say so in chat and ask for the full text
before writing. Clients plant application instructions in the part people skim, most often a
required word at the top of the proposal, and missing one is an instant rejection however good the
letter is. A partial description therefore makes the whole write worthless rather than merely
weaker, and a note in the questions panel is not enough because it is read after the draft.

Fetching the Upwork link does not rescue it: Upwork answers a direct request with HTTP 403. The
fix is the user pasting the post.

**A planted instruction outranks the shape any guide prescribes.** If the post demands a specific
first word, that word goes first, ahead of the greeting or the opening line the guide asks for.

## The Profile tab

**Status, then Workers.** The tab answers "where is everything" before "who is doing it".

**Status** is three cards from `GET /api/stats`, refreshed every 4 seconds while the tab is open:
the queue broken down by feed (`search`, `vollna`, `upwork`), the analysed rows broken down by the
producer's decision (`bid`, `manual check`, `skip`) with the not-yet-analysed count beneath, and
the written proposals split by whether a boost time is set.

The counts are computed server-side on purpose, so what counts as a source, as analysed and as
written is defined once rather than re-derived in the page.

**One caveat the panel states itself:** *analysed* counts survivors only. A dropped row is deleted,
so the number is not a record of how much analysis has been done — six drops in one batch leave no
trace in it.

## Three workers, separated so they do not trip over each other

**The roles are not new. Running them independently is.** The project has always brought jobs in,
analysed them and written proposals; what changed on 2026-10-14 is that each has its own
lifecycle, so one can be paused without stopping the rest. The **Profile tab** shows all three
with their status and a Start, Pause, Resume and Stop button each.

| Worker | Does | Runs as | Model |
| --- | --- | --- | --- |
| **bringer** | holds the long poll on the relay, saves each arrival as a queue row | a **thread in the server** | — |
| **analyzer** | works queue rows in order: marks, person, client name | a Claude session | haiku |
| **writer** | writes proposals for the queue, from a `bid` decision | a Claude session | opus |
| **manual-writer** | writes the proposal when a person presses **Write proposal** | a Claude session | opus |

**Two writers, and a job belongs to whoever asked for it.** `initiator` is recorded at creation
and never changes: a job from the UI belongs to the **manual-writer**, a job the queue writer
created for itself belongs to the **writer**. The server enforces it — `?for=<role>` filters the
queued list and the claim answers 409 on anything the asker does not own — because on 2026-10-14
the queue writer polled the unfiltered list, found a job a person had just clicked, and wrote it.

**The two writers follow the same rules.** `manual-writer.md` deliberately contains no
proposal-writing rules of its own: it points at `CLAUDE.md`, `decision-maker.md`,
`github-researcher.md`, the profiles and the guides, and reads them on every run. So updating a
rule in this project updates both writers, with nothing to fall out of date.

**Five states, and the signal never flatters.** A role with nothing behind it reads **off**, not
running, whatever intent is stored against it — claiming "running" for a role no session had ever
attached to was the bug this replaced.

| Status | Signal | Means |
| --- | --- | --- |
| **off** | red cross | no session is allocated. Nothing is behind the role |
| **not started** | dark grey circle | a session is there, nobody has started it |
| **running** | green circle | working |
| **paused** | light orange circle | started, then paused. Finishes nothing new and waits |
| **error** | red circle | something unexpected. It stopped, and Night Fury was told once |

**`off` is derived, never stored.** A session counts as attached while it has heartbeated within
`WORKER_ATTACH_SECONDS` (90s), so one that dies shows as off within two missed beats. The bringer
is a thread in this process, so it is attached whenever the server is up and never reads off.

**Pressing Start on an unattached role stores the intent and nothing more.** The signal stays a
red cross until a session actually attaches, which is the honest answer: the server cannot start a
Claude session.

**Error is raised by the worker, not guessed at by the server.** `POST /api/worker/<role>/error`
with a one-line reason turns the signal red, stops the role, and rings **Night Fury** once —
machinery alarms are not job info, so Hungry never hears them. Resume clears the error, on the
assumption a person has looked.

**Each role names the session behind it.** A heartbeat carries `"session":"<name>"` and the panel
prints it beside the role, so "who is doing this" is recorded rather than inferred from the role
name. The link is **checked, not trusted**: a session whose name declares a different role gets a
409 and is not recorded, so a row can never light up for the wrong worker.

| Role | Session | Runs as |
| --- | --- | --- |
| **bringer** | none — it is a thread in this process | the server |
| **analyzer** | `analyzer-session` | a Claude session |
| **writer** | `auto-writer-session` | a Claude session |
| **manual-writer** | `manual-writer-session` | a Claude session |

The expected name per role is `WORKER_SESSION` in `server.py`, and the role a name declares is
derived by `role_from_session_name()` rather than matched literally — so renaming
`writer-session` to `auto-writer-session` does not break the link. Sessions are named with
`claude --name <name>` at launch or `/rename <name>` while running, and
`~/.claude/sessions/<pid>.json` maps a live pid to its name.

**Only the bringer really starts and stops**, because it is the only one inside this process.
Paused or stopped it does not poll at all, so no new rows arrive. The other two are sessions, so
the server holds the *intent* and the session obeys it: `POST
/api/worker/<role>/heartbeat` reports what it is on and answers whether it may proceed.

```
curl -s localhost:8765/api/workers                         # all three, with status
curl -s -X POST localhost:8765/api/worker/writer/pause      # start | pause | resume | stop
curl -s -X POST localhost:8765/api/worker/analyzer/heartbeat -d '{"current":"seq 674"}'
```

`run: false` in a heartbeat reply means **finish nothing new and wait**. State survives a restart,
so a paused writer stays paused, but `current` does not: nothing comes back claiming to be busy.

**The writer stands down for you, automatically.** Press **Write proposal**, **Submit and
rewrite** or **Answer screening** and the writer yields; it picks up again when your job lands.
You never queue behind it.

**The server tells the two apart by who asked.** A call to `/api/generate` with no `initiator` is
a person pressing a button; the writer sends `"initiator":"worker"` for jobs it creates itself, so
it does not stand down for its own work.

**Yielding happens between steps, never mid-step.** An armed github gate stays armed and an
unposted draft is held, not discarded. Standing down is not cancelling.

**Telegram is unchanged by any of this.** Hungry still fires once per undropped search row the
moment its analysis lands; Night Fury still carries proposal-done, boost-due and the stalled or
failed write. A paused worker simply produces no events to announce.

## Two sessions, and they do different jobs

**The work splits cleanly in two, so it can run in two sessions side by side.**

| Session | Does | How it starts |
| --- | --- | --- |
| **Conversation** | talking to the user: decisions, rules, changes to this repo and the server | an ordinary session |
| **Queue worker** | the loop: analyse each arrival, write the `bid` ones, one at a time, forever | `/queue-worker` |

**The worker splits again inside itself, by model.** Triage and writing want different things, so
`/queue-worker` orchestrates rather than working: `queue-analyst` runs on **haiku** because the
analysis is a rule table applied to forty rows a day, and `proposal-writer` runs on **opus**
because its output goes to a paying stranger. The models are pinned in each agent's frontmatter,
not chosen per call, so the split cannot drift.

**Only one of them should be working the queue.** The floor is held server-side —
`GET /api/work/inflight` reports it, and `POST /api/queue/<seq>/claim` is refused 409 while
anything else is in flight — so two workers cannot analyse the same row or write two proposals at
once. That guard is what makes a second session safe rather than a race.

**The conversation session should not take queue work while a worker is running.** Not because it
would corrupt anything, the claim prevents that, but because the user then cannot tell which
session is doing what.

## The order of work on one job

Pressing **Write proposal** starts this sequence. It is the same in Auto and Manual mode, and
nothing in it is optional.

0. **Settle who the proposal is for, and record it.** The job carries `person_mode`: `manual`
   means the user chose and you write for them, `auto` means you decide it per **First pick the
   person** in `decision-maker.md` and post it to `/api/job/<id>/person`. This is step zero
   because the search in step 1 is not the same search for every person — Connor's own work pool
   is read first, Zachary's is not.
1. **Search the person's own record** — their career in `profiles/<person>.md` and their work
   pool — for work genuinely close to the job, and **score the closest match out of 1**. This
   comes before the full analysis and before any drafting, on every new job id. Changed on
   2026-10-15: the search no longer starts on public GitHub, and no repository of anybody else's
   is ever published or printed again.
2. **At 0.7 or above, write from that work and publish nothing.** **Below 0.7, or nothing found**,
   post the **job id, the job title, the job description and the person's name** to the relay's
   `github` channel — those four fields and nothing else. Never repository URLs, never a score or a note explaining
   the search, and never the job's Upwork URL, which the relay deduplicates on and drops.
3. **Nothing of anybody else's is carried forward, because nothing of anybody else's is found.**
   The old step here was about forgetting repositories discovered by public search; that search
   is gone, so the hazard is gone with it. What follows stays true of any URL that is not in the
   person's own record.

   **"Forget them" means every one of these, not just the proposal:**

   | Where | Rule |
   | --- | --- |
   | the proposal | never — this one has held |
   | the analysis | never |
   | the note to the user (`/notes_reply`) | **never** — broken on job `9f6f9d6c`, 2026-10-13 |
   | the chat report back to the user | **never** — broken on the same job, same day |
   | a scratch file left on disk | delete it with the publish |
   | a later summary, even "the two I found were…" | **never**, not even by owner name |

   **How to not break it again.** Build the publish body in a file, publish from that file, and
   delete the file in the same step, so the names are never echoed after the send. Evaluating
   candidates means seeing them once, before publishing; after the publish they are gone. When
   something has to be said about them afterwards, say it by shape and count — "two repositories,
   one a QGIS project with a written report, one a travel-time catchment toolbox" — never by
   owner or repository name.

   **The only URLs that may ever reach a proposal are the ones the server sends back**, and since
   2026-10-14 not even those directly: they are read, recorded in the pool, and the letter is
   written from the pool entry.
4. **Hold at the gate.** Arming it presses Pause and sets the status line to *waiting for github
   reply*. Do not draft while the gate is closed. **Nothing found means no publish, no gate, no
   pause** — go straight to step 6.
5. **The reply describes experience of his that the record did not hold.** Not repositories —
   facts about what this person has done. Write the proposal **referencing that new information
   mainly**, with the profile and pool as the context around it. Then, once the proposal is
   posted, **append what you learned to his own files** — the pool for a piece of work, the
   profile for a skill or an experience — with the date and where it came from. That is what
   makes the loop worth having: the record grows, the same question is never asked twice, and
   the next job scores against a fuller picture.

   The older instruction below still governs any URL that does arrive: On the user's instruction of 2026-10-14: **never paste a returned URL
   straight into the proposal.** The order is read, record, then write:

   a. **Read each repository properly** — the file tree, the README, and the libraries actually
      imported in the code. Not the description, which is often absent or wrong.
   b. **Write what you found into `profiles/zachary-github.md`**: what the project does, what it
      demonstrates about his experience, the tech stack the code actually evidences, and the URL.
   c. **Write the proposal from that pool entry**, the same way a Connor letter is written from
      his pool. The letter is built on work you have understood, not on a link you were handed.

   **This is also the check that catches a mirror.** A returned repo created minutes ago, empty,
   with a tree identical to what was just published is not his work and must not be recorded or
   cited. Reading it is how you find that out; pasting the link is how you miss it.
6. **Read the client out of the post, then pick the guide, but only in Auto.** The person was
   settled at step zero, so this step is only about the guide. The job carries
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

**Replies carry the job id, agreed with the counterpart on 2026-10-14, and that is what makes two
open gates safe.** Before it, every reply arrived with no id and the gate released whichever job
had waited longest — right while one search was open, a coin toss once two were, and a job could
be released by a reply that answered a different search and then write from the wrong
repositories. With the id the match is exact and any number of gates can be open at once.

**A reply arriving without an id is now a regression, not the normal case**, so it is treated as
one: the oldest job is still released rather than stalling, but it is marked
`github_match: "guessed"` and the mismatch is logged loudly. Say so in the note to the user when a
letter was written off a guessed match.

**Short replies are detected.** `github_counts` records what was published against what came back,
and `github_partial` is set when fewer repositories return than were asked about or `failed` is
non-zero. A partial answer says so in the job note instead of reaching the writer looking
complete.

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

**Screening questions remembered after the proposal is written.** The **Answer screening** button,
beside Copy prompt, asks for the answers on their own. It does not rewrite anything: the proposal,
the guide and the open questions stay exactly as they are, and the answers appear in the Screening
answers panel under the draft as though they had been pasted in before the write. Watch for it the
way you watch the job queue:

```
curl -s localhost:8765/api/jobs/screening            # {"ids": [...]}
curl -s -X POST localhost:8765/api/job/<id>/screening_answers -d '{"answers":[...]}'
```

**Answer them against the letter that already exists**, which means reading the posted proposal
first. The client reads the answers and the cover letter together, so an answer that leads with a
different project, or contradicts a claim the draft already made, costs more than a vague one
would. Posting the answers clears the flag and empties the queue. **Do not touch `/result`**, and
do not open a new round of questions: this is a gap being filled, not a new attempt at the job.

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

**Every new job searches GitHub before anything else.** The repository search is the *first* step,
ahead of the job analysis and ahead of any drafting. Both modes: a job typed into Manual gets the
same search as one ticked off the Auto queue.

**A rerun searches too.** A queue row is kept after its proposal is written, so the same post can
be run again and arrives as a fresh job id with identical inputs. Search it again anyway. Do not
reuse the repositories an earlier gate returned for that post, and do not skip the publish on the
grounds that the answer is predictable: a rerun is a fresh attempt, and the search is the first
step of that attempt rather than a cached input to it.

**The only thing that does not search is a revision of the same job id** after answers come back
from the questions panel, which rewrites an existing letter rather than making a new attempt.

**The sequence, in order.** Rewritten 2026-10-15: the search looks inward and the channel is
asked about the person, never about repositories.

1. **Search the person's own record** — their career in `profiles/<person>.md` and their work
   pool — for work genuinely close to the job.
2. **Score the closest match out of 1.** Honestly: a shared keyword is not 0.7, a job he has
   substantially done before is.
3. **0.7 or above: write from that work.** No publish, no gate, no waiting.
4. **Below 0.7, or nothing found: publish the job id, the job title, the job description and the
   person's name** to the `github` channel — **those four and nothing else.** The question is
   about one named person's experience, so the responder has to be told whose. No repository URLs, no score, no
   explanation of what was searched, and not the job's Upwork URL, which the relay drops as a
   duplicate. Then arm the gate and hold; the UI shows Pause pressed and the status line reads
   *waiting for github reply*.
5. **The reply is his experience, not repositories.** Write the proposal referencing that new
   information mainly, with the profile and pool as context.
6. **Afterwards, append what you learned to his record** — the pool for a piece of work, the
   profile for a skill — with the date and its source. The record grows, and the same question
   is never asked twice.
7. **Connor is never scored and never published.** Search his career and pool, take one or two
   of his closest works, and write. Whatever the search turns up, there is no gate for him.

```
# 4. the best match scored below 0.7, so send the job. Four fields, nothing else.
curl -s -X POST localhost:8765/api/relay/publish -H 'content-type: application/json' -d '{
  "channel":"github",
  "body":{"job":"<id>","title":"<job title>",
          "description":"<the job description>","person":"Zachary"}}' '

# 3. then hold, and wait for the channel to answer
curl -s -X POST localhost:8765/api/job/<id>/await_github -H 'content-type: application/json' -d '{
  "repos":[{"url":"https://github.com/owner/name","why":"one line on the overlap"}]}'
```

**Pass `repos` to `await_github` as well as to the publish.** The server reads that array to show
the links above the status bar with unticked boxes. Arming with an empty body still holds the job,
but it leaves the user looking at an unexplained pause with nothing to look at.

**For Connor the search never leaves his own work pool.** The sequence above is Zachary's and it
does not apply to him at all. **This is why the person is decided before the search rather than
after**: the two people have different first moves, so the search cannot start until the job knows
who it is for.

1. **Search `profiles/connor-work-pool.md` first.** His 134 own works are pooled there by domain,
   his GitHub merged with the projects on his site, and a match is the best possible answer
   because the work is genuinely his. Read the repository before claiming anything about it.
   **Where a work has a live demo, send the demo and the source together**: ten of them are
   verified working, and a client who can click something beats a repository they will not read.
2. **A hit ends it.** No publish, no gate, no pause: write the proposal from what you found and go
   straight to the draft.
3. **A miss is still a miss, and the search stops there.** On the user's instruction of
   2026-10-14: **never look for a similar project outside his pool.** No public GitHub search, no
   publish, no gate, no waiting. Write the proposal from the nearest thing he has actually built,
   or from his skills and approach where nothing fits, and say so honestly rather than reaching
   for somebody else's repository.

   **Why the rule is right, not just an instruction.** The pool holds 134 of his own works across
   seven domains, which is a better answer than public search can give for almost any post. And
   the gate has never once returned usable portfolio: what comes back is repositories created
   seconds earlier as copies of whatever was just published. Sending Connor down that path spends
   minutes to arrive at something unprintable.

**Never link his account** whichever path ran: 631 of his 755 public repositories are forks. The
rules for reading his repositories are in `profiles/connor-work-pool.md`; `Mario.md` has no GitHub flow at
all.

**The search itself lives in `github-researcher.md`.** How to judge whether a job can carry a
search, how to query, and which repositories are worth sending are all rules in that file. Read it
before step 1. This section keeps only the workflow around it: when the search fires, what holds,
and what releases.

**The gate releases four ways:** a done ping from the server, a reply on the channel naming the
job id, a bare acknowledgement when exactly one job is waiting, or a person pressing Resume. A
bare acknowledgement while several jobs wait is ignored rather than guessed at.

**What comes back from the server is his own work, but it is not proposal material until it has
been read.** Superseded on 2026-10-14 the older line that called a returned URL trustworthy
without checking: read each repository, record what it contains and the stack it evidences into
`profiles/zachary-github.md` with its URL, and write the letter from that entry. **A returned URL
is never pasted directly into a proposal.**

Two things this buys. The letter describes work somebody has actually looked at, which is what
makes it specific enough to be worth reading. And **the pool grows with every job** — a
repository read once is described for every future proposal, so the same reading is never done
twice.

**It is also the only thing standing between us and a mirror.** Every time the gate has answered,
some of what came back was created seconds earlier as a copy of what we had just published. A
repo with no history, no content and a tree matching the search result is not his: do not record
it, do not cite it, and say so in the note to the user.


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
mirrored to `.jobs/<id>.json`. Build `proposals/milestones.jpg` and `proposals/my_approach.jpg` as usual and send them
in chat, since the output box is text only. With an API key set, the same button calls the API
directly and the queue is unused.


## The analyzer

**A job arriving from the `search` feed is analysed the moment it lands.** Nothing else triggers
it: the `upwork` and `vollna` alerts are not analysed, and this happens before any decision to bid,
so it is separate from writing a proposal.

**The mark comes from the sender, not from what the body claims.** `source_for_sender()` decides
it, and the order matters:

| Mark | Sender | What happens |
| --- | --- | --- |
| **search** | the general vollna search producers, listed in `SEARCH_SENDERS` | analysed on arrival, Hungry told, `bid` written unasked |
| **vollna** | a Vollna **alert** bot such as `zachary-upwork-vollna-alert` — it watches a saved search and forwards matches with no verdict | never analysed |
| **upwork** | Upwork's own notification and invitation feeds | never analysed |

`zachary-upwork-vollna-alert` contains both words and is a **Vollna alert**, so vollna is tested
first — corrected on 2026-10-15, along with six rows that had been marked `upwork`.

**An unknown sender gets no mark at all, never `search`.** Defaulting to the search feed is how
seq 930, a Vollna alert, came to be marked `search`: the `fields` reader defaulted the source
instead of deriving it, and a `search` mark is what puts a row into the automatic
analyse-and-write path.

**Two producers are the general vollna search.** The original relay worker and
**`vollna-scraper`** (`w-f55a0da9e1d62940e731f688cd727774`), confirmed on 2026-10-15 as playing
the same role. Both are listed in `SEARCH_SENDERS` and recognised **by sender**, not only by the
`source` their body carries, so either one's rows get the full automatic treatment even if the
label is missing. Everything below about "the search feed" means both of them.

**Everything automatic belongs to the general vollna search alone.** The analysis, the stack
marks, the drop, **and writing the proposal.** Nothing fires by itself for a job from any other
feed.

**A job that does not look like a job raises an alarm now.** A message on the `jobs` channel from
a known search producer that fails the job-shape test is logged loudly and announced on Night
Fury, because it is a bug rather than a conversation. Seq 861 on 2026-10-15 was a real job from
`vollna-scraper` that sat on the Report page for hours: its keys were the capitalised shape
(`Job title`, `Job link`) and normalisation had been skipped, because `"search"` — the value
normalisation *writes* — was missing from the set of values it reads. The body is kept on the
thread either way, so such a message can always be recovered into a row.

**A queued row is not a request to write it.** The server's own `relay_pull` keeps *every*
message on the `jobs` channel as a queue row: the `upwork` and `vollna` alerts, and anything else
that crosses it, including a Vollna report email that became job `647c254c` on 2026-10-12. So a
row appearing in the queue means a message arrived, **not that a person chose it.**

**A row is not a job, though, and that is the safeguard.** Until 2026-10-13 `proposal_bridge.py`
also watched the channel and posted every message to `/api/generate` with its own `--person
Zachary --guide brainstormed` flags, so each arrival became a *written-up job* nobody had picked —
and, because the bridge sent prose rather than fields, one with no Upwork link on it. The bridge
is gone and `/api/generate` now takes a queue seq and nothing else, so a job exists only once
somebody or something has chosen the row it came from.

**Therefore: write it only when the job came from the search feed with `decision: bid`, or when a
person asks for it.** For anything else, leave it queued and say what landed. Jobs now carry their
`source` so the two can be told apart. Writing an alert job unasked spends a Connect on a post
nobody picked, and that is how 35 proposals went out for a 0% reply rate in the week to
2026-10-12.

The server flags the queue row on arrival and it shows on the card as *analysing…*. Watch for the
work the way you watch the job queue:

```
curl -s localhost:8765/api/queue/analyzing            # {"seqs": [...]}
curl -s localhost:8765/api/queue                      # the rows, with their decision and reason
curl -s -X POST localhost:8765/api/queue/<seq>/analysis \
  -d '{"analysis":"..."}'
```

`POST /api/queue/<seq>/analyze -d '{"redo":true}'` asks for one by hand, or re-runs an analysis
that is already there.

**One thing at a time, and the server holds the floor.** On the user's instruction of 2026-10-13:
a new job arriving is analysed, but **the next piece of work does not start until the current one
has finished** — no analysing one row while another is mid-analysis, and nothing started while a
proposal is being written. Claim before working, and the claim is refused if anything else is in
flight:

```
curl -s localhost:8765/api/work/inflight             # {"busy": false, "work": null}
curl -s -X POST localhost:8765/api/queue/<seq>/claim # 409 while something else holds the floor
curl -s -X POST localhost:8765/api/queue/<seq>/release   # let go without having analysed it
```

Two things hold the floor: a **row claimed for analysis** (`analysing_since` set, no analysis
yet), and a **job being written** (status `working` or `revising`). A *queued* job holds nothing —
it exists but nothing has picked it up. Posting the analysis, or the proposal, frees the floor.

**Release an abandoned claim.** A claim is a file on disk, so it outlives the session that made
it; one left behind blocks every later piece of work until it is released or the analysis lands.

**The card has three states, not two.** `awaiting analysis` means the flag is set and nothing is
running — the honest reading, since the analyzer is a Claude Code session and a row sits untouched
when none is watching. `analysing…` shows only while a row is actually claimed. `analysed` is the
finished state, and the stack marks beside the title are its conclusion. Before 2026-10-13 every
unanalysed row said `analysing…`, so three rows that nobody had touched looked like work in
progress for two hours.

**A row waiting to be analysed raises nothing.** There was briefly a *Waiting on the analyzer*
alarm at 8 minutes; it was removed on the user's instruction the same day, because a row that has
not been analysed yet carries nothing a person can act on — no verdict, no person, no client name.
The card saying `awaiting analysis` is the whole of the signal.

**The alarm comes after the analysis, because that is when there is something to say.** The
analysis is what produces the three facts worth a notification: **dropped or not**, **which
person**, and **the client's name** where the reviews gave one. So Hungry's message leads with
them — see the Telegram section below.

**What to analyse is in `analyzer-rule.md`, and nowhere else.** Read it before writing anything.
It now carries the rules: the stack marks, the client's name out of their own reviews, the Telegram
message, and writing the proposal when the decision is `bid`.

**The analysis is posted with its stack marks**, which are what the card actually shows. The card
displays status only, `analysing…` then `analysed`, and the conclusion is the marks beside the
source:

```
curl -s -X POST localhost:8765/api/queue/<seq>/analysis \
  -d '{"analysis":"...","stack":["Data","AI"]}'
```

`Data`, `AI`, `ML`, `Full`, `Crypto` are the only accepted marks. **Two mark sets drop the row:**
an empty list, meaning no engineer here can do the work, and **`Full` on its own**, meaning they
could but plain web or application work with no data, AI, ML or crypto angle is not worth a
Connect (user instruction, 2026-10-14). `Full` beside another mark is kept and is common. A
dropped row sends no Telegram.

**A dropped row is deleted from the queue**, not hidden: nothing here can do the work, so the row
goes. The drop is therefore final — no `redo` can reverse it and the written analysis goes with the
file — so an empty stack is a deletion rather than a label. **Clear all**, beside Refresh, empties
the rest of the queue in one action; Refresh only ever *pulls* from the relay and never removes
anything, which is why the two are separate buttons.

**The client's past contracts** arrive inside the description text, not as fields, and are parsed
out of it: `GET /api/queue/<seq>/history` returns them, and the card shows the count on a button.
Reviews written *to* the client are where their name comes from.

## When a write stalls, the phone hears about it

**Writing starts at one of exactly two moments, and nothing else starts it:**

1. **A person presses "Write proposal"** with a queue row ticked.
2. **A `bid` decision is acted on** — the job came from the general vollna search, the analyzer
   did not drop it, and the decision was `bid`.

Both create the job, so **`job["created"]` is the start of the clock** either way. Two alarms run
off it, both on Night Fury, both once per job:

| Alarm | Fires when | Message |
| --- | --- | --- |
| **Proposal done** | a `/result` lands with proposal text | *Proposal done* (or *rewritten*) + the title + **who it is for**, and who wrote it + the link |
| **Still writing** | 8 minutes (`WRITE_SLOW_AFTER`) since writing started and there is still no proposal | *Still writing* + how long + the status, and it says so when the job is held at the github gate |
| **Failed to write proposal** | a `/result` came back with no proposal text, or a job reached `done` with an empty one | *Failed to write proposal* + what went wrong + the status |

**Why it exists.** Before 2026-10-13 the only proposal alarm fired on a *finished* draft, so a job
that was created and then simply sat said nothing at all — and silence read exactly like success.
Two jobs stalled queued for 218 and 323 minutes that day with no word either way.

**What stays silent, deliberately:**

- **A dropped job**, which rings neither bell: `job["dropped"]`, or a queue row the analyzer
  dropped. A refusal is not a failed write.
- **A cancelled job**, which is a person's own decision.
- **A job with a proposal in it**, however long it took — the done alarm covers that.

**The 8-minute alarm is a warning, not a verdict.** It does not cancel anything and the write may
still land; the done alarm fires normally afterwards. It fires during a github gate hold too,
since a long hold is exactly the thing worth knowing about.

**Both flags are stored on the job** (`notified_slow`, `notified_failed`), so they survive a
restart and cannot double-fire. **Neither alarm is ever sent from inside `JOBS_LOCK`** — a
Telegram round trip must not hold up every other request, which is why an empty `/result` records
`write_error` and the 30-second watcher sends it rather than the request handler.

## Two Telegram bots, and they do not overlap

| Bot | Token in `.env` | Carries |
| --- | --- | --- |
| **Night Fury** `@hiro_upwork_handler_bot` | `TELEGRAM_BOT_TOKEN` | proposal done, boost due, a stalled or failed write, a worker in error |
| **Hungry** `@hiro_upwork_bot` | `TELEGRAM_JOBS_BOT_TOKEN` | job info from the analyzer |

The split is the point: the bot a message arrives from says whether it is a job worth reading or a
proposal worth sending, before either is opened. **Never send job info on Night Fury**, and never
send an alarm on Hungry.

**Hungry rings when an analysed job is worth reading, and on two tests only:** the row came from
the **general vollna search** (`body.source == "search"`), and it was **not dropped**. Sent from
the analysis handler, which is the only place job info is sent, and announced **once** per row —
`notified_jobs` on the row. `POST /api/queue/<seq>/analyze -d '{"redo":true}'` clears that flag,
so a re-analysis whose verdict changed can announce afresh.

One message. The headline carries the title, then the verdict on one line — **the stack marks,
the person they chose and the producer's decision** — then the budget, the client's rank and
location, **the client's name** where there is one, and the link. The posting follows underneath,
**and only the posting**: the work history, the project
info block, the client block and the screening questions are all cut off the end, at whichever of
them comes first. Each has its own home — the queue card and its history and screening buttons —
and in a phone message they only bury the job. User instruction, 2026-10-15; before it the
message carried the whole description, up to 13,700 characters of which 11,000 was apparatus.

**The decision is the most actionable part**, which is why it sits on the verdict line: `bid`
means the auto writer will write this one unasked, `manual check` and `skip` mean it waits for a
person.

**The producer's reason is not sent.** It was added beside the decision on 2026-10-14 and removed
the same day: the message is for judging a job at a glance, and the reasoning lives on the queue
card and in the stored analysis for anybody who wants it.

**Those three facts are why it fires here and not on arrival.** Whether the job is dropped is
expressed by the message existing at all; the person comes straight out of the marks; the client's
name comes from the reviews. None of the three exists before the analysis, which is what makes
this the only useful moment to send anything.

**Nothing rings on arrival.** A new row is not announced — the queue in the UI already shows it
and the phone message was noise. Hungry hears about the *analysed* job, once a verdict exists.

**Dropped rings neither bell**, which is the rule that makes the whole thing legible: Hungry stays
quiet because no engineer here can do the work, and Night Fury stays quiet because the `/result`
posted to a dropped row is a refusal rather than a proposal.

**A dropped job rings neither bell.** Hungry hears nothing because no engineer here can do the
work, and Night Fury hears nothing because the `/result` posted to a dropped row is a refusal
rather than a proposal. Post it with `"dropped": true` alongside the text, which is what tells the
server to stay quiet.

**Each bot has its own sender, and they cannot be confused.** Both call `_telegram_post(token,
chat, ...)`; `telegram_send()` passes Night Fury's pair and `telegram_jobs_send()` passes
Hungry's, and every message names its bot in the log (`telegram[hungry] sent …`). Until
2026-10-13 `TELEGRAM_JOBS_BOT_TOKEN` and `TELEGRAM_JOBS_CHAT_ID` were read by **nothing**: Hungry
was configured and never once used.

`telegram_new_job()` is gone, deleted the same day. It had been dead since 2026-09-24 and it
called `telegram_send()`, so anyone re-enabling it would have pushed job info down Night Fury —
the one thing this section forbids. There is no longer a wrong-bot path to re-enable.

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
