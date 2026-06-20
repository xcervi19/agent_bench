# Archive — legacy platform code

The **Signal Gather** CrewAI stack (`apps/signal_gather`, Redis workers, compose
`api`/`worker`/`scheduler`) was removed from `main` in **#25** (2026-06).

## Restore the full platform tree

```bash
git fetch origin
git checkout archive/signal_gather-platform
# or pin the snapshot:
git checkout archive/pre-slim-2026
```

| Ref | Purpose |
|-----|---------|
| Branch `archive/signal_gather-platform` | Long-lived revival branch (same as pre-slim `main`) |
| Tag `archive/pre-slim-2026` | Immutable snapshot before cleanup |

## What stayed on `main`

| Component | Role |
|-----------|------|
| `apps/claude_agent` | Newsfind topic pipeline (product) |
| `apps/rag_adhoc` | RAG search API + `documents`/`events` models |
| `libs/agentic_core` | Auth, DB, health, middleware (#24) |
| `source_ingest` / `oil_rag_collector` | RAG corpus ops |
| `libs/eval_framework` | Lane A evaluation |

Historical design doc: [`framework_legacy.md`](framework_legacy.md).
