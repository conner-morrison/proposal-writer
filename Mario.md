# Mario

Everything personal lives here: who Mario is, what he has built, and the real numbers behind it.
`CLAUDE.md` holds only the guide for writing proposals and never repeats any of this.

## Identity

**Lead AI & Full-Stack Engineer.** 8+ years building production systems, 5+ of those focused
specifically on Generative AI and LLM engineering: multi-agent platforms, AI copilots, document
intelligence, semantic search, and workflow automation.

**Founder of FCAG** (Fibonacci Consulting Advisory Group).

Owns the full lifecycle: business problem, architecture, data strategy, model selection, RAG
pipeline design, backend, frontend, cloud deployment, MLOps, and long-term optimization.

## The differentiator

Alongside the engineering background he holds an **MBA, an M.S. in Business Administration**. He
reads a problem the way leadership reads it: cost, risk, ROI, time to value. Then he turns it into
a working system.

> "Most engineers can write code. Far fewer can tie that code to the business result it is meant
> to produce."

Four promises to clients:

1. A technical partner who understands the business case, not just the ticket.
2. Executive-ready communication, no jargon walls and no surprises.
3. Honest calls on what to build and, just as important, what not to build.
4. Systems engineered for production, security, and long-term cost.

Explicit stance: **ships production systems, not demos.** Does not hand off prototypes that fall
apart in week two.

## What he builds

| Area | Detail |
| --- | --- |
| AI agents & LLM apps | Custom agents, AI copilots, multi-agent workflows, tool and function-calling systems, AI decision-support, on GPT, Claude, Gemini |
| RAG & knowledge systems | Retrieval-Augmented Generation, vector and hybrid search, enterprise knowledge bases, document Q&A, secure embeddings pipelines with metadata filtering |
| Document intelligence | Extract, classify and summarize PDFs, forms, medical records, logistics documents, reports |
| Full-stack SaaS | Multi-tenant SaaS, dashboards, admin portals, client-facing apps with auth, API integrations, data visualization |
| Backend & API | Python/FastAPI services, REST and GraphQL, webhooks, background jobs, ETL pipelines, CRM/ERP integrations |
| Cloud, data & MLOps | Cloud-native deployments, Dockerized services, CI/CD, monitoring, production AI optimization across Azure, AWS, GCP |

## Technical skills

- **AI/ML:** Generative AI, LLMs, Agentic AI, RAG, MCP, prompt engineering, multi-agent systems, NLP, semantic search, embeddings, model evaluation
- **LLM tools:** OpenAI, Azure OpenAI, Claude, Gemini, AWS Bedrock, LangChain, LangGraph, Vertex AI
- **Languages:** Python, SQL, TypeScript, JavaScript, DAX, Go
- **Frontend:** React, Next.js, Tailwind CSS, responsive component-based UIs
- **Backend:** FastAPI, Django, Flask, Node.js, Express, REST, GraphQL, WebSockets, microservices, serverless
- **Cloud:** Azure AI Foundry, Synapse, Microsoft Fabric, Data Factory, Functions; AWS Lambda, Step Functions, Bedrock; GCP, Vertex AI, Supabase
- **Databases:** PostgreSQL, SQL Server, BigQuery, Neo4j, pgvector, Pinecone-style vector DBs
- **DevOps:** Docker, Kubernetes, Git, GitHub Actions, CI/CD, monitoring, logging
- **Data & BI:** Power BI, DAX, ETL/ELT, data modeling, analytics dashboards

## Industry experience

Healthcare AI and compliance-sensitive workflows · logistics automation and operational
intelligence · aerospace data systems · enterprise workflow automation and executive reporting ·
document processing and knowledge management

## Portfolio

Ten projects. **Every detail below was pulled from the live case-study pages on fib0.ai. The
"Hard numbers" lines are verbatim from those pages: never round them, never restate them as
percentages, never add a figure that is not here.**

"Best fit for" is a matching hint for choosing which project to cite, not a claim to repeat.

**Ownership:** fib0 is FCAG's own platform, and R1O / R1O iOS are self-initiated systems research,
not client engagements. Present them as such. The seven client engagements are SSPR, APS, DigiMed,
TropicalPlus, Magellan, DocScan and PBI-KB.

**Evidence boundary:** SSPR, TropicalPlus, DocScan and R1O publish no outcome metrics at all. For
those, cite scope and system detail, never a number.

