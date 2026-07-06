# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_094_geo_target_ara.md  
**Fáze:** geo_target — krok ara (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**ARA (Amsterdam-Rotterdam-Antwerp)** (`ara`, storage_pricing_hub), 12 slotů. NW Evropa **produktový
storage/pricing hub**. Klíč = **storage (Insights Global týdenní stocks)**, **pricing_hub (ARA barge
gasoil/gasoline)**. Překryv s `gt-rotterdam` → dedup. 2 `proposed`, 1 `unverified`, 9 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-ara-port_authority | ara | port_authority | — (Rotterdam via gt-rotterdam; Antwerp via ca-BE) | — | — | — | — | empty |
| gt-ara-pipeline_operator | ara | pipeline_operator | — | — | — | — | — | empty |
| gt-ara-transit_naval | ara | transit_naval | — | — | — | — | — | empty |
| gt-ara-loading_terminal | ara | loading_terminal | — (refineries via ca-NL/ca-BE) | — | — | — | — | empty |
| gt-ara-national_noc | ara | national_noc | — | — | — | — | — | empty |
| gt-ara-shipping_lane | ara | shipping_lane | — (Rhine barge; low-water logistics) | — | — | — | — | empty |
| gt-ara-customs_border | ara | customs_border | — | — | — | — | — | empty |
| gt-ara-insurance_war_risk | ara | insurance_war_risk | — | — | — | — | — | empty |
| gt-ara-storage_operator | ara | storage_operator | Insights Global weekly ARA product stocks | insights-global.com | infrastructure | data_feed | storage_levels | proposed |
| gt-ara-pricing_hub | ara | pricing_hub | ARA barge gasoil/gasoline (Platts/ICE Gasoil) | — | industry_body | data_feed | pricing_formula | unverified |
| gt-ara-weather_hazard | ara | weather_hazard | — (Rhine low-water restricts barges) | — | — | — | — | empty |
| gt-ara-sanctions_enforcement | ara | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-ara-storage_operator | **Insights Global týdenní produkty** | — | NW Europe barometr | proposed — klíčový EU feed |
| gt-ara-pricing_hub | gasoil/gasoline benchmark | — | ARA barge | unverified |

### Unverified / Anti-patterns

- **Vysoký překryv s `gt-rotterdam`** → záměrně jen ne-duplicitní storage/pricing vrstva; port/refinerie pod ca-NL/ca-BE/gt-rotterdam.
- Insights Global (PJK) = stejný feed jako u Rotterdam — konsolidace při whitelist merge.
- Rhine low-water (sucho) → barge omezení = produktový arb signál.

### Progress po merge

`phase: geo_target`, `last_geo_target: ara`, `last_batch_seq: 94`
