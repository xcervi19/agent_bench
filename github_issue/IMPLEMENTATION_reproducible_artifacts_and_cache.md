# Implementation: Reproducible Run Artifacts & Token-Aware Cache for `/newsfind-queries`

**Status:** ✅ Completed  
**Related Issue:** Agentic Search Structured Claude Code Architecture #9  
**Date:** May 9–10, 2026

---

## What We Built

A complete **reproducible artifact layer** for the `/newsfind-queries` Stage 1 command that:

1. **Preserves every run** — request, live stream events, raw API wrapper, parsed business JSON, metadata — all on disk for replay and debugging.
2. **Avoids duplicate Claude calls** — fingerprints the input and returns cached results when the same topic+args+config is run again.
3. **Keeps full history** — old runs stay on disk; new runs can be forced on demand.

This means Stage 2 and beyond can **consume cached `parsed.json` instead of re-invoking Claude**, saving tokens and time.

---

## Problem We Solved

Before: Every `/newsfind-queries` call hit Claude's API, even if the exact same topic had just been queried. After Stage 1, upper logic had **no way to access cached output** — each pipeline stage would independently re-run Claude.

After: The system detects identical inputs via a stable fingerprint, returns cached results instantly, and preserves both the live stream and the structured business JSON on disk for any downstream consumer.

---

## How It Works

### 1. **Artifact Storage Layout**

Each successful run writes to disk:

```
state/news/<topic_id>/
  ├── index.json                          # Topic index: run history + latest pointer
  └── runs/<run_id>/
      ├── request.json                    # What was asked (args, model, timeout, force_refresh)
      ├── stream.ndjson                   # Raw CLI events, one per line (for replay/debug)
      ├── raw_result.json                 # Full API wrapper (type=result, duration, cost, etc.)
      ├── parsed.json                     # Business JSON only (what Stage 2 consumes)
      └── meta.json                       # Metrics (duration_ms, total_cost_usd, fingerprints, status)
```

### 2. **Caching via Input Fingerprint**

Before calling Claude, we hash:

```
command + args + command_file_hash + schema_hash 
+ schema_version + env_version + model + permission_mode
```

Result: a deterministic `input_fingerprint`. If a previous successful run has the same fingerprint, **use its `parsed.json` instead of calling Claude again.**

### 3. **Force-Refresh on Demand**

Pass `"force_refresh": true` in the request to bypass cache and always call Claude. The new run becomes `latest_queries_run_id`; the old run stays on disk for comparison.

---

## Key Features

| Feature | Benefit |
|---|---|
| **Fingerprint-based cache** | Same topic+args = instant result, no tokens spent |
| **Env/schema versioning** | Bump `CLAUDE_AGENT_ENV_VERSION` to invalidate all caches globally (e.g., after prompt edit) |
| **Full stream capture** | `stream.ndjson` lets you debug, replay, or analyze how Claude reasoned through the problem |
| **Per-run metadata** | `meta.json` tracks `duration_ms`, `total_cost_usd`, `output_fingerprint` for optimization & billing |
| **History preservation** | Old runs never deleted; `index.json` tracks all runs so you can read any historical `parsed.json` |
| **Force-refresh** | On-demand refresh without cache invalidation — new run appended, latest pointer updated |

---

## Files Changed

### New Files
- `apps/claude_agent/artifacts.py` — `ArtifactStore`, `RunRecorder`, fingerprinting, atomic writes
- `apps/claude_agent/orchestrator.py` — `run_newsfind_queries()` & `stream_newsfind_queries()` with cache logic

### Modified Files
- `apps/claude_agent/config.py` — `state_dir`, `state_index_prefix`, `schema_version`, `env_version`
- `apps/claude_agent/schemas.py` — `RunRequest.force_refresh`, `RunResult` fields for caching metadata
- `apps/claude_agent/routes.py` — dispatch `/newsfind-queries` to orchestrator (both `/run` and `/stream`)
- `apps/claude_agent/jobs.py` — background jobs also use orchestrator
- `docker-compose.yml` — mount `./state:/state:rw` for artifact persistence
- `apps/claude_agent/.env` — artifact settings (state dir, schema/env versions)
- `debugging_readme.md` — user-facing docs on cache, fingerprints, force-refresh
- `.gitignore` — ignore `state/` directory (only `state/.gitkeep` in git)

---

## Acceptance Criteria Met

✅ **Same input reused without another Claude call**  
→ `find_cached()` in orchestrator checks fingerprint before `stream_claude()`

