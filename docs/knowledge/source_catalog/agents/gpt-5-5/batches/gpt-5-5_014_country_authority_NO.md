# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_014_country_authority_NO.md  
**Fáze:** country_authority — krok NO (Fáze 2, Norway)  
**Datum:** 2026-07-05  

---

## Shrnutí

Desátá dávka Fáze 2: `NO` × 10 typů autorit podle skeleton dimenze.
Norway je desk-critical pro North Sea gas/oil output, European gas security, offshore maintenance, labor disruptions, pipeline exports a weather/logistics.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NO-ministry_petroleum | NO | — | ministry_petroleum | Norwegian Ministry of Energy | regjeringen.no | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-NO-noc | NO | — | noc | Equinor | equinor.com | noc | official | production, exports, force_majeure, term_contract, pipeline_outage | unverified |
| ca-NO-mfa | NO | — | mfa | Norwegian Ministry of Foreign Affairs | regjeringen.no | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-NO-customs_export | NO | — | customs_export | Norwegian Customs (Tolletaten) | toll.no | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-NO-upstream_regulator | NO | — | upstream_regulator | Norwegian Offshore Directorate | sodir.no | government_regulator | official | production, force_majeure, pipeline_outage | proposed |
| ca-NO-port_maritime_authority | NO | hammerfest | port_maritime_authority | Norwegian Coastal Administration (Kystverket) | kystverket.no | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-NO-national_exchange | NO | — | national_exchange | Oslo Bors | oslobors.no | exchange | data_feed | pricing_formula | proposed |
| ca-NO-central_bank | NO | — | central_bank | Norges Bank | norges-bank.no | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-NO-environment_regulator | NO | — | environment_regulator | Norwegian Environment Agency | miljodirektoratet.no | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-NO-coast_guard_navy | NO | — | coast_guard_navy | Norwegian Coast Guard / Armed Forces | forsvaret.no | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NO-ministry_petroleum | Primary policy source for production and licensing. | European security-of-supply relevance. | Logistics indirect. | proposed |
| ca-NO-noc | Equinor is state-majority and operationally central, but not a formal monopoly NOC. | Strategic energy entity. | Direct production/export and outage relevance. | unverified |
| ca-NO-upstream_regulator | Offshore permits and resource data. | Sovereign regulatory signal. | Direct offshore production relevance. | proposed |
| ca-NO-port_maritime_authority | Coastal and navigation authority. | Sovereign maritime infrastructure source. | Direct navigation/closure relevance. | proposed |
| ca-NO-coast_guard_navy | Coast Guard under Armed Forces. | Maritime security relevance. | Direct offshore/port approach signal. | proposed |

---

### Unverified / Anti-patterns

- `ca-NO-noc` is `unverified`: Equinor is state-majority and desk-critical, but not a clean single NOC equivalent.
- `regjeringen.no` hosts multiple ministries; preserve ministry path in whitelist notes if paths are supported.
- `Oslo Bors` is listed-market context, not physical flow confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 10,
  "last_country": "NO",
  "crosscheck_cursor": 0,
  "last_batch_seq": 14
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_015_country_authority_BR.md`.
