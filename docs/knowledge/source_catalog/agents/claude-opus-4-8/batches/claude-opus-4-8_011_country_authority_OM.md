# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_011_country_authority_OM.md  
**Fáze:** country_authority — krok OM (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Omán (`OM`), 10 slotů (`ca-OM-{authority}`). Non-OPEC (OPEC+ DoC), **Oman crude benchmark**
(DME/Gulf Mercantile, Asie), mimo Hormuz přes Duqm/Sohar. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-OM-ministry_petroleum | ministry_petroleum | Ministry of Energy & Minerals | mem.gov.om | government_regulator | official | production, export_license | proposed |
| ca-OM-noc | noc | Petroleum Development Oman (PDO) | pdo.co.om | noc | official | production, exports, term_contract | proposed |
| ca-OM-mfa | mfa | Ministry of Foreign Affairs | fm.gov.om | diplomacy | official | sanctions | proposed |
| ca-OM-customs_export | customs_export | Directorate General of Customs (ROP) | customs.gov.om | government_regulator | official | exports | unverified |
| ca-OM-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-OM-port_maritime_authority | port_maritime_authority | ASYAD Group (Sohar/Duqm/Salalah) | asyad.om | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-OM-national_exchange | national_exchange | Muscat Stock Exchange | msx.om | exchange | official | pricing_formula | proposed |
| ca-OM-central_bank | central_bank | Central Bank of Oman | cbo.gov.om | government_regulator | official | sanctions | proposed |
| ca-OM-environment_regulator | environment_regulator | Environment Authority | ea.gov.om | government_regulator | official | refinery_outage | proposed |
| ca-OM-coast_guard_navy | coast_guard_navy | Royal Navy of Oman | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-OM-noc (PDO) | produkce (Shell/TotalEnergies JV) | OPEC+ DoC compliance | Mina al-Fahal loading | proposed — OQ jako expanze |
| ca-OM-port_maritime_authority (ASYAD) | — | Duqm mimo Hormuz (strategický) | Sohar/Duqm/Salalah | proposed |

### Unverified / poznámky

- **`customs_export` = unverified:** doména `customs.gov.om` ověřit `/source-discover`.
- **`upstream_regulator` = empty:** pod Ministry of Energy & Minerals.
- **`coast_guard_navy` = empty:** bez oficiálního webu.
- **Expanze NOC:** `ca-OM-noc__oq` (oq.com — integrovaná energetika, LNG/produkty).
- **Duqm** strategicky mimo Hormuz — relevantní pro transit-risk hedging.

### Progress po merge

`last_country: OM`, `last_batch_seq: 11`
