"""Historique des versions de la fiche entreprise (US-M2-03)."""
from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class CompanyHistory(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "company_history"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(60), nullable=False)
    old_value: Mapped[str | None] = mapped_column(String(500))
    new_value: Mapped[str | None] = mapped_column(String(500))
    changed_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
