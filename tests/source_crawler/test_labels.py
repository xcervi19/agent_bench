from __future__ import annotations

import pytest

from source_crawler.labels import LabelError, resolve_promote_labels, validate_config_labels


def test_human_ack_required():
    with pytest.raises(LabelError, match="label_assignment"):
        validate_config_labels(
            source_id="x",
            label_assignment=None,
            document_type="methodology",
            use_for=("pricing_context",),
        )


def test_human_requires_vocab_labels():
    with pytest.raises(LabelError, match="document_type"):
        validate_config_labels(
            source_id="x",
            label_assignment="human",
            document_type=None,
            use_for=("pricing_context",),
        )


def test_agent_ack_allows_empty_labels_at_init():
    validate_config_labels(
        source_id="x",
        label_assignment="agent",
        document_type=None,
        use_for=(),
    )


def test_resolve_human_from_sidecar():
    labels = resolve_promote_labels(
        {
            "source_id": "a",
            "label_assignment": "human",
            "document_type": "methodology",
            "use_for": ["pricing_context"],
        }
    )
    assert labels["document_type"] == "methodology"
    assert labels["use_for"] == ["pricing_context"]


def test_resolve_agent_requires_audit():
    meta = {"source_id": "a", "label_assignment": "agent"}
    with pytest.raises(LabelError, match="QA audit"):
        resolve_promote_labels(meta)
    labels = resolve_promote_labels(
        meta,
        audit_row={
            "document_type": "education",
            "use_for": ["trading_knowhow"],
        },
    )
    assert labels["document_type"] == "education"
