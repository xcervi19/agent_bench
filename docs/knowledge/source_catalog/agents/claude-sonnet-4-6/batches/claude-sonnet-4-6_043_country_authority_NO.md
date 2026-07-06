# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_043_country_authority_NO.md  
**Fáze:** country_authority — krok NO (Norway)  
**Datum:** 2026-07-06  

---

## Shrnutí

Norway = **klíčový Evropský gas a crude supplier post-2022** (~120 bcm/y gas = ~30% EU
spotřeby; ~1.8 mb/d crude). Equinor (státní ~67%) = dominantní operátor. Norné (státní
direktní podíly) = SDFI. Klíčové signály: **NPD (Norwegian Petroleum Directorate)**
měsíční produkce, **Equinor quarterly**, **Gassco transport nominations** (denní plyn
přes norské pipeline do UK/DE/BE/FR). Langeled, FLAGS, SAGE, Polarled, Europipe =
norské gas pipeline do Evropy. 10 proposed, 0 empty, 0 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NO-ministry_petroleum | NO | — | ministry_petroleum | Ministry of Energy | energidepartementet.no | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-NO-noc | NO | — | noc | Equinor ASA | equinor.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-NO-mfa | NO | — | mfa | Ministry of Foreign Affairs | regjeringen.no | international_agency | official | sanctions, policy | proposed |
| ca-NO-customs_export | NO | — | customs_export | Norwegian Customs (Tolletaten) | tolletaten.no | international_agency | official | exports, export_license | proposed |
| ca-NO-upstream_regulator | NO | — | upstream_regulator | NPD – Norwegian Petroleum Directorate | npd.no | international_agency | official | production, force_majeure | proposed |
| ca-NO-port_maritime_authority | NO | — | port_maritime_authority | NCA – Norwegian Coastal Administration | kystverket.no | international_agency | official | vessel_loading, port_closure | proposed |
| ca-NO-national_exchange | NO | — | national_exchange | Oslo Børs (Euronext Oslo) | oslobors.no | international_agency | official | pricing_formula, term_contract | proposed |
| ca-NO-central_bank | NO | — | central_bank | Norges Bank | norges-bank.no | international_agency | official | pricing_formula | proposed |
| ca-NO-environment_regulator | NO | — | environment_regulator | Miljødirektoratet – Norwegian Environment Agency | miljodirektoratet.no | international_agency | official | refinery_outage, force_majeure | proposed |
| ca-NO-gas_tso | NO | — | upstream_regulator | Gassco – Norwegian Gas TSO | gassco.no | international_agency | official | production, pipeline_outage | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NO-upstream_regulator (NPD) | **TIER-1**: NPD monthly production statistics (field-level); Norwegian gas pipeline nominations přes Gassco; každý NPD production miss = European gas supply shortage signal; Troll, Sleipner, Ormen Lange, Johan Sverdrup data | Norway = NATO member; post-2022 = EU's primary gas supplier replacement for Russia; každý Equinor/Aker BP platform outage = TTF price spike | Kårstø gas processing; Kollsnes gas; Mongstad crude terminal; Sture crude; Karsto → Emden (Norpipe) | **proposed** — npd.no aktivní; tier-1 |
| ca-NO-noc (Equinor) | **TIER-1**: Equinor = state 67% (SDFI + direct); ~1.8 mb/d crude + ~120 bcm gas; Johan Sverdrup (750 kb/d Phase 2); quarterly reports; Hammerfest LNG (Snøhvit; freeze outage 2020–2022) | Equinor = Norwegian national champion; Equinor Russia withdrawal (2022, Shtokman abandonment re-confirmed); Equinor Texas wind farms | Langeled (1,173 km → Easington UK); Europipe I+II (→ Dornum DE); FLAGS → St. Fergus UK | **proposed** — equinor.com aktivní; tier-1 |
| ca-NO-gas_tso (Gassco) | Gassco = Norwegian gas infrastructure operator (non-commercial TSO); daily gas transport nominations = tier-1 European gas supply leading indicator; Gassco capacity data → Gasunie/National Grid | Norway non-EU but EEA; gas supply agreements embedded in bilateral deals; každé Gassco maintenance nomination = forward supply signal | Gassco operates: Åsgard Transport, Statpipe, Franpipe (→ Dunkerque), Europipe I+II, Langeled, Polarled | **proposed** — gassco.no aktivní; tier-1 |

### Expansion sloty
- SDFI – State Direct Financial Interest → petoro.no (Petoro manages SDFI; state's non-operated upstream equity)
- Hammerfest LNG → equinor.com/snohvit (Snøhvit LNG; Arctic; freeze incident 2020)
- AkerBP → akerbp.com (second largest Norwegian operator; Valhall, Edvard Grieg, Ivar Aasen fields)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 42, "last_country": "NO", "last_batch_seq": 43 }
```
