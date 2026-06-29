"""Configuration de la grille de readiness (M5) — paramétrable, versionnée (calibrage métier)."""
from __future__ import annotations

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class ScoringConfig(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "scoring_configs"

    version: Mapped[str] = mapped_column(String(40), nullable=False)
    base_weights: Mapped[dict] = mapped_column(JSON, default=dict)
    caps: Mapped[dict] = mapped_column(JSON, default=dict)
    thresholds: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[dict] = mapped_column(JSON, default=dict)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    updated_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
