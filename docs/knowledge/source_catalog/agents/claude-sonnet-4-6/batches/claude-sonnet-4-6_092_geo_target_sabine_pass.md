# Batch 092 — Geo Target: Sabine Pass

## Geo significance
**Sabine Pass** (Cameron Parish, Louisiana / Orange County, Texas, Gulf of Mexico) hosts the **Sabine Pass LNG terminal** — the **first and largest US LNG export facility** (Cheniere Energy, Trains 1–6, ~30 mtpa capacity). It is the bellwether for the entire US LNG export industry. Sabine Pass exports go primarily to Europe (post-2022 Russia-Ukraine war surge) and Asia. Train-level operational data — maintenance shutdowns, train restart notices, feed gas nominations, vessel scheduling — are all tier-1 market signals that directly move TTF/JKM/Henry Hub spreads. Adjacent **Sabine Pass LNG import terminal** (now rarely used) and **Port Arthur LNG** (under construction ~13 mtpa, TotalEnergies + Sempra) will expand the complex. USCG Sector New Orleans manages channel access.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-sabine_pass-cheniere | US | sabine_pass | us_gulf_hub | Cheniere Energy – Sabine Pass LNG operations | cheniere.com | company | official | exports, vessel_loading, production | proposed |
| gt-sabine_pass-marinetraffic | — | sabine_pass | us_gulf_hub | MarineTraffic AIS — Sabine Pass LNG terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-sabine_pass-vortexa | — | sabine_pass | us_gulf_hub | Vortexa — Sabine Pass LNG cargo tracking | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-sabine_pass-kpler | — | sabine_pass | us_gulf_hub | Kpler — Sabine Pass LNG export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-sabine_pass-eia_lng | US | sabine_pass | us_gulf_hub | EIA Natural Gas Weekly – LNG export feed gas | eia.gov | international_agency | official | exports, production | proposed |
| gt-sabine_pass-uscg_nola | US | sabine_pass | us_gulf_hub | USCG Sector New Orleans (Sabine Pass channel) | uscg.mil | international_agency | official | port_closure, force_majeure | proposed |
| gt-sabine_pass-noaa_hurricane | — | sabine_pass | us_gulf_hub | NOAA NHC – Gulf of Mexico hurricane (Sabine Pass) | nhc.noaa.gov | weather | official | force_majeure, port_closure | proposed |
| gt-sabine_pass-ferc | US | sabine_pass | us_gulf_hub | FERC – Natural Gas Pipeline Safety (Sabine Pass filings) | ferc.gov | international_agency | official | production, force_majeure | proposed |
| gt-sabine_pass-platts_hh | — | sabine_pass | us_gulf_hub | S&P Global Platts – Henry Hub / LNG netback | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-sabine_pass-icis_lng | — | sabine_pass | us_gulf_hub | ICIS LNG – Sabine Pass cargo analysis | icis.com | industry_body | official | exports, pricing_formula | proposed |

## Cross-check

### gt-sabine_pass-cheniere (Cheniere Energy)
- **Supply:** Trains 1–6 ~30 mtpa; feed gas nominations (Genscape/Wood Mackenzie feed gas tracker = real-time train status); Train maintenance = HH dip + TTF/JKM rally; Sabine Pass 2024 cargo destinations: ~45% Europe, ~40% Asia; Cheniere earnings = forward export outlook
- **Geopolitics:** US LNG = EU energy security cornerstone post-NordStream; Biden administration LNG export pause (Jan 2024 DOE authorization freeze) = market event; Trump reversal = export acceleration; Qatar competition = contract pricing benchmark
- **Logistics:** 6 trains + marine berths; LNG carriers queue in Gulf of Mexico; feed gas from Haynesville/Perms basin via Sabine Pass pipeline; Trains 1–4 operated, 5–6 newer; Port Arthur LNG 13 mtpa under construction adjacent

### gt-sabine_pass-ferc (FERC)
- **Supply:** FERC approves Sabine Pass maintenance/modification filings; force majeure declarations filed with FERC; train outage engineering notices = advance supply disruption signal
- **Geopolitics:** FERC quorum/appointment = LNG export authorization pace; FERC environmental review = new terminal expansion timeline
- **Logistics:** FERC gas pipeline safety orders; emergency shutdown protocols; feeder pipeline pressure requirements

## Expansion slots
- gt-sabine_pass-genscape_feed — Wood Mackenzie/Genscape feed gas tracker (real-time train status)
- gt-sabine_pass-port_arthur_lng — Port Arthur LNG (TotalEnergies, ~13 mtpa, under construction)
- gt-sabine_pass-bloomberg_lng — Bloomberg LNG Sabine Pass terminal monitor

## Anti-patterns
- Skip: Lake Charles American Press (local press)
- Skip: naturalgasintel.com daily (subscription aggregator; use EIA/FERC primary)
