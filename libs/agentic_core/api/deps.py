"""Reusable FastAPI dependencies: DB session, auth'd user, tenant context."""

from collections.abc import AsyncIterator
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import session_scope, set_tenant_id
from .auth import current_user
from .user_model import User


async def get_db() -> AsyncIterator[AsyncSession]:
    async with session_scope() as session:
        yield session


def get_current_user(user: User = Depends(current_user)) -> User:
    return user


def require_tenant(user: User = Depends(current_user)) -> UUID:
    set_tenant_id(user.tenant_id)
    return user.tenant_id
