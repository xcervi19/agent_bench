# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_004_country_authority_IR.md  
**Fáze:** country_authority — krok IR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-04  

---

## Shrnutí

Írán (`IR`), 10 slotů autorit (`ca-IR-{authority}`). Vysoká **sankční relevance** — oficiální
export data jsou neprůhledná (dark fleet, STS transfery, off-AIS loading), takže oficiální
zdroje sledujeme spíš pro **policy/rétoriku** než pro čísla; skutečné toky se ověřují přes
sankční trackery (Fáze 4) a AIS. 7 `proposed`, 2 `unverified`, 1 `empty`.
Do `source_whitelist.json` nezapisuji.

---

### Navržené / aktualizované sloty

| id | country | authority_type | entity | domain | category | type | signals | status |
|----|---------|----------------|--------|--------|----------|------|---------|--------|
| ca-IR-ministry_petroleum | IR | ministry_petroleum | Ministry of Petroleum (SHANA news) | mop.ir | government_regulator | official | production, export_license, quota_rhetoric | proposed |
| ca-IR-noc | IR | noc | National Iranian Oil Company (NIOC) | nioc.ir | noc | official | production, exports, term_contract | proposed |
| ca-IR-mfa | IR | mfa | Ministry of Foreign Affairs | mfa.ir | diplomacy | official | sanctions | proposed |
| ca-IR-customs_export | IR | customs_export | IRICA (Iran Customs Administration) | irica.ir | government_regulator | official | exports, export_license | proposed |
| ca-IR-upstream_regulator | IR | upstream_regulator | — | — | — | — | — | empty |
| ca-IR-port_maritime_authority | IR | port_maritime_authority | Ports & Maritime Organization (PMO) | pmo.ir | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-IR-national_exchange | IR | national_exchange | Iran Energy Exchange (IRENEX) | irenex.ir | exchange | official | pricing_formula, export_license | proposed |
| ca-IR-central_bank | IR | central_bank | Central Bank of Iran (CBI) | cbi.ir | government_regulator | official | sanctions | proposed |
| ca-IR-environment_regulator | IR | environment_regulator | Department of Environment | doe.ir | government_regulator | official | refinery_outage | unverified |
| ca-IR-coast_guard_navy | IR | coast_guard_navy | IRGC Navy / Iranian Navy | — | diplomacy | official | port_closure, force_majeure | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IR-ministry_petroleum | produkce, kapacita (SHANA) | export policy pod sankcemi, JCPOA rétorika | — | proposed — SHANA (shana.ir) rychlejší kanál |
| ca-IR-noc (NIOC) | produkce, Kharg loading | sovereign export strategy | Kharg Island terminal | proposed |
| ca-IR-mfa | — | JCPOA, sankce, US/EU jednání | — | proposed — vysoká geo priorita |
| ca-IR-customs_export | export objemy (oficiální ≠ skutečné) | sankční obcházení | — | proposed — **čísla neprůhledná**, cross-check AIS |
| ca-IR-national_exchange (IRENEX) | — | — | bourse pro ropné produkty, workaround exportu | proposed |
| ca-IR-port_maritime_authority (PMO) | — | — | Kharg / Bandar Abbas / Assaluyeh throughput | proposed |
| ca-IR-coast_guard_navy | — | Hormuz seizure/harassment, transit riziko | lane closure, tanker zadržení | unverified — IRGC nemá standardní oficiální web |

---

### Unverified / Anti-patterns / poznámky

- **`ca-IR-upstream_regulator` = empty:** integrováno pod MOP + NIOC, žádný nezávislý regulátor.
- **`doe.ir`** (Department of Environment) — doména `unverified`, ověřit `/source-discover`.
- **`ca-IR-coast_guard_navy`** — IRGC Navy nemá spolehlivý oficiální web; sledovat spíš přes
  MFA/state media + sankční trackery. Doména prázdná → `unverified`, kandidát na `empty`.
- **Sankční kontext (kritické):** oficiální íránská export čísla systematicky podhodnocena /
  neprůhledná (dark fleet, STS u Malajsie/Singapuru, off-AIS Kharg loading). Oficiální sloty
  = **policy signal**, ne volume truth; skutečné toky patří sankčním trackerům (Fáze 4) + AIS.
- **SHANA** (`shana.ir`) je oficiální news agentura MOP — rychlejší než `mop.ir`; kandidát na
  `official_social` / news slot ve Fázi 4.
- Anti-pattern: nespoléhat na íránská customs čísla jako ground truth; neuvádět opoziční /
  exilová media jako oficiální autoritu.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 3,
  "last_country": "IR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 4
}
```

Po merge → **další dávka:** `claude-opus-4-8_005_country_authority_IQ.md`
(Fáze 2, třetí země `IQ` = Iraq: MoO, SOMO/Basra Oil Co, MFA, customs, PMO/Basra ports,
exchange, CBI, env, navy; pozor na federal vs. KRG (Kurdistan) export split).
