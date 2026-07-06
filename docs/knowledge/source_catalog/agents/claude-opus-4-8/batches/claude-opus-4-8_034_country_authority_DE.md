# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_034_country_authority_DE.md  
**Fáze:** country_authority — krok DE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Německo (`DE`), 10 slotů (`ca-DE-{authority}`). **Žádný NOC**; post-Rusko přesun na LNG (Wilhelmshaven/
Brunsbüttel FSRU). **Bundesnetzagentur** = klíč pro gas storage/flow data. PCK Schwedt (Druzhba) rafinerie.
Burza EEX v global. 7 `proposed`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-DE-ministry_petroleum | ministry_petroleum | Fed Ministry Economic Affairs & Climate (BMWK) | bmwk.de | government_regulator | official | imports, export_license | proposed |
| ca-DE-noc | noc | — | — | — | — | — | empty |
| ca-DE-mfa | mfa | Federal Foreign Office (Auswärtiges Amt) | auswaertiges-amt.de | diplomacy | official | sanctions | proposed |
| ca-DE-customs_export | customs_export | German Customs (Zoll) | zoll.de | government_regulator | official | imports, exports | proposed |
| ca-DE-upstream_regulator | upstream_regulator | Bundesnetzagentur (energy regulator) | bundesnetzagentur.de | government_regulator | official | storage_levels, pipeline_outage | proposed |
| ca-DE-port_maritime_authority | port_maritime_authority | GDWS (Waterways) / Wilhelmshaven | gdws.wsv.bund.de | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-DE-national_exchange | national_exchange | — (EEX in global) | — | — | — | — | empty |
| ca-DE-central_bank | central_bank | Deutsche Bundesbank | bundesbank.de | government_regulator | official | sanctions | proposed |
| ca-DE-environment_regulator | environment_regulator | Umweltbundesamt (UBA) | umweltbundesamt.de | government_regulator | official | refinery_outage | proposed |
| ca-DE-coast_guard_navy | coast_guard_navy | — | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DE-upstream_regulator (Bundesnetzagentur) | — | plynová bezpečnost po Rusku | **storage fill, FSRU send-out** | proposed — nejcennější data |
| ca-DE-port_maritime_authority | — | LNG diverzifikace | Wilhelmshaven/Brunsbüttel FSRU, PCK Schwedt (Druzhba) | proposed |

### Unverified / poznámky

- **`ca-DE-noc` = empty; `national_exchange` = empty** (EEX v global `gl-exchange-008`).
- **THE (Trading Hub Europe, tradinghub.eu)** — německý gas hub operátor, expanze.
- **PCK Schwedt** rafinerie na Druzhbě — přechod z ruské na KEBCO/tanker crude přes Rostock/Gdańsk.
- Storage data (Bundesnetzagentur + GIE AGSI global) = klíč pro EU zimní gas signál.

### Progress po merge

`last_country: DE`, `last_batch_seq: 34`
