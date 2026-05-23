from __future__ import annotations

EIA_COUNTRY_CODES: tuple[str, ...] = (
    "SAU",
    "RUS",
    "USA",
    "IRQ",
    "IRN",
    "KWT",
    "ARE",
    "NGA",
    "VEN",
    "BRA",
    "CAN",
    "MEX",
    "CHN",
    "IND",
    "NOR",
    "KAZ",
    "AGO",
    "LBY",
    "DZA",
    "QAT",
    "OMN",
    "COL",
    "ECU",
    "GBR",
    "AUS",
    "IDN",
    "MYS",
    "VNM",
    "EGY",
    "TUR",
)


def eia_country_overview_urls() -> list[str]:
    return [
        f"https://www.eia.gov/international/overview/country/{code}"
        for code in EIA_COUNTRY_CODES
    ]
