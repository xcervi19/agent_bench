from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_current_user, get_db, require_tenant

from ..models import Report
from ..schemas import ReportOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[ReportOut])
async def list_reports(
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
    kind: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[Report]:
    stmt = select(Report).where(Report.tenant_id == tenant_id, Report.user_id == user.id)
    if kind:
        stmt = stmt.where(Report.kind == kind)
    stmt = stmt.order_by(Report.created_at.desc()).limit(limit)
    return list((await db.execute(stmt)).scalars().all())


@router.get("/{report_id}", response_model=ReportOut)
async def get_report(
    report_id: UUID,
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
) -> Report:
    stmt = select(Report).where(
        Report.tenant_id == tenant_id, Report.id == report_id, Report.user_id == user.id
    )
    report = (await db.execute(stmt)).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    return report
