# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_025_country_authority_MY.md  
**Fáze:** country_authority — krok MY (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Malajsie (`MY`), 10 slotů (`ca-MY-{authority}`). **Malacca** chokepoint; **dark fleet STS** (íránský/
ruský crude ship-to-ship v malajsijských vodách — sankční relevance). **Petronas** duální role
(operátor + PSC regulátor), Bintulu LNG. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-MY-ministry_petroleum | ministry_petroleum | Ministry of Economy / Energy Commission | st.gov.my | government_regulator | official | production, export_license | unverified |
| ca-MY-noc | noc | Petronas | petronas.com | noc | official | production, exports, term_contract | proposed |
| ca-MY-mfa | mfa | Ministry of Foreign Affairs (Wisma Putra) | kln.gov.my | diplomacy | official | sanctions | proposed |
| ca-MY-customs_export | customs_export | Royal Malaysian Customs (JKDM) | customs.gov.my | government_regulator | official | exports | proposed |
| ca-MY-upstream_regulator | upstream_regulator | — (Petronas MPM integrated) | — | — | — | — | empty |
| ca-MY-port_maritime_authority | port_maritime_authority | Marine Department Malaysia | marine.gov.my | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-MY-national_exchange | national_exchange | Bursa Malaysia | bursamalaysia.com | exchange | official | pricing_formula | proposed |
| ca-MY-central_bank | central_bank | Bank Negara Malaysia | bnm.gov.my | government_regulator | official | sanctions | proposed |
| ca-MY-environment_regulator | environment_regulator | Department of Environment | doe.gov.my | government_regulator | official | refinery_outage | proposed |
| ca-MY-coast_guard_navy | coast_guard_navy | Maritime Enforcement Agency (MMEA) | mmea.gov.my | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MY-coast_guard_navy (MMEA) | — | **dark fleet STS interdikce** | Malacca, off-Tanjung Piai | proposed — sankční signál |
| ca-MY-noc (Petronas) | produkce, LNG | PSC regulátor | Bintulu LNG, Tanjung Pelepas | proposed |

### Unverified / poznámky

- **`ministry_petroleum` = unverified:** Petronas reportuje přímo premiérovi; Energy Commission
  (st.gov.my) je spíš power — ověřit správnou petroleum autoritu.
- **`upstream_regulator` = empty:** Malaysia Petroleum Management pod Petronasem.
- Malajsie = časté "origin laundering" íránského/ruského crude přes STS → MMEA + AIS klíč.
- Malacca = geo cíl Fáze 3 (`malacca`).

### Progress po merge

`last_country: MY`, `last_batch_seq: 25`
