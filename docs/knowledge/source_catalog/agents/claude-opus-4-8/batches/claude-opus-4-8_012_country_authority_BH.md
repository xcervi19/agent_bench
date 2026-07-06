# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_012_country_authority_BH.md  
**Fáze:** country_authority — krok BH (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Bahrajn (`BH`), 10 slotů (`ca-BH-{authority}`). Malý producent; sdílené **Abu Safah** pole se SA,
Bapco refining, import saudské ropy pipeline. Geo: hostí **US 5th Fleet** (transit/security signál).
7 `proposed`, 1 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-BH-ministry_petroleum | ministry_petroleum | National Oil & Gas Authority (NOGA) | noga.gov.bh | government_regulator | official | production, export_license | proposed |
| ca-BH-noc | noc | Bapco Energies | bapco.net | noc | official | production, exports, refinery_outage | proposed |
| ca-BH-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.bh | diplomacy | official | sanctions | proposed |
| ca-BH-customs_export | customs_export | Bahrain Customs Affairs | customs.gov.bh | government_regulator | official | exports | proposed |
| ca-BH-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-BH-port_maritime_authority | port_maritime_authority | Ports & Maritime Affairs (MTT) | mtt.gov.bh | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-BH-national_exchange | national_exchange | Bahrain Bourse | bahrainbourse.com | exchange | official | pricing_formula | proposed |
| ca-BH-central_bank | central_bank | Central Bank of Bahrain | cbb.gov.bh | government_regulator | official | sanctions | proposed |
| ca-BH-environment_regulator | environment_regulator | Supreme Council for Environment | sce.gov.bh | government_regulator | official | refinery_outage | proposed |
| ca-BH-coast_guard_navy | coast_guard_navy | Bahrain Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BH-noc (Bapco) | Bahrain field, Abu Safah (sdílené se SA) | — | Sitra refinery/terminal | proposed |
| ca-BH-mfa | — | US 5th Fleet host, Írán tension | — | proposed — geo/security signál |

### Unverified / poznámky

- **`port_maritime_authority` = unverified:** doména MTT (`mtt.gov.bh`) ověřit; Khalifa Bin Salman Port.
- **`upstream_regulator` = empty:** pod NOGA.
- **`coast_guard_navy` = empty:** bez oficiálního webu; US 5th Fleet security kontext přes MFA.
- **Abu Safah** pole sdílené se SA — produkce/příjmy pozn., ne samostatný export stream.

### Progress po merge

`last_country: BH`, `last_batch_seq: 12`
