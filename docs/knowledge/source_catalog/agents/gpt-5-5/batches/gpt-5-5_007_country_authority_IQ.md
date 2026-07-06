# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_007_country_authority_IQ.md  
**Fáze:** country_authority — krok IQ (Fáze 2, Iraq)  
**Datum:** 2026-07-05  

---

## Shrnutí

Třetí dávka Fáze 2: `IQ` × 10 typů autorit podle skeleton dimenze.
Iraq je desk-critical pro Basra exports, OPEC+ compliance, northern pipeline politics, Kurdistan/federal frictions, Gulf port logistics a payment/security risks.

Do `source_whitelist.json` zatím nezapisovat; tato dávka čeká na review a případný merge do `catalog.json`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IQ-ministry_petroleum | IQ | — | ministry_petroleum | Iraq Ministry of Oil | oil.gov.iq | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-IQ-noc | IQ | basra | noc | Basra Oil Company (BOC) | boc.oil.gov.iq | noc | official | production, exports, force_majeure, vessel_loading | unverified |
| ca-IQ-mfa | IQ | — | mfa | Ministry of Foreign Affairs of Iraq | mofa.gov.iq | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-IQ-customs_export | IQ | — | customs_export | General Customs Authority of Iraq | customs.mof.gov.iq | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-IQ-upstream_regulator | IQ | — | upstream_regulator | Iraq Ministry of Oil | oil.gov.iq | government_regulator | official | production, force_majeure, quota_rhetoric | proposed |
| ca-IQ-port_maritime_authority | IQ | basra | port_maritime_authority | General Company for Ports of Iraq (GCPI) | scp.gov.iq | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-IQ-national_exchange | IQ | — | national_exchange | Iraq Stock Exchange (ISX) | isx-iq.net | exchange | data_feed | pricing_formula | proposed |
| ca-IQ-central_bank | IQ | — | central_bank | Central Bank of Iraq | cbi.iq | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-IQ-environment_regulator | IQ | — | environment_regulator | Iraqi Ministry of Environment | moen.gov.iq | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-IQ-coast_guard_navy | IQ | basra | coast_guard_navy | Iraqi Navy / Ministry of Defense | mod.mil.iq | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IQ-ministry_petroleum | Primary federal source for production, exports, OPEC+ and field policy. | Direct sovereign signal for federal/KRG disputes and quota rhetoric. | Logistics indirect but frames Basra and pipeline export policy. | proposed |
| ca-IQ-noc | Basra operator is the key physical supply path for southern crude exports. | State oil company under Ministry of Oil; federal/KRG politics indirect. | Direct relevance to Basra loading/export operations, but site availability is weak. | unverified |
| ca-IQ-mfa | Not a supply source. | Primary diplomatic source for sanctions, regional relations and pipeline/export negotiations. | Logistics indirect except border or regional crisis statements. | proposed |
| ca-IQ-customs_export | Customs procedures affect import/export clearance and trade controls. | Relevant to sanctions and border enforcement. | Direct clearance signal, less direct for crude liftings. | proposed |
| ca-IQ-upstream_regulator | Ministry of Oil holds federal sector oversight. | Primary federal policy channel. | Logistics indirect. | proposed |
| ca-IQ-port_maritime_authority | State port operator for Umm Qasr, Khor Al-Zubair and southern port system. | Federal infrastructure authority. | Direct vessel/loading/closure signal for Gulf logistics. | proposed |
| ca-IQ-national_exchange | Listed-market signal, not physical crude. | Market stress and listed company disclosure context. | Logistics indirect. | proposed |
| ca-IQ-central_bank | FX auctions, payments and banking rules affect trade settlement. | Sanctions/payment-channel relevance. | Logistics indirect but important for imports/export settlement. | proposed |
| ca-IQ-environment_regulator | Environmental rules can affect refining/industrial operations. | Government compliance signal. | Relevant to outages and site constraints, less first-line export signal. | proposed |
| ca-IQ-coast_guard_navy | Navy would be material for offshore terminal and port security. | Security and sanctions enforcement through defense channels. | Direct Basra/Gulf maritime security relevance, but standalone official Navy site not confirmed. | unverified |

---

### Unverified / Anti-patterns

- `ca-IQ-noc` is marked `unverified`: `boc.oil.gov.iq` is widely referenced for Basra Oil Company, but live access can fail behind a gateway/subscription error; confirm before whitelist.
- `ca-IQ-coast_guard_navy` is marked `unverified`: Iraqi Navy appears under Ministry of Defense rather than a clean standalone public website; preserve exact Navy path if found.
- `ca-IQ-upstream_regulator` intentionally reuses `oil.gov.iq`; do not invent a separate federal upstream regulator where Ministry of Oil holds oversight.
- `ca-IQ-customs_export` uses `customs.mof.gov.iq`; Ministry of Finance pages may be more stable for whitelist notes if subdomain access is gated.
- Do not use KRG-only oil sources for the federal `IQ` authority slot without explicitly separating federal vs Kurdistan coverage in a later country/region expansion.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 3,
  "last_country": "IQ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 7
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_008_country_authority_RU.md` (Fáze 2, Russia autority).
