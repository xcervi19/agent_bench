# `/source-discover` (Python core + skill) — #32

**Status:** done (2026-07-23)  
**Lane:** Platform / Agent Skills  
**Depends on:** #29 (`source_whitelist.json`), #30 (`local_knowledge_sources/playbooks/`)  
**Blocks:** #36 (hybrid pipeline consumes `discover_sources` / `source_targets`)

---

## Goal / Problem

Plan/search agents guessed domains instead of consulting whitelist + coverage playbooks. Need a **deterministic, LLM-free** discover step that returns known sources for an entity/topic, plus an optional Cursor skill for interactive use.

## Solution / What was delivered

- Python package `apps/claude_agent/sources/`:
  - `whitelist.py` — load + entity/domain match
  - `playbooks.py` — local playbook scan + Primary Official Sources parse (whitelist domains only)
  - `discover.py` — `discover_sources(query)` + CLI
- Output includes `#32` skill fields (`known_sources`, `discovered_candidates`) and `#36` `source_targets` shape.
- Cursor skill `.cursor/skills/source-discover/SKILL.md` wraps the CLI; optional WebSearch candidates must already be on the whitelist.
- Offline tests: `tests/sources/test_discover.py` (NIOC → `nioc.ir` + `shana.ir`).

**Playbook lookup is filesystem-based** (not rag_adhoc). RAG has no `document_type` filter today; local playbooks are the reliable ground truth for this module.

## Artifacts

| Path | Role |
|------|------|
| `apps/claude_agent/sources/discover.py` | Public API + CLI |
| `apps/claude_agent/sources/whitelist.py` | Whitelist load/match |
| `apps/claude_agent/sources/playbooks.py` | Playbook parse/match |
| `.cursor/skills/source-discover/SKILL.md` | Cursor skill (explicit invoke) |
| `tests/sources/test_discover.py` | Offline unit tests |
| `source_whitelist.json` | Domain authority |
| `local_knowledge_sources/playbooks/` | Coverage playbooks (#30) |

## Usage

```bash
uv run python -m apps.claude_agent.sources "NIOC"
uv run pytest tests/sources/test_discover.py -q
```

Programmatic:

```python
from apps.claude_agent.sources import discover_sources

result = discover_sources("NIOC")
# result["known_sources"], result["source_targets"], result["discovered_candidates"]
```

## Acceptance criteria

- [x] Skill exists in `.cursor/skills/source-discover/`.
- [x] Valid JSON for input `"NIOC"` with `known_sources` including whitelist domains.
- [x] JSON contains `known_sources` and `discovered_candidates` (candidates filled only by optional skill WebSearch; Python leaves `[]`).
- [x] Python core callable without an LLM; versioned in Git.
- [x] Offline tests pass.

## Known gaps

- Not wired into `pipeline.py` / `run_plan` — that is **#36**.
- `discovered_candidates` via Brave/WebSearch is skill-optional; not executed in Python.
- Playbook RAG query (`document_type: playbook`) not used; local markdown is authoritative until rag_adhoc supports document_type filters.
- Original #32 text assumed agent-inline use from `newsfind-plan`; superseded approach is #36 Python pre-stage (#33 superseded).

## Related

- `docs/architecture/agent_orchestration.md` — two-level model (orchestrator + agent CLI SDK)
- #29 `docs/specs/active/source_whitelist_seed_29.md` (mostly done)
- #30 `docs/specs/done/coverage_playbooks_seed_30.md`
- #36 `docs/specs/active/hybrid_pipeline_orchestration_36.md`
- #33 `docs/specs/active/plan_source_integration_33.md` (superseded)
