### 1. Purpose & Vision

We are building a **reusable, multi-agent orchestration framework** in Python.  

The framework acts as a **generic, installable core** (`agentic-core`) that handles all common infrastructure and orchestration needs. Domain-specific applications (starting with **Signal Gather** – our AI Market Intelligence Platform for commodity trading) are built as clean extensions on top of it.

- Framework = zero domain logic, fully reusable for future apps (energy, finance, supply-chain, etc.).
- Applications = domain models, agents, routers, and scheduler jobs.
- Goal: Rapid development of sophisticated agentic systems while maintaining full production readiness, local/production parity, and multi-tenancy.
- Target initial scale: 1–3 enterprise clients per deployed instance.

### 2. Core Principles (Non-Negotiable)

- **Full environment parity**: `docker compose up` locally behaves identically to production (except config and scale).
- **Reproducibility**: Deterministic seeding, scenarios, and event replay for debugging.
- **Clean separation**: Framework provides orchestration; apps provide business logic.
- **Dependency on mature open-source libraries** (no forking): We depend on proven libraries via `pyproject.toml` for agent orchestration, API, DB, etc.
- **Monorepo structure** for easy development and shared code.
- **Multi-tenant ready** from day one (row-level security, prefixed storage).
- **Simple & scalable**: Start with single-node k3s on Hetzner; horizontal scaling built-in.
- **Best practices**: Observability, security, IaC, CI/CD, zero-downtime deploys.

### 3. High-Level Architecture

Four main long-running services + supporting infrastructure:

1. **API Service** (FastAPI)  
   Handles HTTP requests, authentication, task submission, user profiles, signals, insights, reports, and search.

2. **Agent Worker Service**  
   Processes background tasks from Redis queue.  
   Executes agent workflows (ingestion, document intelligence, signal detection, personalized analysis).

3. **Scheduler Service**  
   Runs periodic jobs (data discovery, report generation, cleanup, dynamic queries) using APScheduler or similar.

4. **Supporting Services**  
   - PostgreSQL (event store, signals, users, profiles)  
   - Redis (task queues, caching)  
   - Weaviate (vector embeddings for knowledge retrieval – enabled by default)  
   - S3-compatible storage (Hetzner Object Storage for raw documents)

Communication: HTTP (API ↔ workers), Redis queues, direct DB (with tenancy filters).

### 4. Technology Stack (Locked)

- **Language**: Python 3.12
- **API**: FastAPI + Pydantic v2 + SQLAlchemy 2.0
- **Database**: PostgreSQL + Alembic migrations
- **Queue/Cache**: Redis
- **Vector DB**: Weaviate
- **Containerization**: Docker (multi-stage builds)
- **Local**: Docker Compose
- **Production**: Kubernetes (k3s on Hetzner) + Helm
- **IaC**: Terraform
- **CI/CD**: GitHub Actions + GHCR
- **Agent Orchestration**: **CrewAI** (primary choice – role-based multi-agent teams)  
  **Rationale**: CrewAI maps naturally to Signal Gather roles (Discovery Agent, Document Intelligence Agent, Signal Engine Agent, Personalized Trader/Analyst Agent). It is fast for prototyping, has good production adoption, and integrates cleanly with FastAPI + Redis workers. We depend on it normally (`crewai` in `pyproject.toml`). Thin wrappers in the framework will register crews, tools, and integrate with our task queue and replay system.
- **Storage**: boto3 for S3
- **Observability**: Structured logging + Prometheus + Grafana (in Helm chart)
- **Auth**: FastAPI Users + JWT + RBAC (tenant-aware)

### 5. Repository Structure (Monorepo)

