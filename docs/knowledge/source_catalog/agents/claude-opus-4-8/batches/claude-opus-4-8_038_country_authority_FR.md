# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_038_country_authority_FR.md  
**Fáze:** country_authority — krok FR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Francie (`FR`), 10 slotů (`ca-FR-{authority}`). **Žádný NOC** (TotalEnergies soukromé). Jaderně těžká
(méně plynu), LNG terminály (Fos, Montoir, Dunkerque), Fos-Lavéra import (Středomoří). **CRE** regulátor.
8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-FR-ministry_petroleum | ministry_petroleum | Ministry for Ecological Transition (DGEC) | ecologie.gouv.fr | government_regulator | official | imports, export_license | proposed |
| ca-FR-noc | noc | — | — | — | — | — | empty |
| ca-FR-mfa | mfa | Ministry for Europe & Foreign Affairs | diplomatie.gouv.fr | diplomacy | official | sanctions | proposed |
| ca-FR-customs_export | customs_export | DGDDI (Douanes) | douane.gouv.fr | government_regulator | official | imports, exports | proposed |
| ca-FR-upstream_regulator | upstream_regulator | CRE (energy regulator) | cre.fr | government_regulator | official | pricing_formula | proposed |
| ca-FR-port_maritime_authority | port_maritime_authority | Grand Port Marseille-Fos | marseille-port.fr | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-FR-national_exchange | national_exchange | — (EEX/EPEX; gas PEG) | — | — | — | — | empty |
| ca-FR-central_bank | central_bank | Banque de France | banque-france.fr | government_regulator | official | sanctions | proposed |
| ca-FR-environment_regulator | environment_regulator | Ministry Ecological Transition / DREAL | ecologie.gouv.fr | government_regulator | official | refinery_outage | proposed |
| ca-FR-coast_guard_navy | coast_guard_navy | Préfecture maritime | premar.gouv.fr | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-FR-port_maritime_authority (Fos) | — | Středomoří import | Fos-Lavéra crude, LNG terminál | proposed |
| ca-FR-upstream_regulator (CRE) | — | — | gas/power market, LNG send-out | proposed |

### Unverified / poznámky

- **`ca-FR-noc` = empty:** TotalEnergies soukromé (total.com — komerční, ne autorita).
- **`national_exchange` = empty:** EEX/EPEX (power), PEG gas hub přes Powernext (EEX global).
- LNG terminály (Fos Cavaou/Tonkin, Montoir, Dunkerque) + FSRU Le Havre — EU LNG kapacita.

### Progress po merge

`last_country: FR`, `last_batch_seq: 38`
