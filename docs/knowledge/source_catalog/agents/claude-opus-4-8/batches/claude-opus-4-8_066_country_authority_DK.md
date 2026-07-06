# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_066_country_authority_DK.md  
**Fáze:** country_authority — krok DK (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dánsko (`DK`), 10 slotů (`ca-DK-{authority}`). **Severomořský producent** (v úpadku; DUC/TotalEnergies, Tyra
redevelopment), plyn tranzit + **Baltic geo** (Nord Stream, Bornholm). Energinet TSO, DEA regulátor. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-DK-ministry_petroleum | ministry_petroleum | Ministry of Climate, Energy & Utilities | kefm.dk | government_regulator | official | production, imports | proposed |
| ca-DK-noc | noc | — (no NOC; DUC/TotalEnergies operate) | — | — | — | — | empty |
| ca-DK-mfa | mfa | Ministry of Foreign Affairs | um.dk | diplomacy | official | sanctions | proposed |
| ca-DK-customs_export | customs_export | Danish Customs (Toldstyrelsen) | skat.dk | government_regulator | official | exports, imports | unverified |
| ca-DK-upstream_regulator | upstream_regulator | Danish Energy Agency (DEA) | ens.dk | government_regulator | official | production, export_license | proposed |
| ca-DK-port_maritime_authority | port_maritime_authority | Danish Maritime Authority / Energinet | energinet.dk | infrastructure | official | pipeline_outage, storage_levels | proposed |
| ca-DK-national_exchange | national_exchange | Nasdaq Copenhagen / Nord Pool (regional) | nordpoolgroup.com | exchange | official | pricing_formula | proposed |
| ca-DK-central_bank | central_bank | Danmarks Nationalbank | nationalbanken.dk | government_regulator | official | sanctions | proposed |
| ca-DK-environment_regulator | environment_regulator | Danish EPA (Miljøstyrelsen) | mst.dk | government_regulator | official | refinery_outage | proposed |
| ca-DK-coast_guard_navy | coast_guard_navy | Danish Defence (Søværnet) | forsvaret.dk | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DK-upstream_regulator (DEA) | Tyra redevelopment (gas restart) | **Baltic / Nord Stream (Bornholm)** | Energinet gas transit | proposed — regional gas + geo chokepoint |
| ca-DK-port_maritime_authority (Energinet) | storage/flows | Baltic infrastruktura security | pipeline transit (DE/SE) | proposed |

### Poznámky

- **Baltic geo:** Nord Stream sabotáž (2022, u Bornholmu) + tanker "stínová flotila" přes Dánské úžiny (Great Belt) = klíčový chokepoint monitoring (propojit s geo target).
- Tyra field redevelopment → dánská plyn produkce restart (supply signál pro NW Evropu).
- Bez NOC (DUC = TotalEnergies/BlueNord/Nordsøfonden); Energinet = TSO/storage.

### Progress po merge

`last_country: DK`, `last_batch_seq: 66` — **Fáze 2 (country_authority) KOMPLETNÍ**
