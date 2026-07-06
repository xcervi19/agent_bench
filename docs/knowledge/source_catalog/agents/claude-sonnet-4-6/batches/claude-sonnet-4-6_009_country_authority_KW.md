# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_009_country_authority_KW.md  
**Fáze:** country_authority — krok KW (Kuwait)  
**Datum:** 2026-07-05  

---

## Shrnutí

Kuwait = ~2.7 mb/d kapacita, čistý producent Kuwaiti Export Crude (KEC). Klíčové signály:
**KPC/KOC produkce** (Burgan field = jedno z největších na světě), **KNPC rafinérie**
(Al-Zour — jedna z největších v regionu), **Shuaiba/Mina Abdullah terminály**. Kuwait
má konzistentní OPEC+ compliance profil. 7 proposed, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KW-ministry_petroleum | KW | — | ministry_petroleum | Ministry of Oil | moo.gov.kw | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-KW-noc | KW | — | noc | KPC – Kuwait Petroleum Corporation | kpc.com.kw | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-KW-mfa | KW | — | mfa | Ministry of Foreign Affairs | mofa.gov.kw | international_agency | official | sanctions, policy | proposed |
| ca-KW-customs_export | KW | — | customs_export | Kuwait General Administration of Customs | customs.gov.kw | international_agency | official | exports, export_license | proposed |
| ca-KW-upstream_regulator | KW | — | upstream_regulator | KOC – Kuwait Oil Company | kockw.com | international_agency | official | production, refinery_outage | unverified |
| ca-KW-port_maritime_authority | KW | — | port_maritime_authority | Kuwait Port Authority | kpa.gov.kw | international_agency | official | vessel_loading, port_closure | proposed |
| ca-KW-national_exchange | KW | — | national_exchange | Boursa Kuwait | boursakuwait.com | exchange | official | pricing_formula | unverified |
| ca-KW-central_bank | KW | — | central_bank | CBK – Central Bank of Kuwait | cbk.gov.kw | international_agency | official | sanctions | proposed |
| ca-KW-environment_regulator | KW | — | environment_regulator | KEPA – Kuwait Environment Public Authority | kepa.gov.kw | international_agency | official | refinery_outage | proposed |
| ca-KW-coast_guard_navy | KW | — | coast_guard_navy | Kuwait Naval Force | mod.gov.kw | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových + unverified)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KW-noc (KPC) | KPC holdingová struktura: KOC (upstream), KNPC (downstream/refinery), KUFPEC (intl upstream), KPI (shipping); KEC + Kuwait Export Crude OSPs se nastavují měsíčně | KPC je 100% státní; každé prohlášení KPC CEO o produkčním výhledu je OPEC+ signal | KPC Trading se stará o cargo allokaci; Mina al-Ahmadi terminal = primární crude export point | **proposed** — kpc.com.kw aktivní |
| ca-KW-upstream_regulator (KOC) | KOC provozuje Burgan (1.7 mb/d), Raudhatain, Sabriya fieldy; produkční data v annual reportu | KOC je plně pod KPC/MoO; separátní entita s vlastním domain a reporting | KOC coordinating maintenance → field-level supply disruption signal | **unverified** — kockw.com: ověřit zda KOC domain; alternativně koc.com.kw |
| ca-KW-national_exchange (Boursa Kuwait) | Equity exchange; KNPC a KPC nejsou listovány veřejně | Omezená komoditní relevance; Kuwait Petroleum futures nejsou na Boursa | Žádná přímá logistická role | **unverified** — boursakuwait.com je pravděpodobná doména pro Boursa Kuwait (rebrand z Kuwait Stock Exchange 2016); ověřit |
| ca-KW-coast_guard_navy | Kuwait Bay + Shuaiba terminál přístupy | Íránský vliv v Zálivu; Kuwait Naval Force chrání offshore fields | Konvoje pro Mina al-Ahmadi VLCC loadingy | **unverified** — mod.gov.kw nemusí mít naval sub-stránku; ověřit |

### Expansion sloty
- KNPC – Kuwait National Petroleum Company (rafinérie) → knpc.com.kw
- KPI – Kuwait Petroleum International (trading) → kpi.com.kw
- Mina al-Ahmadi port authority → separate geo slot

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 8, "last_country": "KW", "last_batch_seq": 9 }
```
