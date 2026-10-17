# Connor's Work Pool

**What this file is.** Every piece of Connor's own work in one searchable pool, so a job
description can be matched to the closest thing he has actually built. Four sources are merged
here, read 2026-10-12:

- **His GitHub**, `github.com/connorodea` — the 124 repositories that are his own, out of 755
  public (631 are forks). This supplies the source code, the language and the dates. **124 is the
  stable figure**: re-counted against the API on 2026-10-12 and unchanged, while the public total
  and the fork total drift upward as he forks things, so expect those two to read higher than this.
- **His consultancy site**, `odeaworks.com/work` — 39 curated projects. This supplies the
  client-facing name, a written description, the tech stack, and in twelve cases a **live demo**.
- **His personal portfolio**, `connorodea.com` — 46 repositories and 8 featured projects, four of
  them with full case-study pages. This supplies the deepest writing: problem, approach,
  architecture and what each one taught him.
- **Three product sites**, `juricratic.com` (8 pages, deep and careful), `lockrooms.com` (~25
  routes, the most completely shipped) and `nexserp.com` (4 pages, a marketing shell). Each is a
  shipped build in its own right, and for all three the product itself is private or gated, so the
  site is the only thing a client can be shown.

**134 works in total**, and the arithmetic matters because the sources overlap heavily:

| | Count |
| --- | --- |
| His own repositories on GitHub (755 public, 631 of them forks) | **124** |
| Works with no public repository, from the two portfolio sites | **+10** |
| **Total in this pool** | **134** |

**The six live websites are not a third category, and adding them is double counting.** All six
were already counted above: `odeaworks.com`, `connorodea.com` and `preecursor.com` exist as
repositories inside the 124, and `juricratic.com`, `lockrooms.com` and `nexserp.com` are
Juricratic, Lockrooms and NexSerp inside the 10. Earlier versions of this file added a further
**+6** and reached 140, and an older one said 129; both are wrong and neither should be quoted.
**134 is the number.**

**The sites still get their own section, because a site is its own kind of evidence.** Shipping
`juricratic.com` — eight pages of dense technical writing — is a different demonstration from
building the simulation engine behind it, and for the three whose product is private or gated the
site is the only thing a client can be shown. So read that section as six works wearing a second
hat, not as six extra works. Three of the rows carry both a source link and a live URL for exactly
that reason.

**The sites add description, not works.** `odeaworks.com/work` lists 39 projects and links 36
repositories; `connorodea.com` features 8 and links 46. **Every one of those 46 is already inside
the 124**, and 33 of odeaworks' 36 are too, so neither site adds a work that GitHub did not
already have. What they add is a name, a description, a tech stack, a demo URL and an industry.

The 10 with no repository are: QuickVisionz, QuickVisionz SAM3, MortgageAI, NexSerp and Upscaled
Inventory from `odeaworks.com`; Sightline, Juricratic, APIDistributed, Lockrooms and
MetroDealReport from `connorodea.com`.

**`odeaworks.com` says "40+ projects shipped" on its homepage, and the list is 39.** Verified
2026-10-12. No other page on that site holds works.

**Every one of the 124 is named somewhere below.** Checked by diffing the names printed in this
file against the GitHub API on 2026-10-12: it listed 123, and the one missing was
`inquizitai-frontend`, now added to the Inquizit row and to the small-SaaS cluster. It was dropped
because it is the second half of a work already in the pool — the Next.js front end whose Vercel
deployment *is* the Inquizit demo, while `inquizit` itself is the generation API. **So Inquizit is
one work across two repositories**, which is why the count of works is 134 rather than 135.

**The two sites position him differently, and that is useful.** `odeaworks.com` speaks as an
agency — *"We build software that thinks"* — while `connorodea.com` speaks as one engineer:
*"Applied AI Engineer · Denver. I build AI-native products end to end, architecture through
ship."* Match the framing to the job: the agency voice for a scoped engagement or a build, the
individual voice for a contract role on somebody's team.

The two sources complement each other and neither is sufficient alone. GitHub tells you what is
real and how big it is; the site tells you what it does and whether you can show it to somebody.

---

## How to use this on a job

1. **Start with his own industry classification** if the job names a sector, since that section
   is his judgement rather than a guess: Video / Media, Infrastructure, Commerce, Real Estate,
   Health, Finance, Consumer. Otherwise **match on the shape of the work**, because a warehouse job
   and a liquidation job want the same inventory pipeline.
2. **Prefer a work with a live demo.** A client who can click something and see it running is
   worth more than a repository they will not read. Those ten are listed first for that reason.
3. **Give both links when both exist**: the source for credibility, the demo for the visual. One
   work with both beats three with neither.
4. **A private repository is not a dead end.** Four works have a full case-study page on
   `connorodea.com/work/`, and five works are live websites with their own URL. Both are linkable
   whether or not the code is public. Send a case study when the client wants to see how he thinks,
   and a site when they want to see something he shipped.
5. **Read the repository before describing it.** The description here comes from his own site, so
   it is positioning rather than an audit. Size is the quickest sanity check: under about 50 KB is
   rarely a working system.
6. **Never link the account**, whichever work you pick. 631 forks is the first thing a visitor
   sees, and it argues against him.

**What you can say about any work in this pool:** what it does, the stack it is built on, roughly
how substantial it is, when he last worked on it, and whether there is something to look at. That
is enough to answer a job description without inventing anything.

---

## Built on an open-source base, so describe the contribution accurately

**All 134 works in this pool are his and all are usable.** A handful were built on top of an
existing open-source project rather than from nothing, which is ordinary engineering and is exactly
what a permissive licence is for. The only thing that matters for a proposal is **saying what he
added**, rather than implying he wrote the whole stack, because two of the upstreams are well known
enough that a client may recognise them.

| Work | Upstream it builds on | What to say |
| --- | --- | --- |
| `ai-hedge-fund-saas` | `virattt/ai-hedge-fund`, MIT, 63,954 stars | His own description is the right one: *"complete SaaS transformation with authentication, subscriptions and monetization."* The product layer is his. Do not imply he wrote the hedge-fund engine |
| `AIrealestateassistant` | `AleksNeStu/ai-real-estate-assistant`, MIT, 315 stars | Natural-language property search built out as a SaaS. Lead on the product and the search experience |
| `medscribd` | scaffold, origin not recorded | Fifty of its fifty-seven commits are his. Safe to lead on, and it has a working demo |
| `metapromptmaker`, `Youtube_Automation_TikTok_To_Youtube_Enhanced`, `facebook-scraper` | not established | Commit names other than his appear, which is normal across machines, accounts and collaborators. Treat as his |

**Commit author names are not a reliable test of authorship**, and this pool should not be filtered
by them. His own commits appear under at least six names across these repositories: `Connor O'Dea`,
`Connor ODea`, `connor odea`, `connorodea`, `cpodea5` and `MacBook Pro 2016`, plus
`gpt-engineer-app[bot]`, `v0` and `AIWholesail Bot` for the tooling he builds with. A name that
looks unfamiliar is far more likely to be another of his machines or accounts than someone else.

