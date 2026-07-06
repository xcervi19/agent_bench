# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_040_country_authority_PL.md  
**Fáze:** country_authority — krok PL (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Polsko (`PL`), 10 slotů (`ca-PL-{authority}`). **Lídr de-rusifikace**: Druzhba→Naftoport (tanker crude),
**Baltic Pipe** (norský plyn), Świnoujście LNG + FSRU Gdańsk. **Orlen** (fúze Lotos/PGNiG) major. **TGE**
gas/power burza. 9 `proposed`, 1 `unverified`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-PL-ministry_petroleum | ministry_petroleum | Ministry of Climate & Environment | gov.pl | government_regulator | official | imports | proposed |
| ca-PL-noc | noc | Orlen | orlen.pl | noc | official | production, imports, refinery_outage | proposed |
| ca-PL-mfa | mfa | Ministry of Foreign Affairs | gov.pl | diplomacy | official | sanctions | proposed |
| ca-PL-customs_export | customs_export | KAS (National Revenue Admin) | gov.pl | government_regulator | official | imports, exports | proposed |
| ca-PL-upstream_regulator | upstream_regulator | URE (Energy Regulatory Office) | ure.gov.pl | government_regulator | official | pricing_formula | proposed |
| ca-PL-port_maritime_authority | port_maritime_authority | Port of Gdańsk (Naftoport) | portgdansk.pl | infrastructure | official | vessel_loading, pipeline_outage | proposed |
| ca-PL-national_exchange | national_exchange | TGE (Polish Power Exchange) | tge.pl | exchange | official | pricing_formula | proposed |
| ca-PL-central_bank | central_bank | Narodowy Bank Polski (NBP) | nbp.pl | government_regulator | official | sanctions | proposed |
| ca-PL-environment_regulator | environment_regulator | GDOŚ | gov.pl | government_regulator | official | refinery_outage | unverified |
| ca-PL-coast_guard_navy | coast_guard_navy | Polish Border Guard (maritime) | strazgraniczna.pl | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PL-noc (Orlen) | rafinace, gas import | de-rusifikace lídr | Płock refinery, Gdańsk | proposed |
| ca-PL-port_maritime_authority (Naftoport) | — | Druzhba náhrada | tanker crude import Gdańsk | proposed — Druzhba geo (`druzhba`) |

### Unverified / poznámky

- **Baltic Pipe** (Norsko→PL přes DK) + Świnoujście LNG + FSRU Gdańsk = diverzifikace od Ruska.
- **Unverified:** GDOŚ (gov.pl sub-path).
- Orlen = regionální konsolidátor (Lotos + PGNiG fúze); i Czechy/Litva rafinerie.

### Progress po merge

`last_country: PL`, `last_batch_seq: 40`
