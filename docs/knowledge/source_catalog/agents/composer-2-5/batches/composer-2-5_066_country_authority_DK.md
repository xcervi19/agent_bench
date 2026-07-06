# Catalog batch — composer-2-5_066_country_authority_DK.md | DK | 64/64 | 2026-07-06

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DK-ministry_petroleum | DK | — | ministry_petroleum | Danish Energy Agency | ens.dk | government_regulator | official | production,imports,storage_levels | proposed |
| ca-DK-noc | DK | — | noc | (no NOC — Nordsøfonden state partner) | — | noc | — | production,exports | empty |
| ca-DK-mfa | DK | — | mfa | Ministry of Foreign Affairs | um.dk | diplomacy | official | sanctions,export_license | proposed |
| ca-DK-customs_export | DK | — | customs_export | Danish Customs (Skat) | skat.dk | government_regulator | official | exports,export_license,imports | proposed |
| ca-DK-upstream_regulator | DK | — | upstream_regulator | Danish Energy Agency — Licensing | ens.dk | government_regulator | official | production,term_contract | proposed |
| ca-DK-port_maritime_authority | DK | — | port_maritime_authority | Danish Maritime Authority | dma.dk | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-DK-national_exchange | DK | — | national_exchange | Nasdaq Copenhagen | nasdaq.com | exchange | official | pricing_formula | unverified |
| ca-DK-central_bank | DK | — | central_bank | Danmarks Nationalbank | nationalbanken.dk | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-DK-environment_regulator | DK | — | environment_regulator | Danish Environmental Protection Agency | mst.dk | government_regulator | official | refinery_outage,production | proposed |
| ca-DK-coast_guard_navy | DK | — | coast_guard_navy | Royal Danish Navy | forsvaret.dk | government_regulator | official | port_closure,vessel_loading | proposed |

**Tier 1:** ens.dk. North Sea producer (Tyra rebuild). **Fáze 2 COMPLETE** — další: `composer-2-5_067_geo_target_hormuz.md`.

### Progress po merge (návrh)

```json
{
  "phase": "geo_target",
  "phase_index": 0,
  "last_country": "DK",
  "crosscheck_cursor": 0,
  "last_batch_seq": 66
}
```
