# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_095_geo_target_saldanha.md  
**Fáze:** geo_target — krok saldanha (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Saldanha Bay** (`saldanha`, storage_pricing_hub), 12 slotů. JAR **crude storage hub (VLCC)** na
**Cape route** — relevance ↑ při **přesměrování z Rudého moře**. Klíč = **storage_operator**,
**shipping_lane (Cape waypoint)**. 1 `proposed`, 3 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-saldanha-port_authority | saldanha | port_authority | Transnet National Ports Authority (Saldanha) | transnet.net | infrastructure | official | port_closure | unverified |
| gt-saldanha-pipeline_operator | saldanha | pipeline_operator | — | — | — | — | — | empty |
| gt-saldanha-transit_naval | saldanha | transit_naval | — | — | — | — | — | empty |
| gt-saldanha-loading_terminal | saldanha | loading_terminal | — | — | — | — | — | empty |
| gt-saldanha-national_noc | saldanha | national_noc | — (SFF strategic stocks) | — | — | — | — | empty |
| gt-saldanha-shipping_lane | saldanha | shipping_lane | Cape route waypoint (Red Sea diversion traffic) | — | shipping | data_feed | vessel_loading | proposed |
| gt-saldanha-customs_border | saldanha | customs_border | — | — | — | — | — | empty |
| gt-saldanha-insurance_war_risk | saldanha | insurance_war_risk | — | — | — | — | — | empty |
| gt-saldanha-storage_operator | saldanha | storage_operator | Saldanha crude storage (MOGS/Oiltanking) + SFF | — | infrastructure | official | storage_levels | unverified |
| gt-saldanha-pricing_hub | saldanha | pricing_hub | — | — | — | — | — | empty |
| gt-saldanha-weather_hazard | saldanha | weather_hazard | — | — | — | — | — | empty |
| gt-saldanha-sanctions_enforcement | saldanha | sanctions_enforcement | — (Iranian crude storage controversy) | — | — | — | — | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-saldanha-storage_operator | VLCC crude storage | JAR strategické zásoby (SFF spor) | Cape route kotva | unverified |
| gt-saldanha-shipping_lane | — | **Rudé moře přesměrování → víc Cape traffic** | waypoint | proposed |

### Unverified / Anti-patterns

- Domény (Transnet/MOGS/Oiltanking) unverified — ověřit.
- Relevance roste s Bab el-Mandeb disruption (propojit s `gt-bab_el_mandeb`).
- SFF (Strategic Fuel Fund) prodej zásob 2015 = precedent (transparentnost spor).

### Progress po merge

`phase: geo_target`, `last_geo_target: saldanha`, `last_batch_seq: 95` — storage/pricing KOMPLETNÍ (3/3)
