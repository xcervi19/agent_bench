# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_052_country_authority_YE.md  
**Fáze:** country_authority — krok YE (Yemen)  
**Datum:** 2026-07-06  

---

## Shrnutí

Yemen = **Bab el-Mandeb chokepoint stát** (Houthi kontrola od 2023 = globální shipping
krizis). Pre-war produkce ~130 kb/d (nyní ~0 z HNC kontrolovaných oblastí); Marib gas
field (JV s TotalEnergies, offline 2015+). Klíčové signály: **Houthi Red Sea útoky**
(každý = okamžitý freight rate spike; insurance surcharge), **Lloyd's Joint War Committee**
listings, **Bab el-Mandeb traffic monitoring** (AIS diversion around Cape of Good Hope).
Většina zdrojů unverified — split government (IRG/Riyadh vs. Houthi/Sana'a). 5 proposed, 2 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-YE-ministry_petroleum | YE | — | ministry_petroleum | Ministry of Oil and Minerals (IRG, Aden) | mom.gov.ye | international_agency | official | policy, export_license | unverified |
| ca-YE-noc | YE | — | noc | YPIC – Yemen Petroleum Industries Corporation | — | — | — | — | empty |
| ca-YE-mfa | YE | — | mfa | Ministry of Foreign Affairs (IRG, Aden) | mofa.gov.ye | international_agency | official | sanctions, policy | proposed |
| ca-YE-customs_export | YE | — | customs_export | Customs Authority (IRG) | customs.gov.ye | international_agency | official | imports | unverified |
| ca-YE-upstream_regulator | YE | — | upstream_regulator | Yemen Petroleum Company (YPC) | ypc.com.ye | international_agency | official | production | unverified |
| ca-YE-port_maritime_authority | YE | — | port_maritime_authority | Aden Port Authority | adenport.gov.ye | international_agency | official | vessel_loading, port_closure | proposed |
| ca-YE-national_exchange | YE | — | national_exchange | — (no functional exchange) | — | — | — | — | empty |
| ca-YE-central_bank | YE | — | central_bank | Central Bank of Yemen (Aden branch) | centralbank.gov.ye | international_agency | official | sanctions | proposed |
| ca-YE-environment_regulator | YE | — | environment_regulator | — (non-functional wartime) | — | — | — | — | empty |
| ca-YE-coast_guard_navy | YE | — | coast_guard_navy | Houthi Naval Forces (de-facto Red Sea) | — | — | — | — | proposed |

---

## ⚠️ Analytická poznámka: Yemen monitoring strategy

**Yemen = monitoring přes third-party, ne official domains:**
- **Houthi attacks tracking**: UKMTO (United Kingdom Maritime Trade Operations) → ukmto.org = tier-1
- **Lloyd's JWC** → jcw.lloyds.com (war risk listings; Bab el-Mandeb zone)
- **CENTCOM** → centcom.mil (US interdiction ops; Operation Prosperity Guardian)
- **Ambrey (UK maritime security)** → ambrey.com (real-time Red Sea incidents)
- **BIMCO** → bimco.org (shipping industry advisories)

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-YE-port_maritime_authority (Aden) | Aden port = IRG (pro-Saudi) controlled; fuel import hub for IRG areas; Aden oil refinery (offline); Houthi missiles target Aden port periodically | IRG vs. Houthi split government; každý Aden port closure = Southern Yemen supply disruption | Hodeidah port (Houthi controlled) = primary Houthi import/export; UN Yemen Humanitarian Operations | **proposed** |
| ca-YE-coast_guard_navy (Houthi) | Houthi naval forces = de-facto Red Sea threat actor; drone boats + missiles; targeting commercial tankers + LNG carriers + container ships | **TIER-1 geo-threat**: Houthi attacks since October 2023 = global freight diversion around Cape of Good Hope; Bab el-Mandeb transit rates; každý Houthi attack = Brent +$1-3 immediate | Bab el-Mandeb (27 km width; ~5 mb/d crude pre-2024 → significantly reduced); Cape of Good Hope route +10-14 days voyage | **proposed** (no official domain; monitor via UKMTO, Ambrey, CENTCOM) |
| ca-YE-mfa | IRG MFA (Aden) prohlášení = Saudi-aligned; každá ceasefire/peace process signal | Yemen peace process (UN envoy, Saudi-Houthi talks 2023-2024); každý peace progress = Bab el-Mandeb normalisation signal = freight rate normalisation | UN Yemen humanitarian corridor; WFP food shipments via Hodeidah | **proposed** |

### Primary monitoring domains (non-official)
- UKMTO → ukmto.org (tier-1 Red Sea/Bab el-Mandeb incident reporting)
- Ambrey → ambrey.com (commercial maritime security; Red Sea incidents)
- Lloyd's JWC → lloyds.com/jwc (war risk premium changes)
- IMB Piracy Centre → icc-ccs.org (piracy + armed robbery reports)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 38, "last_country": "YE", "last_batch_seq": 52 }
```
