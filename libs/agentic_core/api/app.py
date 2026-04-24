"""FastAPI application factory used by every app on the framework."""

from collections.abc import Iterable

from fastapi import APIRouter, FastAPI

from ..logging import configure_logging
from .health import router as health_router
from .middleware import register_middleware


def create_app(*, title: str, routers: Iterable[APIRouter]) -> FastAPI:
    configure_logging()
    app = FastAPI(title=title)
    register_middleware(app)
    app.include_router(health_router)
    for router in routers:
        app.include_router(router)
    return app
