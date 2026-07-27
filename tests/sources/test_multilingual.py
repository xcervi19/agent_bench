"""Multilingual grounding for the lexical source resolver (#38).

The whitelist and playbooks are English. These tests pin what the deterministic
layer can and cannot do about that: it rescues proper nouns the two languages
already share (`Hormuzský` → `hormuz`) and gives up on vocabulary that differs
(`Ormuz`, `ropa`). The second case is the topic_parse leg's job, and pinning it
here keeps anyone from "fixing" it with ever-looser fuzzy matching.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from apps.claude_agent.sources.discover import discover_sources_for_topic
from apps.claude_agent.sources.text import (
    covers,
    explained_by,
    fold,
    matched_tokens,
    significant_tokens,
    token_matches,
    tokens,
)
from apps.claude_agent.sources.whitelist import entities_named_in, load_whitelist

REPO = Path(__file__).resolve().parents[2]
WHITELIST = REPO / "source_whitelist.json"
PLAYBOOKS = REPO / "local_knowledge_sources" / "playbooks"

CZECH_HORMUZ = "Situace kolem Hormuzského průplavu, ropa a plyn a dopady na dodávky"


@pytest.fixture(scope="module")
def whitelist():
    return load_whitelist(WHITELIST)


def topic_result(topic: str):
    return discover_sources_for_topic(
        topic,
        whitelist_path=WHITELIST,
        playbooks_dir=PLAYBOOKS,
    )


# ── Folding ─────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Hormuzský", "hormuzsky"),
        ("PETRÓLEO", "petroleo"),
        ("Ürünler", "urunler"),
        ("Ånderson", "anderson"),
        ("NIOC", "nioc"),
    ],
)
def test_fold_strips_diacritics_and_case(raw: str, expected: str):
    assert fold(raw) == expected


def test_tokens_no_longer_shatter_accented_words():
    """The old ASCII-only split turned `México` into `m` + `xico`."""
    assert tokens("Banco de México") == {"banco", "de", "mexico"}


def test_tokens_keep_non_latin_scripts_whole():
    """They will not match an English whitelist, but silently dropping them
    would hide that from anyone debugging a zero-target topic."""
    assert tokens("النفط الخام") == {"النفط", "الخام"}


# ── Inflection ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "canonical,topical",
    [
        ("hormuz", "hormuzskeho"),
        ("iran", "iranian"),
        ("suez", "suezsky"),
        ("nioc", "nioc"),
    ],
)
def test_canonical_stem_matches_inflected_form(canonical: str, topical: str):
    assert token_matches(canonical, topical)


@pytest.mark.parametrize(
    "canonical,topical",
    [
        ("gas", "gasoline"),  # below MIN_PREFIX_LEN: too generic to extend
        ("oil", "oilfield"),
        ("hormuz", "hormu"),  # truncation is not inflection
        ("portugal", "port"),  # only the canonical side may be the prefix
    ],
)
def test_prefix_matching_stays_bounded(canonical: str, topical: str):
    assert not token_matches(canonical, topical)


def test_matching_helpers_agree_on_direction():
    entity = significant_tokens("Strait of Hormuz")
    topic = significant_tokens(CZECH_HORMUZ)
    assert matched_tokens(entity, topic) == {"hormuz"}
    # `strait` is absent from the Czech text, so the entity is not fully named.
    assert not covers(entity, topic)
    assert covers({"hormuz"}, topic)
    assert explained_by({"hormuzskeho"}, {"hormuz", "strait"})


# ── End to end ──────────────────────────────────────────────────────────────


def test_czech_topic_grounds_through_shared_proper_noun():
    result = topic_result(CZECH_HORMUZ)
    assert "strait_of_hormuz.md" in result["playbook_refs"]
    assert result["source_targets"]["entities"]


def test_czech_and_english_topics_agree_on_the_playbook():
    czech = set(topic_result(CZECH_HORMUZ)["playbook_refs"])
    english = set(topic_result("Strait of Hormuz oil and gas supply")["playbook_refs"])
    assert czech <= english


def test_targets_stay_whitelisted_under_folding(whitelist):
    known = {e.domain for e in whitelist}
    domains = {
        d
        for e in topic_result(CZECH_HORMUZ)["source_targets"]["entities"]
        for d in e["known_domains"]
    }
    assert domains
    assert domains <= known


def test_translated_vocabulary_is_out_of_reach_without_topic_parse():
    """Portuguese `Ormuz` shares no stem with `Hormuz`, so the lexical layer
    cannot reach it. This is the gap topic_parse (#38) exists to close."""
    assert topic_result("Estreito de Ormuz e o fornecimento de petroleo")[
        "source_targets"
    ]["entities"] == []


def test_english_topics_are_unaffected(whitelist):
    """Folding and prefix matching must not cost the English path any recall."""
    hits = entities_named_in(whitelist, "NIOC crude exports under sanctions")
    assert "nioc.ir" in {h.domain for h in hits}
    assert not entities_named_in(whitelist, "crude exports rebound")
