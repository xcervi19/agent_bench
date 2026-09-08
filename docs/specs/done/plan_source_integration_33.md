# Plan Source Integration — #33

**Status:** retired (2026-09-08)  
**Retired because:** superseded by **#36**, which shipped 2026-07-24. Source discovery
runs as a deterministic Python pre-plan stage (`pipeline.py` → `run_source_discover` →
`source_targets.json`), not as agent-inline `/source-discover` calls from
`newsfind-plan.md`. This ticket's acceptance criteria describe a design we deliberately
did not take; nothing in it remains to build.  
**Lane:** Platform / Agent Skills  
**Goal:** ~~Upravit `newsfind-plan.md`, aby používal `/source-discover` skill.~~ → See #36 `hybrid_pipeline_orchestration_36.md`.

## Cíl

V Phase 2 (nebo nové Phase 2.5) `newsfind-plan.md` volat `/source-discover` pro každou top-tier entitu a výsledky uložit do `parsed.json` jako `source_targets[]`.

## Proč

Agent potřebuje vědět, kam se má podívat, než začne generovat obecné WebSearch query.

## Akceptační kritéria

- [ ] `newsfind-plan.md` obsahuje instrukci volat `/source-discover`.
- [ ] Výstup `parsed.json` obsahuje sekci `source_targets`.
- [ ] `source_targets` obsahuje `entity`, `known_domains`, `discovered_domains`.
- [ ] Změna je verzována v Gitu.

## Poznámky

- Tento ticket závisí na #29 (Whitelist) a #32 (Skill).
- **Superseded by #36** — implement source discovery as a Python pre-stage in `pipeline.py`, not as agent-inline skill calls in `newsfind-plan.md`.
