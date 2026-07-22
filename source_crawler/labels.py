from __future__ import annotations

from typing import Any, Literal

DOCUMENT_TYPES = frozenset(
    {
        "playbook",
        "methodology",
        "education",
        "official_data",
        "news",
        "reference",
    }
)

USE_FOR_VALUES = frozenset(
    {
        "source_discovery",
        "pricing_context",
        "trading_knowhow",
        "facts",
    }
)

LabelAssignment = Literal["human", "agent"]
LABEL_ASSIGNMENTS = frozenset({"human", "agent"})


class LabelError(ValueError):
    """Invalid or missing RAG labels / human acknowledgment."""


def _as_use_for(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple)):
        items = [str(v) for v in value]
    else:
        raise LabelError(f"use_for must be a list of strings, got {type(value).__name__}")
    return [u for u in items if u]


def validate_vocab(*, document_type: str | None, use_for: list[str]) -> None:
    if not document_type or document_type not in DOCUMENT_TYPES:
        raise LabelError(
            f"document_type must be one of {sorted(DOCUMENT_TYPES)}, got {document_type!r}"
        )
    if not use_for:
        raise LabelError("use_for must contain at least one value")
    unknown = [u for u in use_for if u not in USE_FOR_VALUES]
    if unknown:
        raise LabelError(
            f"unknown use_for {unknown}; allowed={sorted(USE_FOR_VALUES)}"
        )


def validate_config_labels(
    *,
    source_id: str,
    label_assignment: str | None,
    document_type: str | None,
    use_for: tuple[str, ...] | list[str],
) -> None:
    """Human ack required at source init (seed / manual enrollment)."""
    if label_assignment not in LABEL_ASSIGNMENTS:
        raise LabelError(
            f"{source_id}: label_assignment must be 'human' or 'agent' "
            f"(human must acknowledge labeling; got {label_assignment!r})"
        )
    use = _as_use_for(use_for)
    if label_assignment == "human":
        validate_vocab(document_type=document_type, use_for=use)


def labels_from_meta(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "label_assignment": meta.get("label_assignment"),
        "document_type": meta.get("document_type"),
        "use_for": _as_use_for(meta.get("use_for")),
        "proposed_labels": list(meta.get("proposed_labels") or []),
    }


def resolve_promote_labels(
    meta: dict[str, Any],
    *,
    audit_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Resolve production labels for promote.

    human  → sidecar labels only (agent must not override)
    agent  → audit_row labels required (human deferred assignment)
    """
    source_id = str(meta.get("source_id") or "?")
    assignment = meta.get("label_assignment")
    if assignment not in LABEL_ASSIGNMENTS:
        raise LabelError(
            f"{source_id}: missing label_assignment on sidecar "
            "(re-crawl/sync seed with human ack)"
        )

    if assignment == "human":
        document_type = meta.get("document_type")
        use_for = _as_use_for(meta.get("use_for"))
        validate_vocab(document_type=document_type, use_for=use_for)
        return {
            "label_assignment": "human",
            "document_type": document_type,
            "use_for": use_for,
            "proposed_labels": list(meta.get("proposed_labels") or []),
        }

    # agent assignment — human deferred; labels must come from QA audit
    if audit_row is None:
        raise LabelError(
            f"{source_id}: label_assignment=agent requires QA audit labels"
        )
    document_type = audit_row.get("document_type")
    use_for = _as_use_for(audit_row.get("use_for"))
    validate_vocab(document_type=document_type, use_for=use_for)
    proposed = list(audit_row.get("proposed_labels") or [])
    return {
        "label_assignment": "agent",
        "document_type": document_type,
        "use_for": use_for,
        "proposed_labels": proposed,
    }
