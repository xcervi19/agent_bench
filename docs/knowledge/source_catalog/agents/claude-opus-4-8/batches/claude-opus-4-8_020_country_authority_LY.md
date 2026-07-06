# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_020_country_authority_LY.md  
**Fáze:** country_authority — krok LY (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Libye (`LY`), 10 slotů (`ca-LY-{authority}`). **Politický rozkol** (GNU Tripolis vs. východ) →
většina úřadů duplicitní/nefunkční. **NOC force majeure / blokády** = hlavní supply signál
(Sharara, El Feel, ropné terminály). **CBL** rozdělena, spor o ropné příjmy. Jen 2 `proposed`,
3 `unverified`, 5 `empty` — vědomě, kvalita nad kvótou.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-LY-ministry_petroleum | ministry_petroleum | Ministry of Oil and Gas | oil.gov.ly | government_regulator | official | production, export_license | unverified |
| ca-LY-noc | noc | National Oil Corporation (NOC) | noc.ly | noc | official | production, exports, force_majeure, port_closure | proposed |
| ca-LY-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-LY-customs_export | customs_export | Libyan Customs | — | government_regulator | official | exports | empty |
| ca-LY-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-LY-port_maritime_authority | port_maritime_authority | NOC oil terminals (Es Sider/Ras Lanuf) | noc.ly | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-LY-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-LY-central_bank | central_bank | Central Bank of Libya (CBL) | cbl.gov.ly | government_regulator | official | sanctions | proposed |
| ca-LY-environment_regulator | environment_regulator | Environment General Authority | — | government_regulator | official | refinery_outage | unverified |
| ca-LY-coast_guard_navy | coast_guard_navy | Libyan Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-LY-noc (NOC) | produkce, force majeure declarace | blokády jako politická páka | Es Sider, Ras Lanuf, Zueitina, Brega, Sharara | proposed — **jediný spolehlivý zdroj** |
| ca-LY-central_bank (CBL) | ropné příjmy | rozdělení CBL, spor o distribuci | — | proposed |

### Unverified / Anti-patterns / poznámky

- **Politický rozkol:** duplicitní východní/západní úřady → většina slotů `empty`, nezdvojovat.
- **NOC (noc.ly)** = primární zdroj pro produkci i terminály; force majeure oznámení = okamžitý price signál.
- **Unverified:** Ministry of Oil (`oil.gov.ly`), Environment authority.
- Anti-pattern: brát prohlášení jedné frakce jako národní autoritu; NOC/CBL jsou nejblíž neutrální.

### Progress po merge

`last_country: LY`, `last_batch_seq: 20`
