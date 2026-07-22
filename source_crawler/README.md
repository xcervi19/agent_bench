# source_crawler

Extensible crawl/download foundation for web documents and news.

**Architecture:** [`docs/architecture/source_crawler.md`](../docs/architecture/source_crawler.md)  
**Operator guide (full pipeline + semi-auto):** [`docs/architecture/source_acquisition_pipeline.md`](../docs/architecture/source_acquisition_pipeline.md)  
**Labels:** [`docs/knowledge/rag_label_vocab.md`](../docs/knowledge/rag_label_vocab.md)

## Pipeline

```
crawl   → artifacts/collected/
extract → artifacts/collected_text/  (+ qa_prompt.md)
/source-qa (Cursor or claude_agent) → qa_audit.json
apply-qa → artifacts/rag_corpus/{document_type}/tier_{n}/{domain}/
from_collected → chunks → ingest
```

## Human label gate

Every enrolled source **must** set `label_assignment`:

| Value | Meaning |
|-------|---------|
| `human` | You set `document_type` + `use_for` in the seed |
| `agent` | You ack deferral; QA agent fills labels from vocab |

Missing acknowledgment → crawl/promote blocked.

## Commands

```bash
uv run python -m source_crawler crawl
uv run python -m source_crawler crawl --seed agency_oil_data  # OPEC MOMR/ASB + JODI
uv run python -m source_crawler extract
# /source-qa in Cursor → writes artifacts/collected_text/qa_audit.json
uv run python -m source_crawler apply-qa --dry-run
uv run python -m source_crawler apply-qa
uv run python -m source_ingest.from_collected --sources-dir artifacts/rag_corpus
```

### Browser fetch (Akamai / Platts poloautomat)

When HTTP crawl gets `403`, use browser for the download only; everything else is automatic:

```bash
# 1) Opens SAVE_THESE.html and watches inbox + ~/Downloads (15 min)
uv run python -m source_crawler browser-fetch --extract

# 2) You: for each link → open → Save into artifacts/download_inbox/
#    (or default Downloads; name like URL basename is enough)

# 3) When all matched → written to artifacts/collected/<source_id>/ + meta/labels
#    With --extract also rebuilds collected_text / qa_prompt
```

One-shot import without watch:

```bash
uv run python -m source_crawler import-local
```

Legacy path `artifacts/oil_rag_sources/` is superseded by `artifacts/rag_corpus/`.

```bash
uv run pytest tests/source_crawler/ -q
```
