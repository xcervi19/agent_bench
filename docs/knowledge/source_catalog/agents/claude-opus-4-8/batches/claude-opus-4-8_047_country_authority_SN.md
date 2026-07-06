# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_047_country_authority_SN.md  
**Fáze:** country_authority — krok SN (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Senegal (`SN`), 10 slotů (`ca-SN-{authority}`). **Nový producent 2024**: Sangomar ropa (Woodside) +
GTA LNG (BP/Kosmos, přeshraniční s Mauritánií). **Petrosen** NOC. Centrální banka regionální (BCEAO).
4 `proposed`, 4 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-SN-ministry_petroleum | ministry_petroleum | Ministry of Energy, Petroleum & Mines | energie.gouv.sn | government_regulator | official | production, export_license | unverified |
| ca-SN-noc | noc | Petrosen | petrosen.sn | noc | official | production, exports | proposed |
| ca-SN-mfa | mfa | Ministry of Foreign Affairs | diplomatie.gouv.sn | diplomacy | official | sanctions | unverified |
| ca-SN-customs_export | customs_export | Douanes Sénégal | douanes.sn | government_regulator | official | exports | unverified |
| ca-SN-upstream_regulator | upstream_regulator | Petrosen / COS-Petrogaz | — | government_regulator | official | production | unverified |
| ca-SN-port_maritime_authority | port_maritime_authority | Port Autonome de Dakar | portdakar.sn | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-SN-national_exchange | national_exchange | — (BRVM regional, Abidjan) | — | — | — | — | empty |
| ca-SN-central_bank | central_bank | BCEAO (regional WAEMU) | bceao.int | government_regulator | official | sanctions | proposed |
| ca-SN-environment_regulator | environment_regulator | DEEC (Ministry Environment) | — | government_regulator | official | refinery_outage | empty |
| ca-SN-coast_guard_navy | coast_guard_navy | Senegalese Navy (HauteMar) | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SN-noc (Petrosen) | **Sangomar first oil 2024** (Woodside) | nová vláda, revize kontraktů | FPSO offshore | proposed — nový supply |
| ca-SN-port_maritime_authority | GTA LNG (BP/Kosmos) | **přeshraniční s MR** (Mauritánie) | GTA offshore terminál | proposed |

### Unverified / poznámky

- **Nový producent** → řada domén `unverified` (nedávno založené sekce); ověřit `energie.gouv.sn`, `douanes.sn`.
- **GTA LNG** = sdílené s Mauritánií (MR) → cross-country coordinace; sledovat i MR pokud přidáno.
- Sangomar = FPSO offshore (Woodside operátor); term contracts přes Petrosen/Woodside.
- Nová vláda (Faye/Sonko) signalizovala revizi ropných/plyn. kontraktů → fiskální/policy signál.

### Progress po merge

`last_country: SN`, `last_batch_seq: 47`
