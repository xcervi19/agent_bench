from __future__ import annotations

import re

STOPWORDS = frozenset(
    {
        "a", "an", "and", "at", "by", "de", "del", "for", "from", "in", "la", "las",
        "los", "of", "on", "or", "the", "to", "via", "with",
    }
)


def tokens(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", text.casefold()) if t}


def significant_tokens(text: str) -> set[str]:
    return {t for t in tokens(text) if len(t) >= 3 and t not in STOPWORDS}
