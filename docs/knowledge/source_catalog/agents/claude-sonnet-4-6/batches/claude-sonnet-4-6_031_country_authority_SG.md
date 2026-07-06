# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_031_country_authority_SG.md  
**Fáze:** country_authority — krok SG (Singapore)  
**Datum:** 2026-07-06  

---

## Shrnutí

Singapore = světový bunker hub (#1; ~50 mt/rok) a největší asijský rafinérie hub
(~1.5 mb/d; Shell Bukom, ExxonMobil Jurong Island). Žádná domácí produkce.
**MPA bunkering statistics** = globální shipping fuel demand proxy. Singapore je
klíčový tranzitní uzel: každý VLCC projíždějící Malacca projíždí přes SG waters.
**SLING (Singapore LNG Corp)** = regionální LNG hub + spot cargo. SGX = klíčová pro
Asia commodity pricing (iron ore, crude, LNG derivatives). 8 proposed, 1 empty (noc), 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SG-ministry_petroleum | SG | — | ministry_petroleum | MTI – Ministry of Trade and Industry | mti.gov.sg | international_agency | official | policy, import_licensing | proposed |
| ca-SG-noc | SG | — | noc | — (no Singapore state NOC) | — | — | — | — | empty |
| ca-SG-mfa | SG | — | mfa | MFA – Ministry of Foreign Affairs Singapore | mfa.gov.sg | international_agency | official | sanctions, policy | proposed |
| ca-SG-customs_export | SG | — | customs_export | Singapore Customs | customs.gov.sg | international_agency | official | exports, import_licensing | proposed |
| ca-SG-upstream_regulator | SG | — | upstream_regulator | EMA – Energy Market Authority | ema.gov.sg | international_agency | official | refinery_outage | proposed |
| ca-SG-port_maritime_authority | SG | — | port_maritime_authority | MPA – Maritime and Port Authority of Singapore | mpa.gov.sg | international_agency | official | vessel_loading, port_closure | proposed |
| ca-SG-national_exchange | SG | — | national_exchange | SGX – Singapore Exchange | sgx.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-SG-central_bank | SG | — | central_bank | MAS – Monetary Authority of Singapore | mas.gov.sg | international_agency | official | pricing_formula, sanctions | proposed |
| ca-SG-environment_regulator | SG | — | environment_regulator | NEA – National Environment Agency | nea.gov.sg | international_agency | official | refinery_outage | proposed |
| ca-SG-coast_guard_navy | SG | — | coast_guard_navy | RSN – Republic of Singapore Navy | mindef.gov.sg | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SG-port_maritime_authority (MPA) | **TIER-1**: MPA bunkering statistics (monthly; HSFO/VLSFO/MGO volumes) = global shipping demand proxy; Malacca traffic data; VLCC arrivals; Singapore Port = junction point for ALL Middle East → NEA crude flows | Singapore sovereignty over Southern Malacca approaches; Indonesia/Malaysia trilateral Malacca governance; MPA piracy reports (SSP incidents) | Port of Singapore = world's 2nd busiest by tonnage; Single Point Mooring buoys for VLCC; Jurong Island refinery jetties; Pulau Seraya LNG terminal | **proposed** — mpa.gov.sg aktivní; tier-1 |
| ca-SG-national_exchange (SGX) | SGX crude futures (Singapore Dubai Crude derivative); SGX LNG Index Group (SLInG) spot cargo clearing; iron ore swaps = dry bulk signal | Singapore commodity exchange = Asia price discovery nexus; MAS regulates; SGX LNG = SLING spot reference | SGX clearing = physical delivery at Singapore terminals | **proposed** — sgx.com aktivní |
| ca-SG-coast_guard_navy (RSN) | RSN patrols Eastern Singapore Strait (Malacca Eastern exit); Singapore Strait = VLCC bottleneck (čárka ~15 nm šíře) | Singapore = US ally (basing rights Changi Naval Base); FPDA; critical for US Navy transit | RSN exercises with US 7th Fleet; joint Malacca patrol (MALSINDO) | **unverified** — mindef.gov.sg/rsn ověřit přesnou RSN doménu vs rsn.mindef.gov.sg |

### Expansion sloty
- SLING – Singapore LNG Corporation → slng.com.sg (LNG storage + re-gas; spot cargo hub)
- Shell Bukom → shell.com.sg (largest single-site refinery SEA; ~462 kb/d)
- ExxonMobil Singapore → exxonmobil.com.sg (Jurong Island; ~592 kb/d)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 30, "last_country": "SG", "last_batch_seq": 31 }
```
