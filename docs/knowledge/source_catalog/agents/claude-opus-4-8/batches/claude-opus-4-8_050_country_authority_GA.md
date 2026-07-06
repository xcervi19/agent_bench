# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_050_country_authority_GA.md  
**Fáze:** country_authority — krok GA (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Gabon (`GA`), 10 slotů (`ca-GA-{authority}`). **OPEC člen** (znovu vstoupil 2016); **Gabon Oil Company** NOC;
export **Port-Gentil / Cap Lopez** (Rabi/Mandji blend). Vojenský převrat 2023 (přechodná vláda).
3 `proposed`, 4 `unverified`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-GA-ministry_petroleum | ministry_petroleum | Ministry of Petroleum | — | government_regulator | official | production, export_license | unverified |
| ca-GA-noc | noc | Gabon Oil Company (GOC) | — | noc | official | production, exports | unverified |
| ca-GA-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-GA-customs_export | customs_export | — | — | — | — | — | empty |
| ca-GA-upstream_regulator | upstream_regulator | Ministry of Petroleum | — | government_regulator | official | production | unverified |
| ca-GA-port_maritime_authority | port_maritime_authority | Port-Gentil / Cap Lopez terminal | — | infrastructure | official | vessel_loading | unverified |
| ca-GA-national_exchange | national_exchange | — (BVMAC regional) | — | — | — | — | empty |
| ca-GA-central_bank | central_bank | BEAC (regional CEMAC) | beac.int | government_regulator | official | sanctions | proposed |
| ca-GA-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | proposed |
| ca-GA-coast_guard_navy | coast_guard_navy | Gabonese Navy | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GA-noc (GOC) | Rabi/Mandji; OPEC kvóta | **převrat 2023**, přechod. vláda | Cap Lopez export | unverified |

### Poznámky

- **OPEC člen** → produkce přes OPEC MOMR.
- Cap Lopez (Port-Gentil) = hlavní export terminál; AIS + operátoři (Perenco/TotalEnergies/Assala).
- Post-coup přechod (Oligui) → policy nejistota; sledovat MFA/přechodnou vládu.

### Progress po merge

`last_country: GA`, `last_batch_seq: 50`
