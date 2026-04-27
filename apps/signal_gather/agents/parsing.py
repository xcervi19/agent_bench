"""Parse JSON-ish CrewAI outputs into Python dicts/lists."""

import json
import re
from typing import Any

_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)
_FIRST_OBJECT = re.compile(r"\{.*\}", re.DOTALL)
_FIRST_ARRAY = re.compile(r"\[.*\]", re.DOTALL)


def parse_json_object(raw: Any) -> dict[str, Any]:
    text = _strip_fences(_to_text(raw))
    match = _FIRST_OBJECT.search(text)
    if not match:
        return {}
    return _safe_loads(match.group(0)) or {}


def parse_json_array(raw: Any) -> list[Any]:
    text = _strip_fences(_to_text(raw))
    match = _FIRST_ARRAY.search(text)
    if not match:
        return []
    parsed = _safe_loads(match.group(0))
    return parsed if isinstance(parsed, list) else []


def _to_text(raw: Any) -> str:
    if isinstance(raw, dict):
        return raw.get("result", json.dumps(raw))
    return str(raw or "")


def _strip_fences(text: str) -> str:
    match = _FENCE.search(text)
    return match.group(1) if match else text


def _safe_loads(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
