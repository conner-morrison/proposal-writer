# GitHub Researcher

**What this file is.** The rules for finding one or two GitHub repositories genuinely close to
what a job describes. Nothing else. How to judge a job, how to query, and which repositories are
worth sending.

Everything the system does with what you find — publishing to the channel, arming the gate,
waiting for the release — is workflow and lives in `CLAUDE.md`.

Everything below is the rule as it stands today. Add to it rather than rewriting from memory.

---

## What the search is now, and it is not public GitHub

**Changed on 2026-10-15. The search looks inward first, and what gets published is the job, not
other people's repositories.**

Every person has two sources of truth about what they have done: their **career and experience**
in `profiles/<person>.md`, and their **work pool** — `profiles/connor-work-pool.md` or
`profiles/zachary-github.md`. Those are searched first, always.

### 1. Search the person's own sources

Read the profile and the pool against the job. You are looking for work that is genuinely close
to what the post describes — the same mechanism, the same domain, or the same shape of problem.

### 2. Score the closest match, out of 1

Judge how close the best match really is, as a number between 0 and 1:

| Score | What it means |
| --- | --- |
| **0.7 and above** | genuinely similar work. Write the proposal from it and publish nothing |
| **below 0.7**, or nothing found | his recorded work does not answer this post |

Be honest with the number. A shared keyword is not 0.7; a job he has substantially done before
is. Inflating it to avoid the gate produces a letter built on a claim that does not hold, which
is the failure this whole rule exists to prevent.

### 3. Below 0.7: ask the channel about *him*, not about GitHub

**Publish the job id, the job title, the job description and the person's name to the `github`
channel. Those four and nothing else.**

```
curl -s -X POST localhost:8765/api/relay/publish -H 'content-type: application/json' -d '{
  "channel":"github",
  "body":{"job":"<job id>","title":"<job title>",
          "description":"<the job description>","person":"<Zachary|Connor|Mario>"}}'
```

**The person is required**, added 2026-10-16: the question being asked is about one named
individual's experience, and the responder cannot answer it without knowing whose. In practice it
is always Zachary, since Connor is never published and Mario has no repository flow — but it is
sent explicitly rather than assumed.

**No repository URLs — not his, not anybody's.** Public GitHub is not searched at all any more, so
there is nothing of a stranger's to send. User instruction, 2026-10-16.

**Nothing else in the body either.** No score, no note on what was searched, no person, no type.
A first version of this carried all of those; they were the sender explaining itself, and the
instruction is three fields.

**Do not include the job's Upwork URL.** The relay deduplicates any body carrying it and drops the
message silently, which is what made every earlier github publish vanish.

### 4. Arm the gate and hold

`POST /api/job/<id>/await_github`. Do not draft while it is closed. The gate releases on the
reply, on a done ping, or on a person pressing Resume. If nothing answers in a few minutes,
release it and write from what the profile already holds.

### 5. The reply is his experience, not a repository

What comes back describes **work this person has done that the pool and the career do not
record**. Read it as new facts about him.

**Write the proposal referencing that new information mainly**, combined with what the profile
and pool already said. The new material is the answer to the post; the existing record is the
context around it.

### 6. Afterwards, write the new information into his record

**This is not optional, and it is what makes the whole loop worth having.** Once the proposal is
posted, append what you learned to the person's own files — the pool for a piece of work, the
profile for experience or a skill. Say where it came from and when.

So the pool grows every time the channel teaches us something, the same question is never asked
twice, and the next job scores against a fuller record.

## Connor never publishes, and is never scored

**For Connor, search his career and his work pool and stop there.** No similarity score, no job id
posted, no gate, no waiting — whatever the search turns up. Find **one or two** of his closest
works and write from them.

He has 134 of his own works across seven domains with ten verified live demos, so the pool
answers almost any post; and where it does not, the honest letter is written from his skills and
approach rather than from a question put to a channel. User instruction, 2026-10-14, reaffirmed
2026-10-15.

Mario has no repository flow at all.

---

## When the search runs

