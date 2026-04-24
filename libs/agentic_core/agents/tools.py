"""Lightweight tool registry for CrewAI tools."""

from collections.abc import Callable
from typing import Any

_TOOLS: dict[str, Any] = {}


class ToolRegistry:
    @staticmethod
    def register(name: str, tool: Any) -> None:
        _TOOLS[name] = tool

    @staticmethod
    def get(name: str) -> Any:
        return _TOOLS[name]

    @staticmethod
    def all() -> dict[str, Any]:
        return dict(_TOOLS)


def registered_tools(*names: str) -> list[Any]:
    return [_TOOLS[n] for n in names]


def tool_decorator(name: str) -> Callable[[Any], Any]:
    def decorator(obj: Any) -> Any:
        ToolRegistry.register(name, obj)
        return obj

    return decorator
