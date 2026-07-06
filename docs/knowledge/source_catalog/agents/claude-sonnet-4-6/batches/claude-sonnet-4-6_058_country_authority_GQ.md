# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_058_country_authority_GQ.md  
**Fáze:** country_authority — krok GQ (Equatorial Guinea)  
**Datum:** 2026-07-06  

---

## Shrnutí

Equatorial Guinea = **malý ale strategický producent** (~90 kb/d crude + ~6 mtpa LNG
z Bioko Island). **GEPetrol** = státní NOC; **SONAGAS** = plynová společnost.
**Punta Europa LNG** (Equatorial Guinea LNG / EGLNG; ExxonMobil + Marathon + GEPetrol).
Alba condensate field (Marathon operated). Klíčové signály: **EGLNG loading schedules**,
**Zafiro/Ceiba/Okume field production** (ExxonMobil/Hess). 8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GQ-ministry_petroleum | GQ | — | ministry_petroleum | Ministry of Mines and Hydrocarbons | mmh.gob.gq | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-GQ-noc | GQ | — | noc | GEPetrol – Empresa Nacional de Petróleos de Guinea Ecuatorial | gepetrol.net | international_agency | official | production, exports, term_contract | proposed |
| ca-GQ-mfa | GQ | — | mfa | Ministry of Foreign Affairs | exteriores.gob.gq | international_agency | official | sanctions, policy | proposed |
| ca-GQ-customs_export | GQ | — | customs_export | Ministry of Finance (Customs) | hacienda.gob.gq | international_agency | official | exports, export_license | proposed |
| ca-GQ-upstream_regulator | GQ | — | upstream_regulator | Ministry of Mines and Hydrocarbons (dual) | mmh.gob.gq | international_agency | official | production, force_majeure | proposed |
| ca-GQ-port_maritime_authority | GQ | — | port_maritime_authority | Port Authority of Malabo | — | international_agency | official | vessel_loading, port_closure | proposed |
| ca-GQ-national_exchange | GQ | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-GQ-central_bank | GQ | — | central_bank | BEAC – Banque des États de l'Afrique Centrale | beac.int | international_agency | official | pricing_formula | proposed |
| ca-GQ-environment_regulator | GQ | — | environment_regulator | Ministry of Fisheries and Environment | — | international_agency | official | refinery_outage | proposed |
| ca-GQ-coast_guard_navy | GQ | — | coast_guard_navy | EG Navy / Coast Guard | — | — | — | — | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GQ-noc (GEPetrol) | GEPetrol = state NOC; Zafiro (ExxonMobil 71.25% + GEPetrol 28.75%); Ceiba/Okume complex (Hess operated); Alba condensate (Marathon/Noble); EGLNG (ExxonMobil + Marathon + GEPetrol); ~90 kb/d crude + 6 mtpa LNG | Obiang family dominance = political risk; ExxonMobil + Marathon long-term presence; OPEC member; US relations complex (resource-curse governance) | Punta Europa LNG terminal (Bioko Island); Malabo port crude loading; Luba terminal | **proposed** — gepetrol.net aktivní |
| ca-GQ-ministry_petroleum | MMH = upstream licencing; OPEC quota coordination; EG as EG-OPEC member post-2017 | MMH = Obiang government arm; každá MMH production guidance = OPEC compliance signal | EGLNG = Atlantic basin LNG supply; primarily Asian buyers (Japan, Korea) | **proposed** |

### Expansion
- EGLNG → eglng.com (ExxonMobil+Marathon+GEPetrol; Punta Europa LNG terminal)
- SONAGAS → sonagas.gq (state gas company)

---
```json
{ "phase": "country_authority", "phase_index": 44, "last_country": "GQ", "last_batch_seq": 58 }
```
