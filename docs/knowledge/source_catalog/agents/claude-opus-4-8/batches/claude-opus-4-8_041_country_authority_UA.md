# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_041_country_authority_UA.md  
**Fáze:** country_authority — krok UA (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Ukrajina (`UA`), 10 slotů (`ca-UA-{authority}`). **Ruský plyn tranzit přes UA skončil led 2025**
(transitní smlouva vypršela) = velký EU gas signál. **Naftogaz** + obří podzemní zásobníky (atraktivní
pro EU). Přístavy (Odesa) pod válečnou hrozbou. 6 `proposed`, 3 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-UA-ministry_petroleum | ministry_petroleum | Ministry of Energy | mev.gov.ua | government_regulator | official | production, imports | proposed |
| ca-UA-noc | noc | Naftogaz | naftogaz.com | noc | official | production, storage_levels, pipeline_outage | proposed |
| ca-UA-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.ua | diplomacy | official | sanctions | proposed |
| ca-UA-customs_export | customs_export | State Customs Service | customs.gov.ua | government_regulator | official | exports, imports | proposed |
| ca-UA-upstream_regulator | upstream_regulator | NEURC (regulator) | nerc.gov.ua | government_regulator | official | pricing_formula | unverified |
| ca-UA-port_maritime_authority | port_maritime_authority | Ukrainian Sea Ports Authority (USPA) | uspa.gov.ua | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-UA-national_exchange | national_exchange | Ukrainian Energy Exchange | ueex.com.ua | exchange | official | pricing_formula | unverified |
| ca-UA-central_bank | central_bank | National Bank of Ukraine | bank.gov.ua | government_regulator | official | sanctions | proposed |
| ca-UA-environment_regulator | environment_regulator | Ministry of Environment | mepr.gov.ua | government_regulator | official | refinery_outage | proposed |
| ca-UA-coast_guard_navy | coast_guard_navy | State Border Guard (maritime) | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UA-noc (Naftogaz) | domácí plyn, zásobníky | **konec ruského tranzitu 2025** | GTS operator (tsoua.com), UGS storage | proposed — vysoká priorita |
| ca-UA-port_maritime_authority (USPA) | — | válečná blokace, obilný koridor | Odesa/Pivdennyi | unverified — válka |

### Unverified / poznámky

- **Konec ruského plynového tranzitu (led 2025)** — přesměrování zbytkových objemů (TurkStream) = EU signál.
- **GTS Operator of Ukraine** (tsoua.com) — provozovatel tranzitu; expanze Naftogazu.
- Obří UGS (podzemní zásobníky) — EU trading příležitost (skladování).
- **Unverified/empty:** NEURC, USPA, UEEX, Border Guard — válečný kontext, nestabilní.

### Progress po merge

`last_country: UA`, `last_batch_seq: 41`
