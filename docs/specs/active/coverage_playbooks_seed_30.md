# Coverage Playbooks Seed (3x) — #30

**Status:** planned  
**Lane:** Platform / Data  
**Goal:** Vytvořit první sadu "strategických" dokumentů, které agent může vyhledávat (Meta-RAG).

## Cíl

Vytvořit 3 Markdown soubory v `local_knowledge_sources/playbooks/`:
1.  `iran_oil_geopolitics.md`
2.  `lng_global_supply.md`
3.  `crude_oil_global.md`

## Proč

Playbooky obsahují lidskou strategii ("Pro Írán používej `shana.ir` a `t.me/shananews`"), kterou RAG knihy neobsahují. Agent je pak může vyhledávat, když potřebuje vědět "kde hledat".

## Akceptační kritéria

- [ ] 3 soubory `.md` existují v `local_knowledge_sources/playbooks/`.
- [ ] Každý playbook obsahuje sekci "Primary Official Sources" a "Official Social Media".
- [ ] Soubory jsou ingestovány do stávající RAG databáze (s metadaty `document_type: "playbook"`).
- [ ] Playbooky jsou verzovány v Gitu.

## Poznámky

- Generováno pomocí Cursor/Claude.
- Struktura playbooku je definována v ticketu #34.
