# Source Crawler — Architecture

**Package:** `source_crawler/`  
**Status:** foundation + `static_pdf` crawl path shipped  
**Tests:** `tests/source_crawler/`  
**Operator process (diagrams + checklist):** [`source_acquisition_pipeline.md`](source_acquisition_pipeline.md)

## Purpose

Extensible module for crawling and downloading documents/news from the internet. Source-specific logic lives in adapters so new sources can be added without changing the core.

Distinct from `oil_rag_collector` (static curated batch downloads) and `source_ingest` (chunk → embed → Postgres). This module owns **ongoing, configurable acquisition**; ingest stays downstream.

## Shipped surface

| File | Role |
|------|------|
| `models.py` | Data contracts |
| `base.py` | `SourceAdapter` ABC |
| `registry.py` | Name → adapter registration / lookup |
| `adapters/static_pdf.py` | Fixed-URL PDF fetch (Argus/Platts methodology pattern) |
| `store.py` | Write content + `.meta.json` under collector root |
| `runner.py` | `crawl` / `crawl_many` (hash watermark skip) |
| `seeds/pricing_methodology.py` | Platts + Argus methodology URL catalog (`promote=True`) |
| `extract.py` | `collected` → `collected_text` via `source_ingest.text_extract` |
| `qa_pack.py` | `qa_pack.json` + aggregate `qa_prompt.md` (deterministic samples) |
| `promote.py` | Gate: `collected` → `rag_corpus` |
| `labels.py` | Controlled vocab + human/agent label gate |
| `browser_assist.py` | Semi-auto import for CDN-blocked PDFs (inbox watch) |
| `cli.py` / `__main__.py` | `python -m source_crawler crawl|extract|qa-pack|promote` |

Agent slash command: `/source-qa` in Cursor (`.cursor/commands/`) and `claude_agent_fe` (VPS). Not shipped yet: scheduler hook, whitelist gate on enroll.

## Design

```
SourceTarget
    → adapter.evaluate()  → SourceAssessment (+ optional SourceConfig)
SourceConfig
    → adapter.discover()  → list[DocRef]
DocRef + SourceConfig
    → adapter.fetch()     → DownloadedDoc
```

Python owns deterministic crawl/fetch. Agents (later) own judgment: whether a source is worth enrolling and what `SourceConfig` to propose. Same split as hybrid pipeline (#36): conductor vs analyst.

### Contracts

| Type | Meaning |
|------|---------|
| `SourceTarget` | Candidate URL (+ optional `source_id`, `hints`) to evaluate |
| `SourceAssessment` | Probe result: `viable`, `reason`, optional `proposed_config` |
| `SourceConfig` | Enrolled source: adapter, endpoint, schedule fields, filters, watermark |
| `DocRef` | Discovered document identity (URL + light metadata) |
| `DownloadedDoc` | Bytes + content type + extension + sidecar-ready `meta` |

`SourceConfig` fields that align with `source_ingest.from_collected` sidecars: `source_id`, commodity/region/tier/domain/tags (via `meta` on write).

### Extension point

```python
class SourceAdapter(ABC):
    name: str

    def evaluate(self, target: SourceTarget) -> SourceAssessment: ...
    def discover(self, config: SourceConfig) -> list[DocRef]: ...
    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc: ...
```

Register with `@register`. Resolve with `get(name)`. Unknown or duplicate names fail fast.

### Adding a source adapter (future)

1. Create `source_crawler/adapters/<name>.py` subclassing `SourceAdapter`.
2. Set unique `name`.
3. Implement `evaluate` / `discover` / `fetch`.
4. Decorate with `@register` and import the module from `adapters/__init__.py` (or runner bootstrap).
5. Cover with a unit test using the same registry `clear()` fixture pattern as `tests/source_crawler/test_registry.py`.

Core (`registry`, `base`, `models`) must not import concrete adapters.

## Crawl + promote pipeline (implemented)

```
crawl(config)   → artifacts/collected/<source_id>/              (bronze raw)
extract()       → artifacts/collected_text/<source_id>/*.txt
                → qa_pack.json + qa_prompt.md (only sources needing review)
/source-qa      → artifacts/collected_text/qa_audit.json  (Agent writes audit)
apply-qa        → promote PASS sources with matching source_sha256 + labels
promote         → artifacts/rag_corpus/{document_type}/tier_{n}/{domain}/
from_collected  → chunks → ingest
```

**Extract:** shared `source_ingest.text_extract` + `normalize_raw_text`. Sidecar marks `layer: collected_text` and `source_sha256` (idempotent). Not mixed into KB raw.

**Label gate:** every `SourceConfig` requires `label_assignment` (`human` \| `agent`).  
`human` → `document_type` + `use_for` set at seed time.  
`agent` → human deferral; QA audit must supply production labels.  
Vocab: `docs/knowledge/rag_label_vocab.md`.

**Promote gate:** normal path is `apply-qa` reading `qa_audit.json` (PASS + `source_sha256` match + resolved labels). Manual `promote --source-id` remains for overrides. `meta.promote` no longer set by seeds. Legacy folder `oil_rag_sources/` is replaced by `rag_corpus/`.

```bash
uv run python -m source_crawler extract
# /source-qa in Cursor Agent mode
uv run python -m source_crawler apply-qa --dry-run
uv run python -m source_crawler apply-qa
uv run python -m source_ingest.from_collected --sources-dir artifacts/rag_corpus
```

Pipeline steps append to `artifacts/collected_text/pipeline_run.json`.

**Akamai / bot-blocked PDFs:** `browser-fetch` opens a local save guide, watches `artifacts/download_inbox/` (+ `~/Downloads`), matches filenames to the seed catalog, writes `collected/<source_id>/` + sidecars/labels. Optional `--extract`.

Still planned: agent `/source-evaluate`, whitelist gate on enroll, scheduler on `interval_hours`.

## Boundaries

| In | Out |
|----|-----|
| Adapter contracts + registry | Chunking / embeddings (`source_ingest`) |
| Per-source download logic (adapters) | Static oil corpus batch (`oil_rag_collector`) |
| Config shape for scheduled crawl | Topic plan/deliver agents (consume artifacts later) |

## Public API

```python
from source_crawler import (
    SourceAdapter,
    SourceTarget,
    SourceAssessment,
    SourceConfig,
    DocRef,
    DownloadedDoc,
    register,
    get,
    names,
)
```

`registry.clear()` is for tests only; do not use in product code.

## Related

- `oil_rag_collector/` — one-shot curated downloads
- `source_ingest/from_collected.py` — consumes content + `.meta.json`
- `docs/specs/active/hybrid_pipeline_orchestration_36.md` — Python conductor pattern
- `docs/specs/active/scraping_infrastructure_31.md` — social adapters later
- `source_whitelist.json` — domain allowlist for enrollment
