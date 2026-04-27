"""OpenAI text embeddings. Returns None if no API key (vector ops gracefully skipped)."""

from functools import lru_cache

from openai import OpenAI

from agentic_core.config import get_settings

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536


@lru_cache
def _client() -> OpenAI | None:
    key = get_settings().openai_api_key
    if not key:
        return None
    return OpenAI(api_key=key)


def embed(text: str) -> list[float] | None:
    client = _client()
    if client is None:
        return None
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding
