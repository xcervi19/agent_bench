# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_022_country_authority_CN.md  
**Fáze:** country_authority — krok CN (China)  
**Datum:** 2026-07-05  

---

## Shrnutí

China = primárně největší světový importér ropy (10–11 mb/d); producent ~4.2 mb/d.
Klíčové signály: **GACC monthly import data** (čínské celní statistiky = tier-1 globální
demand signal — každý release pohybuje trhem), **NEA/NDRC fuel pricing** (domestic
retail price adjustments → refinery margins), **INE crude futures** (Shanghai benchmark,
już v globální vrstvě), **CNPC/Sinopec/CNOOC quarterly**. Specifický fokus: "teapot"
rafinerie Shandong (proxy pro spot demand), SPR drawing/filling (opaque).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CN-ministry_petroleum | CN | — | ministry_petroleum | NEA – National Energy Administration | nea.gov.cn | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-CN-noc | CN | — | noc | CNPC – China National Petroleum Corporation | cnpc.com.cn | international_agency | official | production, imports, term_contract, pricing_formula | proposed |
| ca-CN-mfa | CN | — | mfa | Ministry of Foreign Affairs | mfa.gov.cn | international_agency | official | sanctions, policy | proposed |
| ca-CN-customs_export | CN | — | customs_export | GACC – General Administration of Customs China | customs.gov.cn | international_agency | official | imports, exports | proposed |
| ca-CN-upstream_regulator | CN | — | upstream_regulator | MNR – Ministry of Natural Resources | mnr.gov.cn | international_agency | official | production, refinery_outage | proposed |
| ca-CN-port_maritime_authority | CN | — | port_maritime_authority | MSA – Maritime Safety Administration | msa.gov.cn | international_agency | official | vessel_loading, port_closure | proposed |
| ca-CN-national_exchange | CN | — | national_exchange | Shanghai INE – International Energy Exchange | ine.cn | exchange | official | pricing_formula, term_contract | proposed |
| ca-CN-central_bank | CN | — | central_bank | PBOC – People's Bank of China | pbc.gov.cn | international_agency | official | pricing_formula, sanctions | proposed |
| ca-CN-environment_regulator | CN | — | environment_regulator | MEE – Ministry of Ecology and Environment | mee.gov.cn | international_agency | official | refinery_outage | proposed |
| ca-CN-coast_guard_navy | CN | — | coast_guard_navy | China Coast Guard (CCG) | ccg.gov.cn | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CN-customs_export (GACC) | GACC měsíční import data (crude oil volumes po zemích): tier-1 globální demand signal; každý release = pohyb Brent/WTI; čínský crude import data jsou nejdůležitější single monthly dataset pro globální demand tracking | GACC data zobrazují, kdo do Číny dodává crude pod sankcemi (Írán, Venezuela, Rusko) — geopolitický treasure trove | Tanker discharges do Qingdao, Rizhao, Tianjin, Ningbo, Zhoushan | **proposed** — customs.gov.cn aktivní; měsíční data release ca. 10. dne měsíce |
| ca-CN-noc (CNPC) | CNPC = 3.2 mb/d čínská produkce (Daqing, Tarim, Xinjiang); plus zahraniční produkce (Irák, Kazachstán, Súdán, Rusko); quarterly reports | CNPC je státní; geopoliticky pojený se zahraničními E&P aktivitami v sankcionovaných zemích (Írán, Venezuela, Rusko) | CNPC řídí část ropy do Shandong rafinérií; PipeChina (pipeline separace) | **proposed** — cnpc.com.cn aktivní |
| ca-CN-ministry_petroleum (NEA) | NEA pod NDRC nastavuje rafinérní kvóty, LNG import approval, ropy strategic reserve policy | NEA/NDRC fuel price adjustment mechanism: každá NDRC cenová úprava ovlivňuje domestic margin a tím import poptávku | NEA schvaluje nové LNG terminály, rafinérské licence; SPR fill/draw guidance | **proposed** — nea.gov.cn aktivní |
| ca-CN-coast_guard_navy (CCG) | Primárně South China Sea patrol; omezený přímý supply signal | CCG konfrontace v SCS (Filipíny, Vietnam) = South China Sea risk premium; Taiwan Strait incidents | Malacca approach; South China Sea tanker corridor; Zhoushan/Ningbo VLCC přístupy | **unverified** — ccg.gov.cn: ověřit zda CCG má vlastní doménu nebo je pod Ministry of Public Security/Coast Guard Bureau |

### Analytická poznámka: China monitoring framework
Nejdůležitější čínské primární zdroje pro crude desk:
1. **GACC** (customs.gov.cn) — monthly crude import volumes; tier-1
2. **NBS** (stats.gov.cn) — National Bureau of Statistics; industrial output; refinery throughput
3. **NEA** (nea.gov.cn) — fuel pricing adjustments; SPR guidance
4. INE futures data (ine.cn, již v gl-exchange-004)

### Expansion sloty
- NBS – National Bureau of Statistics → stats.gov.cn (refinery throughput = tier-1 demand signal)
- Sinopec → sinopec.com (2nd largest crude processor; teapot analog)
- CNOOC → cnooc.com.cn (offshore China; LNG import arm CNOOC Gas & Power)
- PipeChina → pipelinechina.com.cn (pipeline operator; cross-country crude flows)
- Shandong Independent Refinery Association (teapot) → expansion signal cluster

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 21, "last_country": "CN", "last_batch_seq": 22 }
```
