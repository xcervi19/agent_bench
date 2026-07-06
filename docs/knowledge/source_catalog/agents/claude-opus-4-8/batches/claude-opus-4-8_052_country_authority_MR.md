# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_052_country_authority_MR.md  
**Fáze:** country_authority — krok MR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Mauritánie (`MR`), 10 slotů (`ca-MR-{authority}`). **Nový producent plynu**: **GTA LNG** (BP/Kosmos,
přeshraniční se Senegalem, first gas 2024/25). SMHPM NOC. Nouakchott/Nouadhibou. 3 `proposed`, 4 `unverified`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-MR-ministry_petroleum | ministry_petroleum | Ministry of Petroleum, Mines & Energy | — | government_regulator | official | production, export_license | unverified |
| ca-MR-noc | noc | SMHPM | — | noc | official | production, exports | unverified |
| ca-MR-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-MR-customs_export | customs_export | Douanes Mauritanie | — | government_regulator | official | exports | unverified |
| ca-MR-upstream_regulator | upstream_regulator | Ministry of Petroleum | — | government_regulator | official | production | unverified |
| ca-MR-port_maritime_authority | port_maritime_authority | Port de Nouakchott / GTA FLNG | — | infrastructure | official | vessel_loading | proposed |
| ca-MR-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-MR-central_bank | central_bank | Banque Centrale de Mauritanie | bcm.mr | government_regulator | official | sanctions | proposed |
| ca-MR-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | empty |
| ca-MR-coast_guard_navy | coast_guard_navy | Mauritanian Navy / garde-côtes | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MR-noc (SMHPM) | **GTA gas first output 2024/25** | **přeshraniční se SN** (Senegal) | GTA FLNG (Golar) offshore | unverified — nový supply |
| ca-MR-port_maritime_authority | GTA LNG cargo | BP/Kosmos operátoři | Grand Tortue FLNG | proposed |

### Poznámky

- **GTA LNG** = sdíleno se Senegalem (SN); cross-country projekt → koordinace obou zemí.
- Nový producent → řada domén `unverified`; BCM (`bcm.mr`) ověřit.
- FLNG (Golar Gimi) offshore → sledovat přes BP/Kosmos + AIS na GTA hubu.

### Progress po merge

`last_country: MR`, `last_batch_seq: 52`
