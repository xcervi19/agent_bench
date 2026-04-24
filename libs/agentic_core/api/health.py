"""Liveness + readiness endpoints."""

from fastapi import APIRouter
from sqlalchemy import text

from ..database import get_engine

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
async def readiness() -> dict[str, str]:
    async with get_engine().connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ready"}
