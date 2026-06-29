"""Mandats & honoraires (M17). Gouvernance des conflits (RG-M17-01/03)."""
from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import (
    Currency,
    FeeStatus,
    FeeType,
    MandateStatus,
    MandateType,
    RepresentedParty,
)
from app.models.base import Base, TimestampMixin, UUIDMixin


class Mandate(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "mandates"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    deal_id: Mapped[str | None] = mapped_column(ForeignKey("deals.id"), index=True)
    # Partie représentée — obligatoire (RG-M17-01).
    represented_party: Mapped[RepresentedParty] = mapped_column(
        SAEnum(RepresentedParty, native_enum=False), nullable=False
    )
    mandate_type: Mapped[MandateType] = mapped_column(
        SAEnum(MandateType, native_enum=False), nullable=False
    )
    exclusive: Mapped[bool] = mapped_column(Boolean, default=False)
    duration_months: Mapped[int | None] = mapped_column(Integer)
    scope: Mapped[str | None] = mapped_column(Text)
    status: Mapped[MandateStatus] = mapped_column(
        SAEnum(MandateStatus, native_enum=False), default=MandateStatus.brouillon,
        nullable=False,
    )
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class Fee(UUIDMixin, TimestampMixin, Base):
    """Honoraire rattaché à un mandat (retainer / success fee / arrangement)."""

    __tablename__ = "fees"

    mandate_id: Mapped[str] = mapped_column(ForeignKey("mandates.id"), index=True, nullable=False)
    fee_type: Mapped[FeeType] = mapped_column(SAEnum(FeeType, native_enum=False), nullable=False)
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2))
    currency: Mapped[Currency] = mapped_column(
        SAEnum(Currency, native_enum=False), default=Currency.XOF
    )
    due_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[FeeStatus] = mapped_column(
        SAEnum(FeeStatus, native_enum=False), default=FeeStatus.du, nullable=False
    )
    note: Mapped[str | None] = mapped_column(Text)
