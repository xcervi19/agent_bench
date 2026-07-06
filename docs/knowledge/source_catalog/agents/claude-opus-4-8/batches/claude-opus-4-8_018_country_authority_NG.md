# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_018_country_authority_NG.md  
**Fáze:** country_authority — krok NG (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Nigérie (`NG`), 10 slotů (`ca-NG-{authority}`). Trading: **crude theft / pipeline sabotage**
(Niger Delta), časté **force majeure** (Bonny Light, Forcados), **Dangote refinery** mění tok produktů.
7 `proposed`, 2 `unverified`, 1 pozn.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-NG-ministry_petroleum | ministry_petroleum | Ministry of Petroleum Resources | gov.ng | government_regulator | official | production, export_license | unverified |
| ca-NG-noc | noc | NNPC Limited | nnpcgroup.com | noc | official | production, exports, force_majeure | proposed |
| ca-NG-mfa | mfa | Ministry of Foreign Affairs | foreignaffairs.gov.ng | diplomacy | official | sanctions | unverified |
| ca-NG-customs_export | customs_export | Nigeria Customs Service | customs.gov.ng | government_regulator | official | exports | proposed |
| ca-NG-upstream_regulator | upstream_regulator | NUPRC | nuprc.gov.ng | government_regulator | official | production, export_license | proposed |
| ca-NG-port_maritime_authority | port_maritime_authority | Nigerian Ports Authority (NPA) | nigerianports.gov.ng | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-NG-national_exchange | national_exchange | Nigerian Exchange (NGX) | ngxgroup.com | exchange | official | pricing_formula | proposed |
| ca-NG-central_bank | central_bank | Central Bank of Nigeria | cbn.gov.ng | government_regulator | official | sanctions | proposed |
| ca-NG-environment_regulator | environment_regulator | NOSDRA (oil spill) / NESREA | nosdra.gov.ng | government_regulator | official | refinery_outage | proposed |
| ca-NG-coast_guard_navy | coast_guard_navy | Nigerian Navy | navy.mil.ng | diplomacy | official | port_closure, force_majeure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NG-noc (NNPC) | produkce, force majeure | OPEC+ kvóta (chronicky pod) | Bonny, Forcados, Qua Iboe | proposed |
| ca-NG-coast_guard_navy (Navy) | crude theft interdiction | Delta security | pipeline/terminal ochrana | proposed — theft = supply signál |

### Unverified / poznámky

- **Unverified domény:** Ministry of Petroleum (`gov.ng` sub-path), MFA (`foreignaffairs.gov.ng`).
- **Dangote refinery** (soukromé, dangote.com) — mění import produktů → cenný, ale komerční, ne autorita.
- NMDPRA (downstream) jako expanze upstream_regulator slotu.
- Časté force majeure na Forcados/Bonny = opakovaný price signál.

### Progress po merge

`last_country: NG`, `last_batch_seq: 18`
