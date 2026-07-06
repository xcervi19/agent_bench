# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_050_country_authority_PL.md  
**Fáze:** country_authority — krok PL (Poland)  
**Datum:** 2026-07-06  

---

## Shrnutí

Poland = **klíčový Eastern EU energy diversifikátor** post-2022: Świnoujście LNG
terminál (~5 bcm/y; TotalEnergies Qatar spot + US LNG), Baltic Pipe (Norway→Denmark→Poland;
~10 bcm/y, inaugurated 2022), **PKN Orlen** (mega-integrated NOC post-merger s PGNiG +
Lotos). Polska = největší EU coal producer a net gas importer. Klíčové signály:
**PKN Orlen quarterly**, **POLSKIE LNG terminal nominations**, **URE (regulatory) gas
data**, **Baltic Pipe flows**. 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PL-ministry_petroleum | PL | — | ministry_petroleum | Ministry of Climate and Environment | gov.pl/klimat | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-PL-noc | PL | — | noc | PKN Orlen S.A. | orlen.pl | international_agency | official | production, imports, refinery_outage, term_contract | proposed |
| ca-PL-mfa | PL | — | mfa | Ministry of Foreign Affairs | gov.pl/dyplomacja | international_agency | official | sanctions, policy | proposed |
| ca-PL-customs_export | PL | — | customs_export | KAS – Customs and Revenue Service | gov.pl/kas | international_agency | official | imports, exports | proposed |
| ca-PL-upstream_regulator | PL | — | upstream_regulator | URE – Energy Regulatory Office | ure.gov.pl | international_agency | official | production, refinery_outage | proposed |
| ca-PL-port_maritime_authority | PL | — | port_maritime_authority | Port of Gdańsk Authority | portgdansk.pl | international_agency | official | vessel_loading, port_closure | proposed |
| ca-PL-national_exchange | PL | — | national_exchange | TGE – Polish Power Exchange | tge.pl | exchange | official | pricing_formula, term_contract | proposed |
| ca-PL-central_bank | PL | — | central_bank | NBP – National Bank of Poland | nbp.pl | international_agency | official | pricing_formula, sanctions | proposed |
| ca-PL-environment_regulator | PL | — | environment_regulator | GIOŚ – Chief Inspectorate for Environmental Protection | gios.gov.pl | international_agency | official | refinery_outage | proposed |
| ca-PL-coast_guard_navy | PL | — | coast_guard_navy | Polish Navy | mw.mil.pl | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PL-noc (PKN Orlen) | PKN Orlen = mega-merger (Orlen + PGNiG + Lotos 2022-2023); upstream (Norway North Sea + Poland domestic ~18 kb/d), refining (~900 kb/d total), gas distribution (PGNiG gas contracts); listed on WSE; quarterly = tier-1 Polish energy signal | PKN Orlen = state ~27%; politicky exponovaná (PiS-era merger); PGNiG Russian gas contracts terminated; Baltic Pipe + Świnoujście LNG = independence strategy | Płock refinery (~380 kb/d; Druzhba pipeline crude supply); Gdańsk (Naftoport crude import terminal); Świnoujście LNG | **proposed** — orlen.pl aktivní |
| ca-PL-port_maritime_authority (Gdańsk) | Gdańsk Naftoport = główny crude import port; ~35 mt/yr capacity; Druzhba pipeline crude (KazTransOil + Rosneft pre-2022; post-2022 replacing); Baltic Pipe interconnect nearby | Poland odmítla Russian gas (PGNiG contract terminated April 2022 = first EU country); každý Naftoport alternative crude source = supply diversification signal | Świnoujście LNG (Polskie LNG; 5 bcm/y; expansion to 7.5 bcm/y planned); Baltic Pipe inaugurated Oct 2022 | **proposed** |
| ca-PL-national_exchange (TGE) | TGE = Polish Power Exchange; POLPX gas spot; TGE DAM/IDM = Polish electricity; RDN continuous electricity; gas day-ahead hub = interconnected with EEX | TGE under URE oversight; Polish energy mix (coal 70%+ → declining; gas rising; nuclear planned) | TGE physical delivery at Gas System TSO (Gaz-System = Baltic Pipe Polish landing) | **proposed** — tge.pl aktivní |

### Expansion sloty
- Polskie LNG → polskielng.pl (Świnoujście LNG terminal; 5 bcm/y; QatarEnergy + TotalEnergies)
- Gaz-System → gaz-system.pl (Polish gas TSO; Baltic Pipe operator)
- Baltic Pipe → baltipipe.eu (Norway–Denmark–Poland pipeline)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 36, "last_country": "PL", "last_batch_seq": 50 }
```