```
agentic-platform/
├── libs/
│   ├── agentic-core/          ← Installable framework package (pip installable)
│   │   ├── api/               ← Base FastAPI setup, routers, auth
│   │   ├── workers/           ← Task queue integration, base worker
│   │   ├── agents/            ← Base classes, CrewAI wrappers, tool registry, replay hooks
│   │   ├── scheduler/         ← Base scheduler jobs
│   │   ├── database/          ← SQLAlchemy models, Alembic config
│   │   ├── storage/           ← S3 client
│   │   └── testing/           ← Replay engine, scenarios
│   ├── agentic-infra/         ← Terraform modules + Helm templates
│   └── ...
│
├── apps/
│   └── signal_gather/          ← First application (commodity trading intelligence)
│       ├── agents/            ← Specific crews: discovery_crew, document_intelligence_crew, personalized_trader_crew, etc.
│       ├── models/            ← Domain SQLAlchemy models (Event, Signal, UserProfile, Document)
│       ├── routers/           ← Signal Gather–specific endpoints (/signals, /events, /insights)
│       ├── scheduler_jobs/    ← commodity_discovery_job.py, daily_briefing.py
│       └── scenarios/         ← seed_scenario_commodity_trading.py
│
├── docker/                    ← Base Dockerfiles + app-specific overrides
├── helm/
│   └── agent-platform/        ← Helm chart (deploys core + selected apps)
├── terraform/                 ← Hetzner resources (k3s, network, storage, etc.)
├── database/
│   ├── migrations/
│   └── seeds/
├── scripts/                   ← replay_session.py, synthetic_data.py
├── pyproject.toml             ← Workspace + dependencies (including crewai)
├── docker-compose.yml
├── .env.example
└── README.md
```

### 6. How Applications Are Built on the Framework

1. Developer works in `apps/signal_gather/` (or any future app folder).
2. Imports from `agentic_core.*` (e.g., `from agentic_core.agents import BaseCrewWrapper`).
3. Defines domain-specific models, CrewAI crews/agents/tasks, routers, and scheduler jobs.
4. Registers them with the framework (via config or entry points).
5. Runs `docker compose up --build` → full system (core framework + Signal Gather) starts locally.
6. CI/CD builds combined Docker images containing framework + app code.
7. Helm deploys the tagged image to the cluster.

This is clean **build-time composition** — no runtime code injection.

### 7. Local Development Workflow (One Command)

```bash
git clone <repo>
cd agentic-platform
cp .env.example .env
docker compose up --build
```

Additional commands:
- Seed data: `python -m database.seeds.seed_dev_data`
- Run scenario: `python -m database.seeds.seed_scenario signal_gather_commodity_trading`
- Replay session: `python scripts/replay_session.py --session-id=abc123`

### 8. Production Deployment Workflow

1. `terraform apply` → provisions k3s cluster on Hetzner (single node sufficient for pilot; 4 vCPU / 8–16 GB RAM).
2. `helm upgrade --install agent-platform helm/agent-platform --set app=signal_gather`
3. Automatic Alembic migrations on startup.
4. Worker pods scale horizontally based on Redis queue depth / CPU.

**Multi-tenancy**: Row-level security in Postgres, prefixed Redis/Weaviate keys, tenant_id in JWT.

### 9. Key Framework Features

**Agentic Platform Framework – Main Features**  
**(Functional & Technical Capabilities)**

Here is a clear, direct description of the **main features** of the framework, written from the perspective of **what the system can actually do** (functionality-first):

### Core Platform Features

- **Multi-Service Architecture**  
  The framework runs three independent services that work together:  
  - **API Service**: Accepts HTTP requests, manages users, submits tasks, and returns results (signals, insights, reports).  
  - **Agent Worker Service**: Executes long-running agent workflows asynchronously in the background.  
  - **Scheduler Service**: Automatically runs periodic jobs (e.g., data discovery, report generation, cleanup).

- **Task Queue Management**  
  - Submit tasks from API to a background queue (Redis).  
  - Workers pick up tasks, process them, and update status in real time.  
  - Supports task status tracking (pending, running, completed, failed), retries, and queuing of agent workflows.

- **Database & Persistence**  
  - Stores users, tasks, structured events, market signals, user profiles, and audit logs in PostgreSQL.  
  - Uses Alembic for safe, version-controlled database schema changes (migrations).  
  - Supports multi-tenancy using row-level security (each client sees only their own data).

