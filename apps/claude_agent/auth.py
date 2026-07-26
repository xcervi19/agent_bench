"""Who is calling the topic API: a user (JWT) or the service key (ops/harness).

Product path: `Authorization: Bearer <jwt>` -> Principal bound to a user id.
Ops path: `X-API-Key` -> service Principal with access to every topic. Gated by
CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS so product deployments can turn it off.
"""

import os
import uuid
from dataclasses import dataclass
from typing import Annotated

from agentic_core.api.auth import fastapi_users
from agentic_core.api.user_model import User
from fastapi import Depends, Header, HTTPException

from .config import ClaudeAgentSettings, get_settings

_optional_user = fastapi_users.current_user(active=True, optional=True)


@dataclass(frozen=True)
class Principal:
    user_id: uuid.UUID | None

    @property
    def is_service(self) -> bool:
        return self.user_id is None


async def resolve_principal(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
    user: Annotated[User | None, Depends(_optional_user)] = None,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> Principal:
    if user is not None:
        return Principal(user_id=user.id)
    if _service_key_accepted(settings, x_api_key):
        return Principal(user_id=None)
    raise HTTPException(status_code=401, detail="authentication required")


def _service_key_accepted(settings: ClaudeAgentSettings, key: str | None) -> bool:
    if not settings.allow_service_key_bypass:
        return False
    if not settings.api_key:
        return True
    return key == settings.api_key


CurrentPrincipal = Annotated[Principal, Depends(resolve_principal)]


def bootstrap_auth_env() -> None:
    """Point agentic_core (users table + JWT) at the claude_agent database.

    agentic_core.Settings also requires redis/S3 values that auth never reads;
    placeholders keep it constructible without a full platform .env.
    """
    settings = get_settings()
    os.environ["DATABASE_URL"] = settings.database_url
    os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")
    os.environ.setdefault("S3_ENDPOINT_URL", "http://127.0.0.1:9000")
    os.environ.setdefault("S3_ACCESS_KEY", "unused")
    os.environ.setdefault("S3_SECRET_KEY", "unused")
