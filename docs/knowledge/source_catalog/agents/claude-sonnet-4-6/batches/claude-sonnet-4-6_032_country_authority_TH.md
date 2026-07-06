# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_032_country_authority_TH.md  
**Fáze:** country_authority — krok TH (Thailand)  
**Datum:** 2026-07-06  

---

## Shrnutí

Thailand = ~500 kb/d domestická produkce (Gulf of Thailand gas/condensate; klesající)
+ crude importer ~1 mb/d. **PTT PCL = plně integrovaný státní energetický konglomerát**
(pipeline + upstream via PTTEP + downstream via PTTGC); analogie s PETRONAS v menším
měřítku. Klíčové signály: **PTT natural gas grid** (dominuje domácí distribuci),
**Rayong rafinérie complex** (Thai Oil, IRPC, Star Petroleum → sumárně ~500 kb/d),
**PTTEP production** (SEA upstream: Gulf of Thailand, MTJDA s Malajsií). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TH-ministry_petroleum | TH | — | ministry_petroleum | Ministry of Energy | energy.go.th | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-TH-noc | TH | — | noc | PTT PCL | pttplc.com | international_agency | official | production, imports, force_majeure, term_contract, pricing_formula | proposed |
| ca-TH-mfa | TH | — | mfa | Ministry of Foreign Affairs | mfa.go.th | international_agency | official | sanctions, policy | proposed |
| ca-TH-customs_export | TH | — | customs_export | Thai Customs Department | customs.go.th | international_agency | official | imports, exports | proposed |
| ca-TH-upstream_regulator | TH | — | upstream_regulator | DMF – Department of Mineral Fuels | dmf.go.th | international_agency | official | production, force_majeure | proposed |
| ca-TH-port_maritime_authority | TH | — | port_maritime_authority | Marine Department | md.go.th | international_agency | official | vessel_loading, port_closure | proposed |
| ca-TH-national_exchange | TH | — | national_exchange | SET – Stock Exchange of Thailand | set.or.th | exchange | official | pricing_formula | proposed |
| ca-TH-central_bank | TH | — | central_bank | BOT – Bank of Thailand | bot.or.th | international_agency | official | pricing_formula, sanctions | proposed |
| ca-TH-environment_regulator | TH | — | environment_regulator | ONEP – Office of Natural Resources and Environmental Policy and Planning | onep.go.th | international_agency | official | refinery_outage | proposed |
| ca-TH-coast_guard_navy | TH | — | coast_guard_navy | Royal Thai Navy | navy.mi.th | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TH-noc (PTT PCL) | PTT PCL = holding; PTTEP (upstream E&P; ~450 kboed production); PTT Natural Gas Distribution; PTTGC (petrochemical); Thai Oil (refining ~275 kb/d Sriracha); IRPC, Star Petroleum | PTT = state ~51%; SET-listed; každý PTT guidance = Thai energy policy signal; MTJDA (Malaysia–Thailand Joint Development Area) → coordination s PETRONAS | Rayong seaport (Map Ta Phut Industrial Port) = Thai crude import hub; FSRU Rayong pro LNG import; Pipeline network Bangkok | **proposed** — pttplc.com aktivní |
| ca-TH-upstream_regulator (DMF) | DMF = Concession/PSC issuing body; Gulf of Thailand gas blocks (G1/61, B8/32, G4/43); MTJDA (JDA-B17 block) cross-border | DMF data: remaining reserves in Gulf of Thailand declining; Carigali-Triton (PETRONAS JV) vs PTT | DMF production statistics = monthly Thai gas production signal (replacing declining fields) | **proposed** — dmf.go.th aktivní |
| ca-TH-coast_guard_navy (RTN) | Royal Thai Navy = Gulf of Thailand patrol; Kra Canal advocacy (alternative to Malacca = geopolitical megaproject signal) | Kra Canal = 20-year recurring geo-project: Thai/Chinese periodically revive; any serious Kra discussion = Malacca bypass signal | Gulf of Thailand naval patrol; HTMS Chakri Naruebet carrier group | **unverified** — navy.mi.th ověřit; může být navy.go.th nebo rtna.thaigov.go.th |

### Analytická poznámka: Kra Canal
- Kra Isthmus Canal (10 km shortest southern Thailand) = recurring proposal (1677+)
- Každý Thailand–China feasibility discussion = significant geo-logistics signal pro Malacca
- Pro monitoring: FollowThai parliament statements + Chinese MFA briefings on Kra

### Expansion sloty
- PTTEP → pttep.com (upstream E&P; tier-1 Southeast Asian production)
- Thai Oil → thaioilgroup.com (Sriracha refinery ~275 kb/d; SET-listed)
- Map Ta Phut Port → mtpport.com (Rayong crude import terminal)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 31, "last_country": "TH", "last_batch_seq": 32 }
```
