# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_028_country_authority_JP.md  
**Fáze:** country_authority — krok JP (Japan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Japan = 4. největší LNG importér (~80 mtpa) a 3.–4. největší importér ropy (~3 mb/d).
Žádná domácí produkce. Klíčové signály: **JCC (Japan Crude Cocktail)** = základní
cena pro asijské LNG long-term smlouvy (FOB cena Arabského zálivu do Japonska = JCC index);
**METI monthly energy statistics** (import volumes, stockpile changes); **JOGMEC SPE/stockpile**
(koordinace s IEA na release z japonských strategických zásob). INPEX = Japan's primary
upstream company (Ichthys LNG Australia, Abu Al Bukhoosh UAE). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-JP-ministry_petroleum | JP | — | ministry_petroleum | METI – Ministry of Economy, Trade and Industry | meti.go.jp | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-JP-noc | JP | — | noc | INPEX Corporation | inpex.co.jp | international_agency | official | production, term_contract, force_majeure | proposed |
| ca-JP-mfa | JP | — | mfa | MOFA – Ministry of Foreign Affairs | mofa.go.jp | international_agency | official | sanctions, policy | proposed |
| ca-JP-customs_export | JP | — | customs_export | Japan Customs (MOF) | customs.go.jp | international_agency | official | imports, exports | proposed |
| ca-JP-upstream_regulator | JP | — | upstream_regulator | JOGMEC – Japan Organization for Metals and Energy Security | jogmec.go.jp | international_agency | official | production, force_majeure | proposed |
| ca-JP-port_maritime_authority | JP | — | port_maritime_authority | MLIT – Ministry of Land, Infrastructure, Transport and Tourism (ports) | mlit.go.jp | international_agency | official | vessel_loading, port_closure | proposed |
| ca-JP-national_exchange | JP | — | national_exchange | JPX – Japan Exchange Group (energy derivatives) | jpx.co.jp | exchange | official | pricing_formula | proposed |
| ca-JP-central_bank | JP | — | central_bank | BOJ – Bank of Japan | boj.or.jp | international_agency | official | pricing_formula | proposed |
| ca-JP-environment_regulator | JP | — | environment_regulator | MOE – Ministry of the Environment | env.go.jp | international_agency | official | refinery_outage | proposed |
| ca-JP-coast_guard_navy | JP | — | coast_guard_navy | JMSDF – Japan Maritime Self-Defense Force | mod.go.jp/msdf | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-JP-upstream_regulator (JOGMEC) | JOGMEC spravuje japonské strategické zásoby ropy (IEA člen); koordinuje SPE (Strategic Petroleum Reserve) releases; JOGMEC financuje zahraniční upstream prostřednictvím loan/equity = Japanese energy security tool | JOGMEC loans pro INPEX Ichthys, JAPEX projects = energy diplomacy; Sakhalin-2 (post-2022 Japan stake zachování) = geopolitický signal | JOGMEC oilfield data surveys → Japanese VLCC fleet loading patterns | **proposed** — jogmec.go.jp aktivní |
| ca-JP-ministry_petroleum (METI) | METI = klíčový pro JCC pricing mechanism (Japan Crude Cocktail = weighted average FOB price); METI monthly oil statistics (import volumes, stocks); fuel oil stockpile levels | Japan sanctions compliance (Russia Sakhalin-2 exemption; Iran waiver history); METI export controls (dual-use energy equipment) | METI refinery statistics; Tokyo Bay LNG import terminals; Yokkaichi, Chiba crude terminals | **proposed** — meti.go.jp aktivní |
| ca-JP-noc (INPEX) | INPEX = Japan's largest upstream company (state >18%); Ichthys LNG (Australia, 8.9 mtpa, INPEX 66.1% op.); Abadi LNG (Indonesia, delayed); Abu Al Bukhoosh UAE; Masela block Indonesia | INPEX listed on TSE; quarterly production reports; JAPEX (Japan Petroleum Exploration) = secondary NOC-like entity | Ichthys LNG → Darwin → Japan LNG carriers (Japanese shipping fleets) | **proposed** — inpex.co.jp aktivní |

### Expansion sloty
- JAPEX – Japan Petroleum Exploration → japex.co.jp (domestic + overseas upstream)
- JERA – Japan's largest LNG buyer (TEPCO+Chubu JV) → jera-co.com (critical LNG demand signal)
- TEPCO, Kansai Electric, Chubu Electric: utility LNG demand signals

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 27, "last_country": "JP", "last_batch_seq": 28 }
```
