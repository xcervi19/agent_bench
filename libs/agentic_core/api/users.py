"""UserManager for fastapi-users."""

from collections.abc import AsyncIterator

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from ..config import get_settings
from ..database import get_sessionmaker
from ..logging import get_logger
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


async def get_user_db() -> AsyncIterator[SQLAlchemyUserDatabase]:
    maker = get_sessionmaker()
    async with maker() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)
