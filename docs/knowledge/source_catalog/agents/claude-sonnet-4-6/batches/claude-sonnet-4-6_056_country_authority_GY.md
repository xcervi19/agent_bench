# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_056_country_authority_GY.md  
**Fáze:** country_authority — krok GY (Guyana)  
**Datum:** 2026-07-06  

---

## Shrnutí

Guyana = **fastest-growing crude producer** (~650 kb/d 2024 → ~1.3 mb/d by 2027;
Stabroek Block = ExxonMobil 45% operated + Hess 30% + CNOOC 25%). **Liza crude**
(offshore; light sweet; tier-1 new Atlantic basin supply). GYSB (Guyana och Suriname
Basin) = jedno z největších nových offshore objevů světa (>11 B barrels recoverable).
Klíčové signály: **ExxonMobil Guyana quarterly**, **FPSO loading schedule**
(Destiny, Unity, Prosperity). 8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GY-ministry_petroleum | GY | — | ministry_petroleum | Ministry of Natural Resources | natresources.gov.gy | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-GY-noc | GY | — | noc | GYSB / Guyana Goldfields → via PPCo? → actually: Guyana's NOC is PPCo (Petro Caribe) subsidiary? No: proper NOC is | natresources.gov.gy | international_agency | official | production, term_contract | proposed |
| ca-GY-mfa | GY | — | mfa | Ministry of Foreign Affairs | minfor.gov.gy | international_agency | official | sanctions, policy | proposed |
| ca-GY-customs_export | GY | — | customs_export | Guyana Revenue Authority | gra.gov.gy | international_agency | official | exports, export_license | proposed |
| ca-GY-upstream_regulator | GY | — | upstream_regulator | GRA / Guyana Geology and Mines Commission | ggmc.gov.gy | international_agency | official | production, force_majeure | proposed |
| ca-GY-port_maritime_authority | GY | — | port_maritime_authority | Transport and Harbours Department | thd.gov.gy | international_agency | official | vessel_loading, port_closure | proposed |
| ca-GY-national_exchange | GY | — | national_exchange | — (no stock exchange; ExxonMobil NYSE listed) | — | — | — | — | empty |
| ca-GY-central_bank | GY | — | central_bank | Bank of Guyana | bankofguyana.org.gy | international_agency | official | pricing_formula | proposed |
| ca-GY-environment_regulator | GY | — | environment_regulator | EPA – Environmental Protection Agency Guyana | epaguyana.org | international_agency | official | force_majeure | proposed |
| ca-GY-coast_guard_navy | GY | — | coast_guard_navy | Guyana Defence Force Coast Guard | gdf.mil.gy | international_agency | official | port_closure, force_majeure | unverified |

---

## Poznámka k NOC
Guyana's formal NOC = **Guyana National Oil Company (Gnoc)**, established 2023.
Domain: gnoc.gy (new; verify). Pre-Gnoc = no state equity in Stabroek. PPCo = Petrocaribe predecessor.

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GY-upstream_regulator (GGMC) | GGMC = upstream regulator; Stabroek Block (ExxonMobil operated) = ~11B barrels recoverable; 6 FPSOs planned by 2030; Liza Phase 1 (120 kb/d), Phase 2 (220 kb/d), Payara (220 kb/d), Yellowtail (250 kb/d) | ExxonMobil + Hess (now Chevron post-merger) + CNOOC; Guyana-Venezuela border dispute (Essequibo); 2024 ICJ proceedings | FPSO shuttle tankers → Caribbean STS (ship-to-ship) + US Gulf Coast + Rotterdam | **proposed** |
| ca-GY-ministry_petroleum | Ali government (pro-oil); GNOC established 2023 (state takes carried interest in future blocks); Natural Resource Fund = oil revenue management | Venezuela Essequibo claim (Dec 2023 Maduro referendum) = existential territorial threat to Stabroek Block | Georgetown port (shallow; FPSOs load offshore; shuttle tankers) | **proposed** |

### Expansion
- ExxonMobil Guyana → corporate.exxonmobil.com/guyana (tier-1 Stabroek operator)
- Hess Guyana → hess.com (30% Stabroek; now Chevron acquisition)
- GNOC → gnoc.gy (new Guyana National Oil Company, 2023)

---
```json
{ "phase": "country_authority", "phase_index": 42, "last_country": "GY", "last_batch_seq": 56 }
```
