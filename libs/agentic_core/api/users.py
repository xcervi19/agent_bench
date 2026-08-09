"""UserManager for fastapi-users."""

from collections.abc import AsyncIterator

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from ..config import get_settings
from ..database import get_sessionmaker, session_scope
from ..logging import get_logger
from . import refresh_tokens
from .user_model import User

log = get_logger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager):
    @property
    def reset_password_token_secret(self) -> str:
        return get_settings().jwt_secret

    @property
    def verification_token_secret(self) -> str:
        return get_settings().jwt_secret

    async def on_after_register(self, user, request=None) -> None:
        log.info("user.registered", user_id=str(user.id), tenant_id=str(user.tenant_id))

    async def on_after_update(self, user, update_dict, request=None) -> None:
        """A new password ends the sessions the old one opened.

        Both paths that set a password land here — `PATCH /users/me` and the
        operator's reset script — and the reason to reset is often that the old
        password leaked. Leaving month-long refresh tokens alive would hand the
        account back to whoever prompted the reset.
        """
        if "password" not in update_dict:
            return
        async with session_scope() as session:
            ended = await refresh_tokens.revoke_all(session, user.id)
        log.info("user.password_changed", user_id=str(user.id), sessions_ended=ended)


async def get_user_db() -> AsyncIterator[SQLAlchemyUserDatabase]:
    maker = get_sessionmaker()
    async with maker() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)
