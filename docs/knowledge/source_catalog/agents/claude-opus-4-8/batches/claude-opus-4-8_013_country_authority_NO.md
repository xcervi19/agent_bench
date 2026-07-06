# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_013_country_authority_NO.md  
**Fáze:** country_authority — krok NO (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Norsko (`NO`), 10 slotů (`ca-NO-{authority}`). **Nejtransparentnější producent** — Offshore
Directorate (Sodir) publikuje měsíční produkci; **Gassco** = klíč pro EU plyn (pipeline flows).
9 `proposed`, 1 `unverified`. Norsko je po Rusku hlavní dodavatel plynu do EU.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-NO-ministry_petroleum | ministry_petroleum | Ministry of Energy (OED) | regjeringen.no | government_regulator | official | production, export_license | proposed |
| ca-NO-noc | noc | Equinor | equinor.com | noc | official | production, exports, term_contract | proposed |
| ca-NO-mfa | mfa | Ministry of Foreign Affairs (UD) | regjeringen.no | diplomacy | official | sanctions | proposed |
| ca-NO-customs_export | customs_export | Norwegian Customs (Tolletaten) | toll.no | government_regulator | official | exports | proposed |
| ca-NO-upstream_regulator | upstream_regulator | Norwegian Offshore Directorate (Sodir) | sodir.no | government_regulator | official | production, storage_levels | proposed |
| ca-NO-port_maritime_authority | port_maritime_authority | Norwegian Coastal Admin (Kystverket) | kystverket.no | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-NO-national_exchange | national_exchange | Oslo Børs (Euronext) | euronext.com | exchange | official | pricing_formula | proposed |
| ca-NO-central_bank | central_bank | Norges Bank | norges-bank.no | government_regulator | official | — | proposed |
| ca-NO-environment_regulator | environment_regulator | Norwegian Environment Agency | miljodirektoratet.no | government_regulator | official | refinery_outage | proposed |
| ca-NO-coast_guard_navy | coast_guard_navy | Norwegian Coast Guard (Kystvakten) | forsvaret.no | diplomacy | official | port_closure | unverified |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NO-upstream_regulator (Sodir) | **měsíční produkce ropy/plynu (transparentní)** | — | field-level data | proposed — vysoká data hodnota |
| ca-NO-noc (Equinor) | produkce, Troll/Johan Sverdrup | EU gas security | Mongstad, Kårstø, Hammerfest LNG | proposed — Petoro/Gassco expanze |

### Unverified / poznámky

- **`coast_guard_navy` = unverified:** Kystvakten pod forsvaret.no — ověřit konkrétní stránku.
- **Expanze (kritické pro EU plyn):** `ca-NO-noc__gassco` (gassco.no — provozovatel plynovodů do
  EU, flow data), `ca-NO-noc__petoro` (petoro.no — státní SDFI podíly).
- Oslo Børs finanční; norský plyn se obchoduje na TTF/hubech, ne lokálně.
- Hammerfest LNG = geo cíl Fáze 3 (`hammerfest`).

### Progress po merge

`last_country: NO`, `last_batch_seq: 13`
