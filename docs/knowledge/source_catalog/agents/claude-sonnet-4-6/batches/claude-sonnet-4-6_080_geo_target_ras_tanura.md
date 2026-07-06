# Batch 080 — Geo Target: Ras Tanura

## Geo significance
**Ras Tanura** (Saudi Arabia, Eastern Province) is the **world's largest crude oil export terminal** — ~6.0–6.5 mb/d throughput capacity; handles ~10% of global seaborne crude exports. Operated by Saudi Aramco. It comprises the **Ras Tanura Sea Island** (deep-water VLCC berths), **Tanajib** loading terminal, and the inland **Abqaiq/Qatif** pipeline network. The 2019 **Abqaiq-Khurais drone/missile attack** (Houthi/Iranian responsibility disputed) temporarily shut ~5.7 mb/d = largest-ever single supply disruption. Ras Tanura is also host to the **Ras Tanura refinery** (550 kb/d). Any operational update from Saudi Aramco, Saudi Aramco Shipping Company (SASC), or US DIA/NGA satellite imagery is a tier-1 market signal.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-ras_tanura-aramco | SA | ras_tanura | load_port | Saudi Aramco (Ras Tanura operations) | saudiaramco.com | company | official | vessel_loading, exports, production | proposed |
| gt-ras_tanura-sasc | SA | ras_tanura | load_port | Saudi Aramco Shipping Company (SASC) | saudiaramco.com | company | official | vessel_loading, exports | proposed |
| gt-ras_tanura-marinetraffic | — | ras_tanura | load_port | MarineTraffic AIS — Ras Tanura terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-ras_tanura-vortexa | — | ras_tanura | load_port | Vortexa — Ras Tanura loading analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-ras_tanura-kpler | — | ras_tanura | load_port | Kpler — Ras Tanura crude export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-ras_tanura-mopa | SA | ras_tanura | load_port | Saudi Ports Authority (Mawani) | mawani.gov.sa | international_agency | official | vessel_loading, port_closure | proposed |
| gt-ras_tanura-tanajib | SA | ras_tanura | load_port | Tanajib Terminal (Saudi Aramco satellite) | saudiaramco.com | company | official | vessel_loading, exports | proposed |
| gt-ras_tanura-ukmto | — | ras_tanura | load_port | UKMTO – Arabian Gulf load port advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-ras_tanura-platts_osp | — | ras_tanura | load_port | S&P Global Platts – Saudi OSP vs Ras Tanura loading | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-ras_tanura-navcent | US | ras_tanura | load_port | NAVCENT press releases (Ras Tanura/Gulf security) | navcent.navy.mil | international_agency | official | force_majeure, port_closure | proposed |

## Cross-check

### gt-ras_tanura-aramco (Saudi Aramco)
- **Supply:** Ras Tanura + Tanajib handle majority of Saudi crude exports (Arab Light, Arab Extra Light, Arab Heavy, Arab Medium); OSP announcement first Monday of month = global pricing signal; production cut → fewer VLCC berth calls
- **Geopolitics:** 2019 Abqaiq attack precedent = +$8/bbl overnight; Houthi/Iranian drone threat ongoing; US-Saudi defense pact = deterrent; Ras Tanura vulnerability = price floor argument
- **Logistics:** Sea Island deep-water (VLCC, up to 700 kt DWT); 6 VLCC berths; crude blending for export grades; Red Sea Jubail satellite terminal (backup)

### gt-ras_tanura-vortexa (Vortexa)
- **Supply:** Real-time VLCC berthing at Ras Tanura; crude grade loading identification; export volume vs OPEC quota cross-reference; monthly Saudi actual vs declared production
- **Geopolitics:** Vortexa Ras Tanura data = primary tool for traders tracking OPEC+ compliance
- **Logistics:** Vessel class distribution; crude grade fingerprinting; loading rate = daily output proxy

## Expansion slots
- gt-ras_tanura-abqaiq — Abqaiq/Qatif stabilization complex (pipeline supply to terminal)
- gt-ras_tanura-aramco_shipping_reports — Saudi Aramco Annual Report (terminal capacity data)
- gt-ras_tanura-intelligence_online — Intelligence Online satellite imagery citations (attack/damage reporting)

## Anti-patterns
- Skip: Saudi Gazette energy (state media, secondary)
- Skip: arabianoilandgas.com (commercial/SEO aggregator)
