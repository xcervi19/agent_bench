# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_048_country_authority_TM.md  
**Fáze:** country_authority — krok TM (Turkmenistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Turkmenistan = **4. největší zásoby zemního plynu světa** (~265 tcf; Galkynysh/South
Yolotan field = 2. největší na světě). ~80 bcm/y produkce; primárně exportuje do Číny
(TAPI pipeline proposal; TAP Turkmenistan–Afghanistan–Pakistan–India stagnuje).
**Turkmengaz** = státní plynový monopol. Klíčové signály: **CNPC Galkynysh data**
(Čína operuje část pole), **Central Asia Gas Pipeline (CAGP) flows** (do Číny).
Autoritářský stát = limitovaná data transparency. 6 proposed, 1 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TM-ministry_petroleum | TM | — | ministry_petroleum | Ministry of Energy | minenergo.gov.tm | international_agency | official | policy, export_license, quota_rhetoric | unverified |
| ca-TM-noc | TM | — | noc | Turkmengaz (State Gas Concern) | turkmengaz.gov.tm | international_agency | official | production, exports, term_contract | unverified |
| ca-TM-mfa | TM | — | mfa | Ministry of Foreign Affairs | mfa.gov.tm | international_agency | official | sanctions, policy | proposed |
| ca-TM-customs_export | TM | — | customs_export | State Customs Service | customs.gov.tm | international_agency | official | exports | unverified |
| ca-TM-upstream_regulator | TM | — | upstream_regulator | Turkmennebit (State Oil Concern) | turkmennebit.gov.tm | international_agency | official | production | proposed |
| ca-TM-port_maritime_authority | TM | — | port_maritime_authority | Turkmenbashi International Seaport | turkmenbashiport.gov.tm | international_agency | official | vessel_loading, port_closure | proposed |
| ca-TM-national_exchange | TM | — | national_exchange | — (no functional commodity exchange) | — | — | — | — | empty |
| ca-TM-central_bank | TM | — | central_bank | Central Bank of Turkmenistan | cbt.gov.tm | international_agency | official | pricing_formula | proposed |
| ca-TM-environment_regulator | TM | — | environment_regulator | Ministry of Environmental Protection | mpng.gov.tm | international_agency | official | refinery_outage | proposed |
| ca-TM-coast_guard_navy | TM | — | coast_guard_navy | Turkmenistan Naval Forces (Caspian) | mod.gov.tm | international_agency | official | port_closure, force_majeure | proposed |

---

## ⚠️ Analytická poznámka: Data transparency

Turkmenistan = autoritářský stát; Serdar Berdimuhamedow; energetická data selektivně publikována.
Hlavní monitoring přes: **CNPC reports** (Galkynysh operátor), **IEA/EIA estimates**,
**ADB/WB project finance reports**, **CAGP capacity nomination data** (China).

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TM-noc (Turkmengaz) | Turkmengaz = plynový monopol; Galkynysh/South Yolotan = 2nd largest single gas field world (~26 tcf recoverable); ~80 bcm/y output; 90%+ exportuje do Číny přes CAGP (3× trubka; Lines A, B, C, D) | Turkmenistan non-aligned; odmítá Trans-Caspian gas pipeline pro EU (ruský tlak); TAPI pipeline (do Indie) = multi-decade stall | Turkmenbashi Caspian port = crude export (oil strip from Galkynysh); CAGP pipeline → China direct; no LNG infrastructure | **unverified** — turkmengaz.gov.tm ověřit |
| ca-TM-port_maritime_authority | Turkmenbashi International Seaport (Caspian) = Turkmen crude/product export hub; modernised 2018; ferry to Baku; Caspian oil exploration (Block 1/Block 21) | Trans-Caspian Pipeline (TCP) = long-discussed alternative route for Turkmen gas to Azerbaijan → Turkey → EU; Russia + Iran oppose TCP | Caspian fleet + Turkmenbashi port = limited crude export capacity; main supply = CAGP pipeline to China | **proposed** |
| ca-TM-mfa | Turkmenistan permanent neutrality (UN recognised 1995); odmítá EU gas diversification overtures; každá MFA TM prohlášení o CAGP = signal pro China gas supply security | Neutrality = no NATO, no sanctions compliance obligation; každá China-TM gas pricing renegotiation = CAGP disruption risk | TAPI pipeline diplomatic progress = rare but high-impact signal; MFA TM-Afghanistan security corridor statements | **proposed** |

### Expansion sloty
- CNPC Turkmenistan (Galkynysh operator) → cnpc.com.cn/turkmenistan
- Central Asia Gas Pipeline (CAGP) → cnpc.com.cn/cagp
- ADB Turkmenistan Energy Projects → adb.org

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 26, "last_country": "TM", "last_batch_seq": 48 }
```
