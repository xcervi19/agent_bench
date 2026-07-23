# Book RAG metadata — controlled vocabulary

**Status:** active  
**Scope:** licensed books / education corpus only (not crawler reports)

## Principle

1. Books ≠ live news. Always separate from agency reports/data.
2. DB filters only: `category`, `commodity`, `region` — these must be correct.
3. Rest goes in `entities` / `document_type` / `use_for`.
4. Query must filter — metadata alone is useless if RAG is called without filters.

## Allowed values

| Field | Allowed values |
|------|----------------|
| `document_type` | `book` |
| `category` | `energy_education` (all books) |
| `commodity` | `crude_oil` \| `lng` \| `natural_gas` \| `products` \| `multi` |
| `region` | `null` (default for books) — only if truly regional |
| `use_for` | `playbook_authoring`, `terminology`, `geopolitics_context`, `trading_mechanics`, `refining_context` |
| `content_zone` | ingest `main`; skip `toc` / `appendix` / `front_matter` |

Never put books in `category` = `supply_demand` / `geopolitics` / `market_price`.

## Pipeline

```
oil_gas_knowledge/ → L1_raw/licensed_books → L2_text → L2b_clean → preprocess → ingest
```

Not `source_crawler` promote / `from_collected`.

## CLI

```bash
uv run python -m source_ingest.preprocess \
  --input corpus/L2b_clean/licensed_books/<file>.txt \
  --output-dir artifacts/books/<slug> \
  --book-title "..." --author "..." --book-slug <slug> \
  --category energy_education \
  --commodity crude_oil \
  --document-type book \
  --use-for trading_mechanics --use-for playbook_authoring \
  --prefix-hint "..."
```
