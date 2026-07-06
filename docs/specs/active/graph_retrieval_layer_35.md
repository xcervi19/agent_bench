# Graph Retrieval Layer (Source Graph v2) — #35

**Status:** planned  
**Lane:** Platform / Data  
**Goal:** Postavit nad whitelist/katalogem a playbooky grafovou orchestrační vrstvu pro přesnější výběr zdrojů k danému topicu.

## Cíl

Z ploché source báze (`source_whitelist.json` #29 + katalog `entries`) udělat **graf entit** a přidat retrieval, který pro topic vrátí relevantní zdroje pomocí šíření aktivace (ne fixního počtu hopů).

1. `source_graph.json` (nebo hrany navíc k entitám):
   - **Uzly = entity** (zdroj/orgán/NOC/hub) s fasetami: `country, geo_target, category, type, signals[], commodity, status`.
   - **Hrany = vztahy** s vahou 0–1: `located_in`, `operates`, `transits`, `regulates`, `benchmarks`, `substitutes_for`.
2. Retrieval funkce `retrieve(topic) -> ranked_sources`:
   - LLM extrakce z topicu: `commodity, entities, geo, signals, časové okno`.
   - Seed set = přímé match uzly.
   - **Šíření aktivace / Personalized PageRank**: skóre uzlu = Σ `váha_hrany × decay^vzdálenost`.
   - **Práh, ne hop-limit** (+ top-K beam jako pojistka proti explozi).
   - Finální skóre = `graph_score × vektor_podobnost(topic) × status_boost(proposed) × recency`.

## Proč

Vektor RAG (#30) sám dává široké/nepřesné výsledky u vztahových dotazů (např. „Hormuz zavřen" → dotčené NOC, pojistky, alternativní trasy). Graf přidá strukturovanou expanzi a přesnost.

## Kritičnost / pořadí

**Nadstavba, ne blokující.** MVP (#29+#30+#31+#32+#33) musí fungovat čistě na vektor RAG + whitelist filtr. Tento ticket řešit až **po změření kvality retrievalu**, pokud vektor selhává na vztazích.

- Závisí na: #29 (uzly), #30 (vektor vrstva), ideálně #31 (živá data → `proposed`).
- Navazuje na: #32/#33 (`source-discover` může volat graf místo prostého filtru).

## Akceptační kritéria

- [ ] `source_graph.json` existuje: uzly s fasetami + vážené hrany.
- [ ] Funkce/skript `retrieve(topic)` vrací seřazený seznam zdrojů se skóre a důvodem (matched signal/edge).
- [ ] Práh + decay konfigurovatelné; žádný pevný hop-limit.
- [ ] Benchmark: na ≥3 topicích (Írán/Hormuz, LNG supply, Urals sankce) graf retrieval ≥ vektor baseline.
- [ ] Verzováno v Gitu.

## Poznámky

- Osvědčené vzory: Personalized PageRank / Spreading Activation, Microsoft GraphRAG, Neo4j + vektor hybrid.
- Country zůstává jako **jedna faseta**, ne kořen stromu.
- Nestavět předčasně — trigger je slabý retrieval z #30, ne „protože graf je hezký".
