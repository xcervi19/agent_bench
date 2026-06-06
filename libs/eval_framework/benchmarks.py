"""Pluggable benchmark providers.

A benchmark provider yields :class:`RunArtifacts` for a topic so the *same*
rubric can score our agent against external baselines without redesigning the
evaluation system. Future providers (generic LLM, internet-disabled model,
standard search workflow, human analyst, Bloomberg-/Reuters-style report) only
need to implement :meth:`BenchmarkProvider.produce` and register themselves.

Registration is open: call :func:`register_provider` (or use the
``@benchmark_provider`` decorator) from any module to add a provider without
touching the framework core.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .artifacts import RunArtifacts, load_run


class BenchmarkProvider(ABC):
    """Produces a comparable run output for a topic.

    ``name`` identifies the provider (e.g. ``newsfind``, ``generic_llm``,
    ``internet_disabled``, ``human_analyst``, ``bloomberg_style``).
    ``kind`` groups providers for reporting (e.g. ``agent`` vs ``baseline``).
    """

    name: str = "provider"
    kind: str = "baseline"

    @abstractmethod
    def produce(self, topic: str, **kwargs) -> RunArtifacts:
        """Return run artifacts for ``topic`` (frozen, evaluable)."""


class FixtureProvider(BenchmarkProvider):
    """Provider backed by an already-produced run directory.

    Used for our own agent output and for any baseline captured to disk
    (e.g. a Bloomberg-style report exported to the artifact layout).
    """

    def __init__(self, name: str, run_dir: str, kind: str = "agent") -> None:
        self.name = name
        self.kind = kind
        self.run_dir = run_dir

    def produce(self, topic: str, **kwargs) -> RunArtifacts:
        artifacts = load_run(self.run_dir, label=self.name)
        if topic:
            artifacts.topic = artifacts.topic or topic
        return artifacts


_REGISTRY: dict[str, BenchmarkProvider] = {}


def register_provider(provider: BenchmarkProvider, *, overwrite: bool = False) -> BenchmarkProvider:
    if provider.name in _REGISTRY and not overwrite:
        raise ValueError(f"Benchmark provider '{provider.name}' already registered")
    _REGISTRY[provider.name] = provider
    return provider


def benchmark_provider(name: str, kind: str = "baseline"):
    """Class decorator that instantiates and registers a zero-arg provider."""

    def wrap(cls):
        instance = cls()
        instance.name = name
        instance.kind = kind
        register_provider(instance, overwrite=True)
        return cls

    return wrap


def get_provider(name: str) -> BenchmarkProvider:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown benchmark provider '{name}'. Registered: {list_providers()}")
    return _REGISTRY[name]


def list_providers() -> list[str]:
    return sorted(_REGISTRY)


def clear_registry() -> None:
    _REGISTRY.clear()
