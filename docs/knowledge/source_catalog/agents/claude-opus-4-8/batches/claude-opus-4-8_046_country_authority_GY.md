# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_046_country_authority_GY.md  
**Fáze:** country_authority — krok GY (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Guyana (`GY`), 10 slotů (`ca-GY-{authority}`). **Nejrychleji rostoucí producent** (ExxonMobil Stabroek:
Liza/Payara/Yellowtail, offshore FPSO). **Žádný NOC** (operuje Exxon/Hess/CNOOC). Klíčové geo riziko:
**Venezuela nárokuje Essequibo**. 5 `proposed`, 3 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-GY-ministry_petroleum | ministry_petroleum | Ministry of Natural Resources | nre.gov.gy | government_regulator | official | production, export_license | proposed |
| ca-GY-noc | noc | — (Exxon-operated, no NOC) | — | — | — | — | empty |
| ca-GY-mfa | mfa | Ministry of Foreign Affairs | minfor.gov.gy | diplomacy | official | sanctions | unverified |
| ca-GY-customs_export | customs_export | Guyana Revenue Authority | gra.gov.gy | government_regulator | official | exports | proposed |
| ca-GY-upstream_regulator | upstream_regulator | Petroleum Management Programme | — | government_regulator | official | production | unverified |
| ca-GY-port_maritime_authority | port_maritime_authority | — (offshore FPSO direct export) | — | infrastructure | official | vessel_loading | unverified |
| ca-GY-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-GY-central_bank | central_bank | Bank of Guyana | bankofguyana.org.gy | government_regulator | official | sanctions | proposed |
| ca-GY-environment_regulator | environment_regulator | EPA Guyana | epaguyana.org | government_regulator | official | refinery_outage | proposed |
| ca-GY-coast_guard_navy | coast_guard_navy | Guyana Defence Force Coast Guard | gdf.mil.gy | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GY-ministry_petroleum | **nejrychlejší růst produkce** (Stabroek) | **Essequibo spor s VE** | FPSO offshore loading | proposed — vysoká priorita |
| ca-GY-mfa | — | Venezuela územní nárok (referendum 2023) | — | unverified — geopolitické riziko |

### Unverified / poznámky

- **`ca-GY-noc` = empty:** žádný NOC; Exxon/Hess/CNOOC konsorcium; produkci sledovat přes operátory + vládní ropný účet (NRF).
- **Essequibo:** venezuelský nárok = hlavní geopolitické riziko pro nový supply (invaze/eskalace scénář).
- **FPSO direct export** (Liza Destiny/Unity, Prosperity) → žádný ropný přístav, AIS na FPSO klíč.
- Několik `unverified` domén (nová/malá administrativa).

### Progress po merge

`last_country: GY`, `last_batch_seq: 46`
