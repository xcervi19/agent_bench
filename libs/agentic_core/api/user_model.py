"""Tenant-aware User table used by fastapi-users."""

from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
