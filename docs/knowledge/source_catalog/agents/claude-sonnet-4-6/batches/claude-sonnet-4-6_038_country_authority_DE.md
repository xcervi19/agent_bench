# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_038_country_authority_DE.md  
**Fáze:** country_authority — krok DE (Germany)  
**Datum:** 2026-07-06  

---

## Shrnutí

Germany = **největší evropský importér plynu a ropy**; 2022 = mega-energetický šok
(odříznutí Ruského plynu přes NS1; 55% → 0% Russian gas v 2023). Rychlá LNG diverzifikace:
5 FSRUs instalovaných 2022–2024 (Wilhelmshaven, Brunsbüttel, Lubmin, Deutsche ReGas).
Klíčové signály: **BAFA (Bundesamt für Wirtschaft) import data**, **Bundesnetzagentur
gas storage weekly** (německé zásobníky = tier-1 EU gas supply barometer),
**ONTRAS/Open Grid Europe gas TSO flows**. Žádný státní NOC (BASF/Wintershall Dea = semi-private).
9 proposed, 1 empty (noc).

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DE-ministry_petroleum | DE | — | ministry_petroleum | BMWK – Federal Ministry for Economic Affairs and Climate Action | bmwk.de | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-DE-noc | DE | — | noc | — (no German state NOC) | — | — | — | — | empty |
| ca-DE-mfa | DE | — | mfa | Auswärtiges Amt – Federal Foreign Office | auswaertiges-amt.de | international_agency | official | sanctions, policy | proposed |
| ca-DE-customs_export | DE | — | customs_export | Zoll – German Customs | zoll.de | international_agency | official | imports, exports | proposed |
| ca-DE-upstream_regulator | DE | — | upstream_regulator | LBEG – Landesamt für Bergbau, Energie und Geologie (Lower Saxony) | lbeg.de | international_agency | official | production, refinery_outage | proposed |
| ca-DE-port_maritime_authority | DE | — | port_maritime_authority | WSV – Wasserstraßen- und Schifffahrtsverwaltung des Bundes | wsv.de | international_agency | official | vessel_loading, port_closure | proposed |
| ca-DE-national_exchange | DE | — | national_exchange | EEX – European Energy Exchange | eex.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-DE-central_bank | DE | — | central_bank | Bundesbank | bundesbank.de | international_agency | official | pricing_formula | proposed |
| ca-DE-environment_regulator | DE | — | environment_regulator | UBA – Umweltbundesamt | umweltbundesamt.de | international_agency | official | refinery_outage | proposed |
| ca-DE-gas_tso | DE | — | upstream_regulator | Bundesnetzagentur – Federal Network Agency | bundesnetzagentur.de | international_agency | official | production, pipeline_outage | proposed |

---

## Poznámka ke struktuře
Slot `ca-DE-gas_tso` použit místo coast_guard_navy (bezpředmětné pro Německo).
Bundesnetzagentur = tier-1 pro EU gas storage monitoring.

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DE-gas_tso (Bundesnetzagentur) | **TIER-1**: Bundesnetzagentur týdenní gas storage report = primární EU gas supply barometer; German UGS (underground gas storage) ~24 bcm = ~25% EU total; každý fill rate change = TTF price signal | Bundesnetzagentur NS1 shutdown (August 2022 documentation) = tier-1 geopolitical supply event archival; German gas emergency levels (early warning / alert / emergency) | Open Grid Europe + ONTRAS + bayernets gas TSOs federate přes Bundesnetzagentur | **proposed** — bundesnetzagentur.de aktivní |
| ca-DE-national_exchange (EEX) | EEX Leipzig = **TIER-1**: TTF gas hub (EEX clears TTF); Phelix power base load; EEX crude derivatives; EEX = most liquid European energy exchange | ECB/EU regulation; EEX co-owned by Deutsche Börse; EEX owns Powernext (Paris) | EEX physical delivery at German NCG/GASPOOL → merged to THE (Trading Hub Europe) 2021 | **proposed** — eex.com aktivní; tier-1 |
| ca-DE-ministry_petroleum (BMWK) | BMWK = Robert Habeck era (2021–2025) = LNG terminal fast-track decisions; FSRU deployment timeline; German coal reserve restart (2022) = short-term supply signal | BMWK Diversification Plan: Algeria, Norway, US LNG; Rosneft Deutschland seizure (2022) = precedent for state energy nationalisation | Rostock, Lubmin, Wilhelmshaven, Brunsbüttel FSRU; PCK Schwedt refinery (Rosneft, 55% → German trustee) | **proposed** |

### Expansion sloty
- Trading Hub Europe (THE) → tradinghub.eu (German gas TSO hub; physical gas balancing)
- Bundesnetzagentur gas storage dashboard → bundesnetzagentur.de/gasspeicher (direct URL)
- Wintershall Dea → wintershalldea.com (BASF E&P arm; major North Sea + Russia upstream)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 37, "last_country": "DE", "last_batch_seq": 38 }
```
