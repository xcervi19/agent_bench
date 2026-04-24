"""JWT auth wiring (bearer transport + JWT strategy + FastAPIUsers)."""

from uuid import UUID

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from ..config import get_settings
from .user_model import User
from .users import get_user_manager


def _jwt_strategy() -> JWTStrategy:
    s = get_settings()
    return JWTStrategy(secret=s.jwt_secret, lifetime_seconds=s.jwt_lifetime_seconds)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=_jwt_strategy
)

fastapi_users: FastAPIUsers[User, UUID] = FastAPIUsers[User, UUID](
    get_user_manager, [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
