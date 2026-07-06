# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_027_country_authority_KZ.md  
**Fáze:** country_authority — krok KZ (Kazakhstan)  
**Datum:** 2026-07-05  

---

## Shrnutí

Kazakhstan = ~2 mb/d (Tengiz + Kashagan + Karachaganak). Klíčové signály:
**CPC pipeline throughput** (Caspian Pipeline Consortium → Novorossiysk; ~1.5 mb/d;
každá CPC disruption = přímý supply shock pro Mediterranean/Northwest European market),
**Kashagan restarts** (chronic production problems; každý restart/shutdown je event),
**KMG quarterly** (KazMunayGas), **BTC swap** (Kazakh crude přes Caspian tankers do
Baku → BTC pipeline do Ceyhan). Landlocked přes Caspian = logistická komplexnost.
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KZ-ministry_petroleum | KZ | — | ministry_petroleum | Ministry of Energy | energo.gov.kz | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-KZ-noc | KZ | — | noc | KMG – KazMunayGas | kmg.kz | international_agency | official | production, exports, force_majeure, term_contract | proposed |
| ca-KZ-mfa | KZ | — | mfa | Ministry of Foreign Affairs | mfa.gov.kz | international_agency | official | sanctions, policy | proposed |
| ca-KZ-customs_export | KZ | — | customs_export | State Revenue Committee (Customs) | kgd.gov.kz | international_agency | official | exports, export_license | proposed |
| ca-KZ-upstream_regulator | KZ | — | upstream_regulator | Ministry of Energy (upstream licensing) | energo.gov.kz | international_agency | official | production, refinery_outage | proposed |
| ca-KZ-port_maritime_authority | KZ | — | port_maritime_authority | Aktau Sea Port Authority | aktauport.kz | international_agency | official | vessel_loading, port_closure | unverified |
| ca-KZ-national_exchange | KZ | — | national_exchange | KASE – Kazakhstan Stock Exchange | kase.kz | exchange | official | pricing_formula | proposed |
| ca-KZ-central_bank | KZ | — | central_bank | NBK – National Bank of Kazakhstan | nationalbank.kz | international_agency | official | sanctions | proposed |
| ca-KZ-environment_regulator | KZ | — | environment_regulator | Ministry of Ecology and Natural Resources | ecologia.kz | international_agency | official | refinery_outage, pipeline_outage | proposed |
| ca-KZ-coast_guard_navy | KZ | — | coast_guard_navy | Kazakhstan Naval Forces (Caspian Flotilla) | mod.gov.kz | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KZ-noc (KMG) | KMG = 20 % Kazakhstánské produkce; zbytek přes IOC JVs (Tengizchevroil, NCOC/Kashagan, KPO/Karachaganak); KMG quarterly reports | KMG je státní; Kashagan JV (Eni, Shell, TotalEnergies, ExxonMobil, CNPC, Inpex, KMG) = major Western IOC presence; Kazakhstan balancuje mezi Ruskem a Západem | KMG vlastní CPC pipeline podíl (20.75 %); CPC throughput = KZ primary export signal | **proposed** — kmg.kz aktivní |
| ca-KZ-port_maritime_authority (Aktau) | Aktau Sea Port = jediný ropný přístav Kazakhstánu (Caspian); Kazakh crude loaduje přes Aktau na tankers → Baku/Azerbaijani swap → BTC nebo CPC pipeline | Aktau strategický pro KTZE (Kazakhstan's Caspian pipeline); Russia-Ukraine válka → Kazakhstan hledá alternativní (Trans-Caspian, BTC) | Aktau → Baku route (Trans-Caspian Undersea Pipeline diskuze) je geopolitický signal | **unverified** — aktauport.kz nebo abtport.kz; ověřit správnou doménu Aktau Sea Port |
| ca-KZ-upstream_regulator (Ministry of Energy) | Ministerstvo vydává upstream licences; Kashagan Phase 2 approval; Tengiz Future Growth Project (FGP) approval | Dual role s ministry_petroleum; Kazakhstan Energy Ministry = jeden úřad | Koordinuje CPC allokaci a pipeline tariffs | **proposed** — energo.gov.kz aktivní |

### Analytická poznámka: CPC monitoring
**CPC (Caspian Pipeline Consortium)** = tier-1 monitoring pro Kazakh crude:
- CPC pipeline je pro ~80 % Kazakhstánského exportu
- Každá CPC pumping station outage (Krymský most incident 2022) = okamžitý supply shock
- CPC domain: cpc.ru (Russian-registered); alternativa pro Western tracking = CPC annual capacity reports

### Expansion sloty
- CPC – Caspian Pipeline Consortium → cpc.ru (critical pipeline operator)
- Tengizchevroil → tengizchevroil.com (Chevron 50% operated; ~700 kb/d)
- NCOC (North Caspian Operating Company, Kashagan) → ncoc.kz
- KazTransOil (pipeline operator) → kaztransoil.kz

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 26, "last_country": "KZ", "last_batch_seq": 27 }
```
