"""Pre-assembled auth routers (login/register/users) for apps to mount."""

import uuid
from typing import Any

from fastapi import APIRouter
from fastapi_users import schemas

from .auth import auth_backend, fastapi_users


class UserRead(schemas.BaseUser[uuid.UUID]):
    tenant_id: uuid.UUID


class UserCreate(schemas.BaseUserCreate):
    tenant_id: uuid.UUID


class UserUpdate(schemas.BaseUserUpdate):
    tenant_id: uuid.UUID | None = None


def build_auth_routers(*, public_registration: bool = True) -> list[APIRouter]:
    login = fastapi_users.get_auth_router(auth_backend)
    users = fastapi_users.get_users_router(UserRead, UserUpdate)

    routers = [_prefix(login, "/auth/jwt", ["auth"])]
    if public_registration:
        register = fastapi_users.get_register_router(UserRead, UserCreate)
        routers.append(_prefix(register, "/auth", ["auth"]))
    routers.append(_prefix(users, "/users", ["users"]))
    return routers


def _prefix(router: APIRouter, prefix: str, tags: list[Any]) -> APIRouter:
    wrapper = APIRouter(prefix=prefix, tags=tags)
    wrapper.include_router(router)
    return wrapper
