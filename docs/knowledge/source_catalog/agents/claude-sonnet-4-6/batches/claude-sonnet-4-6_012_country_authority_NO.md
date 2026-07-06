# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_012_country_authority_NO.md  
**Fáze:** country_authority — krok NO (Norway)  
**Datum:** 2026-07-05  

---

## Shrnutí

Norsko = největší producent ropy v Evropě (~2 mb/d) a klíčový dodavatel plynu do EU
(~100 bcm/rok přes Gassco pipeline systém). Klíčové signály: **NPD produkční data**
(Norwegian Petroleum Directorate = jeden z nejransparentnějších upstream regulátorů světa),
**Equinor** (Johannes Operatör na NCS), **Norges Bank GPFG** (Government Pension Fund =
$1.7 trn sovereign fund; petrodollar proxy), **Kystverket** (North Sea port closures).
Všechny 10 proposed — Norsko má vynikající institutional transparency.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NO-ministry_petroleum | NO | — | ministry_petroleum | Ministry of Energy (Energidepartementet) | regjeringen.no/energidepartementet | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-NO-noc | NO | — | noc | Equinor | equinor.com | international_agency | official | production, exports, force_majeure, term_contract | proposed |
| ca-NO-mfa | NO | — | mfa | Norwegian MFA (Utenriksdepartementet) | regjeringen.no/ud | international_agency | official | sanctions, policy | proposed |
| ca-NO-customs_export | NO | — | customs_export | Tolletaten – Norwegian Customs | toll.no | international_agency | official | exports, export_license | proposed |
| ca-NO-upstream_regulator | NO | — | upstream_regulator | NPD – Norwegian Petroleum Directorate | npd.no | international_agency | official | production, force_majeure | proposed |
| ca-NO-port_maritime_authority | NO | — | port_maritime_authority | Kystverket – Norwegian Coastal Administration | kystverket.no | international_agency | official | vessel_loading, port_closure | proposed |
| ca-NO-national_exchange | NO | — | national_exchange | Oslo Børs (Euronext Oslo) | oslobors.no | exchange | official | pricing_formula, term_contract | proposed |
| ca-NO-central_bank | NO | — | central_bank | Norges Bank (incl. GPFG sovereign fund) | norges-bank.no | international_agency | official | pricing_formula, sanctions | proposed |
| ca-NO-environment_regulator | NO | — | environment_regulator | Miljødirektoratet – Norwegian Environment Agency | miljodirektoratet.no | international_agency | official | refinery_outage, pipeline_outage | proposed |
| ca-NO-coast_guard_navy | NO | — | coast_guard_navy | Norwegian Coast Guard (Kystvakten) | forsvaret.no | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NO-upstream_regulator (NPD) | NPD publikuje denní produkci field-by-field (fakticky unikátní globálně); každá neočekávaná revision fieldwise production = přímý NWE gas/crude signal | NPD vydává field closure orders (safety nebo maintenance); Hammerfest LNG (snøhvit) restart/shutdown přes NPD | NCS pipeline systém (Gassco operated) napojený na Emden, Dornum (NO→DE) a St Fergus (NO→UK) | **proposed** — npd.no aktivní s veřejným production datalake |
| ca-NO-noc (Equinor) | Equinor = operator 70 % NCS production; Quarterly reports s field-level data; Troll, Johan Sverdrup, Snøhvit, Oseberg jsou tier-1 fields | Equinor je 67 % státní (Norsk Hydro + Statoil merge 2007); politicky wrappovaný v GPFG mandát | Johan Sverdrup export přes Mongstad/Sture terminal; Hammerfest LNG export = Equinor operated | **proposed** — equinor.com aktivní; silná investor disclosure |
| ca-NO-central_bank (Norges Bank) | GPFG ($1.7 trn) investuje mimo ropný sektor; Norges Bank monetární policy ovlivňuje NOK/USD kurz → crude import cost pro Nore | Norges Bank GPFG divestiture decisions (Exxon, Chevron excluded) jsou politický signal; Norges Bank rate = proxy for Norwegian oil income cycle | Nízká přímá logistická role | **proposed** — norges-bank.no aktivní; GPFG sub-portál nbim.no |
| ca-NO-port_maritime_authority (Kystverket) | Kystverket vydává North Sea weather closures; Ekofisk (BP operated) přístupy přes Teesport/Mongstad | North Sea ice/storm closure → Hammerfest LNG (Arctic) produkční výpadek | Vessel traffic management pro Stavanger, Bergen, Hammerfest porty | **proposed** — kystverket.no aktivní |

### Expansion sloty
- NPD produkční data API → factpages.npd.no (denní field data; tier-1 sub-feed)
- Gassco (NCS pipeline operator) → gassco.no — klíčový pro EU gas flows
- NBIM / Norges Bank Investment Management → nbim.no — GPFG sub-entity
- Mongstad Crude Terminal → equinor.com/mongstad (expansion geo slot)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 11, "last_country": "NO", "last_batch_seq": 12 }
```
