from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_current_user, get_db, require_tenant

from ..models import Alert
from ..schemas import AlertOut, AlertReadUpdate

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertOut])
async def list_alerts(
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
    unread_only: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[Alert]:
    stmt = select(Alert).where(Alert.tenant_id == tenant_id, Alert.user_id == user.id)
    if unread_only:
        stmt = stmt.where(Alert.read.is_(False))
    stmt = stmt.order_by(Alert.created_at.desc()).limit(limit)
    return list((await db.execute(stmt)).scalars().all())


@router.patch("/{alert_id}", response_model=AlertOut)
async def mark_alert(
    alert_id: UUID,
    body: AlertReadUpdate,
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
) -> Alert:
    stmt = select(Alert).where(
        Alert.tenant_id == tenant_id, Alert.id == alert_id, Alert.user_id == user.id
    )
    alert = (await db.execute(stmt)).scalar_one_or_none()
    if alert is None:
        raise HTTPException(status_code=404, detail="alert not found")
    alert.read = body.read
    await db.flush()
    return alert
