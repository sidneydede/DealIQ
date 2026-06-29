"""Entité AuditLog (M22). Journal inaltérable des actions sensibles (RG-M22-01)."""
from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import AuditAction
from app.models.base import Base, TimestampMixin, UUIDMixin


class AuditLog(UUIDMixin, TimestampMixin, Base):
    """Trace : acteur, action, objet, date, méta. Append-only (aucune mutation applicative)."""

    __tablename__ = "audit_logs"

    actor_id: Mapped[str | None] = mapped_column(String(36), index=True)
    actor_email: Mapped[str | None] = mapped_column(String(255))
    action: Mapped[AuditAction] = mapped_column(
        SAEnum(AuditAction, native_enum=False), nullable=False
    )
    object_type: Mapped[str | None] = mapped_column(String(80))
    object_id: Mapped[str | None] = mapped_column(String(36), index=True)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(64))
