# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_010_country_authority_QA.md  
**Fáze:** country_authority — krok QA (Qatar)  
**Datum:** 2026-07-05  

---

## Shrnutí

Qatar = #1 LNG exporter globálně (~77 mtpa + expansion k 126 mtpa do 2030). Crude produkce
~1.7 mb/d. Klíčové signály: **QatarEnergy LNG expansion** (North Field = největší
single gas reservoir), **QatarEnergy OSP** (Qatar Marine/Land crude), **Ras Laffan**
(geo-target pro LNG terminal). QatarEnergy je jeden z nejdůležitějších LNG aktérů
na světě. 7 proposed, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-QA-ministry_petroleum | QA | — | ministry_petroleum | Ministry of Energy and Industry | me.gov.qa | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-QA-noc | QA | — | noc | QatarEnergy | qatarenergy.qa | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-QA-mfa | QA | — | mfa | Qatar Ministry of Foreign Affairs | mofa.gov.qa | international_agency | official | sanctions, policy | proposed |
| ca-QA-customs_export | QA | — | customs_export | Qatar General Authority of Customs | customs.gov.qa | international_agency | official | exports, export_license | proposed |
| ca-QA-upstream_regulator | QA | — | upstream_regulator | QatarEnergy (upstream licensing authority) | qatarenergy.qa | international_agency | official | production, refinery_outage | proposed |
| ca-QA-port_maritime_authority | QA | — | port_maritime_authority | Mwani Qatar – Qatar Ports Management Company | mwani.com.qa | international_agency | official | vessel_loading, port_closure | proposed |
| ca-QA-national_exchange | QA | — | national_exchange | QSE – Qatar Stock Exchange | qse.com.qa | exchange | official | pricing_formula | unverified |
| ca-QA-central_bank | QA | — | central_bank | QCB – Qatar Central Bank | qcb.gov.qa | international_agency | official | sanctions | proposed |
| ca-QA-environment_regulator | QA | — | environment_regulator | MME – Ministry of Municipality and Environment | mme.gov.qa | international_agency | official | refinery_outage | proposed |
| ca-QA-coast_guard_navy | QA | — | coast_guard_navy | Qatar Emiri Naval Forces | mod.gov.qa | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových + unverified)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-QA-noc (QatarEnergy) | QatarEnergy = 77 mtpa LNG (Qatargas 1-4 + RasGas); NF Expansion Phase 1 (+32 mtpa 2026); každý QE train restart/shutdown pohybuje JKM o $0.5–1.5 | QatarEnergy drží stakes v Shell, TotalEnergies, ExxonMobil projektech globálně; sovereign LNG supply weapon | Ras Laffan Port = veškerý LNG export (16 trains); loading nominations od QE jsou leading signal | **proposed** — qatarenergy.qa aktivní (rebrand od Qatar Petroleum 2021) |
| ca-QA-port_maritime_authority (Mwani) | Mwani provozuje Hamad Port (general cargo + kontejnery) a koordinuje Ras Laffan industrial port scheduling | Mwani je under Qatar Ports Management; Ras Laffan je spravován QatarEnergy přímo pro LNG terminal | Ras Laffan berthing schedule = tier-1 LNG loading signal; geo-ras_laffan-port_authority slot bude specifičtější | **proposed** — mwani.com.qa aktivní |
| ca-QA-national_exchange (QSE) | Equity exchange; QatarEnergy je state entity bez veřejného listingu | Omezená commodity relevance; Qatari LNG pricing = OTC přes QatarEnergy bilaterální smlouvy | Žádná logistická role | **unverified** — qse.com.qa nebo qse.qa; ověřit správnou doménu |
| ca-QA-coast_guard_navy | Qatar ENA chrání přístupy k Ras Laffan a offshore North Field | Qatar = US military presence (Al Udeid Air Base); Qatar ENA koordinuje s US Navy Fifth Fleet | Escort pro LNG tankers z Ras Laffan; Strait of Hormuz northern approach | **unverified** — mod.gov.qa nemusí zahrnovat naval sub-stránku; ověřit |

### Expansion sloty
- QatarEnergy LNG (subdiv) → qatarenergy.qa/lng
- Nakilat (Qatar Gas Transport Company) → nakilat.com — LNG shipping arm; tier-1 expansion
- RLIC – Ras Laffan Industrial City Company → rlic.com.qa

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 9, "last_country": "QA", "last_batch_seq": 10 }
```
