# Catalog batch — composer-2-5_087_geo_target_freeport.md | freeport | 21/32 | 2026-07-06

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-freeport-port_authority | US | freeport | port_authority | Port Freeport | portfreeport.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-freeport-pipeline_operator | US | freeport | pipeline_operator | Freeport LNG feedgas | freeportlng.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-freeport-transit_naval | US | freeport | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-freeport-loading_terminal | US | freeport | loading_terminal | Freeport LNG | freeportlng.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-freeport-national_noc | — | freeport | national_noc | (LNG export — no NOC) | — | noc | — | exports | empty |
| geo-freeport-shipping_lane | US | freeport | shipping_lane | Port Freeport channel traffic | portfreeport.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-freeport-customs_border | US | freeport | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-freeport-insurance_war_risk | US | freeport | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-freeport-storage_operator | — | freeport | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-freeport-pricing_hub | US | freeport | pricing_hub | CME Group (Henry Hub / LNG linkage) | cmegroup.com | exchange | official | pricing_formula,exports | unverified |
| geo-freeport-weather_hazard | US | freeport | weather_hazard | NOAA / NWS (Gulf hurricanes) | weather.gov | weather | official | port_closure,hurricane,force_majeure | proposed |
| geo-freeport-sanctions_enforcement | US | freeport | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

**Tier 1:** freeportlng.com + portfreeport.com. June 2022 explosion outage precedent.

**Progress:** `last_batch_seq: 87`. **Další:** corpus_christi (22/32).
