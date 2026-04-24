"""Request-scoped middleware: request id, structured logging context."""

from uuid import uuid4

import structlog
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from ..logging import get_logger

log = get_logger("http")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id, path=request.url.path)
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        structlog.contextvars.clear_contextvars()
        return response


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
