# Catalog batch — composer-2-5_092_geo_target_cove_point.md | cove_point | 26/32 | 2026-07-06

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-cove_point-port_authority | US | cove_point | port_authority | Maryland Port Administration | maryland.gov | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-cove_point-pipeline_operator | US | cove_point | pipeline_operator | Dominion Energy Cove Point feedgas | dominionenergy.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-cove_point-transit_naval | US | cove_point | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-cove_point-loading_terminal | US | cove_point | loading_terminal | Cove Point LNG (Dominion Energy) | dominionenergy.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-cove_point-national_noc | — | cove_point | national_noc | (LNG export — no NOC) | — | noc | — | exports | empty |
| geo-cove_point-shipping_lane | US | cove_point | shipping_lane | Chesapeake Bay LNG transit | dominionenergy.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-cove_point-customs_border | US | cove_point | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-cove_point-insurance_war_risk | US | cove_point | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-cove_point-storage_operator | — | cove_point | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-cove_point-pricing_hub | US | cove_point | pricing_hub | CME Group (Henry Hub / LNG linkage) | cmegroup.com | exchange | official | pricing_formula,exports | unverified |
| geo-cove_point-weather_hazard | US | cove_point | weather_hazard | NOAA / NWS (Atlantic storms) | weather.gov | weather | official | port_closure,hurricane | proposed |
| geo-cove_point-sanctions_enforcement | US | cove_point | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

**Tier 1:** dominionenergy.com + ferc.gov. East Coast US LNG export — Atlantic basin supply.

**Progress:** `last_batch_seq: 92`. **Další:** cushing (27/32).