---

### 1. fib0 — Multi-tenant private AI platform

- **Case study:** https://fib0.ai/portfolio/case/fib0 · **Live:** https://fib0.ai/
- **Client / industry:** FCAG (Fibonacci Consulting Advisory Group); compliance-sensitive enterprises needing tenant isolation
- **Problem:** Clients needed AI that could act on billing and ops without cross-tenant leaks or unsupervised writes. Existing platforms lacked org isolation at the tool-call level.
- **Built:** Multi-tenant SaaS for agent chat, org settings, billing, and human-in-the-loop tool review. 9 ToolLoopAgent agents with 40 Zod-schema'd tools. 176 API routes with dual auth (session + SHA-256-hashed API keys). Stripe metering for per-org token attribution. Every mutation requires human review before production execution.
- **Stack:** Next.js App Router, React, Supabase (Postgres with RLS), Vercel AI SDK, Anthropic Claude primary with optional OpenAI, Stripe, Redis rate limiting.
- **Hard numbers:** 9 agents · 40 tools · 176 API routes · 89 active migrations · 131 PRs of production history.
- **Best fit for:** multi-tenant SaaS, AI platform builds, per-seat or usage billing, tenant isolation, HITL approval design.

### 2. SSPR / CaseFlow — Agentic case management for surgical distribution

- **Case study:** https://fib0.ai/portfolio/case/sspr · **Live:** https://sspr.ai/
- **Client / industry:** Surgical Solutions Puerto Rico; healthcare and medical device distribution
- **Problem:** Ops staff lost cases inside email and PDFs. No agent could track quotes to clinical docs to billing across the case lifecycle.
- **Built:** Authenticated operations portal with agentic case management, document intelligence across 20+ document types, team assignment, TV ops dashboards, and human-in-the-loop approval across the case lifecycle (quotations, clinical paperwork, insurance, document readiness).
- **Stack:** ToolLoopAgent, document classification, case chat, Next.js, Postgres, Supabase auth, Anthropic Messages API via AI SDK, optional OpenAI for classification.
- **Hard numbers:** 20+ document types classified. No outcome metrics published.
- **Best fit for:** healthcare ops, document intelligence, case/workflow tracking, replacing email-and-PDF processes, HIPAA-adjacent work.

### 3. APS — Parking revenue ops and scenario agents

- **Case study:** https://fib0.ai/portfolio/case/aps · **Live:** https://aps-pr.com/
- **Client / industry:** American Parking Systems; commercial parking operations
- **Problem:** Leadership could not run scenario planning or revenue analysis over large transaction histories without burning analyst hours in spreadsheets.
- **Built:** Chat agent over live parking data with 29 domain tools. A runScenario capability renders artifact panels showing cash, credit, and average-daily impact. Operators run rate scenarios conversationally instead of manually.
- **Stack:** AI SDK streamText agents, Anthropic and OpenAI dual provider, Next.js, Supabase, artifact panel UI.
- **Hard numbers:** 162,000+ transactions processed · $1.14M sample data window · 29 domain tools.
- **Best fit for:** analytics copilots, natural-language BI, scenario modeling, replacing spreadsheet analysis, revenue and pricing tools.

### 4. DigiMed — Clinical RPM/CCM AI platform

- **Case study:** https://fib0.ai/portfolio/case/digimed · **Live:** https://dmed.fib0.ai/
- **Client / industry:** Healthcare; remote patient monitoring and chronic care management
- **Problem:** RPM/CCM staff needed AI that could score risk, optimize billing codes, and drive outreach without unsupervised PHI writes.
- **Built:** Multi-agent clinical operations platform with 20+ MCP tools (risk scoring, billing code optimization, PDF handling, SMS and voice), provider dashboards for patients, care plans and outreach, and human-in-the-loop gating on every mutation.
- **Stack:** Anthropic Claude Messages API as primary clinical assistant, OpenAI secondary, Vertex AI (Gemini) plus local MLX hybrid routing, Next.js, Postgres, MCP tool servers.
- **Hard numbers:** ~$1M ARR · 20+ MCP tools. The page describes it as one of the largest production AI systems he has shipped in healthcare.
- **Best fit for:** healthcare AI, PHI and compliance-sensitive builds, medical billing automation, MCP tooling, multi-agent clinical workflows, revenue-generating AI products.

### 5. r1o — Private pocket LLM on Apple Silicon

