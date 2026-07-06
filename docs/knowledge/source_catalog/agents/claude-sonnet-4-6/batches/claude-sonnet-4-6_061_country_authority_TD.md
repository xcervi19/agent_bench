# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_061_country_authority_TD.md  
**Fáze:** country_authority — krok TD (Chad)  
**Datum:** 2026-07-06  

---

## Shrnutí

Chad = **landlocked producer** (~70 kb/d crude; Doba Basin, Esso Chad/ExxonMobil operated).
Veškerý export přes **Chad-Cameroon Pipeline** (Komé–Kribi; 1,070 km; inaugurated 2003).
**SHT (Société des Hydrocarbures du Tchad)** = státní NOC. Klíčové signály:
**ExxonMobil Chad quarterly**, **Kribi terminal (Cameroon) cargo** = Chad's only export route.
Pipeline transit fee dispute s Kamerunem = periodic risk. 6 proposed, 3 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TD-ministry_petroleum | TD | — | ministry_petroleum | Ministry of Petroleum and Energy | — | international_agency | official | policy, export_license | proposed |
| ca-TD-noc | TD | — | noc | SHT – Société des Hydrocarbures du Tchad | sht-tchad.com | international_agency | official | production, exports, term_contract | proposed |
| ca-TD-mfa | TD | — | mfa | Ministry of Foreign Affairs | — | international_agency | official | sanctions, policy | proposed |
| ca-TD-customs_export | TD | — | customs_export | — (export via Cameroon Kribi terminal) | — | — | — | — | empty |
| ca-TD-upstream_regulator | TD | — | upstream_regulator | Ministry of Petroleum (dual) | — | international_agency | official | production | proposed |
| ca-TD-port_maritime_authority | TD | — | port_maritime_authority | — (landlocked; export via Cameroon) | — | — | — | — | empty |
| ca-TD-national_exchange | TD | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-TD-central_bank | TD | — | central_bank | BEAC – Banque des États de l'Afrique Centrale | beac.int | international_agency | official | pricing_formula | proposed |
| ca-TD-environment_regulator | TD | — | environment_regulator | Ministry of Environment | — | international_agency | official | pipeline_outage | proposed |
| ca-TD-coast_guard_navy | TD | — | coast_guard_navy | — (landlocked; no naval forces) | — | — | — | — | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TD-noc (SHT) | SHT = state equity (~25%) in Doba basin; ExxonMobil 40% + Petronas 35% + SHT 25%; ~70 kb/d; Komé-Kribi pipeline = sole export route | Chad-Cameroon Pipeline = World Bank-backed; every TD-Cameroon transit fee dispute = supply disruption risk; ExxonMobil 2023 sold to Savannah Energy (now pending) | Kribi terminal (Cameroon Atlantic coast) = final export point; shuttle tankers from Kribi | **proposed** |
| ca-TD-ministry_petroleum | Chad = fragile state; Deby dynasty; French military presence; each political upheaval = ExxonMobil ops signal | France Barkhane (withdrawn 2022); French Niger/Sahel withdrawal = regional security decline = Chad oil ops risk | Komé fields (southern Chad, relatively stable) | **proposed** |

### Expansion
- Kribi Port terminal (Cameroon section) → portautonomedekribi.com
- Savannah Energy → savannah-energy.com (ExxonMobil Chad assets acquired 2023-pending)

---
```json
{ "phase": "country_authority", "phase_index": 47, "last_country": "TD", "last_batch_seq": 61 }
```
