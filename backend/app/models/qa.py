"""Q&A rattaché à une mise en relation (M14). Échanges tracés, pas d'email parallèle."""
from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import QAStatus
from app.models.base import Base, TimestampMixin, UUIDMixin


class QAItem(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "qa_items"

    interaction_id: Mapped[str] = mapped_column(
        ForeignKey("interactions.id"), index=True, nullable=False
    )
    asked_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str | None] = mapped_column(Text)
    answered_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    status: Mapped[QAStatus] = mapped_column(
        SAEnum(QAStatus, name="qa_status"), default=QAStatus.ouverte, nullable=False
    )
