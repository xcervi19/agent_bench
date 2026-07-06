# Source Whitelist Seed (Top 50) — #29

**Status:** planned  
**Lane:** Platform / Data  
**Goal:** Vytvořit minimální "anchor" (whitelist) pro agenta, aby nemohl halucinovat neexistující domény.

## Cíl

Vytvořit `source_whitelist.json` obsahující **50 nejdůležitějších oficiálních entit** relevantních pro trading energií (NOC, Agentury, Burzy, Přístavy).
 Oficiální Vládní & Regulační Orgány
Co hledat: Ministerstva (Energetiky, Ropy, Obchodu), Regulační úřady, Centrální banky.
Příklad: Íránské Ministerstvo ropy (mop.ir), US DOE (energy.gov), ECB.
2. Národní Ropné & Plynové Společnosti (NOC)
Co hledat: Oficiální stránky NOC, jejich tisková oddělení, reporty o produkci/exportu.
Příklad: NIOC (nioc.ir), Saudi Aramco (aramco.com), ADNOC, QatarEnergy.
3. Mezinárodní Agentury & Datové Zdroje
Co hledat: Organizace, které publikují globální statistiky a reporty.
Příklad: IEA (iea.org), EIA (eia.gov), OPEC (opec.org), IEF.
4. Fyzická Infrastruktura (Ports, Terminals, Pipelines)
Co hledat: Port authorities, provozovatelé terminálů, správci potrubí.
Příklad: Iranian Ports & Maritime Organization (pmo.ir), US Coast Guard, provozovatelé LNG terminálů (Sabine Pass, etc.).
5. Burzy & Clearing Houses
Co hledat: Oficiální stránky burz, jejich reporty o objemech a cenách.
Příklad: CME Group (cmegroup.com), ICE (theice.com), NYMEX.
6. Lodní Doprava & Logistika (Shipping)
Co hledat: Datové zdroje o pohybu tankerů (AIS data), portální systémy.
Příklad: MarineTraffic, VesselFinder, oficiální AIS feedy přístavů.
7. Počasí & Klimatická Data
Co hledat: Zdroje pro předpověď poptávky (zima/léto) a dopadů na produkci.
Příklad: NOAA (noaa.gov), ECMWF, specifické energetické weather API.
8. Geopolitické & Diplomatické Zdroje
Co hledat: Ministerstva zahraničí, velvyslanectví, oficiální prohlášení.
Příklad: US State Department (state.gov), Iranian MFA (mfa.ir).
9. Průmyslové Asociace & Technické Reporty
Co hledat: Organizace, které vydávají technické standardy a reporty o kapacitě.
Příklad: API (American Petroleum Institute), IGU (International Gas Union).
10. Lokální & Regionální Média / Sociální Sítě

*   **Co hledat:** Oficiální účty ministerstev a NOC na Telegramu/X (často rychlejší než web).
*   **Příklad:** Oficiální Telegramy íránských úřadů, lokální novináři v oblasti (Rudaw, Libya Herald).

## Proč

Bez tohoto seedu nemá agent "ground truth" a nemůže spolehlivě rozlišit primární zdroje od agregátorů.

## Akceptační kritéria

- [ ] Soubor `source_whitelist.json` existuje v rootu repozitáře.
- [ ] Obsahuje minimálně 50 záznamů.
- [ ] Každý záznam má: `entity`, `domain`, `type` (`official`, `social`, `data_feed`).
- [ ] Top 20 záznamů bylo ručně validováno (doména existuje a je relevantní).
- [ ] Soubor je verzován v Gitu.

## Poznámky

- Generováno pomocí Cursor/Claude na základě kategorií definovaných v ticketu #34.
- Struktura:
  ```json
  [
    {
      "entity": "EIA",
      "domain": "eia.gov",
      "type": "official",
      "notes": "US Energy Information Administration"
    }
  ]
  ```
