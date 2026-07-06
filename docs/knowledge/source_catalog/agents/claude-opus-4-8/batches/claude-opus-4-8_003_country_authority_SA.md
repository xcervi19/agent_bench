# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_003_country_authority_SA.md  
**Fáze:** country_authority — krok SA (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-04  

---

## Shrnutí

Saudská Arábie (`SA`), 10 slotů autorit (`ca-SA-{authority}`). 7 obsazeno `proposed`,
2 `unverified` (ověřit doménu), 1 `empty` (nemá distinktní nezávislou entitu).
Klíč pro trading: **Saudi Aramco OSP** (Official Selling Price) je hlavní price-moving
signál regionu; MoEnergy nese OPEC+ kvótovou rétoriku. Do `source_whitelist.json` nezapisuji.

---

### Navržené / aktualizované sloty

| id | country | authority_type | entity | domain | category | type | signals | status |
|----|---------|----------------|--------|--------|----------|------|---------|--------|
| ca-SA-ministry_petroleum | SA | ministry_petroleum | Ministry of Energy | moenergy.gov.sa | government_regulator | official | quota_rhetoric, export_license, production | proposed |
| ca-SA-noc | SA | noc | Saudi Aramco | aramco.com | noc | official | production, exports, term_contract, pricing_formula | proposed |
| ca-SA-mfa | SA | mfa | Ministry of Foreign Affairs | mofa.gov.sa | diplomacy | official | sanctions | proposed |
| ca-SA-customs_export | SA | customs_export | ZATCA (Zakat, Tax & Customs) | zatca.gov.sa | government_regulator | official | exports, export_license | proposed |
| ca-SA-upstream_regulator | SA | upstream_regulator | — | — | — | — | — | empty |
| ca-SA-port_maritime_authority | SA | port_maritime_authority | Mawani (Saudi Ports Authority) | mawani.gov.sa | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-SA-national_exchange | SA | national_exchange | Saudi Exchange (Tadawul) | saudiexchange.sa | exchange | official | pricing_formula | proposed |
| ca-SA-central_bank | SA | central_bank | Saudi Central Bank (SAMA) | sama.gov.sa | government_regulator | official | sanctions | proposed |
| ca-SA-environment_regulator | SA | environment_regulator | National Center for Environmental Compliance (NCEC) | ncec.gov.sa | government_regulator | official | refinery_outage | unverified |
| ca-SA-coast_guard_navy | SA | coast_guard_navy | Saudi Border Guard | gdbg.gov.sa | government_regulator | official | port_closure, force_majeure | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SA-ministry_petroleum | produkční politika, capacity | OPEC+ kvóty, rétorika ministra | — | proposed |
| ca-SA-noc (Aramco) | produkce, spare capacity, maintenance | OSP jako sovereign pricing signal | Ras Tanura / Yanbu loading | proposed — nejvyšší priorita SA |
| ca-SA-mfa | — | sankce, diplomacie (Írán, US) | — | proposed |
| ca-SA-customs_export | export objemy | export licence | celní režim | proposed |
| ca-SA-port_maritime_authority | — | — | Ras Tanura/Yanbu/Jubail throughput, closures | proposed |
| ca-SA-national_exchange | — | — | Tadawul = finanční burza, ne crude pricing | proposed (Tier 2, nízká přímá relevance) |
| ca-SA-environment_regulator | refinery compliance | — | — | unverified — doména NCEC k ověření |
| ca-SA-coast_guard_navy | — | Rudé moře / Hormuz transit obrana | port/lane closure | unverified — doména Border Guard k ověření |

---

### Unverified / Anti-patterns / poznámky

- **`ca-SA-upstream_regulator` = empty:** SA nemá nezávislý upstream regulátor odlišný od
  Ministry of Energy + Aramco (vertikálně integrováno). Neduplikuji ministerstvo do slotu.
- **NCEC** (`ncec.gov.sa`) a **Border Guard** (`gdbg.gov.sa`) — domény `unverified`,
  postoupit `/source-discover` k ověření.
- **Tadawul** je akciová/finanční burza; crude pricing jde přes **Aramco OSP**, ne přes
  národní komoditní burzu — proto `pricing_formula` primárně na `ca-SA-noc`.
- Anti-pattern: neuvádět Argus/Platts OSP komentáře jako SA autoritu — OSP publikuje Aramco.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 2,
  "last_country": "SA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 3
}
```

Po merge → **další dávka:** `claude-opus-4-8_004_country_authority_IR.md`
(Fáze 2, druhá země `IR` = Iran: 10 slotů — MOP, NIOC, MFA, customs, ports (PMO),
IRISL/tanker, exchange, central bank, env, IRGC Navy; vysoká sankční relevance).
