# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_026_country_authority_ID.md  
**Fáze:** country_authority — krok ID (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Indonésie (`ID`), 10 slotů (`ca-ID-{authority}`). **Net importér** (opustila OPEC 2016), palivové
dotace, klesající LNG export (Bontang). Straits: Malacca/Sunda/Lombok. **SKK Migas** upstream data.
10 `proposed`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-ID-ministry_petroleum | ministry_petroleum | Ministry of Energy & Mineral Res. (ESDM) | esdm.go.id | government_regulator | official | production, imports | proposed |
| ca-ID-noc | noc | Pertamina | pertamina.com | noc | official | production, imports, refinery_outage | proposed |
| ca-ID-mfa | mfa | Ministry of Foreign Affairs (Kemlu) | kemlu.go.id | diplomacy | official | sanctions | proposed |
| ca-ID-customs_export | customs_export | Customs and Excise (DJBC) | beacukai.go.id | government_regulator | official | exports, imports | proposed |
| ca-ID-upstream_regulator | upstream_regulator | SKK Migas | skkmigas.go.id | government_regulator | official | production | proposed |
| ca-ID-port_maritime_authority | port_maritime_authority | Ministry of Transportation / Pelindo | dephub.go.id | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-ID-national_exchange | national_exchange | Indonesia Stock Exchange (IDX) | idx.co.id | exchange | official | pricing_formula | proposed |
| ca-ID-central_bank | central_bank | Bank Indonesia | bi.go.id | government_regulator | official | sanctions | proposed |
| ca-ID-environment_regulator | environment_regulator | Ministry of Env & Forestry | menlhk.go.id | government_regulator | official | refinery_outage | proposed |
| ca-ID-coast_guard_navy | coast_guard_navy | Bakamla (Coast Guard) | bakamla.go.id | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ID-noc (Pertamina) | domácí produkce, import paliv | dotace, energy security | Cilacap refining, Bontang LNG | proposed |
| ca-ID-upstream_regulator (SKK Migas) | upstream produkce data | — | — | proposed |

### Unverified / poznámky

- Indonésie = net importér ropy, ale stále LNG exportér (klesající) — smíšený signál.
- Straits Sunda/Lombok = alternativy k Malacca pro VLCC (draft) — geo pozn.
- IDX finanční, Tier 2.

### Progress po merge

`last_country: ID`, `last_batch_seq: 26`
