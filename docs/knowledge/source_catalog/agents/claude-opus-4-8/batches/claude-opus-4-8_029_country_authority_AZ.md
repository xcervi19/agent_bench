# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_029_country_authority_AZ.md  
**Fáze:** country_authority — krok AZ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Ázerbájdžán (`AZ`), 10 slotů (`ca-AZ-{authority}`). Klíč: **BTC pipeline** (Baku-Tbilisi-Ceyhan →
Středomoří) + **SGC/TANAP** plyn do EU (diverzifikace od Ruska). **SOCAR** dominantní. Azeri Light crude.
7 `proposed`, 1 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-AZ-ministry_petroleum | ministry_petroleum | Ministry of Energy | minenergy.gov.az | government_regulator | official | production, export_license | proposed |
| ca-AZ-noc | noc | SOCAR | socar.az | noc | official | production, exports, term_contract | proposed |
| ca-AZ-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.az | diplomacy | official | sanctions | proposed |
| ca-AZ-customs_export | customs_export | State Customs Committee | customs.gov.az | government_regulator | official | exports | proposed |
| ca-AZ-upstream_regulator | upstream_regulator | — (SOCAR integrated) | — | — | — | — | empty |
| ca-AZ-port_maritime_authority | port_maritime_authority | Baku Int'l Sea Trade Port | portofbaku.com | infrastructure | official | vessel_loading, pipeline_outage | proposed |
| ca-AZ-national_exchange | national_exchange | Baku Stock Exchange | bfb.az | exchange | official | pricing_formula | unverified |
| ca-AZ-central_bank | central_bank | Central Bank of Azerbaijan | cbar.az | government_regulator | official | sanctions | proposed |
| ca-AZ-environment_regulator | environment_regulator | Ministry of Ecology | eco.gov.az | government_regulator | official | refinery_outage | proposed |
| ca-AZ-coast_guard_navy | coast_guard_navy | — (Caspian) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AZ-noc (SOCAR) | ACG produkce, Shah Deniz gas | **EU gas diverzifikace** (SGC) | BTC → Ceyhan, TANAP | proposed — vysoká priorita |
| ca-AZ-port_maritime_authority | — | Middle Corridor tranzit | Baku port, trans-Caspian | proposed |

### Unverified / poznámky

- **BTC** a **TANAP** = geo cíle Fáze 3 (`btc`, `tanap`).
- **Unverified:** Baku Stock Exchange (`bfb.az`).
- SOCAR obviněn z re-exportu ruského plynu do EU (pozn. pro sankční tracking).

### Progress po merge

`last_country: AZ`, `last_batch_seq: 29`