- **Case study:** https://fib0.ai/portfolio/case/r1o · **Live:** https://r1o.ai/
- **Client / industry:** Self-initiated systems research; relevant to on-prem and edge AI platform work
- **Problem:** Teams needed multi-node Mac inference without cloud egress, and single-node demos did not prove cluster reality.
- **Built:** Electron desktop agent (Hermes), iOS client, control plane and cluster topology dashboard, multi-node Mac inference cluster over Thunderbolt 5 RDMA, local servers exposing OpenAI-compatible /v1/chat/completions, optional Anthropic-shaped cloud fallback.
- **Stack:** MLX, JACCL, Thunderbolt 5 RDMA, Rust, Swift, TypeScript, Python, Next.js, Electron, SwiftUI.
- **Hard numbers:** 5-node / 1.5TB class cluster. No performance or adoption metrics published.
- **Best fit for:** on-prem and air-gapped LLM deployment, data-sovereignty requirements, local inference, OpenAI-compatible API layers, low-level systems work.

### 6. r1o iOS — Native cluster control client

- **Case study:** https://fib0.ai/portfolio/case/r1o-ios · *(TestFlight, gated; no public web URL)*
- **Client / industry:** Self-initiated, paired with r1o
- **Problem:** Operating the cluster meant SSH from a laptop for everything: checking whether a model was serving, restarting a wedged node, seeing whether an agent task finished.
- **Built:** Native iOS client with 13 product panes covering cluster control, on-device inference via MLX, SSH terminal access for node recovery, agent task monitoring, model serving control, node inspection, Live Activities, and Control Center widgets.
- **Stack:** SwiftUI, Swift 6 strict concurrency, mlx-swift-lm, mcp-swift-sdk, SwiftTerm, swift-nio-ssh, Supabase, Keychain, Anthropic Messages API, Tailscale.
- **Hard numbers:** 97,445 lines of Swift across 4 targets · 13 product panes · 127 SwiftUI views · 89 service types · 208 merged PRs.
- **Best fit for:** native iOS/SwiftUI work, on-device inference, mobile ops tooling, Swift concurrency.

### 7. TropicalPlus — Maritime commercial AI suite

- **Case study:** https://fib0.ai/portfolio/case/tropicalplus · **Live:** https://tropicalplus.ai/
- **Client / industry:** Tropical Shipping, Caribbean container carrier; maritime and logistics
- **Problem:** Commercial teams needed AI inside their existing Microsoft identity and Azure estate, with no extra SaaS logins, serving real shipping workflows rather than generic chat.
- **Built:** Entra-gated ops dashboard over Azure data with Claude and GPT copilots for real shipping workflows. Enterprise-authenticated suite with voyage and kanban-style operations views, and an identity gate in front of every model call.
- **Stack:** Azure OpenAI, OpenAI API, Anthropic Claude via Foundry and direct API, Microsoft Entra OAuth, Next.js, Azure Synapse and Fabric, Azure AD.
- **Hard numbers:** No outcome metrics published.
- **Best fit for:** enterprise Azure builds, SSO and Entra requirements, logistics and supply chain, "AI inside our existing Microsoft stack" asks.

### 8. Magellan — Multi-domain freight agent platform

- **Case study:** https://fib0.ai/portfolio/case/magellan · **Live:** https://magellan.tropicalplus.ai/
- **Client / industry:** Tropical Shipping; maritime freight operations
- **Problem:** Freight ops needed agents that could reliably chain schedules, voyage legs, rate quotes, hazmat, and document tools against systems of record, without capability leaking between workflows or producing unverifiable free-text answers.
- **Built:** Multi-agent platform with 13 specialty agents across 21 tool packs and 101 AI-SDK tool bindings that resolve into typed UI components (VesselCardPart, ScheduleDisplayPart, BookingApprovalPart). Human-in-the-loop mutation gates requiring explicit confirmation, document extraction with schema whitelist enforcement, and Entra SSO access control.
- **Stack:** Azure AI Foundry (GLM-5.1 default) with Anthropic Claude alternate, Next.js App Router with 78 API routes, local Qwen/VLM embeddings, MCP server with API-keyed machine tools.
- **Hard numbers:** 13 agents · 21 tool packs · 101 tool bindings · 78 API routes · 34 migrations across 43 tables and 21 views.
- **Best fit for:** large multi-agent architectures, tool-calling at scale, generative UI, agent reliability and guardrails, logistics, enterprise SSO.

