# Batch 069 — Country Authority: EC (Ecuador)

## Country significance
Ecuador is a **mid-tier Andean crude exporter** (~450–480 kb/d) and an **OPEC member** (resigned 2020, rejoined — currently non-member as of 2020 exit). Its fiscal dependence on oil (30–40% of government revenue) makes Petroecuador policy extremely price-sensitive. Key fields: **Ishpingo-Tambococha-Tiputini (ITT/Block 43)** in Yasuní National Park — a politically and legally contested mega-block (2023 referendum voted to halt production; legal battles ongoing). Traditional heavy crude (Napo, Oriente blends) exported via SOTE and OCP pipelines to Pacific coast (Esmeraldas, Balao terminals). **Petroecuador** (state NOC) dominates; **Repsol, Andes Petroleum (CNPC/CNOOC)** are major IOC partners. Ecuador is a **net LNG importer** (small domestic gas, no LNG export). Political instability = force majeure signal: frequent protests blocking oil infrastructure.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-EC-ministry_petroleum | EC | — | ministry_petroleum | Ministry of Energy and Natural Resources | recursosyenergia.gob.ec | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-EC-noc | EC | — | noc | Petroecuador – EP Petroecuador | eppetroecuador.gob.ec | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-EC-mfa | EC | — | mfa | Ministry of Foreign Affairs (Cancillería) | cancilleria.gob.ec | international_agency | official | sanctions, policy | proposed |
| ca-EC-customs_export | EC | — | customs_export | SENAE – Aduana del Ecuador | aduana.gob.ec | international_agency | official | exports, export_license | proposed |
| ca-EC-upstream_regulator | EC | — | upstream_regulator | ARCH – Agencia de Regulación y Control de Energía | arch.gob.ec | international_agency | official | production, force_majeure | proposed |
| ca-EC-port_maritime_authority | EC | — | port_maritime_authority | Autoridad Portuaria de Esmeraldas | puertoesmeraldas.gob.ec | international_agency | official | vessel_loading, port_closure | proposed |
| ca-EC-national_exchange | EC | — | national_exchange | Bolsa de Valores de Quito (BVQ) | ccbvq.com | exchange | official | pricing_formula | proposed |
| ca-EC-central_bank | EC | — | central_bank | Banco Central del Ecuador | bce.fin.ec | international_agency | official | pricing_formula | proposed |
| ca-EC-environment_regulator | EC | — | environment_regulator | Ministry of Environment (MAATE) | ambiente.gob.ec | international_agency | official | pipeline_outage, force_majeure | proposed |
| ca-EC-coast_guard_navy | EC | — | coast_guard_navy | Armada del Ecuador | armada.mil.ec | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-EC-noc (Petroecuador)
- **Supply:** Petroecuador ~350 kb/d (ITT Block 43 halt = ~50–80 kb/d reduction 2024+); Napo heavy crude (19° API); Oriente blend (24° API); SOTE + OCP pipeline delivery to Balao + Esmeraldas Pacific terminals; USD-denominated pre-sale loans (China Eximbank = output encumbrance signal)
- **Geopolitics:** ITT/Yasuní referendum 2023 = structural supply reduction; China debt = CNPC/CNOOC access guaranteed; OPEC exit 2020 = no quota; Noboa government stability
- **Logistics:** Esmeraldas Balao terminal (SOTE end point); OCP pipeline (private, 450 kb/d capacity); Guayaquil refinery (La Libertad + Esmeraldas); VLCC Pacific loading

### ca-EC-upstream_regulator (ARCH)
- **Supply:** Block licensing; ITT Block 43 production suspension orders; Repsol Tivacuno; Andes Petroleum (Tarapoa) Chinese-operated; ARCH force majeure declarations = key signal
- **Geopolitics:** Indigenous consultation protests (CONAIE = Amazon communities) = pipeline blockade risk; Yasuní court orders; China Eximbank loan renegotiation
- **Logistics:** SOTE (Trans-Ecuadorian) pipeline + OCP pipeline; Esmeraldas terminal cargo scheduling

## Expansion slots (10+)
- ca-EC-ocp — OCP Ecuador pipeline (private, 450 kb/d heavy crude)
- ca-EC-andes_petroleum — Andes Petroleum (CNPC+CNOOC; Tarapoa block)
- ca-EC-conaie — CONAIE indigenous federation (protest/blockade signal)
- ca-EC-flopec — FLOPEC (state tanker fleet; export logistics)
- ca-EC-refineria_pacifico — Refinería del Pacífico project (stalled mega-refinery)

## Anti-patterns
- Skip: El Comercio energy coverage (secondary Ecuadorian press)
- Skip: Ecuador.com tourism/aggregation sites
