from __future__ import annotations

from .base import SourceAdapter

_ADAPTERS: dict[str, type[SourceAdapter]] = {}


def register(adapter_cls: type[SourceAdapter]) -> type[SourceAdapter]:
    name = adapter_cls.name
    if not name:
        raise ValueError(f"{adapter_cls.__name__} has empty name")
    if name in _ADAPTERS:
        raise ValueError(f"adapter already registered: {name}")
    _ADAPTERS[name] = adapter_cls
    return adapter_cls


def get(name: str) -> SourceAdapter:
    try:
        return _ADAPTERS[name]()
    except KeyError as exc:
        raise KeyError(f"unknown adapter: {name!r}; known={sorted(_ADAPTERS)}") from exc


def names() -> list[str]:
    return sorted(_ADAPTERS)


def clear() -> None:
    _ADAPTERS.clear()