- **Vector Database & Semantic Search**  
  - Built-in Weaviate vector database.  
  - Ability to store document embeddings and structured events.  
  - Agents can perform **semantic similarity search** (find similar events, documents, or signals by meaning, not just keywords).  
  - Enables powerful knowledge retrieval for agents (e.g., “find all past gas supply disruption events in Europe”).

- **Object Storage for Documents**  
  - Automatically stores raw documents (PDFs, HTML, text) in S3-compatible storage (Hetzner Object Storage).  
  - Agents and workers can retrieve original documents when needed for re-analysis or auditing.

- **Event Replay & Debugging**  
  - Every agent session (user request → agent actions → tool calls → final response) is fully recorded.  
  - Developers can replay any session locally with one command: `python scripts/replay_session.py --session-id=xxx`.  
  - Greatly simplifies debugging complex agent behavior.

- **Deterministic Seeding & Scenarios**  
  - Easy commands to populate the system with realistic test data.  
  - Predefined scenarios (e.g., `scenario_commodity_trading`, `scenario_multi_user_collaboration`, `scenario_agent_failure`).  
  - Allows consistent testing and demo preparation.

### Agent Intelligence Features

- **CrewAI-Based Agent Orchestration**  
  - Supports creation of role-based multi-agent teams (crews).  
  - Example roles: Discovery Agent, Document Intelligence Agent, Signal Detection Agent, Personalized Trader Agent.  
  - Agents can call tools, use structured outputs (Pydantic), and write results directly into the database or vector store.

- **Hybrid Data Ingestion & Processing Pipeline**  
  - Scheduler triggers discovery jobs (search APIs, RSS feeds, structured APIs).  
  - Workers download documents, clean them, detect language, translate if needed.  
  - Document Intelligence agents extract entities, detect events, and analyze market impact.  
  - Results are stored as structured Events and Signals.

- **Personalized Agent Analysis**  
  - Each user has a profile (watched commodities, regions, themes, risk preferences).  
  - Personalized crews interpret events and generate tailored insights, signals, and alerts.

- **Signal Detection Engine**  
  - Combines rule-based logic + agent-based reasoning to detect market-moving signals.  
  - Agents can aggregate multiple events and generate higher-level insights.

### Production & Operational Features

- **Full Local-to-Production Parity**  
  - Run the entire system locally with one command: `docker compose up`.  
  - Same services, same behavior as production (only configuration differs).

- **Infrastructure & Deployment**  
  - Terraform scripts to provision infrastructure on Hetzner (k3s Kubernetes).  
  - Helm chart for easy deployment and upgrades.  
  - GitHub Actions CI/CD pipeline (test → build images → push → deploy).

- **Observability**  
  - Structured logging for all services.  
  - Prometheus metrics for monitoring queue depth, task success rate, agent execution time, etc.  
  - Ready for Grafana dashboards.

- **Security & Multi-Tenancy**  
  - Tenant isolation from day one (data separation between clients).  
  - JWT-based authentication with role-based access control.



### 10. Signal Gather – First Pilot Application (Context)

Signal Gather transforms raw information → structured events → market signals → personalized trader insights for power, gas, LNG, coal, and carbon markets.  
It uses the framework to implement:
- Hybrid discovery (search APIs, RSS, structured APIs, limited scraping)
- Document Intelligence crews
- Rule + agent-based signal detection
- Personalized analyst/trader crews based on user profiles

All Signal Gather code lives **only** in `apps/signal_gather/`. The framework stays domain-agnostic.

### 11. Success Criteria

After implementation, any team member must be able to:
- Clone the repo and start the full system locally in minutes.
- Add new agents/crews or a new application without touching core framework code.
- Deploy to Hetzner using Terraform + Helm.
- Debug any agent run via replay.
- Scale to multiple clients with isolated tenants.

This framework will be our central reusable asset for all future agentic products.

