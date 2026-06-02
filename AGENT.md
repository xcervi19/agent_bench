# agent_bench

Monorepo for the Agentic Platform: a reusable multi-agent framework with two applications built on top.

## Applications

| App | Location | Purpose |
|---|---|---|
| `signal_gather` | `apps/signal_gather/` | Commodity market intelligence (CrewAI crews: discovery → events → signals → briefings) |
| `claude_agent` | `apps/claude_agent/` | Claude-powered topic research pipeline (`/newsfind-*` slash commands) |

The shared framework lives in `libs/agentic_core/`.  
Claude slash commands workspace: `claude_agent_fe/` (mounted into the `claude_agent` container).

## Services & Ports

| Service | Local | VPS |
|---|---|---|
| `api` (signal_gather) | 8000 | 8001 |
| `claude_agent` | 8002 | 8002 |
| `rag_adhoc` | 8003 | 8003 |
| `postgres` | 5432 | — (tunnel to 5433) |
| `redis` | 6379 | — |

## Repo Layout

```
agent_bench/
├── apps/
│   ├── signal_gather/          ← commodity intel API (CrewAI)
│   └── claude_agent/           ← news research pipeline (Claude CLI)
├── libs/
│   └── agentic_core/           ← shared framework (pip-installable)
├── claude_agent_fe/
│   └── .claude/commands/       ← slash commands: /newsfind-*, /trade-*, /rag-*
├── testing/                    ← test scripts + captured runs
├── source_ingest/              ← preprocess + embed local knowledge
├── database/
│   ├── migrations/             ← Alembic
│   └── seeds/
├── docs/
│   ├── architecture/           ← stable system design docs
│   ├── ops/                    ← commands, debugging, DB queries
│   └── specs/
│       ├── active/             ← executable ticket specs (numbered)
│       ├── done/               ← shipped specs — persistent capability context
│       ├── TICKET_REGISTRY.md  ← canonical ticket # list; next available #
│       └── business_requirements/
├── docker-compose.yml
├── .env                        ← top-level (postgres creds, shared)
└── apps/claude_agent/.env      ← claude_agent service config
```

## Quick Commands

```bash
# Start everything locally
docker compose up --build

# Seed demo data (signal_gather)
docker compose exec api python -m database.seeds.seed_scenario signal_gather_commodity_trading

# Run migrations
docker compose run --rm --no-deps --entrypoint alembic api upgrade head

# Rebuild + restart claude_agent only
docker compose build claude_agent && docker compose up -d claude_agent

# Health checks
curl -s http://localhost:8002/readyz
curl -s http://localhost:8002/v1/agent/info -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq

# Run a topic (streaming)
export API="http://localhost:8002"
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}'
```

## Key Documentation

| What | Where |
|---|---|
| **This file** — repo map + SDLC rules | `AGENT.md` |
| Current work, bugs, blockers | `STATUS.md` |
| Long-term vision + domain language | `docs/specs/business_requirements/business_requirements.md` |
| Shipped product surface (V1) | `docs/product/README.md` |
| Platform architecture | `docs/architecture/framework.md` |
| Implemented capabilities (ground truth) | `docs/specs/done/*.md` |
| Planned / in-flight executable tasks | `docs/specs/active/*.md` |
| Ticket numbers + next `#` | `docs/specs/TICKET_REGISTRY.md` |
| Prioritized build order | `STATUS.md` → Build queue |
| Full doc index | `.cursor/skills/technical-architect/doc-map.md` |
| VPS deploy + SSH commands | `docs/ops/commands.md` |
| Debug cheat sheet + war stories | `docs/ops/debugging.md` |
| DB debug queries | `docs/ops/db_commands.md` |
| Testing scenarios + eval harness | `testing/README.md` |

---

## Development Process (SDLC)

This repo uses **documentation as persistent context** for humans and agents. Code shows what runs today; specs record what was agreed, built, and how to use it. The goal is that any agent session can reconstruct full application context without re-deriving history from git or chat.

### Documentation layers

| Layer | Path | Lifetime | Agent role |
|---|---|---|---|
| **Entry point** | `AGENT.md` | Stable | Read first — repo map, SDLC, read order |
| **Session state** | `STATUS.md` | Ephemeral | Read second — what's in progress, bugs, blockers |
| **Business intent** | `docs/specs/business_requirements/` | Stable | Why we build; domain terms (topic, signal, V1 pipeline) |
| **Product truth** | `docs/product/README.md` | Updated on ship | What users get today vs. future apps |
| **Architecture** | `docs/architecture/` | Stable, revised on design change | System design, stack, principles |
| **Prepared tasks** | `docs/specs/active/*.md` | Moves to `done/` on ship | Executable specs for work not yet (or not fully) delivered |
| **Shipped context** | `docs/specs/done/` | Permanent archive | Ground truth for each delivered capability |
| **Validation** | `testing/` | Updated with features | How to verify behavior; eval vectors and results |
| **Operations** | `docs/ops/` | Living playbooks | Deploy, debug, DB — war stories and commands |

