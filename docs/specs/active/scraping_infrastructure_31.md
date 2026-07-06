# Scraping Infrastructure (Twitter/Telegram) — #31

**Status:** planned  
**Lane:** Platform / Infrastructure  
**Goal:** Mít funkční nástroje pro čtení veřejných sociálních účtů zdarma.

## Cíl

Nastavit a ověřit Python knihovny pro scraping:
-   `twscrape` (nebo alternativu) pro X/Twitter.
-   `Pyrogram` nebo `Telethon` pro Telegram.

## Proč

Oficiální API jsou placená nebo příliš omezená. Pro objevování oficiálních účtů potřebujeme scraping.

## Akceptační kritéria

- [ ] `scripts/scrape_twitter.py` existuje a vrací data z veřejného účtu.
- [ ] `scripts/scrape_telegram.py` existuje a vrací data z veřejného kanálu (`t.me`).
- [ ] Skripty jsou verzovány v Gitu.
- [ ] Dokumentace v `README.md` nebo v hlavičce skriptu popisuje, jak získat API ID pro Telegram.

## Poznámky

- Riziko: Scraping je proti ToS Twitteru. Pro produkci bude potřeba přejít na placené API.
