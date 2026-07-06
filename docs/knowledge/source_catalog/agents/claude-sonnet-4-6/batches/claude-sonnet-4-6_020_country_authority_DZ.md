# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_020_country_authority_DZ.md  
**Fáze:** country_authority — krok DZ (Algeria)  
**Datum:** 2026-07-05  

---

## Shrnutí

Algeria = ~1 mb/d crude + condensate + ~100 bcm/rok plynu (klíčový dodavatel do jižní
Evropy přes Medgaz, Transmed/TTPC, GME pipelines). Klíčové signály: **Sonatrach OSP**
(Saharan Blend = light sweet; klíčový pro středomořský cracking), **Sonatrach gas volumes**
(přímé do Itálie, Španělska, Francie — konkurent ruského plynu), **ALNAFT licensing**
(upstream), **Skikda/Arzew LNG** terminály. 8 proposed, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DZ-ministry_petroleum | DZ | — | ministry_petroleum | Ministry of Energy and Mines | energy.gov.dz | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-DZ-noc | DZ | — | noc | Sonatrach | sonatrach.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-DZ-mfa | DZ | — | mfa | Ministry of Foreign Affairs | mae.gov.dz | international_agency | official | sanctions, policy | proposed |
| ca-DZ-customs_export | DZ | — | customs_export | Douanes Algériennes | douane.gov.dz | international_agency | official | exports, export_license | proposed |
| ca-DZ-upstream_regulator | DZ | — | upstream_regulator | ALNAFT – Algerian Agency for Hydrocarbons | alnaft.gov.dz | international_agency | official | production, refinery_outage | proposed |
| ca-DZ-port_maritime_authority | DZ | — | port_maritime_authority | EGPN – Entreprise de Gestion des Ports Non Commerciaux | egpn.dz | international_agency | official | vessel_loading, port_closure | unverified |
| ca-DZ-national_exchange | DZ | — | national_exchange | SGBV – Société de Gestion de la Bourse des Valeurs | sgbv.dz | exchange | official | pricing_formula | unverified |
| ca-DZ-central_bank | DZ | — | central_bank | Bank of Algeria | bank-of-algeria.dz | international_agency | official | sanctions | proposed |
| ca-DZ-environment_regulator | DZ | — | environment_regulator | Ministry of Environment and Quality of Life | mte.gov.dz | international_agency | official | refinery_outage | proposed |
| ca-DZ-coast_guard_navy | DZ | — | coast_guard_navy | Algerian Navy / Coast Guard (Marine Nationale) | mdn.gov.dz | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DZ-noc (Sonatrach) | Sonatrach = největší africká korporace; 100% státní; produkuje Saharan Blend crude + condensate; nastavuje OSP měsíčně; gas contracts s ENI, naturgy, TotalEnergies | Sonatrach se v 2022 stalo klíčovým nahrazením ruského plynu pro Itálii (Mattei Plan); každé Sonatrach capacity announcement = European gas signal | Skikda LNG (4 trains), Arzew LNG/GPL (3 trains); Medgaz pipeline (DZ→ES), Transmed/TTPC (DZ→IT), GME (DZ→ES via Marokko) | **proposed** — sonatrach.com aktivní (alternativně sonatrach.dz) |
| ca-DZ-upstream_regulator (ALNAFT) | ALNAFT vydává upstream licence; bloková kola pro prolific basins (Berkine, Illizi, Ahnet, Ghadames) | ALNAFT reformovaná post-2013 Tiguentourine attack; IOC security concerns omezeny; TotalEnergies, Repsol, Eni přítomni | ALNAFT koordinuje produkci z Haoud el-Hamra a In Amenas processingem | **proposed** — alnaft.gov.dz aktivní |
| ca-DZ-port_maritime_authority (EGPN) | EGPN spravuje průmyslové přístavy Skikda, Arzew, Bejaia (crude export a LNG loading) | Skikda/Arzew jsou criticky důležité pro European gas/LNG supply replacement | EGPN non-commercial ports = přímý LNG loading authority | **unverified** — egpn.dz: ověřit zda EGPN spravuje Skikda a Arzew; alternativně Sonatrach provozuje přímo |

### Expansion sloty
- Sonatrach Gas Pipeline Contracts data → sonatrach.com/gas-export
- Medgaz (Midcat proposal) → medgaz.net
- TIPGAS (Transmed Italy pipeline operator) expansion slot
- Gaz de France/ENGIE long-term DZ supply contracts (bilateral)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 19, "last_country": "DZ", "last_batch_seq": 20 }
```
