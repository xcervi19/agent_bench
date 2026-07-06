# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_025_country_authority_ID.md  
**Fáze:** country_authority — krok ID (Indonesia)  
**Datum:** 2026-07-05  

---

## Shrnutí

Indonesia = net importer ropy (~600 kb/d produkce vs ~1.5 mb/d spotřeba); ale stále
OPEC observer a důležitý LNG exportér (Tangguh, Bontang). Klíčové signály:
**SKK Migas produkční data** (upstream regulator; měsíční field reports),
**Pertamina rafinérie capacity** (6 rafinérií; upgrading program), **Malacca South**
(Batam Island; geopolitický kontrolní bod), **ICP – Indonesian Crude Price** (government
benchmark). Malacca Strait = kriticky důležitý pro Indii, Japonsko, Jižní Koreu.
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-ID-ministry_petroleum | ID | — | ministry_petroleum | MEMR – Ministry of Energy and Mineral Resources | esdm.go.id | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-ID-noc | ID | — | noc | Pertamina | pertamina.com | international_agency | official | production, imports, force_majeure, term_contract | proposed |
| ca-ID-mfa | ID | — | mfa | Kemlu – Ministry of Foreign Affairs | kemlu.go.id | international_agency | official | sanctions, policy | proposed |
| ca-ID-customs_export | ID | — | customs_export | DJBC – Directorate General of Customs and Excise | beacukai.go.id | international_agency | official | exports, import_licensing | proposed |
| ca-ID-upstream_regulator | ID | — | upstream_regulator | SKK Migas – Special Task Force for Upstream Oil and Gas | skkmigas.go.id | international_agency | official | production, force_majeure | proposed |
| ca-ID-port_maritime_authority | ID | — | port_maritime_authority | DJPL – Directorate General of Sea Transportation | hubla.dephub.go.id | international_agency | official | vessel_loading, port_closure | proposed |
| ca-ID-national_exchange | ID | — | national_exchange | IDX – Indonesia Stock Exchange | idx.co.id | exchange | official | pricing_formula | proposed |
| ca-ID-central_bank | ID | — | central_bank | Bank Indonesia | bi.go.id | international_agency | official | pricing_formula, sanctions | proposed |
| ca-ID-environment_regulator | ID | — | environment_regulator | KLHK – Ministry of Environment and Forestry | menlhk.go.id | international_agency | official | refinery_outage | proposed |
| ca-ID-coast_guard_navy | ID | — | coast_guard_navy | TNI AL – Indonesian Navy | tnial.mil.id | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ID-upstream_regulator (SKK Migas) | SKK Migas publikuje daily/monthly production data; Indonesia ICP (Indonesian Crude Price) je government-set benchmark (MEMR vydává); každý SKK Migas production target miss = supply miss vs OPEC forecast | SKK Migas = SOE task force; Prabowo government (2024) zvyšuje produkční ambice; Masela LNG a Natuna Sea | Medco, Chevron Indonesia, ConocoPhillips (Corridor Block) production data přes SKK | **proposed** — skkmigas.go.id aktivní |
| ca-ID-noc (Pertamina) | Pertamina = state refiner + upstream; Rokan Block (Pertamina od 2021, přebral od Chevron); 6 rafinérií (~1 mb/d kapacita); net crude importer | Pertamina holdings = strategic national asset; každý Pertamina CAPEX cut = signal pro Indonesian supply trend | Balikpapan (key Kalimantan terminal), Cilacap (Java refinery), Dumai export point | **proposed** — pertamina.com aktivní |
| ca-ID-coast_guard_navy (TNI AL) | TNI AL patrols Malacca southern approach, Lombok Strait (alternative to Malacca), Makassar Strait | Indonesia controls Lombok/Sunda/Makassar straits = alternative VLCC routes around Malacca; South China Sea EEZ (Natuna Sea vs China) | VLCC deep-draft tankers use Lombok Strait (deeper than Malacca); Indonesia exercises Malacca sovereignty | **unverified** — tnial.mil.id: ověřit domain |

### Expansion sloty
- ICP sub-feed → esdm.go.id/icp (Indonesian Crude Price monthly publication)
- Bontang LNG (Badak facility) → badaklng.co.id (LNG export terminal Kalimantan)
- Tangguh LNG → bp.com/tangguh (BP operated; Papua LNG)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 24, "last_country": "ID", "last_batch_seq": 25 }
```
