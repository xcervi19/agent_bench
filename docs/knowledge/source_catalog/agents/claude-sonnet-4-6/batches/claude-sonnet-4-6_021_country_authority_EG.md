# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_021_country_authority_EG.md  
**Fáze:** country_authority — krok EG (Egypt)  
**Datum:** 2026-07-05  

---

## Shrnutí

Egypt = strategicky klíčový: (1) **Suez Canal** (geo-suez slot, ale EG country-authority
řeší SCA na státní úrovni), (2) **Zohr gas field** (ENI operated; transformoval EG z
importéra na exportéra plynu), (3) **ELNG/SEGAS LNG terminály** (Idku a Damietta),
(4) **EGPC crude production** (~600 kb/d klesající). Klíčové také pro tranzitní roli
(SUMED pipeline z Rudého moře na Středomoří). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-EG-ministry_petroleum | EG | — | ministry_petroleum | Ministry of Petroleum and Mineral Resources | petroleum.gov.eg | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-EG-noc | EG | — | noc | EGPC – Egyptian General Petroleum Corporation | egpc.gov.eg | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-EG-mfa | EG | — | mfa | Ministry of Foreign Affairs | mfa.gov.eg | international_agency | official | sanctions, policy | proposed |
| ca-EG-customs_export | EG | — | customs_export | Egyptian Customs Authority | customs.gov.eg | international_agency | official | exports, export_license | proposed |
| ca-EG-upstream_regulator | EG | — | upstream_regulator | Ministry of Petroleum (dual role — upstream licensing) | petroleum.gov.eg | international_agency | official | production, refinery_outage | proposed |
| ca-EG-port_maritime_authority | EG | — | port_maritime_authority | Egyptian Ports Authority (under Ministry of Transport) | mts.gov.eg | international_agency | official | vessel_loading, port_closure | proposed |
| ca-EG-national_exchange | EG | — | national_exchange | EGX – Egyptian Exchange | egx.com.eg | exchange | official | pricing_formula | proposed |
| ca-EG-central_bank | EG | — | central_bank | CBE – Central Bank of Egypt | cbe.org.eg | international_agency | official | sanctions | proposed |
| ca-EG-environment_regulator | EG | — | environment_regulator | EEAA – Egyptian Environmental Affairs Agency | eeaa.gov.eg | international_agency | official | refinery_outage | proposed |
| ca-EG-coast_guard_navy | EG | — | coast_guard_navy | Egyptian Navy | navy.mod.gov.eg | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-EG-noc (EGPC) | EGPC řídí domácí produkci (~600 kb/d crude) + joint ventures s ENI, BP, Chevron; klíčový je Zohr gas (ENI operated; 2.7 bcf/d) → LNG export signal | EGPC je pod Ministry of Petroleum; každé EGPC vedlejší oznámení o gas export/domestic allocation balance je price-moving pro ELNG loading schedule | Ain Sokhna terminal (Rudé moře crude import/export); SUMED pipeline (Ain Sokhna→Alexandria 120 mb/d) | **proposed** — egpc.gov.eg: ověřit přesnou doménu; alternativně egpc.com.eg |
| ca-EG-port_maritime_authority | Ministry of Transport spravuje Egyptian Ports Authority; Ain Sokhna a Adabiya (Red Sea) jsou klíčové pro crude/products | SCA (Suez Canal Authority) = geo-suez slot, ale EG MoT koordinuje přístupy k Red Sea a Mediterranean terminals | SUMED pipeline přepravuje crude z Ain Sokhna do Sidi Kerir (Alexandra) pro middle-barrel traders | **proposed** — mts.gov.eg je Ministry of Transport; EPA (Egyptian Ports Authority) pod MoT |
| ca-EG-coast_guard_navy | Egyptian Navy hlídá přístupy k Suez Canal, Sinai, Red Sea | Egypt jako Suez-guardian = klíčový geopolitický aktér; Red Sea security post-Houthi (2023+) | Suez Canal closure = tier-1 global supply shock (80 mb transiting/month) | **unverified** — navy.mod.gov.eg: ověřit správnou sub-URL egyptského námořnictva |

### Analytická poznámka: Suez + SUMED
Egypt kontroluje dvě tranzitní tepny: (1) Suez Canal (geo-suez-port_authority slot) a
(2) SUMED pipeline. Monitorování přes SCA (suezcanal.gov.eg, přidán v geo-suez slot)
je tier-1 nad EGPC country slot.

### Expansion sloty
- SCA – Suez Canal Authority → suezcanal.gov.eg (hlavně v geo-suez slot)
- EGAS – Egyptian Natural Gas Holding Company → egas.com.eg (gas upstream/LNG)
- ELNG (Idku LNG) → egyptlng.com (Shell/BG/EGPC JV)
- SEGAS (Damietta LNG) → segas.com.eg

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 20, "last_country": "EG", "last_batch_seq": 21 }
```