**Context rule:** Prefer `docs/specs/done/` over re-reading code for "what was built and how to use it." Prefer `STATUS.md` over guessing what's active. If docs and code disagree, note the drift; code wins for runtime, done specs win for agreed delivery.

### Spec lifecycle

Each feature or task is tracked as a **numbered spec ticket** (e.g. `#11`, `#15`).

```
planned → in progress → done
docs/specs/active/<name>_<n>.md   docs/specs/done/<name>_<n>.md
```

| Stage | Location | Status field | Also update |
|---|---|---|---|
| **Planned** | `docs/specs/active/<name>_<n>.md` | `Status: planned` | — |
| **In progress** | same file | `Status: in progress` | `STATUS.md` → In Progress |
| **Done** | move to `docs/specs/done/` | `Status: done (YYYY-MM-DD)` | `STATUS.md` → Recently Completed; related docs below |

**Starting work:** Pick the next item from [`STATUS.md` → Build queue](#build-queue-and-prioritization) (or get a new ordering via **technical-architect**). Pick or create a spec under `docs/specs/active/`. Add an In Progress entry to `STATUS.md` with spec path, what's done, what's missing, next step.

### Creating a new ticket (task spec)

Use this when workflow, planning, or a Decision brief identifies **new work** that is not covered by an existing active ticket.

#### 1) Allocate a number (required)

1. Open `docs/specs/TICKET_REGISTRY.md` — read **Next available number**.
2. Confirm no file exists matching `*_<n>.md` under `docs/specs/active/` and `docs/specs/done/`.
3. Create `docs/specs/active/<short_snake_name>_<n>.md` (example: `topic_cancel_abort_23.md` for `#23`).
4. Add the row to **Active** in the registry; set **Next available number** to `n+1`.
5. In the spec header, use the same `#n` in the title and in all cross-references.

**Do not** create tickets outside `docs/specs/active/` (legacy `#16` was relocated — follow the registry path).

#### 2) Run technical-architect before prioritizing (recommended)

For anything that affects **what we build next** toward the full V1 application:

1. Invoke the **technical-architect** skill (`.cursor/skills/technical-architect/SKILL.md`).
2. Produce a **Decision brief** (build / defer / split).
3. If the outcome is **build** or **split**, either update an existing ticket or create a new one using the [active spec contract](#active-spec-contract) below.
4. Update **`STATUS.md` → Build queue** with the recommended sequence and one-line rationale per step.

Human override always wins; document overrides in the Build queue (e.g. "demo-first: #16 before #22").

#### 3) Wire dependencies in the ticket

Every new ticket must declare:

| Field | Required | Purpose |
|---|---|---|
| **Depends on** | Yes | Which shipped or active `#` tickets must exist first |
| **Blocks** | If applicable | Which tickets cannot finish until this ships |
| **Lane** | If applicable | e.g. A = business value, B = technical verification, DevOps, Product |
| **Out of scope** | Yes | Point to other `#` tickets — prevents duplicate work |

Mirror dependency changes in related tickets' **Related** sections.

#### 4) Register in session state

| When | Update |
|---|---|
| Ticket created, not started | Registry only; optional one-line under **Planned backlog** in `STATUS.md` |
| Work begins | `Status: in progress` + **In Progress** block in `STATUS.md` |
| Work ships | Move to `done/`, [done spec contract](#done-spec-contract), registry → Done, Build queue |

### Active spec contract (planned / in progress)

Every file in `docs/specs/active/*_<n>.md` must include:

| Section | Purpose |
|---|---|
| **Title + `#n`** | Matches filename suffix |
| **Status** | `planned` or `in progress` |
| **Depends on / Blocks / Lane** | Chain position (see above) |
| **Goal** | Why this ticket exists |
| **Core question** | One sentence — how we know it succeeded |
| **Scope** | Numbered deliverables (what to build) |
| **Out of scope** | Other ticket numbers that own adjacent work |
| **Acceptance criteria** | Checklist — definition of done |
| **Related** | Links to done/active specs, testing, ops |

Optional: responsibility split table (as in #18), server flows, schemas.

**Example (shape):** `docs/specs/active/topic_refresh_scheduler_22.md`  
**Anti-pattern:** A second markdown file as "execution plan" — keep coordination inside the ticket.

### Ticket numbering validation

Before committing a new or renamed ticket:

- [ ] Number in **filename** = number in **title** = number in **registry**
- [ ] Number not already used in registry (active or done)
- [ ] File lives under `docs/specs/active/` until shipped
- [ ] **Depends on** references only existing `#` or documented unnumbered done specs
- [ ] **Blocks** / **Feeds** updated on sibling tickets when chain changes
- [ ] `TICKET_REGISTRY.md` **Next available number** incremented

### Build queue and prioritization

**Per-ticket chaining** lives inside each spec (`Depends on`, `Blocks`).  
**Cross-ticket execution order** for the whole application lives in **`STATUS.md` → Build queue**.

Rules:

1. **Default next work** = first not-done item in Build queue, unless the user assigns a specific `#`.
2. **Build queue order** is derived from technical-architect Decision briefs (business + product + dependency fit), not from ticket number alone (`#22` is not "after #21" by sort order only).
3. When creating or splitting tickets, **recompute** the queue and edit `STATUS.md` in the same session.
4. Ticket numbers are **stable IDs**; priority is **explicit in Build queue**, not implied by `#n`.

Current V1 chain (maintained in `STATUS.md`; update when priorities change):

```
#15 → #19 (advisory) → #22 → #16 → #21 → #18 → #20
```

Parallel work is allowed when **Depends on** is satisfied (e.g. #21 can start once #11 artifacts exist; #16a can start after #17).

### Ticket execution contract (agent behavior)

- Execute tickets only from `docs/specs/active/`.
- A file is executable only if it matches `*_<number>.md` (for example `newsfind_application_verification_15.md`).
- Keep coordination rules inside executable tickets; do not create non-ticket planning anchors for execution flow.
- When a ticket's acceptance criteria are satisfied, move it to `docs/specs/done/` and update `STATUS.md`.

**Finishing work:** Complete the [done spec contract](#done-spec-contract), move the file to `docs/specs/done/`, update `STATUS.md`, and touch any operational docs the feature needs (see [close-out checklist](#close-out-checklist)).

Do not leave shipped work only in chat or commit messages — the done spec is the durable record.

### Done spec contract

Every spec in `docs/specs/done/` must give an agent enough context to use and extend the feature without archaeology. Include:

| Section | Purpose |
|---|---|
| **Status + date** | When it shipped |
| **Depends on** | Linked prior specs (#10, #12, …) |
| **Goal / Problem** | Why this existed |
| **Solution / What was delivered** | What changed — components, endpoints, commands |
| **Artifacts** | Concrete paths (scripts, configs, tables, commands) |
| **Usage** | Copy-paste commands or API examples |
| **Acceptance criteria** | Checklist — all checked when done |
| **Related** | Links to architecture, testing, sibling specs |

Optional but valuable: output layouts, schemas, known gaps, env vars.

**Example:** `docs/specs/done/rag_full_stable_evaluation_11.md`

### Agent read order

Use this order at the start of a session or before substantial work:

1. `AGENT.md` — repo map and SDLC (this file)
2. `STATUS.md` — current work, bugs, recent completions
3. Active spec ticket — `docs/specs/active/*_<n>.md` referenced from STATUS
4. Relevant `docs/specs/done/*.md` — dependencies and patterns for the area
5. `docs/product/README.md` + `docs/architecture/framework.md` — product and platform constraints
6. `testing/README.md` — if the task touches behavior or quality
7. Target code under `apps/`, `libs/` — when docs are missing or suspected stale

For planning, sequencing, and **Build queue** updates, use the **technical-architect** skill (`.cursor/skills/technical-architect/SKILL.md`). Read `docs/specs/TICKET_REGISTRY.md` before allocating a new `#`.

### Close-out checklist

When marking a spec **done**, the agent (or developer) should:

- [ ] Move spec to `docs/specs/done/<name>_<n>.md` and set status + date
- [ ] Fill all sections of the [done spec contract](#done-spec-contract)
- [ ] Add row to `STATUS.md` → Recently Completed (with date + spec path)
- [ ] Remove or shrink the In Progress entry in `STATUS.md`
- [ ] Update `testing/README.md` or `testing/vectors.json` if behavior is testable
- [ ] Update `docs/product/README.md` if user-facing surface changed
- [ ] Update `docs/ops/commands.md` or `docs/ops/debugging.md` if ops/debug workflow changed
- [ ] Add cross-links from related done specs (`Related` section both ways when useful)

### Context handling principles

1. **One capability, one done spec** — persistent context lives in `done/`, not scattered notes.
2. **STATUS is a pointer, not a spec** — keep it short; detail belongs in the spec file.
3. **Specs before large code** — multi-file features get a prepared task spec first; implementation follows the spec.
4. **Don't re-spec done work** — read `docs/specs/done/`; only reopen with an explicit change request.
5. **Link, don't duplicate** — architecture stays in `docs/architecture/`; done specs link to it.
6. **Test artifacts are context** — `testing/results/<env>/` samples help agents see real output shape.
7. **Number specs** — use ticket numbers in filenames (`*_11.md`) for stable IDs; use **Build queue** for priority, not numeric sort.
8. **Registry is source of truth for `#`** — create and retire numbers only via `docs/specs/TICKET_REGISTRY.md`.

---

## Tech Stack

- **Language:** Python 3.12
- **API:** FastAPI + Pydantic v2 + SQLAlchemy 2.0
- **DB:** PostgreSQL + pgvector + Alembic
- **Queue:** Redis
- **Agent orchestration:** CrewAI (`signal_gather`), Claude CLI (`claude_agent`)
- **Containers:** Docker Compose (local) → single-node VPS (production)
- **Embeddings:** OpenAI `text-embedding-3-small`
