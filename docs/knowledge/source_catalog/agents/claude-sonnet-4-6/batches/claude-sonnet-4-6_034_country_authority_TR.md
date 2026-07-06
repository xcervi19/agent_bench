# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_034_country_authority_TR.md  
**Fáze:** country_authority — krok TR (Turkey)  
**Datum:** 2026-07-06  

---

## Shrnutí

Turkey = **geo-klíčový tranzitní stát**: Bosphorus + Dardanelles (Turkish Straits)
= jediný přístup z Černého moře pro ruský Novorossiysk a Kazakh CPC export; Ceyhan port
= BTC pipeline (Kazakh + Azerbaijani crude, ~1.2 mb/d). Turecko nakupuje Ruský diskontní
plyn i ropu a zároveň se hlásí k NATO. Klíčové signály: **BOTAŞ (státní plyn)**,
**TPAO (státní těžba)**, **Turkish Straits transit data** (IMO/MCA monthly),
**Ceyhan terminal loadings** (BOTAS pipeline + Türkiye Denizcilik). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TR-ministry_petroleum | TR | — | ministry_petroleum | Ministry of Energy and Natural Resources | enerji.gov.tr | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-TR-noc | TR | — | noc | TPAO – Turkish Petroleum Corporation | tpao.gov.tr | international_agency | official | production, term_contract, force_majeure | proposed |
| ca-TR-mfa | TR | — | mfa | Ministry of Foreign Affairs | mfa.gov.tr | international_agency | official | sanctions, policy | proposed |
| ca-TR-customs_export | TR | — | customs_export | Turkish Customs Administration | gumruk.gov.tr | international_agency | official | imports, exports | proposed |
| ca-TR-upstream_regulator | TR | — | upstream_regulator | EPDK – Energy Market Regulatory Authority | epdk.gov.tr | international_agency | official | production, refinery_outage | proposed |
| ca-TR-port_maritime_authority | TR | — | port_maritime_authority | UDH – Ministry of Transport and Infrastructure | udhb.gov.tr | international_agency | official | vessel_loading, port_closure | proposed |
| ca-TR-national_exchange | TR | — | national_exchange | BIST – Borsa Istanbul | borsaistanbul.com | exchange | official | pricing_formula | proposed |
| ca-TR-central_bank | TR | — | central_bank | TCMB – Central Bank of the Republic of Turkey | tcmb.gov.tr | international_agency | official | pricing_formula, sanctions | proposed |
| ca-TR-environment_regulator | TR | — | environment_regulator | Ministry of Environment, Urbanisation and Climate Change | csb.gov.tr | international_agency | official | refinery_outage | proposed |
| ca-TR-coast_guard_navy | TR | — | coast_guard_navy | Turkish Navy (Deniz Kuvvetleri) | dzkk.tsk.tr | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TR-port_maritime_authority (Turkish Straits) | **Turkish Straits (Bosphorus + Dardanelles)** = primární Černomořský export chokepoint; CPC pipeline Novorossiysk + Russian VLCC loadings musí projít Tureckem; Turkey využívá Montreux Convention (1936) k omezení non-Black Sea warship transit | Post-2022: Turkey dočasně omezila tanker transit kvůli insurance certificates (Lloyds War Risk); každé Turkish Straits delay announcement = supply signal pro Mediterranean crude; TankerTrackers Bosphorus monitoring tier-1 | Ceyhan BTC terminal (~1.2 mb/d, Azerbaijani + Kazakh crude); BOTAS Kirikkale, Izmit refineries crude supply | **proposed** — udhb.gov.tr aktivní; Turkish Straits transit = tier-1 geo-btc slot |
| ca-TR-mfa | Turkey jako "mediátor": Erdoğan leverages Russian energy (TürkAkım gas pipeline, discounted Russian crude and gas); každé Turkey-Russia energy deal = signal pro European gas alternative supply | Turkey NATO člen ale nerespektuje Russia sanctions fully; každý Turkey MFA statement o Ukrainian shipping insurance = Bosphorus transit signal | TürkAkım pipeline (2× 15.75 bcf/d; přes Turecko do SE Europe) = European gas supply chokepoint | **proposed** |
| ca-TR-noc (TPAO) | TPAO = upstream; Türkiye domestic production ~70 kb/d (Kuzey Irak, Thrace Basin); TPAO participates in Azerbaijani ACG JV (Shah Deniz); Sakarya gas field (Black Sea, 2023+) | TPAO = state; Sakarya offshore = major potential domestic gas supply (reducing import dependency) | TPAO logistics: Black Sea offshore + Kuzey Irak pipelines | **proposed** — tpao.gov.tr aktivní |

### Analytická poznámka: Turkish Straits monitoring
- Bosphorus a Dardanelles = **geo-btc-area slot** (Turkish Straits v geo_target dimension)
- Každý Turkish coast guard "safety inspection" delay = intentional Bosphorus chokepoint event
- Expansion: BOTAS → botas.gov.tr (state gas pipeline; TürkAkım + TANAP interconnect)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 33, "last_country": "TR", "last_batch_seq": 34 }
```
