from __future__ import annotations

from ..models import SourceConfig

_TAGS = ("lng", "outlook", "fundamentals")
_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts", "trading_knowhow"),
}

LNG_REPORT_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="igu_world_lng_report",
        adapter="static_pdf",
        endpoint=(
            "https://www.datocms-assets.com/146580/"
            "1751026179-igu-world-lng-report-2025-hr_dp_c.pdf"
        ),
        title="IGU World LNG Report 2025",
        publisher="International Gas Union",
        interval_hours=8760,
        commodity="natural_gas",
        tier=1,
        domain="market_outlook",
        tags=_TAGS + ("igu", "trade", "infrastructure"),
        extras={
            "download_aliases": [
                "1751026179-igu-world-lng-report-2025-hr_dp_c.pdf",
                "igu-world-lng-report-2025-hr_dp_c.pdf",
                "IGU-World-LNG-Report-2025.pdf",
            ]
        },
        **_LABELS,
    ),
    SourceConfig(
        source_id="bp_energy_outlook",
        adapter="static_pdf",
        endpoint=(
            "https://www.bp.com/api/files/6cqieuqhq4no/master/"
            "7l87OSav7R0jHuVkT06Zj5/8a914ca3361df9d09627f7a60d11f0dc/"
            "bp-energy-outlook-2025.pdf"
        ),
        title="bp Energy Outlook 2025",
        publisher="bp",
        interval_hours=8760,
        commodity="natural_gas",
        tier=1,
        domain="market_outlook",
        tags=_TAGS + ("bp", "energy_outlook", "scenarios"),
        extras={
            "download_aliases": [
                "bp-energy-outlook-2025.pdf",
                "bp_energy_outlook_2025.pdf",
            ]
        },
        **_LABELS,
    ),
]
