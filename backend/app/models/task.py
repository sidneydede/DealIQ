"""Tâches & relances CRM (M20, US-M20-02)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import TaskStatus
from app.models.base import Base, TimestampMixin, UUIDMixin


class CrmTask(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "crm_tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, native_enum=False), default=TaskStatus.a_faire, nullable=False
    )
    # Liens optionnels : dossier concerné, responsable, créateur.
    company_id: Mapped[str | None] = mapped_column(ForeignKey("companies.id"), index=True)
    assignee_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    created_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    done_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
