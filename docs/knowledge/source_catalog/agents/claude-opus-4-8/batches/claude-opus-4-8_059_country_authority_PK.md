# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_059_country_authority_PK.md  
**Fáze:** country_authority — krok PK (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Pákistán (`PK`), 10 slotů (`ca-PK-{authority}`). **LNG/crude importér** v chronické energetické+FX krizi (IMF);
OGRA regulátor, PSO/OGDCL/PPL, Port Qasim LNG. Cenově citlivý spot LNG kupec. 7 `proposed`, 2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-PK-ministry_petroleum | ministry_petroleum | Ministry of Energy (Petroleum Division) | mpnr.gov.pk | government_regulator | official | imports, production | proposed |
| ca-PK-noc | noc | OGDCL / PPL / PSO | ogdcl.com | noc | official | production, imports | proposed |
| ca-PK-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.pk | diplomacy | official | sanctions | proposed |
| ca-PK-customs_export | customs_export | FBR / Pakistan Customs | fbr.gov.pk | government_regulator | official | imports | unverified |
| ca-PK-upstream_regulator | upstream_regulator | OGRA (Oil & Gas Regulatory Authority) | ogra.org.pk | government_regulator | official | pricing_formula, imports | proposed |
| ca-PK-port_maritime_authority | port_maritime_authority | Port Qasim Authority (LNG) | pqa.gov.pk | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-PK-national_exchange | national_exchange | — (PSX financial only) | — | — | — | — | empty |
| ca-PK-central_bank | central_bank | State Bank of Pakistan | sbp.org.pk | government_regulator | official | sanctions | proposed |
| ca-PK-environment_regulator | environment_regulator | Pak-EPA | environment.gov.pk | government_regulator | official | refinery_outage | unverified |
| ca-PK-coast_guard_navy | coast_guard_navy | Pakistan Maritime Security Agency | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PK-upstream_regulator (OGRA) | LNG import tendry | **FX/IMF krize → spot cancel** | Port Qasim LNG | proposed — price-sensitive kupec |

### Poznámky

- **FX/IMF krize:** Pákistán ruší/nekupuje spot LNG při vysokých cenách → demand elasticity signál (JKM).
- Import tendry (PLL/PSO) = klíčový spot LNG poptávkový indikátor.
- PSX = jen finanční (empty).

### Progress po merge

`last_country: PK`, `last_batch_seq: 59`
