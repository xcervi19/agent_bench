# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_030_country_authority_TW.md  
**Fáze:** country_authority — krok TW (Taiwan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Taiwan = ~1 mb/d crude importer + velký LNG importér (~22 mtpa; CPC + TAIPOWER).
**Taiwan Strait risk premium** = globálně nejdůležitější geopolitický signál pro
shipping insurance (Lloyd's, War Risk Club). CPC Corporation (státní) = primární
refinerská + upstream entita. Klíčové signály: **CPC crude import source**,
**Taiwan Strait incidents** (PLA naval exercises → insurance, routing),
**TAIPOWER LNG demand** (elektřina = LNG pull). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TW-ministry_petroleum | TW | — | ministry_petroleum | MOEA Bureau of Energy | boe.gov.tw | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-TW-noc | TW | — | noc | CPC Corporation Taiwan | cpc.com.tw | international_agency | official | production, imports, force_majeure, term_contract | proposed |
| ca-TW-mfa | TW | — | mfa | MOFA – Ministry of Foreign Affairs ROC | mofa.gov.tw | international_agency | official | sanctions, policy | proposed |
| ca-TW-customs_export | TW | — | customs_export | Customs Administration MOEF | customs.mof.gov.tw | international_agency | official | imports, exports | proposed |
| ca-TW-upstream_regulator | TW | — | upstream_regulator | MOEA (upstream, dual with BoE) | moea.gov.tw | international_agency | official | production, refinery_outage | proposed |
| ca-TW-port_maritime_authority | TW | — | port_maritime_authority | MOTC – Ministry of Transportation and Communications | motc.gov.tw | international_agency | official | vessel_loading, port_closure | proposed |
| ca-TW-national_exchange | TW | — | national_exchange | TAIFEX – Taiwan Futures Exchange | taifex.com.tw | exchange | official | pricing_formula | proposed |
| ca-TW-central_bank | TW | — | central_bank | CBC – Central Bank of the ROC (Taiwan) | cbc.gov.tw | international_agency | official | pricing_formula, sanctions | proposed |
| ca-TW-environment_regulator | TW | — | environment_regulator | EPA – Environmental Protection Administration | epa.gov.tw | international_agency | official | refinery_outage | proposed |
| ca-TW-coast_guard_navy | TW | — | coast_guard_navy | ROC Navy (Republic of China Navy) | navy.mnd.gov.tw | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TW-noc (CPC) | CPC = state refiner; Taoyuan + Dalin refineries (~700 kb/d); LNG terminal Yung-An (CPC operated); 70%+ crude from Middle East; post-Ukraine CPC diversifying | CPC = state-owned; sensitive to China-US relations; PLA exercises near Taiwan can disrupt CPC tanker routing | Kaohsiung (Dalin refinery) + Taichung port crude imports; CPC tankers often reroute during PLA exercises (August 2022) | **proposed** — cpc.com.tw aktivní |
| ca-TW-mfa | Taiwan's diplomatic isolation = complex; MOFA Taiwan prohlášení = de-facto proxy; každá změna uznání Taiwan / non-recognition = energy security risk signal | Taiwan Strait = trigger for global insurance premiums (Lloyd's War Risk rate); PLA ADIZ incursions = leading indicator | Taiwan controls key undersea cable routes; Penghu/Matsu proximity to Taiwan Strait chokepoint | **proposed** |
| ca-TW-coast_guard_navy | ROC Navy aktivně patroluje Taiwan Strait; PLA exercises (July 2022, August 2022, April 2023) = direct tanker routing disruption | ROC Navy = geopolitically most sensitive: US Taiwan Relations Act; AUKUS + Quad = signal framework | VLCC routing alternatives při Taiwan Strait closure: Luzon Strait (Philippines EEZ) or southward around Philippines | **unverified** — navy.mnd.gov.tw ověřit vs mnd.gov.tw |

### Analytická poznámka: Taiwan Strait Risk Premium
- Lloyd's Joint War Committee (JWC) Taiwan Strait listing = tier-1 geo signal
- Jakékoli PLA naval exercises v ADIZ → okamžitý CPC/TAIPOWER import logistics signal
- Expansion: TAIPOWER → taipower.com.tw (electricity utility; largest LNG buyer Taiwan)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 29, "last_country": "TW", "last_batch_seq": 30 }
```
