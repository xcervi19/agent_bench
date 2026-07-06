# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_035_country_authority_GR.md  
**Fáze:** country_authority — krok GR (Greece)  
**Datum:** 2026-07-06  

---

## Shrnutí

Greece = **tanker shipping hub světa** (pireus; ~50% světové tanker fleet pod řeckými
vlastníky nebo managementem). Minimální produkce ropy. Klíčové signály: **Hellenic
Shipping News** (tier-1 tanker market), **Greek tanker owners** (Onassis, Tsakos,
Capital Maritime, Dynacom) = bellwether pro tanker rates a dark fleet signalling.
Revithoussa LNG terminál (DESFA; SPA Athens; tier-1 SEE hub). Alexandroupolis FSRU
(Gastrade; 2024; klíčový pro Balkán). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GR-ministry_petroleum | GR | — | ministry_petroleum | Ministry of Environment and Energy | ypen.gr | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-GR-noc | GR | — | noc | HELPE – HELLENiQ Energy (formerly Hellenic Petroleum) | helleniqenergy.gr | international_agency | official | production, imports, refinery_outage, term_contract | proposed |
| ca-GR-mfa | GR | — | mfa | Ministry of Foreign Affairs | mfa.gr | international_agency | official | sanctions, policy | proposed |
| ca-GR-customs_export | GR | — | customs_export | IAPR – Independent Authority for Public Revenue (Customs) | aade.gr | international_agency | official | imports, exports | proposed |
| ca-GR-upstream_regulator | GR | — | upstream_regulator | EDEY – Hellenic Hydrocarbons and Energy Resources Management Company | edey.gr | international_agency | official | production, force_majeure | proposed |
| ca-GR-port_maritime_authority | GR | — | port_maritime_authority | HAF – Hellenic Coast Guard / Ministry of Maritime Affairs | hcg.gr | international_agency | official | vessel_loading, port_closure | proposed |
| ca-GR-national_exchange | GR | — | national_exchange | ATHEX – Athens Stock Exchange | athexgroup.gr | exchange | official | pricing_formula | proposed |
| ca-GR-central_bank | GR | — | central_bank | Bank of Greece | bankofgreece.gr | international_agency | official | pricing_formula | proposed |
| ca-GR-environment_regulator | GR | — | environment_regulator | YPEN (Energy + Environment Ministry, dual) | ypen.gr | international_agency | official | refinery_outage | proposed |
| ca-GR-coast_guard_navy | GR | — | coast_guard_navy | Hellenic Navy | hellenicnavy.gr | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GR-noc (HELLENiQ) | HELLENiQ = Greek state refiner (Motor Oil + HELPE = 2 major Greek refiners); Aspropyrgos + Elefsis refineries (~380 kb/d); crude mix: Russian Urals (pre-2022 ~50%, post-2022 ~35% declining) + Middle East | HELLENiQ listed ATHEX; privatisation process (Paneuropean Oil ~45% stake → Vitol 2023); každá change refiners crude mix = Greek sanctions compliance signal | Revithoussa LNG terminal (DESFA, Athens; 225 mcm working capacity) = Greek + Balkán LNG hub; Alexandroupolis FSRU (2024) = diversification from Russian pipeline gas | **proposed** — helleniqenergy.gr aktivní |
| ca-GR-port_maritime_authority (Piraeus/HCG) | Piraeus = world's largest passenger port; global tanker management hub; Hellenic Coast Guard monitors Aegean tanker traffic | Greek tanker owners (~50% of global VLCC fleet by ownership; 15% by flag) = key dark fleet monitoring; Aegean piracy (limited vs Black Sea/Gulf of Guinea) | Corinth Canal (tanker shortcuts); Patras port crude products; Revithoussa LNG jetty | **proposed** |
| ca-GR-coast_guard_navy | Hellenic Navy patrols Aegean Sea; Turkey-Greece Aegean dispute (overlapping FIRs, EEZ claims) | Greece-Turkey Aegean tension = Eastern Mediterranean energy exploration risk (Crete Basin, Cyprus EEZ disputes) | Greek EEZ offshore hydrocarbon blocks: South Crete, Ionian Sea | **unverified** — hellenicnavy.gr ověřit vs navy.mil.gr |

### Expansion sloty
- DESFA → desfa.gr (Greek gas transmission + Revithoussa LNG; tier-1 SEE gas signal)
- Gastrade (Alexandroupolis FSRU) → gastrade.gr (2024 operational; Balkán gas diversification)
- Motor Oil Hellas → moh.gr (private refiner ~180 kb/d; Corinth refinery)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 34, "last_country": "GR", "last_batch_seq": 35 }
```
