# Coverage Playbooks Seed — #30

**Status:** done (2026-07-23)  
**Lane:** Platform / Data  
**Depends on:** #29 (`source_whitelist.json`), playbook template in `.cursor/skills/trading-geopolitical-analyst/playbook-template.md`

---

## Goal / Problem

Books and education RAG do not encode desk strategy (“for Iran start at SHANA / NIOC / OFAC”). Agents need searchable **coverage playbooks** (Meta-RAG) with `document_type: playbook` so plan/discover stages can answer *where to look first*.

Original seed scope was 3 files (Iran, LNG global, crude global). Delivery expanded to the full A→H coverage set (55 playbooks) while still satisfying the seed acceptance criteria.

---

## Solution / What was delivered

- Markdown playbooks under `local_knowledge_sources/playbooks/` (template sections including **Primary Official Sources** and **Official Social Media**).
- Domains/entities restricted to `source_whitelist.json`; Official Social Media left empty when no verified handle (no invented social).
- Progress tracker: `local_knowledge_sources/playbooks/CHECKLIST.md`.
- Preprocess + ingest with `--document-type playbook` into tenant `00000000-0000-0000-0000-000000000001`.
- Artifacts: `artifacts/playbooks_preprocess/<slug>/` (normalized + chunks.jsonl + manifest).

**Seed trio (original #30 AC):** `iran_oil_geopolitics.md`, `lng_global_supply.md`, `crude_oil_global.md` — present and ingested with the rest.

---

## Artifacts

| Path | Role |
|------|------|
| `local_knowledge_sources/playbooks/*.md` | 55 coverage playbooks |
| `local_knowledge_sources/playbooks/CHECKLIST.md` | Completion + ingest checkbox |
| `source_whitelist.json` | Domain authority for Primary Official Sources |
| `.cursor/skills/trading-geopolitical-analyst/playbook-template.md` | Section template |
| `artifacts/playbooks_preprocess/` | Preprocess output (local; not required in git) |
| `source_ingest/preprocess.py` / `ingest.py` | Chunk + embed pipeline |

---

## Usage

```bash
# Preprocess one playbook
uv run python -m source_ingest.preprocess \
  --input local_knowledge_sources/playbooks/iran_oil_geopolitics.md \
  --output-dir artifacts/playbooks_preprocess/iran_oil_geopolitics \
  --book-title "Iran oil geopolitics" \
  --author coverage_playbook \
  --book-slug iran_oil_geopolitics \
  --category coverage_playbook \
  --document-type playbook \
  --include-non-main \
  --prefix-hint "Coverage playbook for energy trading scan strategy"

# Ingest (SSH tunnel to Postgres on 127.0.0.1:5433; see docs/ops/commands.md)
export DATABASE_URL='postgresql+asyncpg://…@127.0.0.1:5433/agentic'
export OPENAI_API_KEY='…'
export PYTHONPATH="libs:."
uv run python -m source_ingest.ingest \
  --artifact-dir artifacts/playbooks_preprocess/iran_oil_geopolitics \
  --tenant-id '00000000-0000-0000-0000-000000000001'
```

Search via `rag_adhoc` with filter/query intent for `document_type: playbook` (wiring into newsfind pre-stage is **#32 / #36**, not this ticket).

---

## Acceptance criteria

- [x] Seed playbooks exist: `iran_oil_geopolitics.md`, `lng_global_supply.md`, `crude_oil_global.md` (plus full A→H set = 55).
- [x] Each playbook includes **Primary Official Sources** and **Official Social Media**.
- [x] Ingested to RAG with `document_type: "playbook"`.
- [x] Playbooks versioned in Git (`local_knowledge_sources/playbooks/`).

---

## Known gaps

- Authoring RAG query step was unavailable from the Cursor host (`rag_adhoc` Docker DNS); drafts noted that in Changelog and used whitelist + desk logic.
- Automated **source_discover** that queries playbook RAG before `/newsfind-plan` is **#32 / #36** — playbooks are in DB but not yet a mandatory pipeline stage.
- Enumerated A–H backlog is **55** files (plan text said “~52”).

---

## Related

- #29 `docs/specs/active/source_whitelist_seed_29.md` (or done path when closed)
- #32 source discover skill/module
- #36 `docs/specs/active/hybrid_pipeline_orchestration_36.md`
- `docs/knowledge/oil_rag_source_strategy.md`
- `docs/ops/commands.md` — Local Knowledge Ingest