✅ **Inspect full stream after the run**  
→ Every event written line-buffered to `stream.ndjson`

✅ **Parse business output without reading stream logs**  
→ `parsed.json` contains only the business object; separate from stream

✅ **Stage 2 consumes `latest_queries_parsed_path` from `index.json`**  
→ `index.json` updated on every successful run; `latest_queries_parsed_path` points to the most recent

✅ **Cost/duration preserved for optimization**  
→ `meta.json` records `duration_ms`, `total_cost_usd` per run

✅ **Files are the source of truth (no DB)**  
→ All persistence is on-disk; `index.json` is the coordination layer

---

## Usage Examples

### Default: Cache-aware run
```bash
curl -X POST http://localhost:8002/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{
    "command": "/newsfind-queries",
    "args": "Hormuz strait closure options to lower price",
    "timeout_sec": 900
  }' | jq '{cached, run_id, status, parsed_path}'
```

**First call:** Calls Claude, writes artifacts  
**Second call (same args):** Returns cached `parsed.json` instantly, `cached: true`

### Force a fresh run
```bash
curl -X POST http://localhost:8002/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{
    "command": "/newsfind-queries",
    "args": "Hormuz strait closure options to lower price",
    "force_refresh": true,
    "timeout_sec": 900
  }'
```

**Result:** Bypasses cache, calls Claude, appends new run to `runs[]`, updates `latest_*` pointers. Old run preserved.

### Streaming (SSE) with cache transparency
```bash
curl -N -X POST http://localhost:8002/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{
    "command": "/newsfind-queries",
    "args": "...",
    "timeout_sec": 900
  }'
```

**Cache hit:** Emits `cache_hit`, then a synthetic `result` event with `cached: true`, then `end`  
**Cache miss:** Emits `run_started`, then all live Claude events, then `artifact_finalized`, then `end`

---

## Invalidating Cache

Choose the right lever:

| Goal | Action | Scope |
|---|---|---|
| Force one topic fresh | `"force_refresh": true` in request | One call |
| Edit prompts, invalidate all | Bump `CLAUDE_AGENT_ENV_VERSION` | All topics |
| Schema shape changed | Bump `CLAUDE_AGENT_SCHEMA_VERSION` | All topics |
| Delete topic history | `rm -rf state/news/<topic_id>/` | One topic, wipe history |

---

## Architecture Notes

- **Single responsibility:** `artifacts.py` owns I/O; `orchestrator.py` owns logic
- **No external DB:** Files on disk are the single source of truth; `index.json` is the manifest
- **Backward-compatible API:** Existing `/run` and `/stream` endpoints unchanged; caching is transparent
- **Extensible:** Design supports future stages (Stage 2, 3, 4) — each records its own artifact set in the same layout
- **Auditable:** Every call's `request.json` includes `force_refresh` flag, so replays know the intent

---

## Testing & Verification

✅ Unit tests pass: fingerprint differentiation, cache miss/hit, history preservation  
✅ E2E test: seed run → cache hit (no Claude call) → force_refresh run (new run appended)  
✅ Imports clean: all new modules load without errors  
✅ Linter: no lint errors in new/modified files  
✅ Smoke test: real fixture (`artifacts/agent_output/querires1.json`) round-trips through the artifact layer

---

## Deployment

### Local dev
```bash
docker compose build claude_agent
docker compose up -d claude_agent
```

### VPS
```bash
scp -i ~/.ssh/contabo_ed25519 ./apps/claude_agent/.env root@79.143.179.212:~/agent_bench/apps/claude_agent/.env
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench
git pull origin main
docker compose build claude_agent
docker compose up -d claude_agent
docker compose logs -f claude_agent
```

The container now mounts `./state` (host) at `/state` (container) for artifact persistence.

---

## Next Steps

This implementation enables:

1. **Stage 2 (Intro)** — Read `latest_queries_parsed_path` from `index.json`, consume cached `parsed.json` without re-invoking Claude
2. **Multi-stage orchestration** — Each stage follows the same artifact pattern; `index.json` tracks lineage
3. **Webhook delivery** — Emit events as topics flow through stages; subscribers receive structured JSON
4. **User gates** — Pause pipeline after Stage 1, let user edit queries before proceeding to Stage 2
5. **Billing & optimization** — Analyze `meta.json` across runs to find costly or slow topics

---

## Questions / Debugging

See `debugging_readme.md` for:
- How to force a fresh run
- How to read historical runs
- How to invalidate the cache
- What the stream events look like
- How to inspect artifacts on disk
