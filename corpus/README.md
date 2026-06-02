# Oil / WTI RAG — Data Corpus

**Not committed to git** — large binaries live under `L1_raw/` (see root `.gitignore`).

**Data cut-off:** `manifest.json` → `data_cutoff`.

## Pipeline levels

| Level | Folder | Content |
|-------|--------|---------|
| **L1** | `L1_raw/` | Original files (PDF, HTML, JSON, TXT) |
| **L2** | `L2_text/` | Extracted plain text (one `.txt` per L1 file) |
| **L2b** | `L2b_clean/` | **Manual** semantic clean (NOT reproducible) — see `@corpus-l2b-manual-curate` |
| **L3** | `L3_chunks/` | Chunk JSONL — today: `../artifacts/chunks/` |
| **L4** | Postgres | Embeddings + `rag_adhoc` search |

## L1_raw layout

```
L1_raw/
  official_web/     tier_{n}/{domain}/{source_id}.ext
  licensed_books/   {slug}.pdf|.txt
  reference/        oil101.txt
```

**Inventory:** `manifest.json`

## Rebuild L1 (copy only; does not delete legacy folders)

```bash
uv run python scripts/data_processing/consolidate_corpus_l1.py
```

## Build L2 (L1 → clear text)

```bash
uv run python scripts/data_processing/corpus_l1_to_l2_text.py
uv run python scripts/data_processing/corpus_l1_to_l2_text.py --force   # rebuild
```

Mirrors L1 folder structure with `.txt` extension. Report: `L2_manifest.json`.

## L2b manual clean (not scripted)

- Skill: `.cursor/skills/corpus-l2b-manual-curate/`
- Policy: `docs/knowledge/corpus_l2b_manual_policy.md`
- Resume: copy `L2b_run_state.template.json` → `L2b_run_state.json`; set **`current_batch.start`** and **`end`**
- Outputs: `L2b_clean/`, `L2b_provenance/` (gitignored)

```text
@corpus-l2b-manual-curate resume from L2_text/...
```

## Legacy paths

| Old | L1 bucket |
|-----|-----------|
| `artifacts/oil_rag_sources/` | `official_web/` |
| `oil_gas_knowledge/` | `licensed_books/` |
| `local_knowledge_sources/oil101.txt` | `reference/oil101.txt` |
