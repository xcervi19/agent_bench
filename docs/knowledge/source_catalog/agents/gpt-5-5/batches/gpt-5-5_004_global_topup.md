# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_004_global_topup.md  
**Fáze:** global — krok topup (Fáze 1, završení plánovaných 115 slotů)  
**Datum:** 2026-07-04  

---

## Shrnutí

Čtvrtá dávka doplňuje globální vrstvu o 35 slotů po merge `gpt-5-5_003_global_expansion.md`.
Po schválení a merge této dávky bude globální fáze na plánovaných **115 slotech** a další pevná fáze je `country_authority` pro `SA`.

Do `source_whitelist.json` zatím nezapisovat; tato dávka čeká na review a případný merge do `catalog.json`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-international_agency-015 | — | — | international_agency | European Commission DG Energy | energy.ec.europa.eu | international_agency | official | sanctions, imports, storage_levels, pricing_formula | proposed |
| gl-international_agency-016 | — | — | international_agency | EU Agency for the Cooperation of Energy Regulators (ACER) | acer.europa.eu | international_agency | data_feed | pricing_formula, storage_levels, imports | proposed |
| gl-international_agency-017 | — | — | international_agency | ENTSOG Transparency Platform | transparency.entsog.eu | international_agency | data_feed | imports, pipeline_outage, storage_levels | proposed |
| gl-international_agency-018 | — | — | international_agency | ENTSO-E Transparency Platform | transparency.entsoe.eu | international_agency | data_feed | imports, pricing_formula, storage_levels | proposed |
| gl-international_agency-019 | — | — | international_agency | Energy Community Secretariat | energy-community.org | international_agency | official | imports, export_license, sanctions | proposed |
| gl-international_agency-020 | — | — | international_agency | UNCTAD | unctad.org | international_agency | official | exports, imports, vessel_loading | proposed |
| gl-international_agency-021 | — | — | international_agency | World Customs Organization (WCO) | wcoomd.org | international_agency | official | export_license, sanctions, imports, exports | proposed |
| gl-international_agency-022 | — | — | international_agency | European Environment Agency (EEA) | eea.europa.eu | international_agency | data_feed | refinery_outage, pricing_formula, imports | proposed |
| gl-exchange-017 | FR | — | exchange | Euronext | euronext.com | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-018 | US | — | exchange | Nasdaq Commodities | nasdaq.com | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-019 | ES | — | exchange | MIBGAS | mibgas.es | exchange | data_feed | pricing_formula, storage_levels, imports | proposed |
| gl-exchange-020 | — | — | exchange | OMIP | omip.pt | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-021 | JP | — | exchange | Japan Electric Power Exchange (JEPX) | jepx.jp | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-022 | KR | — | exchange | Korea Exchange (KRX) | krx.co.kr | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-023 | BR | — | exchange | B3 | b3.com.br | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-024 | MX | — | exchange | MexDer | mexder.com.mx | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-025 | — | — | exchange | HUPX | hupx.hu | exchange | data_feed | pricing_formula, imports | proposed |
| gl-weather-017 | BR | — | weather | Instituto Nacional de Meteorologia (INMET) | inmet.gov.br | weather | data_feed | hurricane, production, port_closure | proposed |
| gl-weather-018 | MX | — | weather | Servicio Meteorologico Nacional / CONAGUA | smn.conagua.gob.mx | weather | data_feed | hurricane, port_closure, refinery_outage | proposed |
| gl-weather-019 | ID | — | weather | BMKG Indonesia | bmkg.go.id | weather | data_feed | hurricane, port_closure, imports | proposed |
| gl-weather-020 | MY | — | weather | Malaysian Meteorological Department | met.gov.my | weather | data_feed | hurricane, port_closure, imports | proposed |
| gl-weather-021 | TH | — | weather | Thai Meteorological Department | tmd.go.th | weather | data_feed | hurricane, port_closure, imports | proposed |
| gl-weather-022 | VN | — | weather | Viet Nam National Center for Hydro-Meteorological Forecasting | nchmf.gov.vn | weather | data_feed | hurricane, port_closure, imports | proposed |
| gl-weather-023 | OM | — | weather | Oman Meteorology | met.gov.om | weather | data_feed | port_closure, imports | proposed |
| gl-shipping-019 | BE | — | shipping | Port of Antwerp-Bruges | portofantwerpbruges.com | shipping | official | vessel_loading, port_closure, storage_levels | proposed |
| gl-shipping-020 | NL | ara | shipping | Port of Amsterdam | portofamsterdam.com | shipping | official | vessel_loading, port_closure, storage_levels | proposed |
| gl-shipping-021 | US | — | shipping | Port of Los Angeles | portoflosangeles.org | shipping | official | vessel_loading, imports, port_closure | proposed |
| gl-shipping-022 | US | — | shipping | Port of Long Beach | polb.com | shipping | official | vessel_loading, imports, port_closure | proposed |
| gl-shipping-023 | US | sabine_pass | shipping | Sabine-Neches Navigation District | navigationdistrict.org | shipping | official | vessel_loading, port_closure, exports | proposed |
| gl-shipping-024 | US | freeport | shipping | Freeport LNG | freeportlng.com | shipping | official | vessel_loading, exports, force_majeure | proposed |
| gl-shipping-025 | US | sabine_pass | shipping | Cheniere Energy / Sabine Pass LNG | cheniere.com | shipping | official | vessel_loading, exports, force_majeure | proposed |
| gl-shipping-026 | AE | jebel_ali | shipping | AD Ports Group | adportsgroup.com | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-027 | OM | — | shipping | ASYAD Group | asyad.om | shipping | official | vessel_loading, port_closure, exports | proposed |
| gl-industry_body-017 | GB | — | industry_body | Energy UK | energy-uk.org.uk | industry_body | official | imports, pricing_formula, storage_levels | proposed |
| gl-industry_body-018 | — | — | industry_body | World Liquid Gas Association | worldliquidgas.org | industry_body | official | imports, exports, term_contract | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-international_agency-015 | EU energy balances, storage, emergency policy. | Direct sanctions and market-intervention signal. | Indirect but important for European import flows. | proposed |
| gl-international_agency-017 | Gas flow and capacity transparency. | EU security-of-supply relevance. | Direct pipeline and storage logistics signal. | proposed |
| gl-exchange-019 | Iberian gas pricing and hub data. | EU market intervention sensitivity. | Useful for LNG-to-Europe price signal. | proposed |
| gl-exchange-025 | Central European power pricing context. | Relevant to regional energy stress. | Indirect gas-to-power demand signal. | proposed |
| gl-weather-019 | Indonesian weather and disaster warnings. | Official sovereign source. | LNG/coal port disruption path. | proposed |
| gl-weather-023 | Oman weather conditions. | Official national source. | Useful for Arabian Sea and Omani port operations. | proposed |
| gl-shipping-019 | ARA product and chemical logistics hub. | EU port policy relevance. | Direct throughput/storage relevance. | proposed |
| gl-shipping-023 | US Gulf navigation channel for refining/LNG corridor. | US infrastructure relevance. | Direct vessel transit and port closure signal. | proposed |
| gl-shipping-024 | Freeport LNG operations and outages. | US LNG export infrastructure relevance. | Direct cargo/export/force majeure signal. | proposed |
| gl-industry_body-018 | LPG trade and market structure context. | Policy less direct. | Useful for LPG cargo and term-market context. | proposed |

Rows not individually expanded above follow the same rule: `proposed` only where the source is institutionally identifiable and has a direct supply, logistics, pricing, or policy use case.

---

### Unverified / Anti-patterns

- `gl-exchange-020` and `gl-exchange-025` intentionally keep country blank because Portugal and Hungary are not in the current skeleton country list.
- `gl-shipping-024` and `gl-shipping-025` are company/operator sources for LNG infrastructure, not sovereign authorities; use them for operational confirmation, then cross-check with regulators/ports.
- `energy.ec.europa.eu`, `transparency.entsog.eu`, and `transparency.entsoe.eu` are subdomains. If whitelist policy collapses to root domains, preserve the publication path in notes.
- Do not promote weather or exchange sources to alert priority unless the playbook maps the event trigger to a commodity flow, storage, demand, or price channel.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 0,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 4
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_005_country_authority_SA.md` (Fáze 2, Saudi Arabia autority).
