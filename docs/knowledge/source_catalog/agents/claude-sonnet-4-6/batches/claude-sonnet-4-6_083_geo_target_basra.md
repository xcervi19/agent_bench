# Batch 083 — Geo Target: Basra (Iraq)

## Geo significance
**Basra** is Iraq's primary crude export hub — **Basra Oil Terminal (BOT)** + **Al-Faw SPM** + the upcoming **Al-Faw Grand Port** handle ~3.3–3.5 mb/d of Iraqi exports (~95% of Iraq's crude revenue). Key grades: **Basra Heavy** (~3.5° API heavier, dominant volume) and **Basra Medium**. The terminal complex is operated by **SOMO** (State Organization for Marketing of Oil) and **South Oil Company (SOC)**. Basra is vulnerable to: (1) **port congestion** (SPM mooring failures = loading delays); (2) **Shatt al-Arab waterway** silting + Iranian/Iraqi water politics; (3) **PMF/militia activity** (Kataib Hezbollah = supply disruption risk); (4) **summer heat** (temperatures >55°C = worker stoppage risk). Basra crude OSP = key OPEC+ output signal monthly.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-basra-somo | IQ | basra | load_port | SOMO – State Organization for Marketing of Oil | somo.gov.iq | international_agency | official | exports, pricing_formula, vessel_loading | proposed |
| gt-basra-marinetraffic | — | basra | load_port | MarineTraffic AIS — Basra Oil Terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-basra-vortexa | — | basra | load_port | Vortexa — Basra crude loading analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-basra-kpler | — | basra | load_port | Kpler — Basra/Iraq crude export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-basra-soc | IQ | basra | load_port | South Oil Company (SOC) – terminal operations | soc.gov.iq | international_agency | official | production, vessel_loading, force_majeure | proposed |
| gt-basra-ukmto | — | basra | load_port | UKMTO – Northern Arabian Gulf / Basra advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-basra-platts_osp | — | basra | load_port | S&P Global Platts – Basra OSP assessment | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-basra-iraq_mop | IQ | basra | load_port | Iraqi Ministry of Oil (Basra policy) | oil.gov.iq | international_agency | official | policy, exports, quota_rhetoric | proposed |
| gt-basra-iraq_navy | IQ | basra | load_port | Iraqi Navy / Umm Qasr Port Authority | iqnavy.iq | international_agency | official | port_closure, force_majeure | unverified |
| gt-basra-bimco | — | basra | load_port | BIMCO Arabian Gulf/Basra circulars | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |

## Cross-check

### gt-basra-somo (SOMO)
- **Supply:** SOMO issues monthly loading programs; Basra Heavy + Basra Medium OSP (announced ~5th of month); SOMO term contract holders (Asian refineries, Mediterranean); production outages at Rumalia/West Qurna = SOMO loading program cut
- **Geopolitics:** SOMO under MoO = political appointments signal; KRG Kirkuk pipeline dispute = north vs south Iraq output; PMF attacks on BOT approach = supply disruption; US-Iran proxy conflict in Basra
- **Logistics:** BOT has 4 SPMs (single point moorings); SPM failure = loading suspension; Shatt al-Arab silting = VLCC draft restriction; Al-Faw Grand Port (under construction, ~2028)

### gt-basra-soc (South Oil Company)
- **Supply:** SOC operates Rumalia (largest Iraqi field, ~1.3 mb/d), West Qurna 1 (ExxonMobil→PetroChina), Majnoon (Shell→Basra Oil); SOC field shutdown = SOMO loading suspension
- **Geopolitics:** SOC management = Basra political economy; electricity/water for oilfield operations = local government tension; PMF influence over service contracts
- **Logistics:** Pipeline network from Rumalia to BOT; onshore gathering stations; SPM buoy maintenance (key constraint)

## Expansion slots
- gt-basra-basra_oil_terminal — BOT official (SPM status + vessel scheduling)
- gt-basra-eia_iraq — EIA Iraq country analysis (weekly production estimates)
- gt-basra-iea_iraq — IEA OMR Iraq chapter

## Anti-patterns
- Skip: BasraNews.net (local news, no primary data)
- Skip: Iraqi state TV energy coverage (SOMO official announcements preferred)
