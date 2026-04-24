"""Task registry: apps register callables by string name for safe enqueueing."""

from collections.abc import Callable
from typing import Any

TaskFn = Callable[..., Any]
TASK_REGISTRY: dict[str, TaskFn] = {}


def task(name: str) -> Callable[[TaskFn], TaskFn]:
    """Decorator: register a task handler under a stable string name."""

    def decorator(fn: TaskFn) -> TaskFn:
        TASK_REGISTRY[name] = fn
        return fn

    return decorator
