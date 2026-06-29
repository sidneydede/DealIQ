"""Espace mission / préparation (M8)."""
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DeliverableKind, DeliverableStatus, MissionStatus, Role
from app.models.base import Base, TimestampMixin, UUIDMixin


class Mission(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "missions"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    status: Mapped[MissionStatus] = mapped_column(
        SAEnum(MissionStatus, name="mission_status"), default=MissionStatus.en_cours, nullable=False
    )
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class MissionTask(UUIDMixin, TimestampMixin, Base):
    """Tâche de la checklist investor-ready."""

    __tablename__ = "mission_tasks"

    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True, nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Deliverable(UUIDMixin, TimestampMixin, Base):
    """Livrable versionné (BP, modèle financier, teaser…) avec double validation."""

    __tablename__ = "deliverables"

    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True, nullable=False)
    kind: Mapped[DeliverableKind] = mapped_column(SAEnum(DeliverableKind, name="deliverable_kind"))
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[DeliverableStatus] = mapped_column(
        SAEnum(DeliverableStatus, name="deliverable_status"),
        default=DeliverableStatus.brouillon,
        nullable=False,
    )
    note: Mapped[str | None] = mapped_column(Text)


class MissionReview(UUIDMixin, TimestampMixin, Base):
    """Validation de revue (double validation analyste + senior, RG-M8-02)."""

    __tablename__ = "mission_reviews"

    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True, nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role"), nullable=False)
    reviewer_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    note: Mapped[str | None] = mapped_column(Text)
