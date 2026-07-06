# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_025_country_authority_IN.md  
**Fáze:** country_authority — krok IN (Fáze 2, India)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá první dávka Fáze 2: `IN` × 10 typů autorit podle skeleton dimenze.  
India je desk-critical pro crude import demand, Russian crude sanctions risk, refinery/export margins, SPR/product flows, rupee settlement and Indian Ocean maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IN-ministry_petroleum | IN | — | ministry_petroleum | Ministry of Petroleum and Natural Gas | mopng.gov.in | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-IN-noc | IN | — | noc | Oil and Natural Gas Corporation (ONGC) | ongcindia.com | noc | official | production, imports, force_majeure, term_contract, vessel_loading | proposed |
| ca-IN-mfa | IN | — | mfa | Ministry of External Affairs | mea.gov.in | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-IN-customs_export | IN | — | customs_export | Central Board of Indirect Taxes and Customs (CBIC) | cbic-gst.gov.in | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-IN-upstream_regulator | IN | — | upstream_regulator | Directorate General of Hydrocarbons | dghindia.gov.in | government_regulator | official | production, force_majeure, export_license | unverified |
| ca-IN-port_maritime_authority | IN | — | port_maritime_authority | Directorate General of Shipping | dgshipping.gov.in | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-IN-national_exchange | IN | — | national_exchange | National Stock Exchange of India | nseindia.com | exchange | data_feed | pricing_formula | proposed |
| ca-IN-central_bank | IN | — | central_bank | Reserve Bank of India | rbi.org.in | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-IN-environment_regulator | IN | — | environment_regulator | Central Pollution Control Board | cpcb.gov.in | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-IN-coast_guard_navy | IN | — | coast_guard_navy | Indian Navy | indiannavy.nic.in | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IN-ministry_petroleum | Primary petroleum policy and market source. | Russian crude, product exports and settlement relevance. | Logistics indirect. | proposed |
| ca-IN-noc | ONGC anchors domestic upstream; not the only state oil actor. | Strategic state company context. | Less direct for import cargoes than refiners/ports. | proposed |
| ca-IN-customs_export | Customs is relevant for import/export enforcement. | Sanctions and tariff-policy relevance. | Direct trade-flow context. | proposed |
| ca-IN-port_maritime_authority | DG Shipping is key maritime regulator. | Indian Ocean security/regulatory relevance. | Direct maritime/logistics signal. | proposed |
| ca-IN-upstream_regulator | DGH is the expected upstream regulator. | Licensing and production relevance. | Domain should be manually confirmed before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-IN-upstream_regulator` is `unverified`: validate `dghindia.gov.in` and current publication surface before whitelist.
- India has several state oil companies and major private refiners; ONGC is the upstream NOC anchor, not a complete proxy for refinery/import behavior.
- Do not use product-export or Russian-crude claims without cross-checking ministry, customs, port/shipping and refiner evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 21,
  "last_country": "IN",
  "crosscheck_cursor": 0,
  "last_batch_seq": 25
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_026_country_authority_MY.md`.
