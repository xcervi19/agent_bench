# `/source-discover` Skill (MVP) — #32

**Status:** planned  
**Lane:** Platform / Agent Skills  
**Goal:** Vytvořit skill, který pro danou entitu vrací zdroje z Whitelistu/Playbooků.

## Cíl

Vytvořit `.cursor/skills/source-discover/SKILL.md`, který:
1.  Načte `source_whitelist.json`.
2.  Načte relevantní Playbooky z RAG.
3.  Provede `WebSearch` (Brave) pro nalezení nových kandidátů (omezeno na whitelist TLD).
4.  Vrátí strukturovaný JSON s `known_sources` a `discovered_candidates`.

## Proč

Toto je základní "Source Discovery" logika, kterou může volat `newsfind-plan.md`.

## Akceptační kritéria

- [ ] Skill existuje v `.cursor/skills/source-discover/`.
- [ ] Skill vrací validní JSON pro vstup `"NIOC"`.
- [ ] JSON obsahuje pole `known_sources` (z Whitelistu) a `discovered_candidates` (z Brave).
- [ ] Skill je verzován v Gitu.

## Poznámky

- Skill běží v "Ask mode" (vyžaduje explicitní volání).
- Neprovádí automatickou validaci (ta je v #33).
