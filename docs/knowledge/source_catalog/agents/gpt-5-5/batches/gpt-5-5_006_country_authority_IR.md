# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_006_country_authority_IR.md  
**Fáze:** country_authority — krok IR (Fáze 2, Iran)  
**Datum:** 2026-07-05  

---

## Shrnutí

Druhá dávka Fáze 2: `IR` × 10 typů autorit podle skeleton dimenze.
Iran je desk-critical pro sankce, Hormuz, crude/condensate exports, tanker opacity a regionální security risk; u některých slotů je potřeba držet explicitní caveat kvůli omezené dostupnosti a paralelním institucím.

Do `source_whitelist.json` zatím nezapisovat; tato dávka čeká na review a případný merge do `catalog.json`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IR-ministry_petroleum | IR | — | ministry_petroleum | Ministry of Petroleum of Iran | mop.ir | government_regulator | official | production, exports, sanctions, quota_rhetoric | proposed |
| ca-IR-noc | IR | kharg | noc | National Iranian Oil Company (NIOC) | nioc.ir | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-IR-mfa | IR | — | mfa | Ministry of Foreign Affairs of Iran | mfa.gov.ir | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-IR-customs_export | IR | — | customs_export | Islamic Republic of Iran Customs Administration (IRICA) | irica.ir | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-IR-upstream_regulator | IR | — | upstream_regulator | Ministry of Petroleum of Iran | mop.ir | government_regulator | official | production, force_majeure, sanctions | proposed |
| ca-IR-port_maritime_authority | IR | hormuz | port_maritime_authority | Ports and Maritime Organization of Iran (PMO) | pmo.ir | infrastructure | official | vessel_loading, port_closure, exports, sanctions | proposed |
| ca-IR-national_exchange | IR | — | national_exchange | Iran Energy Exchange (IRENEX) | irenex.ir | exchange | data_feed | pricing_formula, exports, sanctions | unverified |
| ca-IR-central_bank | IR | — | central_bank | Central Bank of the Islamic Republic of Iran | cbi.ir | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-IR-environment_regulator | IR | — | environment_regulator | Department of Environment of Iran | doe.ir | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-IR-coast_guard_navy | IR | hormuz | coast_guard_navy | Islamic Republic of Iran Navy (NEDAJA) | aja.ir | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IR-ministry_petroleum | Primary policy source for oil/gas production and export posture. | Sanctions-linked sovereign source; directly relevant to quota rhetoric. | Logistics indirect but frames export policy. | proposed |
| ca-IR-noc | Direct NOC source for crude, condensate, downstream and export operations. | State-owned entity under sanctions pressure. | Relevant to Kharg/loading and export operations; also check NIOC International Affairs. | proposed |
| ca-IR-mfa | Not a supply source. | Primary diplomatic source for sanctions, nuclear talks, regional escalation and retaliation language. | Logistics indirect except crisis statements affecting Hormuz or neighboring routes. | proposed |
| ca-IR-customs_export | Customs source for official trade procedures and clearances. | Relevant for sanctions/export controls and enforcement language. | Direct clearance/import-export signal, though oil flows may remain opaque. | proposed |
| ca-IR-upstream_regulator | MOP supervises oil/gas sector and upstream subsidiaries. | Same sovereign/sanction signal as ministry slot. | Logistics indirect. | proposed |
| ca-IR-port_maritime_authority | Port authority for Iranian ports and maritime rules. | Sovereign maritime source with sanctions and ship-call implications. | Direct port/closure/vessel-loading relevance, especially Gulf/Caspian ports. | proposed |
| ca-IR-national_exchange | Energy exchange can reveal domestic product/electricity/oil-product pricing. | Sanctions-sensitive market venue. | Logistics indirect; domain should be manually confirmed before whitelist. | unverified |
| ca-IR-central_bank | Monetary, FX and banking rules affect trade settlement. | Critical sanctions/payment-channel source. | Logistics indirect but important for payment and import/export viability. | proposed |
| ca-IR-environment_regulator | Environmental restrictions can affect refinery/industrial operation. | Government compliance signal. | Relevant to shutdown/compliance constraints, less to first-line crude flows. | proposed |
| ca-IR-coast_guard_navy | Naval source would be material for maritime security. | Direct Hormuz/security escalation signal. | Direct maritime risk relevance, but public official web presence is not cleanly separated from `aja.ir`. | unverified |

---

### Unverified / Anti-patterns

- `ca-IR-national_exchange` is marked `unverified`: search evidence points to `irenex.ir` / IRENEX, while some public traces mention `iee.ir`; confirm canonical production domain before whitelist.
- `ca-IR-coast_guard_navy` is marked `unverified`: Iran Navy public communications appear hosted under broader Army / state-media channels; preserve exact Navy path if found before whitelist.
- `ca-IR-upstream_regulator` intentionally reuses `mop.ir`; do not invent a separate upstream regulator where MOP/NIOC split already covers regulator/operator roles.
- `ca-IR-customs_export` uses `irica.ir`; older traces also reference `irica.gov.ir`. Confirm the live canonical site before whitelist.
- Do not treat secondary media or sanctions databases as primary sources for Iran slots; use them only to validate entity/domain relationships.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 2,
  "last_country": "IR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 6
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_007_country_authority_IQ.md` (Fáze 2, Iraq autority).
