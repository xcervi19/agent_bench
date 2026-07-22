# Hybrid Pipeline Orchestration — #36

**Status:** planned  
**Lane:** Platform / Backend  
**Goal:** Refactor the Newsfind pipeline so Python orchestrates deterministic steps and agents handle only judgment-heavy stages — improving reliability, debuggability, eval separation (P1–P3), and token cost.

## Problem

Today `/newsfind-plan` runs framing, RAG, source discovery, and query design in **one long agent session**. Failures are hard to isolate, artifacts are coarse-grained, and source grounding (#29 whitelist, #30 playbooks) is not enforced before the agent searches the open web.

The existing Python shell (`apps/claude_agent/topics/pipeline.py`) only chains two agent legs (`plan` → `deliver`). Deterministic work (whitelist lookup, playbook RAG, scrape, search execution) is left inside agent prompts instead of code.

## Target architecture

**Python = conductor. Agent = analyst only where judgment is required.**

```
topic
  → [Python] source_discover     whitelist + playbook RAG → source_targets.json
  → [Python] topic_parse         optional LLM once → facets.json (commodity/geo/entities/signals)
  → [Agent]  plan                framing + query plan only → parsed.json (thin session)
  → [Python] execute_search      WebSearch/scrape per query plan → raw_hits.json
  → [Agent]  deliver             dedup, score, synthesize → report.json / report.md
  → [Python] refresh             scheduler + delta (#22) — unchanged pattern
```

Reuse the artifact + fingerprint pattern from `apps/claude_agent/orchestrator.py` (see `docs/specs/done/reproducible_artifacts_and_cache.md`) **at every stage boundary**, not only `/newsfind-queries`.

## Scope

### In scope

1. **`source_discover` Python module** (`apps/claude_agent/sources/discover.py` or `scripts/source_discover.py`):
   - Load `source_whitelist.json` (repo root).
   - Query playbook RAG (`document_type: playbook`) for topic/entity matches.
   - Output `source_targets.json`:

     ```json
     {
       "entities": [
         {
           "entity": "NIOC",
           "known_domains": ["shana.ir"],
           "playbook_refs": ["iran_oil_geopolitics.md"],
           "signals": ["production", "exports"],
           "type": "official"
         }
       ]
     }
     ```

   - No hallucinated domains; whitelist is the hard filter (#29).

2. **Extend `pipeline.py`** with explicit pre-plan stage:
   - `run_source_discover(topic_id, topic, run_dir)` before `run_plan`.
   - Write `source_targets.json` into the plan run directory.
   - Emit SSE events: `stage.started` / `stage.finished` with `stage: "source_discover"`.

3. **Thin `/newsfind-plan`**:
   - Remove inline source-discovery logic from the prompt.
   - Read `source_targets.json` from run dir; use it when building `queries[]` and `parsed.json`.
   - Agent session scope = P1 framing + P2 query design only.

4. **Optional stage: `execute_search` (MVP stub acceptable)**:
   - Python runs configured search/scrape calls from `parsed.json` queries.
   - Writes `raw_hits.json` for deliver agent to consume.
   - If full implementation is too large for one ticket, stub the interface + artifact schema and keep search in deliver agent temporarily — but **document the contract**.

5. **Artifact layout** — extend run directory:

   ```
   state/news/<hash>/runs/<run_id>/
     input.json
     source_targets.json      ← new (Python)
     facets.json              ← optional
     parsed.json              ← agent (plan)
     raw_hits.json            ← new (Python, or stub)
     summary.json
   ```

6. **Tests**: offline unit tests for `source_discover` (whitelist filter, dedup by domain); pipeline integration test that plan run dir contains `source_targets.json` before agent starts.

### Out of scope

- Graph retrieval layer (#35) — later v2.
- Full social scrape execution (#31) — integrate when #31 ships; this ticket defines the hook (`source_targets` → scrape queue).
- Frontend changes (#16).
- Replacing `/newsfind-refresh` agent (keep as-is for now).

## Dependencies

| Ticket | Relationship |
|--------|--------------|
| **#29** Source whitelist | **Required** — `source_whitelist.json` must exist and be loaded by Python |
| **#30** Coverage playbooks | **Required** — at least one playbook ingested for RAG lookup |
| **#32** `/source-discover` skill | **Optional overlap** — core logic should live in Python; skill may wrap the same module for Cursor/dev use |
| **#31** Scraping infrastructure | **Soft dependency** — scrape stage plugs in later |
| **#33** Plan source integration | **Superseded** — do not implement agent-inline `/source-discover` in `newsfind-plan.md`; use Python pre-stage instead |

## Why now

- Whitelist (#29) and catalog merge are done (`source_whitelist.json`, `catalog_final.json`).
- Playbooks (#30) are the next platform input this ticket consumes.
- Fixes the root cause of unreliable search: agent guessing domains before consulting ground truth.
- Enables per-phase evaluation (#18/#23): P1/P2/P3 become separate artifacts with pass/fail.

## Acceptance criteria

- [ ] `source_discover` Python module exists and is callable without an LLM.
- [ ] `run_plan` pipeline path invokes `source_discover` **before** the plan agent; `source_targets.json` is written to the run dir.
- [ ] `/newsfind-plan` reads `source_targets.json`; `parsed.json` includes `source_targets[]` (entity, known_domains, playbook_refs).
- [ ] Plan agent prompt no longer instructs open-ended domain discovery — it consumes pre-resolved targets.
- [ ] SSE events include `source_discover` stage in the plan leg.
- [ ] Offline tests pass for whitelist filtering and pipeline pre-stage wiring.
- [ ] Changes versioned in Git; `STATUS.md` Build queue updated.

## Implementation notes

- Follow existing patterns: `pipeline.py`, `orchestrator.py`, `artifacts.py`, `RunRecorder`.
- Whitelist path: repo root `source_whitelist.json` (610 entries today).
- Playbook RAG: use existing `RAG_BASE_URL` / tenant env vars (same as `newsfind-plan` Phase 2).
- Fingerprint/cache: include whitelist hash + playbook corpus version in plan-stage fingerprint when caching is added.
- Keep backward compatibility: if `source_targets.json` is missing (old runs), plan agent falls back with a logged warning.

## Related files

- `apps/claude_agent/topics/pipeline.py` — extend with pre-plan stage
- `apps/claude_agent/orchestrator.py` — artifact/fingerprint pattern to replicate
- `claude_agent_fe/.claude/commands/newsfind-plan.md` — thin down
- `source_whitelist.json` — ground truth input
- `local_knowledge_sources/playbooks/` — RAG input (#30)
- `docs/specs/active/plan_source_integration_33.md` — superseded approach

## Suggested execution order (Platform lane)

```
#29 (whitelist) ──► #30 (playbooks) ──► #32 (discover module/skill) ──► #36 (this ticket)
                                              └──► #31 (scraping, parallel) ──► hooks into #36 later
#35 (graph) — after #36 MVP measured
```
