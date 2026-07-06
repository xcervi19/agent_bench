# Plan Source Integration — #33

**Status:** planned  
**Lane:** Platform / Agent Skills  
**Goal:** Upravit `newsfind-plan.md`, aby používal `/source-discover` skill.

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
- Neřeší automatickou validaci objevených zdrojů (ta je mimo scope MVP).