**On every new job, and before anything else.** Pressing **Write proposal** starts with the
repository search, ahead of the job analysis and ahead of any drafting. Both modes behave the
same: a job typed into Manual gets the same search as one ticked off the Auto queue.

**Including a rerun of a post already searched.** Queue rows are kept after writing, so the same
job can come round again. Search it again rather than reusing the last answer. Only a revision of
the same job id, after answers come back from the panel, skips the search.

**This file does not apply to Connor at all.** On the user's instruction of 2026-10-14, a
proposal for Connor is written from **his own work pool and nothing else**: search
`profiles/connor-work-pool.md`, which holds 134 of his works by domain with ten verified live
demos, and stop there. **Never go looking for a similar project outside it.** No public GitHub
search, no publish, no gate, no hold — a match goes straight to the draft, and a miss goes
straight to the draft too, written from the nearest thing he has genuinely built or from his
skills where nothing fits.

Everything below is for **Zachary**, who starts here directly. Mario has no repository flow.

## Whether the job can carry a search at all

**It qualifies when the post names something implementable:** a stack, a platform, a data domain,
or a concrete artefact. "Apify actor for CRE listings", "GA4 and GTM audit", "NFL power ratings in
Sheets", "Power BI Embedded with row-level security" all qualify.

**It does not qualify when the post is only a role shape with no buildable object.** "We need an
operations lead", "an analyst to support reporting". There is nothing to match on, and a forced
keyword match is worse than none: it puts noise on the channel and stalls the write behind a
pointless gate.

When it does not qualify, send nothing and write the proposal immediately. No publish, no gate, no
pause. The channel only ever hears about jobs that produced repositories, so a message arriving
there always carries something worth opening.

## How to search

Search the GitHub API directly rather than guessing at URLs:

```
curl -s -H 'accept: application/vnd.github+json' \
  "https://api.github.com/search/repositories?q=<terms>&sort=stars&order=desc&per_page=5"
```

**Query the distinctive half of the job, not the generic half.** Almost every data job mentions
dashboards, SQL and reporting; those words match tens of thousands of student projects and tell
you nothing. Search the thing that makes this post different from the last one. On a Power BI
post, `powerbi embedded row-level-security` finds the integration work, while
`power bi dax star schema` returns a wall of coursework dashboards.

**Run two or three queries, not one.** Vary the angle: the platform, the mechanism, the artefact.
A single query that returns nothing usually means the vocabulary was wrong, not that nothing
exists.

## The date window

**Only repositories whose work falls between February 2019 and April 2026 qualify.** Anything
outside that window is not a candidate, however well it matches the job.

Narrow the search itself with a date qualifier rather than filtering by hand afterwards:

```
curl -s -H 'accept: application/vnd.github+json' \
  "https://api.github.com/search/repositories?q=<terms>+pushed:2019-02-01..2026-04-30&sort=stars&order=desc&per_page=5"
```

**Then confirm on the commit history, because the qualifiers lie.** `created:` is the date the
repository was made on GitHub and `pushed:` is the date it was last written to, and neither is the
date the code was written. A repository created in 2026 can hold commits from 2018, which is
exactly the trap: `ssdotai/Report-Portal-PowerBI` reports `created: 2026-07-01` and carries
commits from September 2018. Read the commits before sending:

```
curl -s "https://api.github.com/repos/<owner>/<name>/commits?per_page=10" \
 | python3 -c "import sys,json;[print(c['commit']['author']['date']) for c in json.load(sys.stdin)]"
```

The commit dates are the ones that have to sit inside the window. Use the search qualifier to cut
the candidate pool, and the commit history to decide.

## Choosing what to send

**One or two repositories, never more.** The point is a close match, not coverage.

**Judge closeness by what the repository actually contains**, which means reading the file tree,
not the description. A repo whose tree shows the mechanism the job is about is a match; a repo
whose README uses the same nouns is not.

**Say plainly in the `why` what actually overlaps.** One line, naming the specific thing shared. A
repo that merely shares a keyword is noise the channel does not need, and the `why` is where that
gets caught.
