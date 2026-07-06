# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_024_country_authority_MY.md  
**Fáze:** country_authority — krok MY (Malaysia)  
**Datum:** 2026-07-05  

---

## Shrnutí

Malaysia = ~550 kb/d crude; klíčovější pro LNG (světově 3.–4. vývozce: **Bintulu LNG**
= největší single-location LNG komplex světa). PETRONAS = primární entita pro obě osy
(crude + LNG). Malacca Strait security = geo-malacca slot. Klíčové signály: **PETRONAS
annual/quarterly** (disclosure standard Malaysian governance), **MLNG Bintulu loading
schedules**, **Tapis crude OSP** (Malaysian light sweet benchmark). PETRONAS je zároveň
NOC i upstream regulátor (Petroleum Development Act 1974). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MY-ministry_petroleum | MY | — | ministry_petroleum | Ministry of Economy (energy division) | ekonomi.gov.my | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-MY-noc | MY | — | noc | PETRONAS – Petroliam Nasional Berhad | petronas.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-MY-mfa | MY | — | mfa | Ministry of Foreign Affairs (Wisma Putra) | kln.gov.my | international_agency | official | sanctions, policy | proposed |
| ca-MY-customs_export | MY | — | customs_export | Royal Malaysian Customs Department | customs.gov.my | international_agency | official | exports, export_license | proposed |
| ca-MY-upstream_regulator | MY | — | upstream_regulator | PETRONAS (upstream licensing under PDA 1974) | petronas.com | international_agency | official | production, refinery_outage | proposed |
| ca-MY-port_maritime_authority | MY | — | port_maritime_authority | Port Klang Authority | pka.gov.my | international_agency | official | vessel_loading, port_closure | proposed |
| ca-MY-national_exchange | MY | — | national_exchange | Bursa Malaysia | bursamalaysia.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-MY-central_bank | MY | — | central_bank | Bank Negara Malaysia | bnm.gov.my | international_agency | official | pricing_formula, sanctions | proposed |
| ca-MY-environment_regulator | MY | — | environment_regulator | DOE – Department of Environment Malaysia | doe.gov.my | international_agency | official | refinery_outage | proposed |
| ca-MY-coast_guard_navy | MY | — | coast_guard_navy | Royal Malaysian Navy | navy.mil.my | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MY-noc (PETRONAS) | PETRONAS = sole national oil company; annual reports + quarterly highlights; Bintulu LNG (29 mtpa, 9 trains) = tier-1 LNG supply signal; Tapis crude OSP monthly | PETRONAS reportuje přímo PM office; každý change leadership nebo budget = signal; Malaysia non-aligned (sanctions) | MLNG Bintulu = key JKM price driver; Labuan offshore hub; Melaka refinery | **proposed** — petronas.com aktivní; strong Anglická disclosure |
| ca-MY-port_maritime_authority (PKA) | Port Klang = 2. největší kontejnerový přístav v regionu; méně crude-centric; Kertih petrochemical complex přes Kemaman port | Malacca transit fee discussion; Malaysia-Indonesia-Singapore trilateral Malacca governance | Bintulu LNG port přes MLNG (PETRONAS-managed, ne PKA); Tanjung Langsat crude terminal | **proposed** — pka.gov.my aktivní; pro LNG: Bintulu Port Authority separátní expansion slot |
| ca-MY-coast_guard_navy | RMN patrols Malacca Strait southern section; South China Sea EEZ (Spratly dispute vs China) | SCS tension = Malaysian neutral stance vs Chinese pressure; Malacca closure risk premium | VLCC convoy přes Malacca; piracy/theft incidents (Sulawesi Sea) | **unverified** — navy.mil.my nebo rmn.mil.my; ověřit správnou doménu |

### Expansion sloty
- MLNG – Malaysia LNG Sdn Bhd → mlng.com.my (Bintulu operator; Shell/PETRONAS JV)
- Bintulu Port Authority → bintuluportharbourboard.com (expansion port slot)
- MISC Berhad (PETRONAS shipping arm) → misc.com.my — LNG tanker fleet

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 23, "last_country": "MY", "last_batch_seq": 24 }
```
