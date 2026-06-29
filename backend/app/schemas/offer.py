"""Schémas Pydantic — offres & demande de devis (M7)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import DealTypeCode


class OfferOut(BaseModel):
    key: str
    label: str
    pricing: str  # gratuit | ticket_engagement | sur_devis — jamais de montant
    deliverables: list[str]


class OffersResponse(BaseModel):
    offers: list[OfferOut]
    anti_pay_to_play: str


class QuoteCreate(BaseModel):
    offer_key: str | None = None
    message: str | None = Field(default=None, max_length=2000)
    contact_phone: str | None = Field(default=None, max_length=50)


class QuoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    offer_key: str | None
    deal_type: DealTypeCode | None
    message: str | None
    contact_phone: str | None
    status: str
    created_at: datetime
