# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_017_country_authority_NG.md  
**Fáze:** country_authority — krok NG (Nigeria)  
**Datum:** 2026-07-05  

---

## Shrnutí

Nigeria = ~1.5 mb/d (po roky pod OPEC kvótou ~1.8 mb/d kvůli vandalismu, theft, kapacitním
problémům). Největší africký producent, Bonny Light = key Sweet African benchmark pro Evropu.
Klíčové signály: **NNPC Ltd produkce** (privatizovaná 2022, komerčnější disclosures),
**NUPRC** (regulátor post-PIA 2021 reforma), **Niger Delta vandalism** (pipeline theft = chronic
supply disruption), **Dangote refinery** (650 kb/d, 2024 startup = africký refinery revolution).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NG-ministry_petroleum | NG | — | ministry_petroleum | Ministry of Petroleum Resources | petroleum.gov.ng | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-NG-noc | NG | — | noc | NNPC Ltd – Nigerian National Petroleum Company | nnpcgroup.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-NG-mfa | NG | — | mfa | Ministry of Foreign Affairs | mfa.gov.ng | international_agency | official | sanctions, policy | proposed |
| ca-NG-customs_export | NG | — | customs_export | Nigeria Customs Service | customs.gov.ng | international_agency | official | exports, export_license | proposed |
| ca-NG-upstream_regulator | NG | — | upstream_regulator | NUPRC – Nigerian Upstream Petroleum Regulatory Commission | nuprc.gov.ng | international_agency | official | production, force_majeure | proposed |
| ca-NG-port_maritime_authority | NG | — | port_maritime_authority | NPA – Nigerian Ports Authority | nigerianports.gov.ng | international_agency | official | vessel_loading, port_closure | proposed |
| ca-NG-national_exchange | NG | — | national_exchange | NGX – Nigerian Exchange Group | ngxgroup.com | exchange | official | pricing_formula | proposed |
| ca-NG-central_bank | NG | — | central_bank | CBN – Central Bank of Nigeria | cbn.gov.ng | international_agency | official | sanctions | proposed |
| ca-NG-environment_regulator | NG | — | environment_regulator | NOSDRA – National Oil Spill Detection and Response Agency | nosdra.gov.ng | international_agency | official | force_majeure, pipeline_outage | proposed |
| ca-NG-coast_guard_navy | NG | — | coast_guard_navy | Nigerian Navy | navy.mil.ng | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NG-noc (NNPC Ltd) | NNPC Ltd (komerčnější post-PIA 2022) publikuje monthly oil production; Nigeria chronicky pod OPEC kvótou (~300 kb/d gap); každé NNPC produkční oznámení = OPEC compliance signal | NNPC Ltd = 100 % státní ale komerčnější board structure; prezident Tinubu (od 2023) = pozitivní signal pro IOC partnerships | Forcados, Bonny, Brass, Qua Iboe terminály; Forcados = chronicky narušovaný vandaly (Force Majeure 2016) | **proposed** — nnpcgroup.com aktivní (nové branding post-PIA) |
| ca-NG-upstream_regulator (NUPRC) | NUPRC nahradil DPR (Department of Petroleum Resources) po PIA 2021; vydává produkční licence; nové blokové tendry | NUPRC je pod Ministry of Petroleum; PIA implementace = strukturální signal pro IOC (Shell, TotalEnergies, Chevron, Exxon) | NUPRC koordinuje terminal allocation; Bonny Light cargo lifting schedule | **proposed** — nuprc.gov.ng aktivní |
| ca-NG-environment_regulator (NOSDRA) | NOSDRA reportuje Niger Delta oil spills; každý velký spill = produkční výpadek signal + force majeure risk | Niger Delta vandalism (IPOB, MEND activists) = chronický geopolitický risk pro supply | Spill incidents blokují pipeline přístupy k export terminálům | **proposed** — nosdra.gov.ng aktivní |
| ca-NG-coast_guard_navy | Nigerian Navy chrání terminály (Forcados, Bonny, Brass); pirátství v Guinejském zálivu = tier-1 maritime security signal | Nigerian Navy bojuje s pirátstvím; IMB (International Maritime Bureau) piracy report je primárnější signal | Bonny terminal vessel přístupy; Brass terminal bezpečnostní eskorty | **unverified** — navy.mil.ng: ověřit domain; nigerijská vládní domény .mil.ng jsou méně standardizované |

### Analytická poznámka: Niger Delta vandalism
Chronické narušení pipeline (Shell, Agip, TotalEnergies trunklines) = hlavní driver produkčního gappu. Monitoring přes:
- NNPC Ltd production reports
- Shell Nigeria press statements (shell.com.ng)
- NOSDRA spill database
Toto je expansion monitoring cluster pro NG.

### Expansion sloty
- Shell Nigeria (SPDC) → shell.com.ng (major IOC operator; Force Majeure declarant)
- TotalEnergies EP Nigeria → totalenergies.com/ng
- Seplat Energy (indigenous E&P) → seplatpetroleum.com
- Dangote Refinery → dangote.com/oil-and-gas (650 kb/d; tier-1 West African refinery signal)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 16, "last_country": "NG", "last_batch_seq": 17 }
```
