"""Data room (M13). Solution ACHETÉE — ici métadonnées + connecteur mock.

Cloisonnement strict par deal (RG-M13-03), droits par document/investisseur, watermark
dynamique et logs d'accès (M22).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DataRoomLogAction, DataRoomStatus
from app.models.base import Base, TimestampMixin, UUIDMixin


class DataRoom(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "datarooms"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    provider_ref: Mapped[str | None] = mapped_column(String(120))  # réf. prestataire (mock)
    status: Mapped[DataRoomStatus] = mapped_column(
        SAEnum(DataRoomStatus, native_enum=False),
        default=DataRoomStatus.ouverte,
        nullable=False,
    )
    created_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class DataRoomDocument(UUIDMixin, TimestampMixin, Base):
    """Pièce publiée dans la data room (issue de M4)."""

    __tablename__ = "dataroom_documents"

    dataroom_id: Mapped[str] = mapped_column(ForeignKey("datarooms.id"), index=True, nullable=False)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)


class DataRoomAccess(UUIDMixin, TimestampMixin, Base):
    """Droit d'accès d'un investisseur (gaté KYC + NDA), expirable/révocable."""

    __tablename__ = "dataroom_access"

    dataroom_id: Mapped[str] = mapped_column(ForeignKey("datarooms.id"), index=True, nullable=False)
    investor_id: Mapped[str] = mapped_column(ForeignKey("investors.id"), index=True, nullable=False)
    granted_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class DataRoomLog(UUIDMixin, TimestampMixin, Base):
    """Journal d'accès aux documents (append-only, RG-M13-03)."""

    __tablename__ = "dataroom_logs"

    dataroom_id: Mapped[str] = mapped_column(ForeignKey("datarooms.id"), index=True, nullable=False)
    document_id: Mapped[str | None] = mapped_column(ForeignKey("documents.id"))
    investor_id: Mapped[str | None] = mapped_column(ForeignKey("investors.id"))
    actor_id: Mapped[str | None] = mapped_column(String(36))
    action: Mapped[DataRoomLogAction] = mapped_column(
        SAEnum(DataRoomLogAction, native_enum=False), nullable=False
    )
