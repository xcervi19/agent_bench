# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_032_country_authority_TR.md  
**Fáze:** country_authority — krok TR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Turecko (`TR`), 10 slotů (`ca-TR-{authority}`). **Tranzitní/hub velmoc**: Turkish Straits (Bospor),
Ceyhan terminal (BTC + KRG Irák), TANAP/TurkStream/Blue Stream. "Gas hub" ambice; kupuje diskontovanou
ruskou ropu/plyn. Vysoká **logistics** relevance. 10 `proposed`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-TR-ministry_petroleum | ministry_petroleum | Ministry of Energy & Natural Res. | enerji.gov.tr | government_regulator | official | production, imports | proposed |
| ca-TR-noc | noc | TPAO (Turkish Petroleum) | tpao.gov.tr | noc | official | production, imports, term_contract | proposed |
| ca-TR-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.tr | diplomacy | official | sanctions | proposed |
| ca-TR-customs_export | customs_export | Ministry of Trade (Customs) | ticaret.gov.tr | government_regulator | official | exports, imports | proposed |
| ca-TR-upstream_regulator | upstream_regulator | EPDK (Energy Market Regulator) | epdk.gov.tr | government_regulator | official | production, pricing_formula | proposed |
| ca-TR-port_maritime_authority | port_maritime_authority | Directorate of Coastal Safety (Straits) | kiyiemniyeti.gov.tr | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-TR-national_exchange | national_exchange | EPIAS (Energy Exchange) | epias.com.tr | exchange | official | pricing_formula | proposed |
| ca-TR-central_bank | central_bank | CBRT | tcmb.gov.tr | government_regulator | official | sanctions | proposed |
| ca-TR-environment_regulator | environment_regulator | Ministry of Environment | csb.gov.tr | government_regulator | official | refinery_outage | proposed |
| ca-TR-coast_guard_navy | coast_guard_navy | Turkish Coast Guard | sg.gov.tr | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TR-port_maritime_authority (Straits) | — | **Bospor/Dardanely tranzit** (tanker delays) | ruský crude, Novorossiysk exit | proposed — vysoká priorita |
| ca-TR-noc (TPAO) | domácí produkce (Black Sea Sakarya gas) | Ceyhan hub (BTC+KRG) | BOTAS gas hub ambice | proposed — BOTAS expanze |

### Unverified / poznámky

- **BOTAS** (botas.gov.tr) — gas importér/tranzit + hub ambice; expanze NOC slotu.
- **Turkish Straits** = geo cíl Fáze 3 (`bospor`); tanker delays = opakovaný signál.
- **Ceyhan** = výstup BTC (Ázerbájdžán) + KRG (Irák); ITP halted 2023 → KRG část mimo provoz.
- EPIAS = energetická burza (plyn/elektřina); Borsa Istanbul finanční (Tier 2, expanze).

### Progress po merge

`last_country: TR`, `last_batch_seq: 32`
