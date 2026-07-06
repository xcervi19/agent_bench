# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_033_country_authority_PK.md  
**Fáze:** country_authority — krok PK (Pakistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Pakistan = klíčový pro **Hormuz downstream signalling** (Karachi přístav = primární
crude import hub pro jižní Asii po Indii). Produkce ~80 kb/d (klesající); importuje
~250 kb/d + LNG (~12 mtpa). Ekonomicky nestabilní → **IMF program + FX krize**
= pravidelné problémy s platbami za energetické importy. Klíčové signály:
**OGRA (Oil and Gas Regulatory Authority)** upstream data, **SSGC/SNGPL gas utilities**
(spotřeba), **State Bank of Pakistan** FX reserves (platební kapacita). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PK-ministry_petroleum | PK | — | ministry_petroleum | Ministry of Energy (Petroleum Division) | moenergyp.gov.pk | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-PK-noc | PK | — | noc | PSO – Pakistan State Oil | psopk.com | international_agency | official | imports, term_contract, pricing_formula | proposed |
| ca-PK-mfa | PK | — | mfa | Ministry of Foreign Affairs | mofa.gov.pk | international_agency | official | sanctions, policy | proposed |
| ca-PK-customs_export | PK | — | customs_export | FBR – Federal Board of Revenue (Customs) | fbr.gov.pk | international_agency | official | imports, export_license | proposed |
| ca-PK-upstream_regulator | PK | — | upstream_regulator | OGRA – Oil and Gas Regulatory Authority | ogra.org.pk | international_agency | official | production, refinery_outage | proposed |
| ca-PK-port_maritime_authority | PK | — | port_maritime_authority | Karachi Port Trust | kpt.gov.pk | international_agency | official | vessel_loading, port_closure | proposed |
| ca-PK-national_exchange | PK | — | national_exchange | PSX – Pakistan Stock Exchange | psx.com.pk | exchange | official | pricing_formula | proposed |
| ca-PK-central_bank | PK | — | central_bank | SBP – State Bank of Pakistan | sbp.org.pk | international_agency | official | pricing_formula, sanctions | proposed |
| ca-PK-environment_regulator | PK | — | environment_regulator | SEPA – Sindh Environmental Protection Agency | sepa.gos.pk | international_agency | official | refinery_outage | proposed |
| ca-PK-coast_guard_navy | PK | — | coast_guard_navy | Pakistan Navy | paknavy.gov.pk | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PK-central_bank (SBP) | SBP FX reserves = primární indikátor platební kapacity za energetické importy; Pakistan opakovaně odkládá LNG FSRU platby při FX krizi; IMF program adherence = energy import continuity signal | SBP USD reserves ($9–14B range 2022–2024); každý sharp drop → PSO delays payment to LNG suppliers → Engro/PGPL FSRU disruption | PSO = importer + distributor; každý PSO payment default = downstream supply disruption | **proposed** — sbp.org.pk aktivní |
| ca-PK-noc (PSO) | PSO = state oil company; not upstream NOC but primary crude/product importer; buys ~60% of Pakistan's oil imports; PSO payment delays = major energy security signal | PSO state-owned; politicky exponovaná firma; PSO default na LNG spot contracts 2022 | Karachi Port Trust = crude arrival; PSO Port Qasim terminal | **proposed** — psopk.com aktivní |
| ca-PK-upstream_regulator (OGRA) | OGRA reguluje E&P licencing; Pakistan domestic gas ~3.5 bcf/d (declining); každý OGRA gas shortfall report = industrial disruption signal; RLNG imports přes ECC | OGRA pod Ministry of Energy; gas circular debt crisis (PKR 2.5T+) = systémový signal | Sui Northern (SNGPL) + Sui Southern (SSGC) pipeline networks; Karachi FSRU Port Qasim | **proposed** |

### Expansion sloty
- RLNG terminal: Engro Elengy → elengy.com.pk (Port Qasim FSRU; tier-1 LNG arrival signal)
- SNGPL – Sui Northern Gas Pipelines → sngpl.com.pk (northern Pakistan gas utility)
- SSGC – Sui Southern Gas Company → ssgc.com.pk (Karachi + Sindh gas)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 32, "last_country": "PK", "last_batch_seq": 33 }
```
