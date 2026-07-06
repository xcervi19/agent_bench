# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_062_country_authority_PE.md  
**Fáze:** country_authority — krok PE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Peru (`PE`), 10 slotů (`ca-PE-{authority}`). **Camisea plyn + Peru LNG** (jediný LNG exportér J. Ameriky);
Petroperú (potíže, rafinerie Talara), Perupetro (kontrakty). Politická nestabilita. 7 `proposed`, 2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-PE-ministry_petroleum | ministry_petroleum | Ministry of Energy & Mines (MINEM) | gob.pe/minem | government_regulator | official | production, export_license | proposed |
| ca-PE-noc | noc | Petroperú / Perupetro | petroperu.com.pe | noc | official | production, exports, refinery_outage | proposed |
| ca-PE-mfa | mfa | Ministry of Foreign Affairs | gob.pe/rree | diplomacy | official | sanctions | unverified |
| ca-PE-customs_export | customs_export | SUNAT (Aduanas) | sunat.gob.pe | government_regulator | official | exports, imports | proposed |
| ca-PE-upstream_regulator | upstream_regulator | Perupetro / Osinergmin | perupetro.com.pe | government_regulator | official | production, export_license | proposed |
| ca-PE-port_maritime_authority | port_maritime_authority | APN / Peru LNG (Pampa Melchorita) | apn.gob.pe | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-PE-national_exchange | national_exchange | — (BVL financial only) | — | — | — | — | empty |
| ca-PE-central_bank | central_bank | BCRP (Banco Central de Reserva) | bcrp.gob.pe | government_regulator | official | sanctions | proposed |
| ca-PE-environment_regulator | environment_regulator | OEFA | oefa.gob.pe | government_regulator | official | refinery_outage | proposed |
| ca-PE-coast_guard_navy | coast_guard_navy | DICAPI (Peruvian Coast Guard) | dicapi.mil.pe | diplomacy | official | port_closure | unverified |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PE-upstream_regulator (Perupetro) | Camisea plyn; Peru LNG export | politická nestabilita (protesty) | **Pampa Melchorita LNG** | proposed — jediný LNG export J. Am. |
| ca-PE-noc (Petroperú) | Talara rafinerie potíže | fiskální riziko (bailouty) | — | proposed |

### Poznámky

- **Peru LNG (Pampa Melchorita)** = jediný LNG export terminál v Jižní Americe → Atlantic/Pacific arb signál.
- Petroperú chronické finanční potíže (Talara refinery overrun) → refinery outage / restrukturalizace.
- Politická nestabilita (protesty v Camisea regionu) → občasné production shut-in.

### Progress po merge

`last_country: PE`, `last_batch_seq: 62`
