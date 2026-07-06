# Batch 082 — Geo Target: Kharg Island

## Geo significance
**Kharg Island** (Iran, northern Persian Gulf, 25 km offshore) handles **~90% of Iranian crude exports** — ~1.3–1.5 mb/d (2023–2024, sanctions-era), peak 2.5+ mb/d (pre-sanctions). It is the operational core of NIOC's export infrastructure: **T-jetty** (deep-water, 7 VLCC berths), **Dara jetty**, **Hormuz jetty**, and the **Kharg oil terminal**. Kharg was attacked during the Iran-Iraq War (1980–88) — any conflict scenario puts Kharg at direct risk. Post-2018 re-sanctions: Iranian crude exports primarily flow to **China** (clandestine, AIS dark, ship-to-ship off Malaysia/Fujairah/Oman), with smaller flows to Syria/Venezuela. Monitoring = shadow fleet tracking + Chinese refinery (Shandong teapot) import data. Kharg = Iran's strategic oil export vulnerability = top tier for geopolitical supply risk.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-kharg-nioc_exports | IR | kharg | load_port | NIOC – National Iranian Oil Company (Kharg exports) | nioc.ir | company | official | exports, vessel_loading, production | proposed |
| gt-kharg-marinetraffic | — | kharg | load_port | MarineTraffic AIS — Kharg Island / dark tanker feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-kharg-tanker_trackers | — | kharg | load_port | Tanker Trackers — Iranian crude shadow fleet | tanker-trackers.com | shipping | official | exports, vessel_loading | proposed |
| gt-kharg-vortexa | — | kharg | load_port | Vortexa — Iran crude export tracking (Kharg) | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-kharg-kpler | — | kharg | load_port | Kpler — Iranian crude flows (Kharg origin) | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-kharg-windward | — | kharg | load_port | Windward AI — AIS manipulation / dark tanker detection | windward.ai | shipping | official | exports, vessel_loading | proposed |
| gt-kharg-ukmto | — | kharg | load_port | UKMTO – Northern Gulf / Kharg area advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-kharg-ofac_sdn | US | kharg | load_port | OFAC SDN List (Iran petroleum sanctions) | treasury.gov | international_agency | official | sanctions, exports | proposed |
| gt-kharg-oil_price | — | kharg | load_port | OilPrice.com – Iran production / Kharg export analysis | oilprice.com | industry_body | official | exports, production | unverified |
| gt-kharg-iaea | — | kharg | load_port | IAEA Iran nuclear monitoring (sanctions risk context) | iaea.org | international_agency | official | sanctions, policy | proposed |

## Cross-check

### gt-kharg-tanker_trackers + gt-kharg-windward (shadow fleet)
- **Supply:** Iranian crude exported primarily to Shandong teapot refineries (via STS off Oman/Malaysia/Fujairah); AIS manipulation = vessel name + flag change + transponder off; Kharg loading rate = ~40–60 vessels/month estimated
- **Geopolitics:** US-Iran nuclear deal status = sanctions on/off toggle; JCPOA revival = +500–800 kb/d supply surge signal; Israel-Iran strike = Kharg attack = -1.5 mb/d overnight; Iran-China "25-year deal" = permanent shadow flow
- **Logistics:** STS off Khor Fakkan (UAE waters), Labuan (Malaysia), Kalamata (Greece); vessel AIS blackout → satellite SAR imagery gap filling; Vortexa/Kpler use proprietary models

### gt-kharg-ofac_sdn (OFAC)
- **Supply:** New OFAC designations (Iranian entities/vessels) = shadow fleet vessel count reduction; waiver grants = supply increase; SDN list expansion = shipping cost increase via insurance exclusions
- **Geopolitics:** US election cycle = OFAC enforcement intensity signal; Biden vs Trump JCPOA posture; Israel lobbying for tighter Iran sanctions
- **Logistics:** Vessel designation = P&I withdrawal = decommission from shadow fleet

## Expansion slots
- gt-kharg-cnbc_iran — CNBC/Reuters Iran crude production monthly estimates
- gt-kharg-shandong_imports — China Customs / Mysteel teapot refinery import data
- gt-kharg-iea_iran — IEA Oil Market Report Iran chapter

## Anti-patterns
- Skip: PressTV (Iranian state propaganda; not primary data)
- Skip: IRNA energy section (state agency, unverifiable)
