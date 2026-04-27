from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_current_user, get_db, require_tenant

from ..models import UserProfile
from ..schemas import ProfileOut, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/me", response_model=ProfileOut)
async def get_my_profile(
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    return await _load_profile_or_404(db, tenant_id, user.id)


@router.patch("/me", response_model=ProfileOut)
async def update_my_profile(
    body: ProfileUpdate,
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    profile = await _load_profile_or_404(db, tenant_id, user.id)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.flush()
    return profile


async def _load_profile_or_404(db: AsyncSession, tenant_id: UUID, user_id: UUID) -> UserProfile:
    stmt = select(UserProfile).where(
        UserProfile.tenant_id == tenant_id, UserProfile.user_id == user_id
    )
    profile = (await db.execute(stmt)).scalar_one_or_none()
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile
