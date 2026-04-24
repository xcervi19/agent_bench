"""Shared LLM factory for all crews."""

from functools import lru_cache

from crewai import LLM

from agentic_core.config import get_settings


@lru_cache
def default_llm() -> LLM:
    s = get_settings()
    return LLM(model=s.openai_model, api_key=s.openai_api_key)
