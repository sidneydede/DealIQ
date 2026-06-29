"""Teaser anonymisé (M11) et interaction investisseur / mise en relation (M12)."""
from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import (
    DealTypeCode,
    Instrument,
    InteractionStatus,
    TeaserStatus,
)
from app.models.base import Base, TimestampMixin, UUIDMixin


class Teaser(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "teasers"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    deal_type: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    template: Mapped[str | None] = mapped_column(String(120))

    # Contenu anonymisé (RG-M11-01) — aucun champ ré-identifiant.
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str] = mapped_column(String(120))
    zone: Mapped[str | None] = mapped_column(String(40))  # UEMOA/CEMAC, pas le pays précis
    revenue_band: Mapped[str | None] = mapped_column(String(60))
    amount_band: Mapped[str | None] = mapped_column(String(60))
    instrument: Mapped[Instrument | None] = mapped_column(SAEnum(Instrument, name="instrument"))
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    summary: Mapped[str | None] = mapped_column(Text)

    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[TeaserStatus] = mapped_column(
        SAEnum(TeaserStatus, name="teaser_status"), default=TeaserStatus.brouillon, nullable=False
    )
    validated_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class Interaction(UUIDMixin, TimestampMixin, Base):
    """Intérêt investisseur → mise en relation (M12). E-sign NDA = brique achetée (hors scope)."""

    __tablename__ = "interactions"

    teaser_id: Mapped[str] = mapped_column(ForeignKey("teasers.id"), index=True, nullable=False)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    investor_id: Mapped[str] = mapped_column(ForeignKey("investors.id"), index=True, nullable=False)
    status: Mapped[InteractionStatus] = mapped_column(
        SAEnum(InteractionStatus, name="interaction_status"),
        default=InteractionStatus.interesse,
        nullable=False,
    )
    note: Mapped[str | None] = mapped_column(Text)