### 9. DocScan / Email Document Processor — Email-to-document AI pipeline

- **Case study:** https://fib0.ai/portfolio/case/docscan · **Live:** https://tropicalplus.ai/ *(confirmed: it ships inside the TropicalPlus environment)*
- **Client / industry:** Tropical Shipping; commercial customer service
- **Problem:** Commercial email buried bookings, invoices, and claims in attachments, and agents needed structured fields without manually re-keying every message.
- **Built:** Email ingestion with attachment classification, field extraction from documents, a human-in-the-loop review queue before anything reaches systems of record, and a production review dashboard.
- **Stack:** Classification and field extraction with multi-provider LLMs, Anthropic Messages API primary with OpenAI alternate, TypeScript and Python services, review dashboard and email ingest workers, HITL gates.
- **Hard numbers:** No outcome metrics published.
- **Best fit for:** document extraction and OCR-adjacent work, invoice and form processing, email automation, data entry elimination, human review queue design.

### 10. PBI-KB — GraphRAG over an enterprise Power BI estate

- **Case study:** https://fib0.ai/portfolio/case/pbi-kb · **Live:** https://frontend-pbi-kb.braveground-2789e4ff.eastus2.azurecontainerapps.io/ *(raw Azure hostname, reads as internal; lead with the case study)*
- **Client / industry:** Tropical Shipping; commercial, operations, and partner reporting
- **Problem:** The Power BI estate was opaque and could not be traversed as a system. Vector RAG over report text surfaces reports using similar language, but cannot answer the question people actually asked: which measures depend on this source table, and what breaks if it changes.
- **Built:** A PBIX-to-Neo4j pipeline with 23 Python extraction tools materializing 20 node labels and 13 relationship types into a graph, a hybrid BM25-plus-embedding retrieval layer, a Next.js frontend (44 routes, 16 pages), a FastAPI backend, and 5 MCP servers for machine clients.
- **Stack:** Neo4j, Python extraction pipeline, FastAPI, Next.js, Azure Container Apps, Bicep IaC, Anthropic Messages API, MiniLM and bge-large embeddings, Microsoft Fabric and Power BI REST APIs.
- **Hard numbers:** 19 reports · 202 measures · 38 tables · 40 queries indexed · 23 extraction tools · 5 MCP servers.
- **Best fit for:** GraphRAG and knowledge graphs, hybrid search, data lineage and impact analysis, Power BI and Fabric work, RAG that plain vector search cannot handle.

---

### Fast matching index

| If the job is about | Cite |
| --- | --- |
| RAG, hybrid search, knowledge graph | PBI-KB, SSPR |
| Multi-agent / tool calling at scale | Magellan, fib0, DigiMed |
| Document extraction, invoices, forms, email | DocScan, SSPR |
| Healthcare, PHI, clinical, medical billing | DigiMed, SSPR |
| Logistics, shipping, supply chain | Magellan, TropicalPlus, DocScan |
| Multi-tenant SaaS, billing, org isolation | fib0 |
| Analytics copilot, natural-language BI | APS, PBI-KB |
| Azure, Entra SSO, Fabric, enterprise Microsoft | TropicalPlus, Magellan, PBI-KB |
| On-prem, local, air-gapped, data sovereignty | r1o, r1o iOS |
| iOS / SwiftUI / mobile | r1o iOS |
| Human-in-the-loop, guardrails, safe AI writes | fib0, DigiMed, Magellan |

## How he works

The rhythm he offers clients, consistent across engagements:

- **Understand** the goals and constraints, and what cannot break.
- **Map** the dependencies and the risk before changing anything.
- **Build** in waves, lowest risk first, old and new running in parallel where it matters.
- **Prove** it with evidence rather than assertion: diffs, tests, measured numbers.
- **Hand over** with a runbook and documentation, so the team owns it without him.

**Communication is the spine, not a footnote.** Written update twice a week, a working demo at
every milestone, Slack or Upwork chat at the client's preference, and blockers raised the same day
rather than buried. Plain English, no jargon walls. The client always knows what is done, what is
next, and what is at risk.

## Voice

Direct and senior. Contractions throughout: "I've", "I'm", "it's", "don't". No em dashes. No hype,
no "passionate about", no jargon walls. Confident but concrete: a specific mechanism beats an
adjective. Says what he would not build as readily as what he would.
