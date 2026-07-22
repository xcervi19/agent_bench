# Source QA

Review crawled source text packs and write a machine-readable QA audit.

**Also available in Cursor:** `.cursor/commands/source-qa.md` (primary local workflow).

**Optional args:** path to `collected_text` root (default: `artifacts/collected_text` relative to repo root).

## Steps

1. Resolve text root: `$ARGUMENTS` if set, else `artifacts/collected_text`.
2. Read `{text_root}/qa_prompt.md` — review **only** the packs listed there.
3. Write audit JSON to `{text_root}/qa_audit.json` using the exact schema and path in the prompt.
4. Include every listed `source_id` with matching `source_sha256`.
5. Labeling:
   - `label_assignment=human` → copy `document_type` + `use_for` from the pack.
   - `label_assignment=agent` → set `document_type` + `use_for` from controlled vocab.
   - Optional `proposed_labels` for new vocab only.
6. Set `safe_to_promote` only for sources with `verdict: PASS`.
7. Do **not** edit any other files. Do **not** run promote or ingest.

## After QA (human or script)

```bash
uv run python -m source_crawler apply-qa --dry-run
uv run python -m source_crawler apply-qa
uv run python -m source_ingest.from_collected --sources-dir artifacts/rag_corpus
```

Normal promote path is `apply-qa` only. Manual `promote --source-id` is an override.
