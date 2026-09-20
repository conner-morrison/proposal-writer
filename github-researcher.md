# GitHub Researcher

**What this file is.** The rules for finding one or two GitHub repositories genuinely close to
what a job describes. Nothing else. How to judge a job, how to query, and which repositories are
worth sending.

Everything the system does with what you find — publishing to the channel, arming the gate,
waiting for the release — is workflow and lives in `CLAUDE.md`.

Everything below is the rule as it stands today. Add to it rather than rewriting from memory.

---

## When the search runs

**On the first write only, and before anything else.** Pressing **Write proposal** starts with the
repository search, ahead of the job analysis and ahead of any drafting. A rewrite never searches
again. Both modes behave the same: a job typed into Manual gets the same search as one ticked off
the Auto queue.

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
