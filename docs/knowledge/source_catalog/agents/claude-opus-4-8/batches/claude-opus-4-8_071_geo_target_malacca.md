# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_071_geo_target_malacca.md  
**Fáze:** geo_target — krok malacca (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Strait of Malacca** (`malacca`, chokepoint), 12 slotů. Objemově **nejvytíženější ropný chokepoint**
(ME→Čína/Japonsko/Korea). Klíč = **shipping_lane (MPA Singapore + ReCAAP piracy)**, **transit_naval
(littoral patrols)**, **insurance (JWC piracy)**. Alternativy (Sunda/Lombok) = dny navíc. 3 `proposed`, 1 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-malacca-port_authority | malacca | port_authority | — (Singapore MPA via ca-SG) | — | — | — | — | empty |
| gt-malacca-pipeline_operator | malacca | pipeline_operator | — | — | — | — | — | empty |
| gt-malacca-transit_naval | malacca | transit_naval | Malacca Strait Patrol (littoral: MY/ID/SG/TH) | — | diplomacy | official | port_closure | unverified |
| gt-malacca-loading_terminal | malacca | loading_terminal | — | — | — | — | — | empty |
| gt-malacca-national_noc | malacca | national_noc | — | — | — | — | — | empty |
| gt-malacca-shipping_lane | malacca | shipping_lane | ReCAAP ISC (piracy) + MPA Singapore | recaap.org | shipping | official | force_majeure | proposed |
| gt-malacca-customs_border | malacca | customs_border | — | — | — | — | — | empty |
| gt-malacca-insurance_war_risk | malacca | insurance_war_risk | Lloyd's Joint War Committee (piracy zones) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-malacca-storage_operator | malacca | storage_operator | — (Singapore storage via ca-SG) | — | — | — | — | empty |
| gt-malacca-pricing_hub | malacca | pricing_hub | — (Singapore Platts MOC via ca-SG) | — | — | — | — | empty |
| gt-malacca-weather_hazard | malacca | weather_hazard | — (haze/monsoon — minor) | — | — | — | — | empty |
| gt-malacca-sanctions_enforcement | malacca | sanctions_enforcement | — (STS transfers offshore — via OFAC global) | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-malacca-shipping_lane (ReCAAP) | ~nejvyšší objem ropy | pirátství/ozbrojené loupeže | MPA VTS | proposed |
| gt-malacca-transit_naval | ME crude do V. Asie | littoral suverenita (MY/ID/SG) | Sunda/Lombok = dny navíc | unverified |

### Unverified / Anti-patterns

- **Malacca Strait Patrol** nemá centrální web → unverified; monitorovat přes ReCAAP + národní navy.
- port/storage/pricing `empty`: pokryto `ca-SG` (Singapur) — bez duplicity.
- Malacca = spíš objemový/pirátský než uzavírací risk (na rozdíl od Hormuz).

### Progress po merge

`phase: geo_target`, `last_geo_target: malacca`, `last_batch_seq: 71` — chokepointy 5/7 (zbývá Bospor, Gibraltar)
