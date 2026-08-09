"""Pre-assembled auth routers (login/refresh/logout/register/users) for apps to mount."""

import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import schemas
from fastapi_users.authentication import JWTStrategy
from fastapi_users.router import ErrorCode
from pydantic import BaseModel

from ..config import get_settings
from ..database import session_scope
from . import refresh_tokens
from .auth import auth_backend, fastapi_users
from .users import UserManager, get_user_manager


class UserRead(schemas.BaseUser[uuid.UUID]):
    tenant_id: uuid.UUID


class UserCreate(schemas.BaseUserCreate):
    tenant_id: uuid.UUID


class UserUpdate(schemas.BaseUserUpdate):
    tenant_id: uuid.UUID | None = None


class TokenPair(BaseModel):
    """`access_token` keeps the name fastapi-users used, so old clients still read it."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshBody(BaseModel):
    refresh_token: str


def build_auth_routers(*, public_registration: bool = True) -> list[APIRouter]:
    users = fastapi_users.get_users_router(UserRead, UserUpdate)

    routers = [_prefix(_session_router(), "/auth/jwt", ["auth"])]
    if public_registration:
        register = fastapi_users.get_register_router(UserRead, UserCreate)
        routers.append(_prefix(register, "/auth", ["auth"]))
    routers.append(_prefix(users, "/users", ["users"]))
    return routers


def _session_router() -> APIRouter:
    """Login/refresh/logout.

    This replaces fastapi-users' own auth router rather than sitting beside it.
    Its login hands back only an access token, and there is no second call that
    could mint a refresh token for the session — the pair has to be issued
    together, at the one moment the password was actually checked.
    """
    router = APIRouter()

    @router.post("/login", response_model=TokenPair)
    async def login(
        request: Request,
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_manager: Annotated[UserManager, Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy, Depends(auth_backend.get_strategy)],
    ) -> TokenPair:
        user = await user_manager.authenticate(credentials)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        settings = get_settings()
        async with session_scope() as session:
            refresh = await refresh_tokens.issue(
                session,
                user.id,
                lifetime_seconds=settings.jwt_refresh_lifetime_seconds,
            )
        await user_manager.on_after_login(user, request)
        return TokenPair(access_token=await strategy.write_token(user), refresh_token=refresh)

    @router.post("/refresh", response_model=TokenPair)
    async def refresh(
        body: RefreshBody,
        user_manager: Annotated[UserManager, Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy, Depends(auth_backend.get_strategy)],
    ) -> TokenPair:
        settings = get_settings()
        async with session_scope() as session:
            rotated = await refresh_tokens.rotate(
                session,
                body.refresh_token,
                lifetime_seconds=settings.jwt_refresh_lifetime_seconds,
            )
        if rotated is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token"
            )
        user_id, successor = rotated
        user = await user_manager.get(user_id)
        if not user.is_active:
            # Deactivated between refreshes. The row is already spent, so this
            # session ends here whatever the client does next.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="account is inactive"
            )
        return TokenPair(access_token=await strategy.write_token(user), refresh_token=successor)

    @router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
    async def logout(body: RefreshBody) -> Response:
        """Deliberately takes no access token: a session should be endable after it expired."""
        async with session_scope() as session:
            await refresh_tokens.revoke(session, body.refresh_token)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router


def _prefix(router: APIRouter, prefix: str, tags: list[Any]) -> APIRouter:
    wrapper = APIRouter(prefix=prefix, tags=tags)
    wrapper.include_router(router)
    return wrapper
