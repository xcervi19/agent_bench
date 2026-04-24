# Agentic Platform Framework — Iteration 1 (Simple MVP)

## 1. Purpose

This document defines the first implementation iteration focused on:
- Fast development speed
- Reliable local setup
- Easy first client demos
- Low operational complexity

Iteration 1 is intentionally minimal. The goal is to prove that the system can ingest trading information, retrieve relevant knowledge, and generate useful insights with a small, stable architecture.

## 2. Iteration 1 Outcomes

By the end of this iteration, the team should be able to:
- Run the full system locally with one command
- Load sample trading knowledge and recent data
- Ask a query and get grounded, useful results
- Demo tenant-aware behavior for first client conversations
- Add or modify one crew/agent quickly without infra changes

## 3. Scope Boundaries

### In scope
- API service
- Worker service
- Scheduler service
- PostgreSQL with pgvector
- Redis queue/cache
- S3-compatible object storage
- Basic authentication + tenant_id isolation
- Deterministic seed data and one replay flow

### Out of scope (moved to Iteration 2)
- Kubernetes deployment
- Terraform infrastructure automation
- Full Prometheus/Grafana stack
- Advanced autoscaling policies
- Complex RBAC matrix
- Multi-cluster/high availability setup

## 4. Architecture (Simple by Design)

Four services only:

1. API Service (FastAPI)
- Receives requests
- Stores tasks and returns status/results

2. Agent Worker Service
- Executes background jobs and crews
- Writes events/signals/results into Postgres

3. Scheduler Service
- Runs periodic discovery and cleanup jobs

4. Supporting Services
- PostgreSQL + pgvector (main relational DB + embeddings)
- Redis (task queue + short-lived cache)
- S3-compatible storage (raw documents)

Communication model:
- API to Worker via Redis jobs
- Services read/write Postgres with tenant_id filtering
- Agents read documents from object storage

## 5. Technology Stack (Iteration 1 Locked)

- Language: Python 3.12
- API: FastAPI + Pydantic v2 + SQLAlchemy 2.0
- Database: PostgreSQL + Alembic + pgvector
- Queue/Cache: Redis
- Agent orchestration: CrewAI
- Storage: boto3 with S3-compatible backend
- Containerization: Docker + Docker Compose
- CI (minimal): GitHub Actions for lint/test/build

## 6. Data and Retrieval Strategy

Iteration 1 uses a single database approach:
- Structured data and embeddings in PostgreSQL
- Semantic retrieval using pgvector
- Optional lexical matching using Postgres full-text search

This keeps operations simple and reduces services to maintain.

## 7. Multi-Tenancy (MVP Level)

- tenant_id on core business records
- Row-level security in Postgres for tenant isolation
- Redis keys prefixed by tenant when needed
- JWT includes tenant context

## 8. Development Workflow

One-command startup:

```bash
docker compose up --build
```

Typical flow:
1. Start stack
2. Seed deterministic demo data
3. Run one ingestion scenario
4. Ask demo queries and validate output quality
5. Replay one agent session for debugging

## 9. Demo-Ready Use Case

Primary demo narrative:
- Load internal trading knowledge
- Discover fresh external market signals
- Retrieve relevant context with pgvector
- Generate concise specialist insight for a user profile

## 10. Quality Gates for Iteration 1

A release candidate is ready when:
- New developer can run system in under 15 minutes
- End-to-end demo query works consistently
- Seed + replay commands are deterministic
- Basic tenant isolation checks pass
- Error traces are readable and actionable

## 11. Success Criteria

Iteration 1 is successful if it proves business value with minimal complexity:
- Fast learning loops for the team
- Confident first client demos
- Clear path to production upgrades without rewrite

This iteration optimizes for speed, clarity, and reliability over completeness.
