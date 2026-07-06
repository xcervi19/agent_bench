# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_016_country_authority_VE.md  
**Fáze:** country_authority — krok VE (Venezuela)  
**Datum:** 2026-07-05  

---

## Shrnutí

Venezuela = komplexní sankční případ. Největší prokázané zásoby ropy světa (~300 Gbbl),
ale produkce collapsovala z 3.2 mb/d (2000) na ~850 kb/d (2020) a částečně se zotavila
na ~1 mb/d (2024) po US General Licences pro Chevron. Klíčové signály: **OFAC GL waiver**
(každá změna Chevron licence pohybuje trhem), **PDVSA export tracking** (většinou přes
tanker surveillance), **BCV FX** (hyperinflace; proxy pro ekonomický kolaps). NOC slot
obsahuje PDVSA (SDN-listed). 8 proposed, 2 unverified (jeden empty zvážit).

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-VE-ministry_petroleum | VE | — | ministry_petroleum | Menpet – Ministry of Petroleum | minpet.gob.ve | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-VE-noc | VE | — | noc | PDVSA – Petróleos de Venezuela | pdvsa.com | international_agency | official | production, exports, force_majeure, term_contract | proposed |
| ca-VE-mfa | VE | — | mfa | Cancillería – Ministry of Foreign Affairs | mppre.gob.ve | international_agency | official | sanctions, policy | proposed |
| ca-VE-customs_export | VE | — | customs_export | SENIAT – National Customs and Tax Administration | seniat.gob.ve | international_agency | official | exports, export_license | proposed |
| ca-VE-upstream_regulator | VE | — | upstream_regulator | Ministry of Petroleum (upstream, dual role) | minpet.gob.ve | international_agency | official | production, refinery_outage | proposed |
| ca-VE-port_maritime_authority | VE | — | port_maritime_authority | INEA – Instituto Nacional de los Espacios Acuáticos | inea.gob.ve | international_agency | official | vessel_loading, port_closure | proposed |
| ca-VE-national_exchange | VE | — | national_exchange | — (BVC non-functional; no commodity exchange) | — | — | — | — | empty |
| ca-VE-central_bank | VE | — | central_bank | BCV – Banco Central de Venezuela | bcv.org.ve | international_agency | official | sanctions | proposed |
| ca-VE-environment_regulator | VE | — | environment_regulator | Ministerio del Poder Popular para el Ecosocialismo | minec.gob.ve | international_agency | official | refinery_outage | unverified |
| ca-VE-coast_guard_navy | VE | — | coast_guard_navy | Armada Nacional Bolivariana | armada.mil.ve | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-VE-noc (PDVSA) | PDVSA = ~950 kb/d (2024); Orinoco Belt heavy crude (Merey, Boscan); Chevron JV = základní kamínek obnovené produkce | PDVSA je SDN-listed OFAC; Chevron General Licence (OFAC) = primární sledování; každé obnovení/revokace GL = $1–2 WTI swing; PDVSA monitorovat přes tanker surveillance, ne přímou web stránku | José Antonio Anzoátegui terminal = hlavní export; AIS tracking klíčovější než PDVSA vlastní reporty | **proposed** — pdvsa.com existuje ale data nespolehlivá; monitorovat jako sekundární potvrzení |
| ca-VE-ministry_petroleum (Menpet) | Menpet deklaruje produkční cíle (obvykle nadhodnocené); každý výrok ministra Tellechea = production narrative | Menpet koordinuje OPEC+ komunikaci; Maduro vládní prohlášení o energetice | Policy signal pro Orinoco upgrade projekty | **proposed** — minpet.gob.ve existuje; spolehlivost omezená |
| ca-VE-coast_guard_navy (Armada) | Armada chrání terminály a přístupy k José; PDVSA ghost fleet operace | Venezuela Navy má omezené kapacity; US/Caribbean Coast Guard surveillance je reálnější monitoring | Tanker departures z Puerto La Cruz, José, Amuay | **unverified** — armada.mil.ve: ověřit aktuálnost; alternativně GBF/ACNUR incidents jako proxy |

### Analytická poznámka: Venezuela monitoring reálně
Primární tracking venezuelské produkce = **Equasis + tanker surveillance** (Kpler, VesselsValue jsou aggregátory ale de-facto monitoring nástroje). OFAC General Licence status (ofac.treas.gov) je tier-1 primary signal — nikoliv PDVSA vlastní komunikace.

### Expansion sloty
- PDVSA Gas (subsidiary) → pdvsa.com/gas
- Sinovensa JV (PDVSA/CNPC) → expansion slot CN×VE
- CVP (Corporación Venezolana del Petróleo) → cvp.pdvsa.com

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 15, "last_country": "VE", "last_batch_seq": 16 }
```
