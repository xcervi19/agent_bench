# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_054_country_authority_JP.md  
**Fáze:** country_authority — krok JP (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Japonsko (`JP`), 10 slotů (`ca-JP-{authority}`). **Top LNG importér** + velký rafinér; bez NOC. METI/ANRE
politika, **JOGMEC** (SPR + JKM kontext), TOCOM burza. Vysoká transparentnost. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-JP-ministry_petroleum | ministry_petroleum | METI / ANRE | meti.go.jp | government_regulator | official | imports, storage_levels | proposed |
| ca-JP-noc | noc | JOGMEC (SPR / stockpiling) | jogmec.go.jp | international_agency | official | storage_levels, imports | proposed |
| ca-JP-mfa | mfa | Ministry of Foreign Affairs | mofa.go.jp | diplomacy | official | sanctions | proposed |
| ca-JP-customs_export | customs_export | Japan Customs (MoF) | customs.go.jp | government_regulator | official | imports | proposed |
| ca-JP-upstream_regulator | upstream_regulator | ANRE (METI) | meti.go.jp | government_regulator | official | pricing_formula | proposed |
| ca-JP-port_maritime_authority | port_maritime_authority | MLIT Ports & Harbours | mlit.go.jp | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-JP-national_exchange | national_exchange | TOCOM / JPX (Osaka) | jpx.co.jp | exchange | official | pricing_formula | proposed |
| ca-JP-central_bank | central_bank | Bank of Japan | boj.or.jp | government_regulator | official | sanctions | proposed |
| ca-JP-environment_regulator | environment_regulator | Ministry of Environment | env.go.jp | government_regulator | official | refinery_outage | unverified |
| ca-JP-coast_guard_navy | coast_guard_navy | Japan Coast Guard | kaiho.mlit.go.jp | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-JP-noc (JOGMEC) | SPR, LNG stockpile | Hormuz/Malacca závislost | import terminály | proposed — demand/storage signál |
| ca-JP-ministry_petroleum (METI) | týdenní zásoby (PAJ) | — | rafinerie | proposed |

### Poznámky

- **Bez NOC** (INPEX je privátní-ish, ale JOGMEC = stát/SPR); JOGMEC klasifikováno jako international_agency (stockpiling).
- Klíčové feedy: METI/ANRE zásoby, PAJ (Petroleum Association of Japan) — social/data layer.
- LNG demand = hlavní driver JKM; závislost na Hormuz/Malacca chokepointech.

### Progress po merge

`last_country: JP`, `last_batch_seq: 54`
