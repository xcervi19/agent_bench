from __future__ import annotations

from ..models import SourceConfig

_TAGS = ("methodology", "pricing", "pra")
_LABELS = {
    "label_assignment": "human",
    "document_type": "methodology",
    "use_for": ("pricing_context",),
}

PRICING_METHODOLOGY_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="argus_crude_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.argusmedia.com/-/media/project/argusmedia/mainsite/"
            "english/documents-and-files/methodology/argus-crude.pdf"
        ),
        title="Argus Crude Methodology and Specifications Guide",
        publisher="Argus Media",
        interval_hours=720,
        tier=1,
        tags=_TAGS + ("argus", "crude"),
        **_LABELS,
    ),
    SourceConfig(
        source_id="argus_americas_crude_methodology",
        adapter="static_pdf",
        endpoint="https://www.argusmedia.com/-/media/Files/methodology/argus-americas-crude.ashx",
        title="Argus Americas Crude Methodology",
        publisher="Argus Media",
        interval_hours=720,
        region="americas",
        tier=1,
        tags=_TAGS + ("argus", "crude", "americas"),
        **_LABELS,
    ),
    SourceConfig(
        source_id="argus_european_products_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.argusmedia.com/-/media/project/argusmedia/mainsite/"
            "english/documents-and-files/methodology/argus-european-products.pdf"
        ),
        title="Argus European Products Methodology",
        publisher="Argus Media",
        interval_hours=720,
        region="europe",
        tier=1,
        tags=_TAGS + ("argus", "products", "europe"),
        **_LABELS,
    ),
    SourceConfig(
        source_id="argus_us_products_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.argusmedia.com/-/media/project/argusmedia/mainsite/"
            "english/documents-and-files/methodology/argus-us-products.pdf"
        ),
        title="Argus US Products Methodology",
        publisher="Argus Media",
        interval_hours=720,
        region="americas",
        tier=1,
        tags=_TAGS + ("argus", "products", "us"),
        **_LABELS,
    ),
    SourceConfig(
        source_id="platts_assessments_methodology_guide",
        adapter="static_pdf",
        endpoint=(
            "https://www.spglobal.com/content/dam/spglobal/ci/en/documents/platts/"
            "en/our-methodology/methodology-specifications/"
            "platts-assessments-methodology-guide.pdf"
        ),
        title="Platts Assessments Methodology Guide",
        publisher="S&P Global Commodity Insights",
        interval_hours=2160,
        tier=1,
        tags=_TAGS + ("platts", "moc"),
        extras={
            "download_aliases": [
                "platts-assessments-methodology-guide.pdf",
            ]
        },
        **_LABELS,
    ),
    SourceConfig(
        source_id="platts_americas_crude_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.spglobal.com/commodityinsights/PlattsContent/_assets/_files/"
            "en/our-methodology/methodology-specifications/americas-crude-methodology.pdf"
        ),
        title="Platts Americas Crude Oil Specifications Guide",
        publisher="S&P Global Commodity Insights",
        interval_hours=720,
        region="americas",
        tier=1,
        tags=_TAGS + ("platts", "crude", "americas"),
        extras={
            "download_aliases": [
                "america-crude-specifications.pdf",
                "americas-crude-specifications.pdf",
            ]
        },
        **_LABELS,
    ),
    SourceConfig(
        source_id="platts_emea_crude_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.spglobal.com/platts/PlattsContent/_assets/_files/en/"
            "our-methodology/methodology-specifications/emea-crude-methodology.pdf"
        ),
        title="Platts Europe and Africa Crude Oil Specifications Guide",
        publisher="S&P Global Commodity Insights",
        interval_hours=720,
        region="europe_africa",
        tier=1,
        tags=_TAGS + ("platts", "crude", "emea"),
        extras={
            "download_aliases": [
                "emea-crude-specifications.pdf",
            ]
        },
        **_LABELS,
    ),
    SourceConfig(
        source_id="platts_apag_crude_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.spglobal.com/platts/PlattsContent/_assets/_files/en/"
            "our-methodology/methodology-specifications/apag-crude-methodology.pdf"
        ),
        title="Platts Asia Pacific and Middle East Crude Oil Specifications Guide",
        publisher="S&P Global Commodity Insights",
        interval_hours=720,
        region="asia_pacific",
        tier=1,
        tags=_TAGS + ("platts", "crude", "apag"),
        extras={
            "download_aliases": [
                "apac-me-crude-specifications.pdf",
                "apag-crude-specifications.pdf",
            ]
        },
        **_LABELS,
    ),
    SourceConfig(
        source_id="platts_europe_africa_refined_methodology",
        adapter="static_pdf",
        endpoint=(
            "https://www.spglobal.com/platts/PlattsContent/_assets/_files/en/"
            "our-methodology/methodology-specifications/"
            "europe-africa-refined-products-methodology.pdf"
        ),
        title="Platts Europe and Africa Refined Oil Products Specifications Guide",
        publisher="S&P Global Commodity Insights",
        interval_hours=720,
        region="europe_africa",
        tier=1,
        tags=_TAGS + ("platts", "products", "europe"),
        extras={
            "download_aliases": [
                "refined-products-europe-africa-specifications.pdf",
                "europe-africa-refined-products-specifications.pdf",
            ]
        },
        **_LABELS,
    ),
]
