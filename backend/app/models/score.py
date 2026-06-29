"""Entité Score — Financing Readiness Score (M5). Usage interne ; jamais exposé brut."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Float, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import DealTypeCode, ReadinessCategory
from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.company import Company


class Score(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "scores"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    # Sous-scores par dimension (Annexe C) — structure JSON
    subscores: Mapped[dict] = mapped_column(JSON, default=dict)
    total: Mapped[float | None] = mapped_column(Float)
    category: Mapped[ReadinessCategory | None] = mapped_column(
        SAEnum(ReadinessCategory, native_enum=False)
    )
    confidence: Mapped[float | None] = mapped_column(Float)  # indice de confiance (RG-M5-03)
    grid_version: Mapped[str | None] = mapped_column(String(40))
    deal_type_applied: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, native_enum=False)
    )

    company: Mapped[Company] = relationship(back_populates="score")
