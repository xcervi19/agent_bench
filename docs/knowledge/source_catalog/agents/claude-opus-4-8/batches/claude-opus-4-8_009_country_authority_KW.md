# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_009_country_authority_KW.md  
**Fáze:** country_authority — krok KW (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Kuvajt (`KW`), 10 slotů (`ca-KW-{authority}`). NOC struktura: **KPC** holding + dcery
(KOC upstream, KNPC refining, KOTC tankers). Klíč: Mina al-Ahmadi loading. 8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-KW-ministry_petroleum | ministry_petroleum | Ministry of Oil | moo.gov.kw | government_regulator | official | production, export_license | proposed |
| ca-KW-noc | noc | Kuwait Petroleum Corp (KPC) | kpc.com.kw | noc | official | production, exports, term_contract | proposed |
| ca-KW-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.kw | diplomacy | official | sanctions | proposed |
| ca-KW-customs_export | customs_export | General Administration of Customs | customs.gov.kw | government_regulator | official | exports | proposed |
| ca-KW-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-KW-port_maritime_authority | port_maritime_authority | Kuwait Ports Authority | kpa.gov.kw | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-KW-national_exchange | national_exchange | Boursa Kuwait | boursakuwait.com.kw | exchange | official | pricing_formula | proposed |
| ca-KW-central_bank | central_bank | Central Bank of Kuwait | cbk.gov.kw | government_regulator | official | sanctions | proposed |
| ca-KW-environment_regulator | environment_regulator | Environment Public Authority | epa.org.kw | government_regulator | official | refinery_outage | proposed |
| ca-KW-coast_guard_navy | coast_guard_navy | Kuwait Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KW-noc (KPC) | produkce, KOC fields | OPEC+ compliance | Mina al-Ahmadi / Mina Abdullah | proposed — KOC/KNPC jako expanze |
| ca-KW-national_exchange (Boursa) | — | — | akciová, Tier 2 | proposed |

### Unverified / poznámky

- **`upstream_regulator` = empty:** Supreme Petroleum Council bez webu; KOC operuje.
- **`coast_guard_navy` = empty:** bez oficiálního webu.
- **Expanze NOC:** `ca-KW-noc__koc` (kockw.com, upstream), `ca-KW-noc__knpc` (refining), KOTC (tankers).
- Neutrální zóna (Wafra/Khafji) sdílená se SA — geo/produkce pozn.

### Progress po merge

`last_country: KW`, `last_batch_seq: 9`
