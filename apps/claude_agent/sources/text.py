"""Lexical normalization shared by whitelist (#29) and playbook (#30) matching.

The whitelist and the playbooks are written in English, but topics arrive in
whatever language the operator thinks in. Two normalizations bridge most of
that gap without a translation round-trip:

* diacritics are folded away, so `Hormuzský` and `Hormuzsky` tokenize alike;
* a canonical token also matches an inflected form that extends it, so the
  whitelist stem `hormuz` still matches the Czech genitive `hormuzskeho`.

What is deliberately *not* here is vocabulary: `ropa` will never match `oil`.
Translation is the topic_parse leg's job (#38); this module only makes sure the
proper nouns both sides already share survive tokenization.
"""

from __future__ import annotations

import re
import unicodedata

STOPWORDS = frozenset(
    {
        "a", "an", "and", "at", "by", "de", "del", "for", "from", "in", "la", "las",
        "los", "of", "on", "or", "the", "to", "via", "with",
    }
)

MIN_PREFIX_LEN = 4
"""Shortest canonical token allowed to match by prefix.

Keeps `gas` from swallowing `gasoline` while still admitting real stems like
`suez` and `iran`.
"""

_SPLIT_RE = re.compile(r"[\W_]+", re.UNICODE)


def fold(text: str) -> str:
    """Casefold and strip diacritics down to the base characters.

    NFKD splits `ý` into `y` plus a combining acute; dropping the combining
    marks leaves the ASCII skeleton the whitelist is written in.
    """
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def tokens(text: str) -> set[str]:
    return {t for t in _SPLIT_RE.split(fold(text)) if t}


def significant_tokens(text: str) -> set[str]:
    return {t for t in tokens(text) if len(t) >= 3 and t not in STOPWORDS}


def contains_folded(haystack: str, needle: str) -> bool:
    return fold(needle) in fold(haystack)


def token_matches(canonical: str, topical: str) -> bool:
    """True when `topical` is `canonical` or an inflected form extending it.

    Directional on purpose: Latin-script languages inflect by suffix, so the
    canonical English stem is a prefix of the inflected form and never the
    reverse. Matching both ways would let a topic about ports pull in every
    entity whose name merely starts with those letters.
    """
    if canonical == topical:
        return True
    return len(canonical) >= MIN_PREFIX_LEN and topical.startswith(canonical)


def matched_tokens(canonical: set[str], topical: set[str]) -> set[str]:
    """The canonical tokens that appear in `topical`, inflections included."""
    return {c for c in canonical if any(token_matches(c, t) for t in topical)}


def covers(canonical: set[str], topical: set[str]) -> bool:
    """True when every canonical token appears somewhere in `topical`."""
    return bool(canonical) and matched_tokens(canonical, topical) == canonical


def explained_by(topical: set[str], canonical: set[str]) -> bool:
    """True when every topical token is accounted for by some canonical token.

    The mirror of `covers`, for when the operator's words are the needle
    narrowing down a known entity name rather than the haystack being searched.
    """
    return bool(topical) and all(
        any(token_matches(c, t) for c in canonical) for t in topical
    )
