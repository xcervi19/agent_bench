# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_104_crosscheck.md  
**Fáze:** crosscheck (Fáze 5 — revalidace, žádné nové sloty)  
**Datum:** 2026-07-06  

---

## Kontroly

| kontrola | výsledek |
|----------|----------|
| JSON parse | OK |
| Unikátní `id` | OK (0 duplicit) |
| Počet entries | 1178 |
| geo_target sloty | 384 (32 cílů × 12 subjektů) ✓ |
| country_social sloty | 92 smysluplných (zbytek `empty` přes dimension matrix) |

## Anti-duplikace `ca-*` vs `gt-*`

- Přístavní/celní sloty u chokepointů (`gt-hormuz-*`, `gt-bab_el_mandeb-*`) drženy `empty`, aby
  neduplikovaly národní autority (`ca-*`). Ceyhan/BTC → `national_noc` odkazuje na `ca-AZ` (SOCAR),
  ne nová entita.
- `cs-*` odkazuje na již katalogizované oficiální entity (`verify handle`), nevytváří nové domény.

## Signály k pohlídání (deska)

- **Hormuz/Bab el-Mandeb** — transit_disruption (Houthi, cross-check UKMTO/CENTCOM, ne jen `cs-YE`).
- **Druzhba** — pipeline_outage z UA dronů (`gt-druzhba-insurance_war_risk`, `unverified`).
- **Cushing / ARA** — storage_levels (EIA / Insights Global) = klíčové balance feedy.
- **Sankce IR/RU/VE** — `sanctions_tracker` proposed (UANI, price-cap monitors, OFAC).

## Otevřené `unverified` (priorita k dohledání handlů/domén)

- Všechny `cs-*-official_social_*` s „verify handle" — nutné potvrdit reálné účty před `proposed`.
- `gt-saldanha-*`, `gt-btc-loading_terminal`, `gt-druzhba-*` — doménová/operátorská verifikace.

**Stav:** Fáze 0-5 dokončeny. Katalog připraven k použití; `unverified` sloty = backlog verifikace.
