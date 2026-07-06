# Batch 089 — Geo Target: Kozmino

## Geo significance
**Kozmino** (Kozmino Bay, Russian Far East, Primorsky Krai) is the Pacific terminus of the **ESPO pipeline** (Eastern Siberia–Pacific Ocean, 1.6 mb/d capacity) — Russia's primary crude export route to **China, Japan, South Korea**. The **ESPO blend** (~33° API, low sulphur) is a premium grade commanding a discount/premium to Dubai depending on refinery demand. Kozmino loaded ~1.0–1.1 mb/d in 2023–2024, and is Russia's fastest-growing export terminal (ESPO-2 expansion). Since western sanctions, ESPO buyers have maintained (China ~80% share); Japan + Korea reduced off-take. Kozmino does not face Bosphorus constraints — direct Pacific routing. Key risks: **ESPO pipeline freeze/mechanical failure** (Siberian permafrost = infrastructure risk), weather-related port closure, and US secondary sanctions on Asian ESPO buyers.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-kozmino-transneft | RU | kozmino | load_port | Transneft – ESPO pipeline operator | transneft.ru | company | official | pipeline_flow, exports, vessel_loading | proposed |
| gt-kozmino-marinetraffic | — | kozmino | load_port | MarineTraffic AIS — Kozmino terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-kozmino-vortexa | — | kozmino | load_port | Vortexa — Kozmino/ESPO loading analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-kozmino-kpler | — | kozmino | load_port | Kpler — Kozmino crude export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-kozmino-tanker_trackers | — | kozmino | load_port | Tanker Trackers — ESPO blend/Pacific shadow fleet | tanker-trackers.com | shipping | official | exports, vessel_loading | proposed |
| gt-kozmino-platts_espo | — | kozmino | load_port | S&P Global Platts – ESPO blend price assessment | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-kozmino-ofac_russia | US | kozmino | load_port | OFAC Russia oil sanctions (secondary buyer risk) | treasury.gov | international_agency | official | sanctions, exports | proposed |
| gt-kozmino-japan_meti | JP | kozmino | load_port | Japan METI – Sakhalin-2 / ESPO off-take policy | meti.go.jp | international_agency | official | policy, imports | proposed |
| gt-kozmino-china_customs | CN | kozmino | load_port | China Customs – ESPO crude import statistics | customs.gov.cn | international_agency | official | imports, vessel_loading | proposed |
| gt-kozmino-weather_vnap | — | kozmino | load_port | Japan Meteorological Agency – Pacific NW weather | jma.go.jp | weather | official | force_majeure, port_closure | proposed |

## Cross-check

### gt-kozmino-transneft (ESPO pipeline)
- **Supply:** ESPO-1 (600 kb/d, Taishet → Skovorodino) + ESPO-2 (600 kb/d Pacific extension); Kozmino SPM loading; ESPO-2 expansion target 1.6 mb/d 2024–2025; pipeline freeze incident = loading suspension (rare but high impact)
- **Geopolitics:** China ESPO dependency (~800 kb/d to Daqing spur + Kozmino); Japan Sakhalin-2 (LNG + oil) partial integration; US secondary sanctions on Chinese ESPO buyers = market risk signal; Sino-Russian energy lock-in post-2022
- **Logistics:** Kozmino Bay SPM (ice-free Pacific port); Aframax fleet (Kozmino is Aframax-sized, no VLCC due to depth); ~90 voyages/month to China

### gt-kozmino-china_customs (China Customs)
- **Supply:** China Customs publishes monthly crude import by origin; ESPO/Russia import = primary ESPO demand signal; Chinese teapot refinery off-take; Shandong port import data
- **Geopolitics:** China-Russia "no limits" partnership energy component; China ESPO discount pricing; US pressure on Chinese banks financing ESPO trades
- **Logistics:** Qingdao + Ningbo + Rizhao = primary ESPO receiving ports in China; pipeline from Skovorodino to Daqing (1 mb/d capacity)

## Expansion slots
- gt-kozmino-argus_espo — Argus Media ESPO blend price (Kozmino FOB)
- gt-kozmino-icis_espo — ICIS ESPO-Dubai differential tracking
- gt-kozmino-sakhalin_energy — Sakhalin Energy (Sakhalin-2 Nogliki port cross-check)

## Anti-patterns
- Skip: Russia state TASS Pacific energy coverage (propaganda)
- Skip: The Diplomat energy section (geopolitics commentary, no primary data)