**One licence housekeeping note**, which is about compliance rather than authorship and is the
user's to deal with, not a proposal's. MIT asks that the copyright notice be kept in copies.
`AIrealestateassistant` carries an Apache-2.0 file instead of the original MIT notice, and
`ai-hedge-fund-saas` has no licence file. Restoring the upstream notices alongside his own would
settle both, and neither affects whether the work can be shown.

## Works with a live demo, which are the strongest to send

Ten unique demos across twelve cards. **Verified 2026-10-12** — status noted where it is not
simply working.

| Work | What it is | Stack | Code | Live |
| --- | --- | --- | --- | --- |
| **Inquizit** | AI-powered assessment and quiz generation platform — mint fresh assessments with AI and instant grading. **Two repositories**: `inquizit` is the generation API, `inquizitai-frontend` is the UI the demo serves. | TypeScript, Next.js, AI | [inquizit](https://github.com/connorodea/inquizit) 387 KB, [inquizitai-frontend](https://github.com/connorodea/inquizitai-frontend) 102 KB | https://v0-inquizitai-frontend.vercel.app |
| **MedScribd** | Medical documentation platform with AI agent-powered clinical note generation, patient management, and workflow automation. | TypeScript, Next.js, AI | [medscribd](https://github.com/connorodea/medscribd) | https://v0-medscribd-agent-ui.vercel.app |
| **MortgageAI** | AI-powered mortgage processing and analysis platform with intelligent loan evaluation and automation. | TypeScript, Next.js, AI | none | https://mortgageai.dev |
| **NexSerp** | A SaaS marketing site and interactive product demo for a programmatic-SEO API: six-stage animated walkthrough, four-tier pricing page, developer-experience section. **Reference the site itself, not the product behind it.** | TypeScript, Next.js | none | https://nexserp.com |
| **QuickLotz Logistics** | End-to-end logistics and freight management platform for liquidation distribution operations. | TypeScript, React, PostgreSQL | [quicklotzlogistics](https://github.com/connorodea/quicklotzlogistics) | ~~https://www.quicklotzlogistics.com~~ **parked domain** |
| **QuickLotz WMS** | Enterprise warehouse management system powering inventory tracking, 3PL logistics, and real-time analytics for circular economy operations. | TypeScript, React, PostgreSQL | [upscaled-quicklotz-dashboard](https://github.com/connorodea/upscaled-quicklotz-dashboard) | https://v0-sourcing-platform-ui.vercel.app |
| **RateMyPsych** | Provider rating and review platform for mental health professionals with search, matching, and NPPES data integration. | TypeScript, Next.js, PostgreSQL | [ratemypsych.com](https://github.com/connorodea/ratemypsych.com) | https://ratemypsych.com |
| **Upscaled Distribution** | B2B wholesale distribution platform connecting suppliers with buyers in the circular economy. | TypeScript, Next.js, React | [upscaledist.com](https://github.com/connorodea/upscaledist.com) | https://v0-upscaledist-com.vercel.app |
| **Upscaled Inventory** | Inventory management portal for Upscaled Inc distribution operations with real-time stock tracking. | TypeScript, React | none | https://inventory.upscaledinc.com **login wall** |
| **VideoCallSync** | Video conferencing synchronization platform for seamless multi-party calls and recording. | TypeScript, WebRTC, Real-time | [videocallsync](https://github.com/connorodea/videocallsync) | https://v0-videocallsync.vercel.app |
**Six of the ten sit on default `v0-*.vercel.app` hostnames**, which tells a reader the UI was
v0-generated and never given a domain. They work and they look finished, but on a job sensitive
about production maturity prefer one on its own domain: `mortgageai.dev` or `ratemypsych.com`.
`nexserp.com` is also on its own domain and is fine to send **as a site he built**, which is how
the pool frames it. Just never present it as a working API or quote its figures. See **Do not cite
these**.

---

## His live websites, each a shipped work with a URL

**Six sites, all his, all verified live on 2026-10-12.** Each one is a deliverable in its own
right — design, build, copy, SEO and deployment — separate from whatever product sits behind it.
**The URL is the reference**, which matters most for the three whose code is private.

| Site | What it is | Scale | Stack | Repo |
| --- | --- | --- | --- | --- |
| [lockrooms.com](https://lockrooms.com) | Creator content vault with a paywall. **The most completely shipped**: working sign-up, revenue-share pricing, 13 vertical landing pages, explore directory, glossary, blog, DMCA and privacy | 198 KB landing, 161 KB room page, ~25 routes | Next.js | private |
| [juricratic.com](https://juricratic.com) | Litigation simulation product site. **The deepest**: 8 pages covering engine, simulation, matter state, governance, security and firm | 255 KB landing, 35–65 KB per sub-page | Next.js | private |
| [odeaworks.com](https://odeaworks.com) | His AI consultancy. 39-project portfolio, services, pricing, blog, tools, resources | 63 KB work page, 9 routes | Astro | [`odeaworks.com`](https://github.com/connorodea/odeaworks.com) 3.6 MB |
| [connorodea.com](https://connorodea.com) | Personal portfolio. Raymarched WebGL hero, GitHub-generated shipping log, 4 case-study pages | 71 KB landing, 24 KB per case study | Next.js static | [`connorodea.com`](https://github.com/connorodea/connorodea.com) 275 KB |
| [nexserp.com](https://nexserp.com) | Programmatic-SEO product site: 6-stage animated demo, 4-tier pricing, developer-experience section | 48 KB landing, 4 routes | Next.js | private |
| [preecursor.com](https://www.preecursor.com) | Applied-AI consultancy. Capabilities, 4 industry pages, labs, leadership, careers, glossary, a comparison page and a work section. **Its four case studies are illustrative, not client work — see below** | 108 KB landing, 87 KB work index, ~20 routes | Next.js static | [`preecursor`](https://github.com/connorodea/preecursor) 708 KB |

**Why these are worth referencing as sites rather than only as products.** Three of the five have
private or access-gated products, so the site is the only thing a client can actually look at. And
the web work is independently good: `juricratic.com` sustains eight pages of dense technical
writing, `lockrooms.com` ships the whole compliance surface including DMCA takedown handling, and
`connorodea.com` carries a raymarched WebGL hero and a shipping log generated from the GitHub API.

**What each one is the best evidence for:**

- **Front-end and design craft** — `connorodea.com` for the WebGL and the typography,
  `nexserp.com` for the animated product demo
- **Programmatic SEO done rather than sold** — `lockrooms.com`, whose 13 `/for/` vertical pages
  plus a 94 KB glossary and 6 comparison posts are a worked example of exactly what `nexserp.com`
  advertises as an API
- **Technical writing and information architecture** — `juricratic.com`, eight pages that stay
  specific and hedge honestly throughout
- **Static-site and build tooling** — `odeaworks.com` on Astro, `connorodea.com` as a Next.js
  static export
- **Compliance and policy surfaces** — `lockrooms.com` DMCA, DMCA-report and privacy;
  `juricratic.com` security and governance

**Two caveats carried from the checks.** Reference `nexserp.com` as a site only, never as a
working API, and never quote its figures. Reference `juricratic.com` as a site and an
architecture, not as a product a client can sign up for today.

## The four case studies, his strongest written material

From `connorodea.com/work/`. **Each page is linkable even where the repository is private**, which
makes them the thing to send when a client wants depth rather than a demo. The prose is also the
best model for his voice: a sharp problem, three design decisions, and an honest lesson.

| Work | One line | Stack | Code | Page |
| --- | --- | --- | --- | --- |
| **Cutroom** | An AI-native video editor that cuts from the transcript | TypeScript, React, Vite, Hono, Claude | [`cutroom`](https://github.com/connorodea/cutroom) **public** | `connorodea.com/work/cutroom/` |
| **Sightline** | Tells Shopify merchants when AI recommends their store | Next.js, TypeScript, Postgres, Shopify | private | `connorodea.com/work/sightline/` |
| **Juricratic** | Litigation strategy modelled as a game rather than a guess | Python, Neo4j, LangGraph, Anthropic | private | `connorodea.com/work/juricratic/` **and the live site `juricratic.com`, 8 pages** |
| **APIDistributed** | An API marketplace built for agents, not portals | Cloudflare Workers, TypeScript, MCP, D1 | private | `connorodea.com/work/apidistributed/` |

### Cutroom — video, AI-assisted editing

**Problem.** Editing long-form footage is mostly search: an editor knows the moment they want and
spends the session scrubbing for it. Tools sold as AI editors have been wrappers that generate a
rough cut you then fix in a real NLE, so the work happens twice.

**Approach.** Transcribe on ingest and treat the transcript as the primary timeline surface, so
deleting a sentence performs the cut. Build a real editor underneath it — media pool, multi-track
timeline, colour, delivery — so the transcript is an interface onto a project rather than a
preprocessor. Keep the model advisory: it proposes selects, it never commits a change unasked.

**Architecture.** React and Vite with a custom canvas timeline renderer; Hono API with streaming
responses for long transcription jobs; Claude for select reasoning with ASR for the transcript;
FFmpeg pipeline generating proxies on import.

**His lesson, quotable.** *"The hard part was never the model. It was making a timeline that stays
responsive at hour-long durations while a second view of the same project stays in sync with it."*
Use this on any job that is nervous about AI features in a real application.

### Juricratic — the live site, `juricratic.com`

**This is the strongest single reference in the pool.** His flagship company has a deep, careful
product site: a main page plus seven substantial sub-pages (`/engine`, `/simulation`,
`/matter-state`, `/governance`, `/security`, `/firm`, `/request`), each 35 to 65 KB of real
content. Verified 2026-10-12.

**What it says it is.** *"Live adversarial matter intelligence."* It models a lawsuit as an
imperfect-information game so attorneys can rehearse it: fork the matter, simulate the adversary,
and watch leverage and risk deform as the facts change. Its own framing: *"Most legal AI
summarizes documents. Juricratic models the fight."*

**The intelligence stack**, which is the part to quote on an architecture job: Ingestion (pleadings,
docket, discovery parsed into source-linked matter objects, every assertion tied to its page and
line) → Matter Ontology (parties, claims, defenses, filings, citations as a case-scoped graph) →
Claim & Evidence Matrix (each element of each claim mapped to the evidence carrying it, and the
gaps) → Argument Map → Simulation Engine.

**The synthetic bench** is four role agents, each bound by the evidence graph, the posture and the
venue: **Judge** (applies standards, evaluates motions), **Jury** (narrative credibility and
sympathy), **Opposing Counsel** (hunts the attack surface), **Client/Party** (settlement
psychology, incentives, agency costs). Described as *"a state-constrained red team, not a
chatbot."*

**The privilege boundary**, from `/security`, which is the best compliance-architecture material
in either person's pool: the boundary is treated as an architectural invariant, with deterministic
local redaction of pattern-PII before any egress, matter-scoped role-aware access, encryption in
transit and at rest, no training on client matters, and every figure traceable to a document with
an audit trail.

**Data and stack.** CourtListener docket ingestion with offline-first saved exports; Python,
Neo4j, LangGraph and Anthropic per the case study; a deterministic solver core, and the site is
explicit that *"no ML is required to be correct; the engine is the moat."* Beliefs are exposed as
**user dials**, described as *"swept parameters, never claimed as calibrated truth."*

**Four equations** are given on the page: matter evolution, counterfactual branching, possibility
space, and strategic alpha as the maximum over reachable futures.

**What makes it safe to reference, unlike his other product site.** It carries **no fabricated
social proof at all**: no customer logos, no user counts, no uptime or SLA claims. And it hedges
carefully and consistently throughout — *"simulation, not prediction"*, *"not legal advice"*, *"a
simulation artifact, never a prophecy"*, *"never claimed as calibrated truth"*. Checked for the
NexSERP pattern and found none of it.

**Use it for:** legal tech, multi-agent and adversarial simulation, knowledge graphs, RAG that has
to cite its source, human-in-the-loop design, and any job where PII or privilege has to be
enforced architecturally. **Its hedging language is also the model to copy** when writing about
AI reliability for a client who is rightly suspicious of it.

**The one caveat.** The product is access-gated — `mailto:access@juricratic.com` and a
*"Request access"* call to action, no public sign-up — and `connorodea.com` marks Juricratic **In
build** with a private repository. So reference the **site** and the architecture it documents, and
do not imply a client can go and use the product today.

### Sightline — commerce, LLM visibility monitoring

**Problem.** Purchase research is moving into assistants, where there is no rank to check and no
impressions to read, so a merchant cannot tell whether ChatGPT recommends them or a competitor.

**Approach.** A prompt set per merchant reflecting how buyers actually ask, in category, comparison
and problem-first phrasings rather than brand lookups. Query each engine on a schedule from clean
sessions so results reflect the model and not an accumulated conversation. Score presence and
sentiment as **separate** series, because they fail independently.

**Architecture.** Next.js embedded in Shopify admin; ChatGPT, Perplexity and Claude queried on a
schedule; Postgres holding a time series per prompt per engine.

**His lesson, quotable.** *"Answers vary enough run to run that a single query says almost nothing.
The product only became useful once it reported trends across repeated runs instead of
point-in-time results."* This is the best thing in either site to use on an LLM-evaluation, AI-SEO
or model-monitoring job.

### Juricratic — legal, game theory over court data

**Problem.** Litigation strategy runs on intuition and war stories, and attorneys make settlement
and posture calls with no model of how other parties will respond.

**Approach.** Model the case as what it structurally is, a multi-party game with payoffs,
incomplete information and sequential moves. Compute equilibria over realistic settlement
positions and model co-defendant dynamics where cooperating and defecting carry asymmetric costs.
Ground payoffs in real court data rather than assumed numbers.

**Architecture.** Python game-theoretic solver over party payoffs; Neo4j for parties, claims and
precedent relationships; LangGraph orchestrating multi-step case analysis; CourtListener and
eyecite for citation extraction.

**His lesson, quotable.** *"The model is only as good as the payoff estimates, and those are where
domain expertise is irreplaceable. The valuable output turned out to be sensitivity analysis:
which assumptions actually change the recommendation."* Strong on any job where a model has to be
trusted by a professional, and it pairs with the human-in-the-loop framing in `Connor.md`.

### APIDistributed — infrastructure, MCP at the edge

**Problem.** API marketplaces were built for a human browsing a catalogue and copying a key.
Agents need to discover, authenticate and transact programmatically, and every existing
marketplace makes that the hard path.

**Approach.** Make the marketplace MCP-native so an agent can enumerate and call APIs through a
protocol it already speaks. Run the whole surface at the edge, because an agent chaining calls pays
every millisecond more than once. Keep provider onboarding to an OpenAPI spec, so listing an API is
configuration rather than an integration project.

**Architecture.** Cloudflare Workers, global by default; D1 for the catalogue with KV for hot
routing; an MCP server exposing the catalogue as tools; per-call metering at the edge.

**His lesson, quotable.** *"Edge runtimes change what you can assume. A surprising amount of
standard Node middleware simply does not exist there, and the constraint pushed the design toward
something simpler than what I would have built on a server."* Use on MCP, agent-infrastructure or
Cloudflare work.

## The other four featured on connorodea.com

| Work | One line | Domain | Status | Code |
| --- | --- | --- | --- | --- |
| **GeoStamp** | Geotags photos for local SEO in seconds | Commerce | **Live**, the only one marked so | [`geostamp`](https://github.com/connorodea/geostamp) |
| **ScreenRec Studio** | A native macOS screen recorder and editor | Video / Media | In build | [`screenrec-studio`](https://github.com/connorodea/screenrec-studio) |
| **Lockrooms** | A creator content vault with a paywall: upload anything, organise it like Drive, charge for access like Patreon. **See the live-site note below — `connorodea.com` describes this one wrongly** | Creator tools / SaaS | **live product, sign-up open** | private |
| **MetroDealReport** | A publication for real-estate investors, not a listings feed | Real Estate | In build | private |

**`lockrooms.com` is the most complete product of his I have checked**, and his own portfolio
undersells it. Verified 2026-10-12.

`connorodea.com` lists Lockrooms as *"multi-sport film study as a subscription"* under Video /
Media. The live site is broader: *"Your content vault. Your paywall. Upload anything, organise it
like Drive, and charge for access like Patreon — for coaches, consultants, educators, and every
creator."* Sports coaching is one of thirteen verticals, not the product.

**What is actually shipped**, which is more than any other Connor product site: working
`/sign-in` and `/sign-up`, a revenue-share pricing page (*"Free to start. Pay only when you earn"*,
98 KB), **thirteen vertical landing pages** at `/for/` (coaches, consultants, course-creators,
designers, educators, filmmakers, musicians, newsletter-creators, photographers, podcasters,
trainers, writers, artists-makers), a `/explore` directory, a 94 KB creator-monetisation
`/glossary`, six SEO blog posts targeting *"patreon alternatives"* and *"dropbox alternative"*
style queries, and real `/dmca`, `/dmca/report` and `/privacy` pages. A sample room at
`/room/john` runs to 161 KB.

**It carries no fabricated social proof** — no customer logos, no user counts, no SLA. The only
soft spot is `/explore` describing *"public, live rooms from creators of every kind"* over three
demo rooms.

**So reference it as a shipped creator-monetisation SaaS**, and it is the strongest thing in the
pool for a payments, paywall, multi-tenant SaaS, creator-platform or programmatic-SEO job: the
thirteen vertical pages and the glossary are themselves a worked example of programmatic SEO, and
the DMCA and privacy pages show he built the compliance surface rather than only the happy path.

**Seven of the eight featured works are marked "In build"**, and only GeoStamp says Live. So on a
job where the client wants to click something working, `odeaworks.com`'s ten verified demos are the
better source and this site is the weaker one. Where the client wants to see how he thinks, the
case studies win outright.

**One claim here does check out.** The site says *"forty-six shipped across seven industries in
the last eight months"*, and **49 of his own repositories were created in that window** — so it is
accurate and slightly conservative, which is unusual among his numbers.

## Documented on the site, no demo

His own descriptions and stacks, which are the most quotable text in the pool.

| Work | What it is | Stack | Code | Size |
| --- | --- | --- | --- | --- |
| **QuickVisionz** | YOLO-based computer vision sorting pipeline with barcode scanning, automated product classification, and thermal label printing. | Python, YOLO, OpenCV | none | site only |
| **LunaScopeAI** | AI-powered astrological insights platform with professional chart generation and personalized life guidance. | C, AI, Data Viz | [LunaScopeAI](https://github.com/connorodea/LunaScopeAI) | 30215 KB |
| **AI YouTube Pipeline** | Full-stack AI video generation pipeline with DeepInfra integration for automated content creation at scale. | Python, TypeScript, DeepInfra | [ai-youtube-pipeline-deepinfra](https://github.com/connorodea/ai-youtube-pipeline-deepinfra) | 48 KB |
| **YouTube Automation Pipeline** | Enhanced YouTube automation tool with React web UI for creating, scheduling, and publishing AI-generated video content at scale. | Python, React, YouTube API, AI, Software Engineering | [Youtube_Automation_TikTok_To_Youtube_Enhanced](https://github.com/connorodea/Youtube_Automation_TikTok_To_Youtube_Enhanced) | 135 KB |
| **ClawdHub** | Interactive terminal IDE for spawning and orchestrating multiple Claude Code agents in real time. 13,000 lines across 26 files. | Python, Textual, Claude SDK | [clawd-hub](https://github.com/connorodea/clawd-hub) | 65 KB |
| **AI Amazon Seller Central** | AI-powered Amazon marketplace management — automated listing optimization, pricing, and inventory intelligence. | Python, Amazon API, AI | [AI_AmazonSellerCentral](https://github.com/connorodea/AI_AmazonSellerCentral) | 35721 KB |
| **AI Call Spread Trader** | AI-assisted options trading platform combining quantitative analysis, ML pattern recognition, and LLM reasoning for execution. | Python, Finance, ML | [ai-call-debit-spread-trader](https://github.com/connorodea/ai-call-debit-spread-trader) | 56 KB |
| **AI Schematic Generator** | Generate electronic circuit schematics from natural language descriptions using Anthropic's Claude 3.5 Sonnet. | Python, Claude API, Electronics | [ai-schematic-generator](https://github.com/connorodea/ai-schematic-generator) | 23 KB |
| **QuickVisionz SAM3** | Serverless GPU inference service for warehouse computer vision — SAM 3 model deployed on-demand for real-time object segmentation. | Python, SAM 3, GPU, Serverless | none | site only |
| **AI YouTube Analyzer** | Conversational interface for analyzing YouTube videos — talk with any video and extract insights, summaries, and key moments. | TypeScript, AI, YouTube API | [AIYoutubeAnalyzer](https://github.com/connorodea/AIYoutubeAnalyzer) | 13 KB |
| **AI Real Estate Assistant** | AI-powered property search and real estate advisory SaaS — find your perfect property with natural language queries. | Python, AI, SaaS | [AIrealestateassistant](https://github.com/connorodea/AIrealestateassistant) | 6908 KB |
| **GRIDIRON** | Custom YOLO8 ML model trained on football footage and synthetic datasets for real-time player and formation detection. | JavaScript, YOLO8, ML | [GRIDIRON](https://github.com/connorodea/GRIDIRON) | 61337 KB |
| **ClipsMachine** | Automated video clip extraction and compilation tool for creating highlight reels from long-form content. | Python, FFmpeg, AI | [ClipsMachine](https://github.com/connorodea/ClipsMachine) | 103 KB |
| **Vidmation** | End-to-end AI video automation platform. Generates faceless YouTube content with AI narration, captions, and automated publishing. | Python, FastAPI, Claude API, FFmpeg | [aividio](https://github.com/connorodea/aividio) | 2640 KB |
| **Shopify Store Builder** | Automated Shopify store creation and product listing tool with AI-generated content. | Python, Shopify API, AI | [ObsidiaanShopifyStoreBuilder](https://github.com/connorodea/ObsidiaanShopifyStoreBuilder) | 128 KB |
| **Facebook Marketplace Scraper** | Marketplace scraper with flexible search, real-time alerts, anti-detection, and reliable data extraction. | Python, Scraping | [facebook-scraper](https://github.com/connorodea/facebook-scraper) | 220 KB |
| **Pinintel** | Pinterest intelligence and analytics platform for content strategy and trend analysis. | TypeScript, Analytics, API | [Pinintel](https://github.com/connorodea/Pinintel) | 240 KB |
| **UPC Database Scrapers** | Scalable product data collection pipeline for barcode and UPC database aggregation. | TypeScript, Web Scraping, Data | [upc-database-scrapers](https://github.com/connorodea/upc-database-scrapers) | 296 KB |
| **Upscaled Inventory Processing** | Automated inventory data processing pipeline for wholesale distribution — parsing, enrichment, and stock management. | Python, Data Processing, Automation, &rarr; | [Upscaled_inv_processing](https://github.com/connorodea/Upscaled_inv_processing) | 34307 KB |
| **GoDaddy CLI** | Beautiful command-line interface for managing domains and DNS records via the GoDaddy API. | Shell, GoDaddy API, CLI | [godaddypy-cli](https://github.com/connorodea/godaddypy-cli) | 21 KB |
| **Meta Prompt Maker** | Build brief generator for crafting optimized LLM prompts — clean finance-friendly UI for prompt engineering. | Next.js, TypeScript, AI | [metapromptmaker](https://github.com/connorodea/metapromptmaker) | 109 KB |
| **LiqOS** | Bloomberg Terminal-style inventory management system for liquidation operations with real-time data. | TypeScript, Terminal, PostgreSQL | [LiqOS](https://github.com/connorodea/LiqOS) | 318 KB |
| **QuickReturnz** | Returns and RMA management system for the QuickSuite warehouse platform. | TypeScript, React, PostgreSQL | [quickreturnz](https://github.com/connorodea/quickreturnz) | 49 KB |
| **AgentAgent** | Multi-agent orchestration system for Claude Code — run a master agent that controls worker agents in parallel via tmux. | Shell, tmux, Python | [AgentAgent](https://github.com/connorodea/AgentAgent) | 26 KB |
| **AdPilot** | Powerful CLI for the Meta/Facebook Marketing API — manage ad campaigns, audiences, and creatives from the terminal. | TypeScript, Meta API, CLI | [adpilot](https://github.com/connorodea/adpilot) | 255 KB |
| **Facebook Car Flipping** | Automated Facebook Marketplace vehicle sourcing and flipping tool with deal analysis. | Python, Scraping, Automation | [FacebookMarketplaceCarFlipping](https://github.com/connorodea/FacebookMarketplaceCarFlipping) | 187 KB |
| **EbayAutolister** | Production-ready eBay listing automation CLI with GitHub-style navigation and bulk inventory operations. | Python, eBay API, CLI | [EbayAutolister](https://github.com/connorodea/EbayAutolister) | 82 KB |
---

## His own industry classification, from the connorodea.com shipping log

**He sorts his 46 portfolio repositories into seven domains himself.** This is the fastest way to
match a job, because it is his judgement about which industry each piece of work belongs to rather
than mine. A tick in the last column means the work also has a written description and sometimes a
demo on `odeaworks.com`; everything else is described only by its repository.


**Video / Media** (12)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`ClipsMachine`](https://github.com/connorodea/ClipsMachine) | 103 KB | 2025-11 | yes |
| [`ai-faceless-yt`](https://github.com/connorodea/ai-faceless-yt) | 66 KB | 2026-08 | — |
| [`videocallsync`](https://github.com/connorodea/videocallsync) | 145 KB | 2026-01 | yes |
| [`youtube-transcript-analyzer`](https://github.com/connorodea/youtube-transcript-analyzer) | 12 KB | 2026-04 | — |
| [`aividio`](https://github.com/connorodea/aividio) | 2 MB | 2026-04 | — |
| [`ryvio-ai`](https://github.com/connorodea/ryvio-ai) | 76 KB | 2026-04 | — |
| [`ytauto`](https://github.com/connorodea/ytauto) | 149 KB | 2026-04 | — |
| [`framewright`](https://github.com/connorodea/framewright) | 134 KB | 2026-05 | — |
| [`sonyobs`](https://github.com/connorodea/sonyobs) | 160 KB | 2026-08 | — |
| [`cutroom`](https://github.com/connorodea/cutroom) | 996 KB | 2026-06 | — |
| [`screenrec-studio`](https://github.com/connorodea/screenrec-studio) | 187 KB | 2026-06 | — |
| [`reelwire`](https://github.com/connorodea/reelwire) | 278 KB | 2026-06 | — |

**Infrastructure** (11)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`AgentAgent`](https://github.com/connorodea/AgentAgent) | 26 KB | 2026-02 | yes |
| [`clawd-hub`](https://github.com/connorodea/clawd-hub) | 65 KB | 2026-04 | yes |
| [`ai-blog-system`](https://github.com/connorodea/ai-blog-system) | 27 KB | 2026-04 | — |
| [`PaywallScraper`](https://github.com/connorodea/PaywallScraper) | 5 KB | 2026-04 | — |
| [`premium-website-builder`](https://github.com/connorodea/premium-website-builder) | 72 KB | 2026-04 | — |
| [`LiqOS`](https://github.com/connorodea/LiqOS) | 318 KB | 2026-04 | yes |
| [`OpenHarness`](https://github.com/connorodea/OpenHarness) | 9 MB | 2026-04 | — |
| [`auditiq`](https://github.com/connorodea/auditiq) | 107 KB | 2026-04 | — |
| [`odeaworks.com`](https://github.com/connorodea/odeaworks.com) | 3 MB | 2026-06 | — |
| [`python-mastery-cli`](https://github.com/connorodea/python-mastery-cli) | 744 KB | 2026-06 | — |
| [`preecursor`](https://github.com/connorodea/preecursor) | 708 KB | 2026-07 | — |

**Commerce** (10)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`upc-database-scrapers`](https://github.com/connorodea/upc-database-scrapers) | 296 KB | 2025-12 | yes |
| [`Pinintel`](https://github.com/connorodea/Pinintel) | 240 KB | 2025-12 | yes |
| [`upscaledist.com`](https://github.com/connorodea/upscaledist.com) | 533 KB | 2026-01 | yes |
| [`adpilot`](https://github.com/connorodea/adpilot) | 255 KB | 2026-04 | yes |
| [`cartai`](https://github.com/connorodea/cartai) | 40 KB | 2026-04 | — |
| [`FacebookMarketplaceCarFlipping`](https://github.com/connorodea/FacebookMarketplaceCarFlipping) | 187 KB | 2026-04 | yes |
| [`supply-pulse`](https://github.com/connorodea/supply-pulse) | 242 KB | 2026-04 | — |
| [`microsoft-ads-manager`](https://github.com/connorodea/microsoft-ads-manager) | 35 KB | 2026-04 | — |
| [`ShopifyScraper`](https://github.com/connorodea/ShopifyScraper) | 256 KB | 2026-06 | — |
| [`geostamp`](https://github.com/connorodea/geostamp) | 178 KB | 2026-06 | — |

**Real Estate** (3)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`AIrealestateassistant`](https://github.com/connorodea/AIrealestateassistant) | 6 MB | 2025-12 | yes |
| [`wholesale-lead-finder`](https://github.com/connorodea/wholesale-lead-finder) | 116 KB | 2026-04 | — |
| [`aiwholesail`](https://github.com/connorodea/aiwholesail) | 182 MB | 2026-09 | — |

**Health** (4)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`medscribd`](https://github.com/connorodea/medscribd) | 1 MB | 2026-01 | yes |
| [`medscribd-agent-ui`](https://github.com/connorodea/medscribd-agent-ui) | 74 KB | 2026-01 | yes |
| [`ratemypsych.com`](https://github.com/connorodea/ratemypsych.com) | 124 KB | 2026-01 | yes |
| [`BreatheEasy`](https://github.com/connorodea/BreatheEasy) | 137 KB | 2026-04 | — |

**Finance** (2)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`SpendWise`](https://github.com/connorodea/SpendWise) | 31 KB | 2026-04 | — |
| [`spycli`](https://github.com/connorodea/spycli) | 18 KB | 2026-06 | — |

**Consumer** (6)

| Work | Size | Last pushed | Also on odeaworks.com |
| --- | --- | --- | --- |
| [`inquizit`](https://github.com/connorodea/inquizit) | 387 KB | 2026-01 | yes |
| [`FocusFlow`](https://github.com/connorodea/FocusFlow) | 30 KB | 2026-04 | — |
| [`PhotoGlowAI`](https://github.com/connorodea/PhotoGlowAI) | 39 KB | 2026-04 | — |
| [`ScanMasterPro`](https://github.com/connorodea/ScanMasterPro) | 40 KB | 2026-04 | — |
| [`geostamp`](https://github.com/connorodea/geostamp) | 178 KB | 2026-06 | — |
| [`screenrec-studio`](https://github.com/connorodea/screenrec-studio) | 187 KB | 2026-06 | — |

**31 of these are on `connorodea.com` only**, so before today they sat in the
undescribed list further down this file despite being on his portfolio. They are now classified:
`BreatheEasy`, `FocusFlow`, `OpenHarness`, `PaywallScraper`, `PhotoGlowAI`, `ScanMasterPro`, `ShopifyScraper`, `SpendWise`, `ai-blog-system`, `ai-faceless-yt`, `aividio`, `aiwholesail`, `auditiq`, `cartai`, `cutroom`, `framewright`, `geostamp`, `microsoft-ads-manager`, `odeaworks.com`, `preecursor`, `premium-website-builder`, `python-mastery-cli`, `reelwire`, `ryvio-ai`, `screenrec-studio`, `sonyobs`, `spycli`, `supply-pulse`, `wholesale-lead-finder`, `youtube-transcript-analyzer`, `ytauto`.

**Where the two sites disagree, that is information.** A work on both is one he leads with in two
different voices. A work on `connorodea.com` only is recent portfolio material, and the shipping
log is generated from GitHub so it tracks what he is actually pushing. A work on `odeaworks.com`
only is one he sells as a service rather than shows as a build.

## The rest of his repositories

Not on the site, so there is no written description beyond what the repository itself carries.
Grouped by the shape of the work. Sizes are the repository's own and include committed assets.

**Video and YouTube automation**

- `AI-video-automation-nodejs` (155 MB, 2025-02) — ai video automation using nodejs. complete pipeline with AI script generation, AI voiceover, ba…
- `youtube-ai-cli` (104 MB, 2025-09) — 🎬 Professional YouTube AI CLI - Complete automated video generation with MoviePy, FFmpeg, TTS, …
- `FilmFusion` (3 MB, 2025-08) — _undescribed_
- `cutroom` (996 KB, 2026-06) — AI-native pro video editor (Studio). A Preecursor app.
- `python-mastery-cli` (744 KB, 2026-06) — An interactive terminal course that teaches Python from absolute beginner to advanced — lessons…
- `yt_automation_tool` (336 KB, 2025-07) — _undescribed_
- `reelwire` (278 KB, 2026-06) — Reelwire — the newswire that ships reels. Automated YouTube videos from live news.
- `screenrec-studio` (187 KB, 2026-06) — Native macOS screen recorder + video editor (ScreenFlow-class). Phase 0: ScreenCaptureKit → H.2…
- `ai-youtube-pipeline-deepinfra-frontend` (177 KB, 2025-10) — _undescribed_
- `sonyobs` (160 KB, 2026-08) — Mac automation that drives OBS Studio over WebSocket to record from a Sony RX100, MacBook camer…
- `ytauto` (149 KB, 2026-04) — AI-powered YouTube video creation from a single prompt
- `framewright` (134 KB, 2026-05) — Interactive CLI for crafting AI videos in your terminal — HyperFrames + Claude Code + skills.
- `AI_VIDEO_AUTOMATION` (93 KB, 2025-02) — AI video automation for youtube video automation. working towards making it 100% autonomous.
- `ai-faceless-yt` (66 KB, 2026-08) — Faceless YouTube channels leveraging the omniscient power of AI
- `morphmesh` (61 KB, 2026-08) — Event-driven media transformation and closed-loop learning infrastructure
- `InstagramFacelessAutomation` (19 KB, 2025-10) — _undescribed_
- `youtube-transcript-analyzer` (12 KB, 2026-04) — CLI tool to download YouTube transcripts and analyze videos
- `VimeoHDDownloader` (3 KB, 2024-11) — _undescribed_
- `YTautomationShortGPT` (**empty**, 2025-10) — _undescribed_
- `ai-video-pipeline-july2025` (**empty**, 2025-07) — _undescribed_
- `FilmFusion_VideoAutomation_2025` (**empty**, 2025-05) — _undescribed_
- `football_film_analyzer` (**empty**, 2025-03) — American Football AI analyzer for personnel, formation, concept, etc.
- `aivideoautomation` (**empty**, 2024-12) — Enhanced Video Automation SaaS project

**Agents, orchestration and dev tooling**

- `OpenHarness` (9 MB, 2026-04) — _undescribed_
- `mach` (2 MB, 2026-09) — Mach · i. am. speed. — a chat-to-browser agent powered by Jev
- `gitamesh` (980 KB, 2026-10) — The coordination mesh for autonomous coding agents.
- `JudgementSpace` (157 KB, 2026-08) — JudgementSpace: governed decision traces and multimodal intent contracts for a local-first CLI.
- `amani` (110 KB, 2026-08) — Amani — the nervous system of your Mac. Replaces Spotlight with one command bar that launches a…
- `tethr` (97 KB, 2026-09) — Cloud task queue and shared-context tether layer for AI agents — thoughts become a vision, goal…
- `premium-website-builder` (72 KB, 2026-04) — CLI tool to generate scroll-driven animated websites with AI agent lead capture — Claude Code +…
- `shell-assist` (69 KB, 2026-08) — Quiet, teaching-first inline AI recommendations for Zsh
- `alphalayer` (67 KB, 2026-08) — A compositing framework for AI skills — Skill, Layer, Flow — for piping automations programmati…
- `openrouter-toolkit` (41 KB, 2026-08) — A CLI toolkit for OpenRouter: ask, repl, models, config. Clean-room, MIT licensed.
- `keel` (35 KB, 2026-08) — Keel - guardrails/evals flywheel CLI to keep a project locked to its VISION.md
- `tmp-tracker` (7 KB, 2026-08) — Watches a directory (default: OS temp dir) and logs every write to JSONL — visibility into what…
- `ai_enhanced` (5 KB, 2024-10) — decorator for AI LLMs to make it seamless, easy and effortless to integrate in your python code…
- `homebrew-tap` (2 KB, 2026-08) — Personal Homebrew tap (Connor O'Dea)

**Scraping and data collection**

- `ShopifyScraper` (256 KB, 2026-06) — Shopify App Store intel pipeline: scrape every listing + reviews, score market opportunities, a…
- `wholesale-lead-finder` (116 KB, 2026-04) — Automated lead generation for liquidation/wholesale businesses - Reddit, Craigslist, notificati…
- `PaywallScraper` (5 KB, 2026-04) — Scrapes paywallscreens.com to identify high-demand, low-competition iOS/Android app opportuniti…

**E-commerce, WMS and logistics**

- `ai_manifest_analyzer` (636 KB, 2025-07) — _undescribed_
- `supply-pulse` (242 KB, 2026-04) — SupplyPulse — AI-powered supply chain planning platform. Demand forecasting, inventory analytic…
- `upscaled-frontend-design1` (49 KB, 2026-01) — _undescribed_
- `microsoft-ads-manager` (35 KB, 2026-04) — Comprehensive Microsoft Advertising manager for UPSCALED Inc. - liquidation, overstock, and who…

**Finance, trading and statistics**

- `ai-hedge-fund-saas` (3 MB, 2025-10) — Complete SaaS transformation of AI Hedge Fund with authentication, subscriptions, and monetizat…
- `life-insurance-blog-website-template` (146 KB, 2026-01) — _undescribed_
- `statistics-toolkit-cli` (21 KB, 2025-08) — 📊 A comprehensive command-line statistics learning tool with step-by-step explanations
- `spycli` (18 KB, 2026-06) — SPY backtest & alpha-discovery CLI — Typer + Rich, with bull/bear debit and credit spreads, gri…
- `ai-financial-analyst` (**empty**, 2025-01) — ai financial analyst

**Health, legal and vertical AI**

- `privileged` (530 KB, 2026-08) — Privileged AI — serverless inference for law. Landing page.
- `sullyai_replica` (72 KB, 2025-05) — _undescribed_
- `ailegaladvice` (47 KB, 2025-10) — _undescribed_
- `aidentalnotes` (33 KB, 2025-05) — _undescribed_
- `juricratic-datasets` (**empty**, 2026-09) — Juricratic open legal-data platform dataset releases. Source: juricratic Legal Data Platform (c…

**CLI tooling over third-party APIs**

- `namecheap-cli` (68 KB, 2026-08) — A beautiful command-line interface for managing Namecheap DNS records
- `hostinger-cli` (60 KB, 2025-08) — A comprehensive command-line interface for Hostinger API
- `Leonardo_CLI` (36 KB, 2025-06) — _undescribed_
- `do-cli` (10 KB, 2024-12) — DigitalOcean CLI program to manage your account using PyDO and DO api token for authenti

**Vision and model training**

- `ScanMasterPro` (40 KB, 2026-04) — QR & Barcode Scanner iOS app with StoreKit 2 paywall - targets $100K/mo utility niche
- `PhotoGlowAI` (39 KB, 2026-04) — AI Photo Enhancement iOS app with CoreImage filters and StoreKit 2 paywall
- `GridironV2` (**empty**, 2024-12) — _undescribed_

**iOS apps in Swift**

- `BreatheEasy` (137 KB, 2026-04) — Meditation & Breathing Timer iOS app with animated exercises and StoreKit 2 paywall
- `SpendWise` (31 KB, 2026-04) — Expense Tracker iOS app with charts, budgets, and StoreKit 2 paywall - Finance niche
- `FocusFlow` (30 KB, 2026-04) — Habit Tracker iOS app with streaks, stats, and StoreKit 2 paywall - Health & Fitness niche

**Marketing, SEO, blogs and small SaaS**

- `competitor-analysis-app` (2 MB, 2024-11) — competitor analysis AI software. Generate competitor analysis reports on-demand and via API.
- `AI_BLOGGER` (1 MB, 2024-12) — _undescribed_
- `geostamp` (178 KB, 2026-06) — GeoStamp — geotag photos for Local SEO in seconds. Desktop + web, sold on Gumroad.
- `ryvio-ai` (76 KB, 2026-04) — Ryvio AI - Analytics. Automated.
- `gmb-ai-pro` (48 KB, 2025-10) — 🤖 AI-Powered Google My Business Management Platform | Automate review responses, boost local SE…
- `cartai` (40 KB, 2026-04) — CartAI - AI-powered juicing & grocery automation SaaS. Get fresh produce delivered on autopilot.
- `AI_blogging_system` (37 KB, 2025-04) — Autonomous AI blogging system
- `inquizitai-frontend` (102 KB, 2026-01) — Next.js front end for Inquizit, and its Vercel deployment is the live demo. Pairs with `inquizit`, the generation API
- `ai-blog-system` (27 KB, 2026-04) — AI-powered blog automation system with content generation, social media, email marketing, and r…
- `outline-ai-saas` (3 KB, 2025-04) — AI outline SaaS for internal company information. The open-source mashup of Slack and Notion.
- `blog-generator` (3 KB, 2024-12) — AI blog generation
- `competitive-analysis-tool` (**empty**, 2024-12) — competitor analysis tool using AI LLMs

**Sites and portfolio**

- `Connorodea_consulting_May2025` (5 MB, 2025-05) — _undescribed_
- `odeaworks.com` (3 MB, 2026-06) — Odea Works — AI Consulting, Tech Consulting & Software Engineering
- `preecursor` (708 KB, 2026-07) — Preecursor — applied-AI studio site (boutique BCG competitor). Next.js static export.
- `connorodea.com` (275 KB, 2026-07) — connorodea.com — personal portfolio. Black/mono aesthetic, raymarched WebGL hero, Next.js stati…
- `connorodea` (63 KB, 2026-08) — _undescribed_
- `deploy-preview-template` (**empty**, 2024-11) — deploy preview template for preview URLs for all new repos.

**Everything else**

- `aiwholesail` (182 MB, 2026-09) — _undescribed_
- `wob` (1 MB, 2026-08) — The ivy-league book radar: cross-web used-book price search, 35 university course packs, taste-…
- `forest-floor-metrics` (369 KB, 2025-08) — _undescribed_
- `furnishedrentals` (223 KB, 2025-07) — _undescribed_
- `snap-swipe-stash` (210 KB, 2025-09) — _undescribed_
- `auditiq` (107 KB, 2026-04) — _undescribed_
- `ai-diagnostics-refurbishment-software` (37 KB, 2024-11) — 🔧 AI Diagnostics and Refurbishment Software | A cutting-edge AI-powered diagnostic platform for…
- `ODea-thoughts-and-ideas` (4 KB, 2026-08) — as it sounds
- `ai-vidio-generation-june2025` (**empty**, 2025-06) — _undescribed_
---

## Patterns worth leading with

**He writes a clean CLI over somebody else's REST API, repeatedly.** GoDaddy, Namecheap,
Hostinger, DigitalOcean, OpenRouter, Meta Marketing (`adpilot`), eBay (`EbayAutolister`). On an
API-integration job that is a stronger and far more checkable claim than anything in the video
cluster, because there are six of them and they are small enough to read.

**AI video automation is his deepest cluster**, roughly 25 repositories across two years and
several languages, including the three largest things he owns. On a media or content-automation
job, lead here.

**Agent infrastructure is his current work.** `OpenHarness`, `gitamesh`, `mach`, `tethr`,
`alphalayer`, `morphmesh`, `keel`, `AgentAgent`, `clawd-hub` were all pushed in 2026. On an agent
or orchestration job this is live interest rather than history.

**`GRIDIRON` is the only genuinely trained model in the pool**, a YOLOv8 trained on synthetic
American-football formation data at 61 MB. It is the honest answer to any job asking for real ML
rather than an API call.

**The e-commerce and warehouse cluster is where his operator half shows.** `Upscaled_inv_processing`,
`LiqOS`, `quickreturnz`, `ai_manifest_analyzer`, `supply-pulse`, plus the QuickLotz work. He ran
these businesses as well as building the systems, which most engineers bidding will not have.

---

## Do not cite these

**Two dead links on his own site.** `QuickVisionz` and `quickvisionz-sam3` both 404 on GitHub,
and QuickVisionz is one of four projects featured on his homepage with a "View project" button.
The computer-vision work is real per his profile but **has no public repository**, so describe it
and never link it.

**One parked demo.** `quicklotzlogistics.com` returns HTTP 200 but serves a Namecheap
domain-auction page: the domain lapsed and was re-registered. The repository is fine; the demo is
not. Never send that URL.

**One demo nobody can enter.** `inventory.upscaledinc.com` is a genuine working system, the
Upscaled Inventory Hub ops console, but it sits behind "Secure Access — Sign in". Fine to
describe, useless as a demo.

**The ClawdHub line count.** His site says "13,000 lines across 26 files". Measured on
2026-10-12: **26 Python files exactly, 4,426 lines** of Python, 5,133 counting README, shell and
config. The file count is right and the line count is about 3x over. Say "a few thousand lines" or
nothing.

**"Millions in revenue generated", "10+ ventures built", "systems serving thousands daily."**
Homepage copy, unverifiable, and the first belongs with the $2.1M licensing and $9M equity figures
that `Connor.md` records as notional and never realised. Fine on his own marketing, not in a
proposal.

**Empty repositories — eleven of them, not six.** Re-counted against the API on 2026-10-12 and
these are every 0 KB repository he owns, which matches the `**empty**` flags in the cluster lists
above exactly: `FilmFusion_VideoAutomation_2025`, `GridironV2`, `YTautomationShortGPT`,
`ai-financial-analyst`, `ai-video-pipeline-july2025`, `ai-vidio-generation-june2025`,
`aivideoautomation`, `competitive-analysis-tool`, `deploy-preview-template`,
`football_film_analyzer`, `juricratic-datasets`. An earlier version of this list named only six and
omitted the last five of those; the flags in the clusters were right and the list was short.

**So 113 of the 124 repositories have code in them**, which is the figure to keep in mind when
reading the cluster lists: a name with no size and no description is one of these eleven.

**`nexserp.com` is referenced as the site, never as the product.** The site is real, shipped and
good: a four-page SaaS funnel with a six-stage interactive product demo, a four-tier pricing page
and a developer-experience section. **That is the work, and the URL is the proof of it.** Say "a
SaaS marketing site and interactive product demo I designed and built" and the link backs the
claim exactly.

**What must not be claimed is the API behind it.** Verified 2026-10-12: `@nexserp/sdk` is **404 on
npm** and so is `create-nexserp-app`, `/docs` is an empty 6.6 KB page, `status.nexserp.com` does
not resolve, and the analytics tag is still the placeholder `G-XXXXXXXXXX`. **Never repeat its
metrics either** — *"Trusted by teams at Shopify, Vercel, Linear, Notion, Stripe"*, *"10M+ pages
indexed monthly"*, *"99.9% uptime SLA guaranteed"*, *"500+ companies"* — all of which sit directly
below the words *"Now in public beta"*. Describe the site and the craft; make no claim about
traffic, customers or uptime.

**`preecursor.com`'s four case studies are illustrative, not delivered client work.** This is the
most dangerous thing in the pool to misread, so it is stated plainly here. The site has
`/work/underwriting-copilot/`, `/work/clinical-documentation/`, `/work/network-ops-copilot/` and
`/work/predictive-operations/`, and they read like case studies: "The challenge", "What stood in
the way", and past-tense narrative such as *"commercial credit officers were spending the better
part of a week assembling each memo."*

**The work index disclaims them twice**, in its own words: *"Illustrative examples of the systems
we build"*, *"Examples, not specific client results"*, and *"the scenarios below are illustrative
examples of the kind of work we do — not specific delivered client results."* Each case-study page
repeats the qualifier only once, as *"an illustration of the kind of system we build"*, and then
narrates in the past tense.

**So never cite any of the four as past work, and never name a client, a sector engagement or a
metric from them.** They are positioning material. Connor labelled them honestly; the risk is a
reader skimming the body and taking it for delivery. **What is safe** is to cite the *site* as his
build, and to use the four scenarios as evidence of the kind of system he can describe and scope.

**Landing pages that are not systems.** `privileged` ("serverless inference for law") and
`preecursor` are sites. So are `odeaworks.com`, `connorodea.com` and `upscaledist.com`, though the
last has a working demo as a storefront.

**The flagships with no public code.** QuickWMS and QuickVisionz are the two systems his profile
leads on, and neither has a repository. The closest public evidence is
`upscaled-quicklotz-dashboard` (788 KB), which his site presents as QuickLotz WMS. Claims about
them are profile-backed, not code-backed.
