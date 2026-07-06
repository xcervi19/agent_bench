# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_006_country_authority_RU.md  
**Fáze:** country_authority — krok RU (Fáze 2, země 4/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Russia × 10 autorit. **9 proposed**, **1 unverified** (coast_guard_navy — MOD site; FSB coastal role separate).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-RU-ministry_petroleum | RU | — | ministry_petroleum | Ministry of Energy | minenergo.gov.ru | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-RU-noc | RU | — | noc | Rosneft | rosneft.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-RU-mfa | RU | — | mfa | Ministry of Foreign Affairs | mid.ru | diplomacy | official | sanctions,export_license | proposed |
| ca-RU-customs_export | RU | — | customs_export | Federal Customs Service (FTS) | customs.gov.ru | government_regulator | official | exports,export_license,imports | proposed |
| ca-RU-upstream_regulator | RU | — | upstream_regulator | Rosnedra (Subsoil Use Agency) | rosnedra.gov.ru | government_regulator | official | production,term_contract | proposed |
| ca-RU-port_maritime_authority | RU | — | port_maritime_authority | Rosmorport | rosmorport.ru | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-RU-national_exchange | RU | — | national_exchange | Moscow Exchange (MOEX) | moex.com | exchange | official | pricing_formula,exports | proposed |
| ca-RU-central_bank | RU | — | central_bank | Bank of Russia | cbr.ru | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-RU-environment_regulator | RU | — | environment_regulator | Rosprirodnadzor | rpn.gov.ru | government_regulator | official | refinery_outage,production | proposed |
| ca-RU-coast_guard_navy | RU | — | coast_guard_navy | Ministry of Defence (Russian Navy) | mod.gov.ru | government_regulator | official | port_closure,vessel_loading | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-RU-ministry_petroleum | Production guidance, OPEC+ coordination | Energy diplomacy, price-cap response | Export policy / redirect to Asia | **proposed** |
| ca-RU-noc | Field output, maintenance, capex | Sanctions / ownership changes | ESPO / Urals export programs | **proposed** — desk also watches Lukoil, Gazprom Neft (private/state mix) |
| ca-RU-mfa | — | Sanctions retaliation, Ukraine war diplomacy | Insurance / tanker flag restrictions | **proposed** |
| ca-RU-customs_export | — | Export ban enforcement (diesel etc.) | Border / pipeline metering disputes | **proposed** |
| ca-RU-upstream_regulator | License awards, field approvals | Subsoil law changes | New capacity timelines | **proposed** |
| ca-RU-port_maritime_authority | — | — | Novorossiysk, Primorsk, Ust-Luga, Kozmino loading | **proposed** — pair with **Transneft** (`transneft.ru`) in playbook |
| ca-RU-national_exchange | Urals / gas futures settlement | — | Domestic price discovery vs export netbacks | **proposed** |
| ca-RU-central_bank | — | Sanctions FX controls | Payment routing for oil exports | **proposed** |
| ca-RU-environment_regulator | Environmental orders | — | Refinery / field compliance shutdowns | **proposed** |
| ca-RU-coast_guard_navy | — | Black Sea / Baltic security | Port access, drone attacks on Novorossiysk | **unverified** — operational updates often via MOD press service |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-RU-coast_guard_navy | `mod.gov.ru` — defence ministry, not dedicated navy portal; Black Sea ops also need playbook context |
| ca-RU-noc | Rosneft = largest state-influenced oil co.; not sole NOC — matrix slot anchor only |

**Playbook extensions (Tier 1 logistics, mimo slot):** `transneft.ru` (pipeline export monopoly), `gazprom.com` (gas/LNG).

**Desk note:** Tier 1 = **minenergo.gov.ru + rosneft.com + rosmorport.ru + transneft.ru**. Urals discount / export redirect signals from MOEX + customs before newswires.

**Anti-patterns:** sanctioned-entity mirrors; aggregator «Urals price» blogs without MOEX/customs source.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 5,
  "last_country": "RU",
  "crosscheck_cursor": 0,
  "last_batch_seq": 6
}
```

**Další dávka:** `composer-2-5_007_country_authority_US.md` (United States × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`minenergo.gov.ru`, `rosneft.com`, `mid.ru`, `customs.gov.ru`, `rosnedra.gov.ru`, `rosmorport.ru`, `moex.com`, `cbr.ru`, `rpn.gov.ru`
