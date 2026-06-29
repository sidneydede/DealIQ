"""Deal & pipeline d'exécution (M16)."""
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DealStage, DealTypeCode
from app.models.base import Base, TimestampMixin, UUIDMixin


class Deal(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "deals"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    investor_id: Mapped[str] = mapped_column(ForeignKey("investors.id"), index=True, nullable=False)
    interaction_id: Mapped[str | None] = mapped_column(ForeignKey("interactions.id"))
    deal_type: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, native_enum=False)
    )
    stage: Mapped[DealStage] = mapped_column(
        SAEnum(DealStage, native_enum=False), default=DealStage.interesse, nullable=False
    )
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))  # consultant en charge


class DealStageHistory(UUIDMixin, TimestampMixin, Base):
    """Historique des changements d'étape (traçabilité RG-M16-02)."""

    __tablename__ = "deal_stage_history"

    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), index=True, nullable=False)
    old_stage: Mapped[DealStage | None] = mapped_column(SAEnum(DealStage, native_enum=False))
    new_stage: Mapped[DealStage] = mapped_column(
        SAEnum(DealStage, native_enum=False), nullable=False
    )
    actor_id: Mapped[str | None] = mapped_column(String(36))
    note: Mapped[str | None] = mapped_column(Text)


class DealMilestone(UUIDMixin, TimestampMixin, Base):
    """Jalon de closing (initialisé selon le type de deal, RG-M16-03)."""

    __tablename__ = "deal_milestones"

    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), index=True, nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
