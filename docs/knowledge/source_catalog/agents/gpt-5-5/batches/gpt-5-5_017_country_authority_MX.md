# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_017_country_authority_MX.md  
**Fáze:** country_authority — krok MX (Fáze 2, Mexico)  
**Datum:** 2026-07-05  

---

## Shrnutí

Třináctá dávka Fáze 2: `MX` × 10 typů autorit podle skeleton dimenze.
Mexico je desk-critical pro Pemex output/refining, Gulf export flows, product imports, tax/customs enforcement, US-linked gas/products trade a hurricane/refinery outage risk.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MX-ministry_petroleum | MX | — | ministry_petroleum | Secretaria de Energia (SENER) | gob.mx/sener | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-MX-noc | MX | — | noc | Pemex | pemex.com | noc | official | production, exports, force_majeure, refinery_outage, term_contract | proposed |
| ca-MX-mfa | MX | — | mfa | Secretaria de Relaciones Exteriores (SRE) | gob.mx/sre | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-MX-customs_export | MX | — | customs_export | Servicio de Administracion Tributaria (SAT) | sat.gob.mx | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-MX-upstream_regulator | MX | — | upstream_regulator | ASEA | gob.mx/asea | government_regulator | official | production, force_majeure, refinery_outage | proposed |
| ca-MX-port_maritime_authority | MX | — | port_maritime_authority | ASIPONA / Mexican port system | gob.mx/asipona | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-MX-national_exchange | MX | — | national_exchange | Bolsa Mexicana de Valores (BMV) | bmv.com.mx | exchange | data_feed | pricing_formula | proposed |
| ca-MX-central_bank | MX | — | central_bank | Banco de Mexico (Banxico) | banxico.org.mx | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-MX-environment_regulator | MX | — | environment_regulator | SEMARNAT | semarnat.gob.mx | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-MX-coast_guard_navy | MX | — | coast_guard_navy | Secretaria de Marina (SEMAR) | gob.mx/semar | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MX-ministry_petroleum | Primary federal energy policy source. | Sovereign policy and import/export stance. | Logistics indirect. | proposed |
| ca-MX-noc | Pemex is direct operational source for production/refining. | State strategic entity and fiscal/policy channel. | Direct export/refinery outage relevance. | proposed |
| ca-MX-customs_export | SAT handles tax/customs enforcement. | Sanctions/export control relevance. | Direct clearance/import/export signal. | proposed |
| ca-MX-upstream_regulator | ASEA covers safety/environment for hydrocarbons. | Federal regulatory signal. | Direct outage/safety relevance. | proposed |
| ca-MX-port_maritime_authority | ASIPONA coverage appears relevant, but exact canonical federal port path should be confirmed. | Infrastructure policy. | Direct port/logistics signal if confirmed. | unverified |
| ca-MX-coast_guard_navy | SEMAR has maritime security/port authority relevance. | Sovereign maritime/security source. | Direct Gulf/Pacific port and vessel movement signal. | proposed |

---

### Unverified / Anti-patterns

- `ca-MX-port_maritime_authority` is `unverified`: confirm current canonical ASIPONA / port authority path before whitelist.
- `BMV` is listed-market context, not physical crude/product flow confirmation.
- `gob.mx/*` paths are important; if whitelist collapses domains to `gob.mx`, preserve agency path in notes.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 13,
  "last_country": "MX",
  "crosscheck_cursor": 0,
  "last_batch_seq": 17
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_018_country_authority_VE.md` (Fáze 2, Venezuela autority).
