"""Historique des changements de type de deal (M24, US-M24-05 / RG-M24-06).

Trace de premier ordre, requêtable depuis la fiche, en complément du journal d'audit (M22).
"""
from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DealTypeChangeSource, DealTypeCode
from app.models.base import Base, TimestampMixin, UUIDMixin


class DealTypeHistory(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "deal_type_history"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), index=True, nullable=False
    )
    old_primary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    new_primary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    old_secondary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    new_secondary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    source: Mapped[DealTypeChangeSource] = mapped_column(
        SAEnum(DealTypeChangeSource, name="deal_type_change_source"), nullable=False
    )
    actor_id: Mapped[str | None] = mapped_column(String(36))
    motif: Mapped[str | None] = mapped_column(Text)  # obligatoire pour une requalification cabinet
