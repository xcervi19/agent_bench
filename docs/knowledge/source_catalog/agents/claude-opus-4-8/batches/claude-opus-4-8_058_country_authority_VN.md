# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_058_country_authority_VN.md  
**Fáze:** country_authority — krok VN (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Vietnam (`VN`), 10 slotů (`ca-VN-{authority}`). **PetroVietnam (PVN)** NOC; producent + rafinér (Dung Quat,
Nghi Son) + rostoucí LNG importér. South China Sea nároky = geo riziko. 7 `proposed`, 2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-VN-ministry_petroleum | ministry_petroleum | Ministry of Industry & Trade (MOIT) | moit.gov.vn | government_regulator | official | production, imports | proposed |
| ca-VN-noc | noc | PetroVietnam (PVN) | pvn.vn | noc | official | production, imports, refinery_outage | proposed |
| ca-VN-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.vn | diplomacy | official | sanctions | proposed |
| ca-VN-customs_export | customs_export | Vietnam Customs | customs.gov.vn | government_regulator | official | imports, exports | proposed |
| ca-VN-upstream_regulator | upstream_regulator | MOIT / PVN | moit.gov.vn | government_regulator | official | production | unverified |
| ca-VN-port_maritime_authority | port_maritime_authority | Vietnam Maritime Admin (Vinamarine) | vinamarine.gov.vn | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-VN-national_exchange | national_exchange | — (HOSE financial only) | — | — | — | — | empty |
| ca-VN-central_bank | central_bank | State Bank of Vietnam | sbv.gov.vn | government_regulator | official | sanctions | proposed |
| ca-VN-environment_regulator | environment_regulator | Ministry of Natural Resources & Env | monre.gov.vn | government_regulator | official | refinery_outage | proposed |
| ca-VN-coast_guard_navy | coast_guard_navy | Vietnam Coast Guard | canhsatbien.vn | diplomacy | official | port_closure | unverified |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-VN-noc (PVN) | domácí produkce, Dung Quat/Nghi Son | **South China Sea** blokové spory (CN) | rafinerie, LNG terminál (Thi Vai) | proposed |

### Poznámky

- **South China Sea:** čínské nároky blokují VN offshore průzkum → supply/geo signál.
- Rostoucí LNG import (Thi Vai terminál) → regionální JKM demand.
- HOSE = jen finanční burza (empty pro komodity).

### Progress po merge

`last_country: VN`, `last_batch_seq: 58`
