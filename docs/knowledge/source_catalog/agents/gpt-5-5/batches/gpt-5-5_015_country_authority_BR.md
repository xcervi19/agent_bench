# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_015_country_authority_BR.md  
**Fáze:** country_authority — krok BR (Fáze 2, Brazil)  
**Datum:** 2026-07-05  

---

## Shrnutí

Jedenáctá dávka Fáze 2: `BR` × 10 typů autorit podle skeleton dimenze.
Brazil je desk-critical pro pre-salt production growth, Petrobras capex/outages, Atlantic export flows, refining/fuels policy, FPSO/weather risk a product imports.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BR-ministry_petroleum | BR | — | ministry_petroleum | Brazil Ministry of Mines and Energy (MME) | mme.gov.br | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-BR-noc | BR | — | noc | Petrobras | petrobras.com.br | noc | official | production, exports, force_majeure, refinery_outage, term_contract | proposed |
| ca-BR-mfa | BR | — | mfa | Ministry of Foreign Affairs of Brazil (Itamaraty) | itamaraty.gov.br | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-BR-customs_export | BR | — | customs_export | Receita Federal do Brasil | receita.fazenda.gov.br | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-BR-upstream_regulator | BR | — | upstream_regulator | ANP | anp.gov.br | government_regulator | official | production, force_majeure, export_license, refinery_outage | proposed |
| ca-BR-port_maritime_authority | BR | — | port_maritime_authority | Portos do Brasil | portosdobrasil.gov.br | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-BR-national_exchange | BR | — | national_exchange | B3 | b3.com.br | exchange | data_feed | pricing_formula | proposed |
| ca-BR-central_bank | BR | — | central_bank | Central Bank of Brazil | bcb.gov.br | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-BR-environment_regulator | BR | — | environment_regulator | IBAMA | ibama.gov.br | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-BR-coast_guard_navy | BR | — | coast_guard_navy | Brazilian Navy | marinha.mil.br | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BR-ministry_petroleum | Primary policy source for oil/gas and fuels. | OPEC+ observer/producer diplomacy context. | Logistics indirect. | proposed |
| ca-BR-noc | Petrobras is operationally central for pre-salt, refining and exports. | State-controlled strategic entity. | Direct production/export/outage relevance. | proposed |
| ca-BR-upstream_regulator | ANP is direct petroleum regulator and data source. | Sovereign licensing and fuel policy signal. | Direct production and downstream relevance. | proposed |
| ca-BR-port_maritime_authority | Federal port source appears relevant, but exact official canonical domain should be checked. | Infrastructure policy. | Direct port/logistics signal if confirmed. | unverified |
| ca-BR-coast_guard_navy | Navy authority matters for offshore and maritime security. | Sovereign maritime source. | Direct offshore/weather/security relevance. | proposed |

---

### Unverified / Anti-patterns

- `ca-BR-port_maritime_authority` is `unverified`: confirm canonical current government port authority domain/path before whitelist.
- `B3` is listed-market context, not physical oil-flow confirmation.
- Petrobras is state-controlled and desk-critical, but specific operational incidents should be cross-checked with ANP, ports, and company releases.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 11,
  "last_country": "BR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 15
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_016_country_authority_CA.md`.
