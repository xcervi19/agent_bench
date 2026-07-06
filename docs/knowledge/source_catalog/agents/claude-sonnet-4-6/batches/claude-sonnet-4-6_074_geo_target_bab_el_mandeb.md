# Batch 074 — Geo Target: Bab el-Mandeb

## Geo significance
**Bab el-Mandeb** ("Gate of Grief") is the southern Red Sea chokepoint between Yemen and Djibouti/Eritrea — ~4.8 mb/d crude + products transit (northbound Europe-Asia, southbound LNG). Since late 2023, **Houthi (Ansar Allah)** missile, drone, and drone-boat attacks have diverted >60% of container shipping and significant tanker traffic around the **Cape of Good Hope**, adding ~10–14 days and $500k–$1m per voyage. US/UK Operation Prosperity Guardian + EU ASPIDES conduct escort operations. Key monitoring: UKMTO (covers Red Sea/BaM zone), Combined Maritime Forces (CMF), Yemen MFA signals, Djibouti port authority, Eritrea coast.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-babelmandeb-ukmto | — | bab_el_mandeb | chokepoint | UKMTO – UK Maritime Trade Operations (Red Sea desk) | ukmto.org | shipping | official | port_closure, force_majeure, vessel_loading | proposed |
| gt-babelmandeb-cmf | — | bab_el_mandeb | chokepoint | Combined Maritime Forces (CMF) – CTF-151 | combinedmaritimeforces.com | international_agency | official | force_majeure, port_closure | proposed |
| gt-babelmandeb-houthi | YE | bab_el_mandeb | chokepoint | Ansar Allah (Houthi) military spokesman | ansarallah.com | international_agency | official | force_majeure, port_closure | unverified |
| gt-babelmandeb-djibouti_port | DJ | bab_el_mandeb | chokepoint | Port de Djibouti (DPFZA) | dpfza.dj | international_agency | official | vessel_loading, port_closure | proposed |
| gt-babelmandeb-eu_aspides | — | bab_el_mandeb | chokepoint | EU Operation ASPIDES | euperspectives.eu | international_agency | official | force_majeure, port_closure | proposed |
| gt-babelmandeb-lloyds_war | — | bab_el_mandeb | chokepoint | Lloyd's JWRSG – Red Sea war risk premium | lloydsmarket.com | shipping | official | force_majeure | proposed |
| gt-babelmandeb-marinetraffic | — | bab_el_mandeb | chokepoint | MarineTraffic AIS — Bab el-Mandeb/Red Sea feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-babelmandeb-imb | — | bab_el_mandeb | chokepoint | IMB Piracy Reporting Centre (Red Sea alerts) | icc-ccs.org | shipping | official | force_majeure, port_closure | proposed |
| gt-babelmandeb-suez_canal_auth | EG | bab_el_mandeb | chokepoint | Suez Canal Authority (upstream transit impact) | suezcanal.gov.eg | international_agency | official | vessel_loading, exports | proposed |
| gt-babelmandeb-ambrey | — | bab_el_mandeb | chokepoint | Ambrey Maritime Intelligence | ambrey.com | shipping | official | force_majeure, port_closure | proposed |

## Cross-check (key entries)

### gt-babelmandeb-houthi (Ansar Allah)
- **Supply:** Houthi missile/drone attacks on tankers = immediate Red Sea diversion; Suez Canal transit drop 40–50% (2024); LNG diversion = Asian spot price spike; Bab el-Mandeb closure threat = Cape diversion premium
- **Geopolitics:** Iran proxy (IRGCN weapons supply); Gaza war trigger; US-UK retaliatory strikes = escalation ladder; Yemen ceasefire = diversion normalization signal
- **Logistics:** Cape of Good Hope rerouting +14 days; Suez Canal revenue collapse ($800m/day → $100m/day); tanker war risk insurance +0.5–1.5% hull value per transit

### gt-babelmandeb-ambrey (Ambrey)
- **Supply:** Ambrey provides real-time ship attack advisories; vessel risk ratings; Red Sea corridor vessel tracking
- **Geopolitics:** Premium intelligence service used by ship operators; tracks drone attack patterns; coordinates with CMF + UKMTO
- **Logistics:** Vessel diversion recommendations; convoy coordination; incident database

## Expansion slots
- gt-babelmandeb-dryad_global — Dryad Global maritime security (Red Sea alerts)
- gt-babelmandeb-kpler_red_sea — Kpler Red Sea throughput analytics
- gt-babelmandeb-bimco_red_sea — BIMCO Red Sea circular advisories

## Anti-patterns
- Skip: Yemen data aggregators (secondary; unreliable in conflict zone)
- Skip: Al-Masirah TV (Houthi propaganda; use official Ansar Allah statements only)
