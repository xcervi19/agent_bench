# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_008_country_authority_AE.md  
**Fáze:** country_authority — krok AE (United Arab Emirates)  
**Datum:** 2026-07-05  

---

## Shrnutí

UAE = druhý největší producent v OPEC+ (~3.3 mb/d kapacita), dominantní v Abu Dhabi.
Klíčové signály: **ADNOC OSP** (Abu Dhabi crude benchmarks pro Asii), **Fujairah** (blending hub
a storage, blízko Hormuz), **Abu Dhabi Ports** (Ruwais terminal, VLCC loading), **UAE MFA**
(normalizace s Izraelem 2020, Jemen, sankce). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AE-ministry_petroleum | AE | — | ministry_petroleum | Ministry of Energy and Infrastructure | moei.gov.ae | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-AE-noc | AE | — | noc | ADNOC – Abu Dhabi National Oil Company | adnoc.ae | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-AE-mfa | AE | — | mfa | MOFAIC – Ministry of Foreign Affairs & International Cooperation | mofaic.gov.ae | international_agency | official | sanctions, policy | proposed |
| ca-AE-customs_export | AE | — | customs_export | Federal Customs Authority | federalcustoms.gov.ae | international_agency | official | exports, export_license | proposed |
| ca-AE-upstream_regulator | AE | — | upstream_regulator | Ministry of Energy and Infrastructure (upstream) | moei.gov.ae | international_agency | official | production, refinery_outage | proposed |
| ca-AE-port_maritime_authority | AE | — | port_maritime_authority | AD Ports Group (Abu Dhabi Ports) | adports.ae | international_agency | official | vessel_loading, port_closure | proposed |
| ca-AE-national_exchange | AE | — | national_exchange | ADX – Abu Dhabi Securities Exchange | adx.ae | exchange | official | pricing_formula | proposed |
| ca-AE-central_bank | AE | — | central_bank | CBUAE – Central Bank of UAE | centralbank.ae | international_agency | official | sanctions | proposed |
| ca-AE-environment_regulator | AE | — | environment_regulator | MOCCAE – Ministry of Climate Change and Environment | moccae.gov.ae | international_agency | official | refinery_outage | proposed |
| ca-AE-coast_guard_navy | AE | — | coast_guard_navy | UAE Armed Forces / Naval Forces | mod.gov.ae | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových + unverified)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AE-noc (ADNOC) | ADNOC produkuje ~3.3 mb/d; ADNOC Distribution a Trading reportují quarterly; ADNOC OSP pro ADCO/Upper Zakum/Das Blend pohybují asijský market | ADNOC je de-facto sovereign energy arm UAE; každé ADNOC capacity expansion announcement pohybuje trhem (5 mb/d cíl 2027) | Ruwais terminal (VLCC loading), Jebel Ali (produkty), Das Island (offshore loading); koordinace s AD Ports | **proposed** |
| ca-AE-port_maritime_authority (AD Ports) | AD Ports Group provozuje terminály pro ropný export; Khalifa Port + KIZAD industrial zone; Ruwais oilport | AD Ports spravuje Fujairah Port (geo-fujairah slot) → klíčové pro Hormuz-vicinity blending hub | VLCC scheduling přes AD Ports; notice of arrivals/departures = leading loading signal | **proposed** |
| ca-AE-mfa (MOFAIC) | Nízký přímý supply signal | Abraham Accords 2020, Jemen proxy war, Írán normalizace (2023) — UAE MFA prohlášení mění Gulf risk premium | Nízká přímá logistická role | **proposed** |
| ca-AE-coast_guard_navy | Omezený supply signal | UAE Navy chrání Abu Dhabi offshore fields (ADCO, Upper Zakum) a přístupy k Hormuz | Escort pro VLCC convoy; koordinace s US Fifth Fleet Bahrain | **unverified** — mod.gov.ae existuje; ověřit UAE Naval Forces sub-stránku |

### Expansion sloty
- ADNOC Logistics & Services (maritime arm) → adnoc.ae/logistics
- Fujairah Oil Industry Zone (FOIZ) → foiz.gov.ae (geo-fujairah expansion)
- Dubai Supply Authority (DUSUP) → dusup.gov.ae

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 7, "last_country": "AE", "last_batch_seq": 8 }
```
