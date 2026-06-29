"""Demande de devis / RDV (M7). Tracée pour le cabinet (conversion sans prix public)."""
from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DealTypeCode
from app.models.base import Base, TimestampMixin, UUIDMixin


class QuoteRequest(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quote_requests"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), index=True, nullable=False
    )
    requested_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    offer_key: Mapped[str | None] = mapped_column(String(60))  # offre visée (M7)
    deal_type: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    message: Mapped[str | None] = mapped_column(Text)
    contact_phone: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(30), default="nouveau")  # nouveau | traite
