"""Convert a user's natural-language description into a structured UserProfile."""

from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import ProfileSetupCrew
from ..agents.parsing import parse_json_object
from ..models import UserProfile

ALLOWED_RISK = {"low", "medium", "high"}
ALLOWED_CADENCE = {"daily", "weekly", "none"}
ALLOWED_CHANNELS = {"web", "email", "chat"}


@task("signal_gather.setup_profile")
async def setup_profile(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    user_id = UUID(payload["user_id"])
    text = payload.get("text", "")

    parsed = await _interpret_text(tenant_id, text)
    profile = await _upsert_profile(tenant_id, user_id, text, parsed)
    return {"profile_id": str(profile.id)}


async def _interpret_text(tenant_id: UUID, text: str) -> dict[str, Any]:
    result = await ProfileSetupCrew().run(
        CrewRunContext(tenant_id=tenant_id, inputs={"text": text})
    )
    return parse_json_object(result.output)


async def _upsert_profile(
    tenant_id: UUID, user_id: UUID, raw_text: str, parsed: dict[str, Any]
) -> UserProfile:
    async with session_scope() as db:
        existing = await _load_existing(db, tenant_id, user_id)
        profile = existing or UserProfile(id=uuid4(), tenant_id=tenant_id, user_id=user_id)
        _apply_parsed(profile, parsed)
        profile.raw_setup_text = raw_text
        if existing is None:
            db.add(profile)
    return profile


async def _load_existing(db, tenant_id: UUID, user_id: UUID) -> UserProfile | None:
    stmt = select(UserProfile).where(
        UserProfile.tenant_id == tenant_id, UserProfile.user_id == user_id
    )
    return (await db.execute(stmt)).scalar_one_or_none()


def _apply_parsed(profile: UserProfile, parsed: dict[str, Any]) -> None:
    profile.display_name = parsed.get("display_name") or profile.display_name
    profile.commodities = _string_list(parsed.get("commodities"))
    profile.regions = _string_list(parsed.get("regions"))
    profile.themes = _string_list(parsed.get("themes"))
    profile.risk_appetite = _enum(parsed.get("risk_appetite"), ALLOWED_RISK, "medium")
    profile.alert_channels = _filter_channels(parsed.get("alert_channels"))
    profile.briefing_cadence = _enum(parsed.get("briefing_cadence"), ALLOWED_CADENCE, "daily")
    profile.impact_threshold = float(parsed.get("impact_threshold") or 0.6)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip().lower() for v in value if str(v).strip()]


def _filter_channels(value: Any) -> list[str]:
    return [c for c in _string_list(value) if c in ALLOWED_CHANNELS] or ["web"]


def _enum(value: Any, allowed: set[str], default: str) -> str:
    candidate = (value or default).lower()
    return candidate if candidate in allowed else default
