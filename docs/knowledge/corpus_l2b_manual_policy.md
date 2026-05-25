# L2b manual curation policy (v1)

**Status:** Active  
**Reproducible:** **NO** — judgment + subscription LLM; do not claim deterministic replay.

## Purpose

Turn automated `corpus/L2_text/` into semantically dense `corpus/L2b_clean/` for WTI/crude oil RAG (L3 chunking).

## Pipeline position

```
L1_raw → L2_text (script) → L2b_clean (MANUAL) → L3_chunks → L4 Postgres
```

## Operator workflow

1. Invoke skill: `@corpus-l2b-manual-curate`
2. Agent sets `corpus/L2b_run_state.json` → `current_batch.start` / `end`
3. Process files in sorted path order within batch
4. Per file: `L2b_clean/` + `L2b_provenance/*.provenance.json`
5. Update `completed` + `last_completed` for resume

## Trash (remove)

- Navigation, legal footers, ads, social links
- Duplicate headers/footers from pagination
- Meaningless OCR noise
- Boilerplate HTML leftovers

## Keep

- Market fundamentals, logistics, contracts, geopolitics, terminal/port facts
- Numeric data with units
- Surviving tables (normalize whitespace)

## Figures and graphs

PDF→text often **drops** charts. Rules:

1. **Never invent** series or values not stated in L2 body.
2. If context on the same page/section clearly describes the chart → short prose caption; tag `MISSING_DESCRIBED` in provenance.
3. If important but unknown → `[FIGURE MISSING: <what> p.<n>]`; tag `MISSING_TAGGED`.
4. If irrelevant to RAG → `MISSING_OMITTED`.
5. Do not output fake graph ASCII art as a substitute for data.

Record each case in `figures[]` on the provenance sidecar.

## Provenance sidecar (required per file)

Path: `corpus/L2b_provenance/<same-rel-as-L2>.txt.provenance.json`

Template: `.cursor/skills/corpus-l2b-manual-curate/provenance.template.json`

## Run state (resume)

Path: `corpus/L2b_run_state.json`

Template: `.cursor/skills/corpus-l2b-manual-curate/run_state.template.json`

Fields `current_batch.start` and `current_batch.end` define what a single agent run may touch. `completed` lists finished L2 paths (relative to `corpus/`).

## Git

All L2b outputs are **gitignored**. This policy doc is committed.

## After L2b complete

Re-chunk from `L2b_clean/` only (not L2). Re-ingest to Postgres when ready.
