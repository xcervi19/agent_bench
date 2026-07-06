# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_011_country_authority_OM.md  
**Fáze:** country_authority — krok OM (Oman)  
**Datum:** 2026-07-05  

---

## Shrnutí

Oman = ~1.05 mb/d crude + condensate; klíčová pozice na jihozápadním pobřeží Arabského poloostrova,
kontroluje přístupy do Hormuz z jihu (Musandam). Specifika: **PDO** (Petroleum Development Oman) =
joint venture (60 % stát, 34 % Shell, 4 % TotalEnergies) — neobvyklá struktura; **OQ** jako
státní holding; **Oman Crude** benchmark (Oman/Dubai forward curve = Middle East sour marker).
8 proposed, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-OM-ministry_petroleum | OM | — | ministry_petroleum | Ministry of Energy and Minerals | mem.gov.om | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-OM-noc | OM | — | noc | OQ – Oman's Energy Company (state holding) | oq.com | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-OM-mfa | OM | — | mfa | Ministry of Foreign Affairs | mfa.gov.om | international_agency | official | sanctions, policy | proposed |
| ca-OM-customs_export | OM | — | customs_export | Royal Oman Police – Customs Department | rop.gov.om | international_agency | official | exports, export_license | proposed |
| ca-OM-upstream_regulator | OM | — | upstream_regulator | PDO – Petroleum Development Oman | pdo.co.om | international_agency | official | production, refinery_outage, force_majeure | proposed |
| ca-OM-port_maritime_authority | OM | — | port_maritime_authority | Asyad Group (Oman Ports) | asyad.om | international_agency | official | vessel_loading, port_closure | proposed |
| ca-OM-national_exchange | OM | — | national_exchange | MSX – Muscat Stock Exchange | msx.om | exchange | official | pricing_formula | proposed |
| ca-OM-central_bank | OM | — | central_bank | CBO – Central Bank of Oman | cbo.gov.om | international_agency | official | sanctions | proposed |
| ca-OM-environment_regulator | OM | — | environment_regulator | Environment Authority of Oman | ea.gov.om | international_agency | official | refinery_outage | unverified |
| ca-OM-coast_guard_navy | OM | — | coast_guard_navy | Royal Navy of Oman | rno.gov.om | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových + unverified)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-OM-upstream_regulator (PDO) | PDO = 70 % ománské produkce (~660 kb/d); annual sustainability report s produkčními daty je spolehlivý source (Shell disclosure standard) | PDO JV structure = atypická transparentnost pro region; Shell má board seat → western-standard disclosures | PDO produkce teče přes pipeline do Mina al-Fahal (Muscat) a Duqm terminál | **proposed** — pdo.co.om je ověřená doména |
| ca-OM-noc (OQ) | OQ (merger Oman Oil + Orpic 2019) spravuje downstream, LNG stakes (Oman LNG), petrochemie; trading arm OQ Trading pro crude export | OQ je plně státní; každý capacity announcement = sovereign supply signal | OQ zajišťuje prodej Oman Blend crude; DME Oman futures settlement přes OQ | **proposed** — oq.com aktivní (anglická a arabská verze) |
| ca-OM-environment_regulator | EA Oman dohlíží na rafinérie Sohar a Duqm; omezené veřejné publikace | Nízká přímá geopolitická role | Sohar refinery compliance; Duqm SEZ environmental approvals | **unverified** — ea.gov.om existuje ale nejistá příslušnost k Environment Authority; alternativa: mohe.gov.om nebo jiný suffix |
| ca-OM-coast_guard_navy | Royal Navy of Oman (RNO) chrání Musandam peninsula — kontrolní bod Hormuz jižní přístup | Oman je tradičně neutrální; RNO neprovokuje; ale kontroluje klíčové Hormuz waters | VLCC escort přes Hormuz + Mina al-Fahal přístupy | **unverified** — rno.gov.om je předpokládaná doména; ověřit |

### Expansion sloty
- Oman LNG LLC → omanlng.co.om — LNG joint venture (Oman 51%, Shell, TotalEnergies, Mitsubishi)
- OQ Trading (crude trading arm) → oq.com/trading
- Port of Duqm → duqmseaport.com (SEZ export hub; expansion)
- Mina al-Fahal terminal → OQ/PDO operated (geo expansion slot)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 10, "last_country": "OM", "last_batch_seq": 11 }
```
