# Agent orchestration — two-level model

**Status:** decision (2026-07-24)  
**Not a ticket** — architectural direction; executable work lives in specs (#36, #32, …).

## Decision

Newsfind uses **two levels** of agent + code cooperation:

1. **Level 1 — Python orchestrator (primary)**  
   `pipeline.py` runs deterministic stages directly (no LLM). Agents run only for judgment-heavy work (query design, synthesis, “what does this text mean for the desk”).

2. **Level 2 — Agent SDK via CLI (secondary)**  
   When an agent is already in a session and needs a **fixed capability**, it calls a **versioned CLI** (or future MCP tool) — same Python module the orchestrator uses, not a second implementation.

**Principle:** Python = conductor. Agent = analyst. One module, two entrypoints (library + CLI).

## Target pipeline (Level 1)

Implemented incrementally; first slice is **#36**:

```
topic
  → [Python] source_discover     whitelist + local playbooks → source_targets.json
  → [Python] topic_parse         optional LLM once → facets.json
  → [Agent]  plan                  framing + query plan → parsed.json
  → [Python] execute_search        WebSearch/scrape per query plan → raw_hits.json
  → [Agent]  deliver               dedup, score, synthesize → report
  → [Python] refresh               scheduler + delta (#22)
```

Spec: `docs/specs/active/hybrid_pipeline_orchestration_36.md`

### Stage artifact contracts

Each stage boundary is a JSON file in the run dir. Shipped in #36:

| Artifact | Written by | Shape |
|----------|-----------|-------|
| `source_targets.json` | `[Python] source_discover` | `{"entities": [{entity, known_domains[], playbook_refs[], signals[], type}]}` |
| `parsed.json` | `[Agent] plan` | framing + `queries[]` + `source_targets[]` copied from above |

`execute_search` is **not implemented** (#36 stub). Search stays inside the deliver
agent until #31 ships the scraper. Frozen contract for when it lands:

```json
{"query_id": "q01", "hits": [{"url": "...", "domain": "...", "title": "...", "snippet": "...", "whitelisted": true}]}
```

`raw_hits.json` is `{"queries": [<the object above>, ...]}`. Every hit passes the
#29 whitelist filter before it is written; `whitelisted: false` must never appear.

## When to use which level

| Situation | Use |
|-----------|-----|
| Step always required in a known order | **Level 1** — orchestrator calls Python |
| Optional / iterative lookup mid-reasoning | **Level 2** — agent calls CLI |
| Auth, scheduling, full pipeline sequencing | **Orchestrator only** — never agent-discretionary |
| Cursor / dev interactive workflows | **Level 2** — skill wraps CLI (e.g. #32 `/source-discover`) |

## Level 2 — CLI as agent SDK

Expose **stable verbs**, not internal plumbing:

| Verb (example) | Module / CLI today | Agent use |
|----------------|-------------------|-----------|
| `discover` | `apps.claude_agent.sources` (#32) | Re-resolve entities after plan changes |
| `rag-search` | `rag_adhoc` / curl | Ground a claim, fetch desk context |
| `filter-whitelist` | whitelist helpers (#32) | Validate a candidate domain |
| `execute-queries` | #36 / #31 (future) | Run query plan → `raw_hits.json` |
| `qa-check` | eval / QA harness | Score draft before finalize |

**CLI contract rules:**

- **JSON in / JSON out** — frozen schema; agent reads artifacts, not free-text simulation.
- **Artifacts in run dir** — same fingerprint/cache pattern as `orchestrator.py` / #36.
- **Idempotent where possible** — replayable runs for eval (#15, #23).
- **Prompts:** “Call the tool; do not simulate it.”

**Future:** same functions exposed as MCP tools for autonomous agents and Cursor.

## Playbooks — local vs RAG (related decision)

Two roles; do not conflate:

| Role | Mechanism | Why |
|------|-----------|-----|
| **Where to look** (domains, entities) | Local markdown + whitelist via `#32` | Deterministic, offline, testable; small structured corpus (~55 files) |
| **How/why to read** (signals, cadence, anti-patterns) | RAG-ingested playbooks (`document_type: playbook`) | Semantic context during plan/deliver; books + playbook chunks |

`source_discover` does **not** depend on RAG until `rag_adhoc` supports reliable `document_type` filters. Ingested playbooks remain valuable for agent search sessions, not for hard domain lookup.

## Risks (guardrails)

1. **Two brains** — if orchestrator sequences steps *and* agent freely re-runs them, runs become nondeterministic. Orchestrator owns **ordering**; agent CLI is for **optional** in-session calls only.
2. **Token win is not automatic** — requires thin prompts and mandatory tool use; otherwise the agent narrates what the CLI would do.
3. **YAGNI on SDK** — do not build a general SDK framework before #36 ships real Python stages. Formalize CLI wrappers **after** 2–3 call sites exist.

## Sequencing

| When | What |
|------|------|
| **Now** | #36 — wire `#32` `discover_sources` into `run_plan`; thin plan agent; stub `execute_search` |
| **After #36** | Document CLI contracts for shipped stages; thin agent prompts to call them |
| **Later** | MCP exposure; optional RAG filter for discover if rag_adhoc gains `document_type` |

## Related

- `docs/specs/active/hybrid_pipeline_orchestration_36.md` — Level 1 implementation ticket
- `docs/specs/done/source_discover_skill_32.md` — first Level 1 + Level 2 module
- `docs/specs/done/coverage_playbooks_seed_30.md` — playbook corpus
- `apps/claude_agent/topics/pipeline.py` — orchestrator shell
- `apps/claude_agent/orchestrator.py` — artifact + fingerprint pattern
- `.cursor/skills/source-discover/SKILL.md` — Level 2 skill example
