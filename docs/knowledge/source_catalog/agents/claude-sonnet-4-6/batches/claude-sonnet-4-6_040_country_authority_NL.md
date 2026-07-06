# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_040_country_authority_NL.md  
**Fáze:** country_authority — krok NL (Netherlands)  
**Datum:** 2026-07-06  

---

## Shrnutí

Netherlands = **TTF (Title Transfer Facility) = globální referenční cena plynu**
(nejlikvidnější evropský gas hub). Rotterdam = největší evropský přístav a rafinérie hub
(~1.2 mb/d; Shell Pernis = největší rafinérie Evropy). EBN = státní upstream partner.
Groningen gas field = historicky velký (uzavřen 2024 po seizmice).
Klíčové signály: **TTF spot + forward curve** (GasTerra/ICE TTF), **Rotterdam
crude arrivals** (Argus/Vortexa), **ACM (energy regulator) storage reports**.
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NL-ministry_petroleum | NL | — | ministry_petroleum | Ministry of Economic Affairs and Climate Policy | rijksoverheid.nl | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-NL-noc | NL | — | noc | EBN – Energy Beheer Nederland | ebn.nl | international_agency | official | production, term_contract | proposed |
| ca-NL-mfa | NL | — | mfa | Ministry of Foreign Affairs | government.nl | international_agency | official | sanctions, policy | proposed |
| ca-NL-customs_export | NL | — | customs_export | Dutch Customs (Douane) | douane.nl | international_agency | official | imports, exports | proposed |
| ca-NL-upstream_regulator | NL | — | upstream_regulator | SodM – State Supervision of Mines | sodm.nl | international_agency | official | production, force_majeure | proposed |
| ca-NL-port_maritime_authority | NL | — | port_maritime_authority | Port of Rotterdam Authority | portofrotterdam.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-NL-national_exchange | NL | — | national_exchange | ICE Endex TTF (Amsterdam) | theice.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-NL-central_bank | NL | — | central_bank | De Nederlandsche Bank | dnb.nl | international_agency | official | pricing_formula | proposed |
| ca-NL-environment_regulator | NL | — | environment_regulator | RIVM – National Institute for Public Health and the Environment | rivm.nl | international_agency | official | refinery_outage | proposed |
| ca-NL-coast_guard_navy | NL | — | coast_guard_navy | Koninklijke Marine (Royal Netherlands Navy) | defensie.nl | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NL-national_exchange (ICE TTF) | **TIER-1 global**: TTF (Title Transfer Facility) = Evropský referenční gas hub; ICE Endex clearinghouse Amsterdam; TTF forward curve = forward hedging benchmark pro celou Evropu; TTF spot (daily) = trigger pro LNG diversion rozhodnutí | TTF = regulovaný ACM + Dutch MEA; každý Russian supply cut → TTF spike → global LNG rerouting | TTF physical delivery na Dutch gas network (GTS/Gasunie); Rotterdam Gate LNG terminal = physical delivery point | **proposed** — theice.com/endex aktivní; tier-1 |
| ca-NL-port_maritime_authority (Rotterdam) | **TIER-1**: Rotterdam Port Authority = největší evropský přístav (13.5 mt crude/y); Shell Pernis (~400 kb/d) + ExxonMobil Rotterdam (~190 kb/d) + BP Rotterdam; monthly crude throughput statistics = European oil demand leading indicator | Rotterdam = European crude pricing hub; ARA (Amsterdam-Rotterdam-Antwerp) barge market = European product pricing benchmark | Rotterdam Gate LNG terminal (12 bcm/y; Shell operated); ECT crude tanker terminal; Maasvlakte II deep-water (VLCC capable) | **proposed** — portofrotterdam.com aktivní |
| ca-NL-upstream_regulator (SodM) | SodM = regulator Groningen field closure (2024); offshore North Sea Dutch sector (NAM, Neptune Energy, ONE-Dyas); seismicity reports přímý supply signal | Groningen closure = Dutch gas production ~$3 bcm/y loss; Dutch dependency on imports increased; NAM (Shell-ExxonMobil JV) wind-down | SodM well inspection reports; offshore Wadden Sea drilling permits | **proposed** — sodm.nl aktivní |

### Expansion sloty
- Gasunie (GTS) → gasunie.nl (Dutch gas TSO; TTF physical backbone)
- Rotterdam Gate LNG → gate.nl (Shell/Gasunie FSRU + regasification terminal)
- ARA product barge market: Argus ARA crack spreads (no official domain; third-party data)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 39, "last_country": "NL", "last_batch_seq": 40 }
```
