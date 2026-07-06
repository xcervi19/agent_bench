# Batch 085 — Geo Target: Jebel Ali

## Geo significance
**Jebel Ali** (Dubai, UAE) is the **Middle East's largest port** and the world's 9th busiest container port (15m TEU/y), operated by **DP World**. It is the primary UAE product import/export hub and a strategic **LNG import terminal** (Dubai Supply Authority, DUSUP, FSRUs). Jebel Ali hosts **DEWA (Dubai Electricity and Water Authority)** power stations, the **Jebel Ali Free Zone (JAFZA)** — a critical energy services hub — and the **Dubai Petroleum storage complex**. Crude import (from ADNOC via Abu Dhabi pipelines) and refined products exports are the primary energy flows. Jebel Ali also serves as a logistics base for operations in the broader Gulf region. The **Jebel Ali Power Station** (gas-fired, DEWA) is a major gas demand indicator.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-jebel_ali-dp_world | AE | jebel_ali | load_port | DP World – Jebel Ali Port operations | dpworld.com | company | official | vessel_loading, port_closure, exports | proposed |
| gt-jebel_ali-marinetraffic | — | jebel_ali | load_port | MarineTraffic AIS — Jebel Ali terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-jebel_ali-vortexa | — | jebel_ali | load_port | Vortexa — Jebel Ali products/crude analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-jebel_ali-kpler | — | jebel_ali | load_port | Kpler — Jebel Ali export/import tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-jebel_ali-dusup | AE | jebel_ali | load_port | DUSUP – Dubai Supply Authority (LNG imports) | dusup.ae | international_agency | official | imports, vessel_loading | proposed |
| gt-jebel_ali-platts_bunker | — | jebel_ali | load_port | S&P Global Platts – Jebel Ali bunker assessment | spglobal.com | industry_body | official | pricing_formula, vessel_loading | proposed |
| gt-jebel_ali-ukmto | — | jebel_ali | load_port | UKMTO – Arabian Gulf / Jebel Ali advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-jebel_ali-jafza | AE | jebel_ali | load_port | JAFZA – Jebel Ali Free Zone Authority | jafza.ae | international_agency | official | exports, vessel_loading | proposed |
| gt-jebel_ali-dubai_customs | AE | jebel_ali | load_port | Dubai Customs (Jebel Ali trade data) | dubaicustoms.gov.ae | international_agency | official | exports, imports | proposed |
| gt-jebel_ali-bimco | — | jebel_ali | load_port | BIMCO Arabian Gulf / Jebel Ali circulars | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |

## Cross-check

### gt-jebel_ali-dp_world (DP World)
- **Supply:** DP World Jebel Ali = primary UAE product/container throughput; port congestion = regional supply chain disruption; Jebel Ali closure (rare) = major ME logistics shock; DP World global network = freight market signal
- **Geopolitics:** Jebel Ali as US Navy ship calls location (5th Fleet coordination); UAE-Israel Abraham Accords = new trade routes; Iran threat to UAE ports (DP World Hormuz exposure)
- **Logistics:** 67 berths; 22m draft; 24/7 ops; DUSUP LNG FSRU at dedicated berth; product tanker + LNG carrier + VLCC mix

### gt-jebel_ali-dusup (DUSUP)
- **Supply:** DUSUP manages Dubai gas + LNG supply; two FSRUs at Jebel Ali for LNG regasification; Dubai power sector (DEWA) primary gas demand; LNG import cargo = JKM/TTF spot signal
- **Geopolitics:** Dubai gas demand growth = ADNOC supply expansion signal; Abu Dhabi-Dubai energy interdependency; LNG import diversification (Qatar + SPOT)
- **Logistics:** FSRU mooring at Jebel Ali berth; regasification → DEWA gas grid; annual LNG procurement tender

## Expansion slots
- gt-jebel_ali-dewa — DEWA gas consumption reports (gas demand = Jebel Ali import signal)
- gt-jebel_ali-adnoc_distribution — ADNOC Distribution (fuel retail UAE = demand proxy)
- gt-jebel_ali-dp_world_reports — DP World Annual Report (port throughput stats)

## Anti-patterns
- Skip: Gulf News port coverage (secondary)
- Skip: khaleejtimes.com energy section (aggregator)
