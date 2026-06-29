"""Schémas Pydantic — teaser (M11) et interactions (M12)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import DealTypeCode, Instrument, InteractionStatus, TeaserStatus


class TeaserOut(BaseModel):
    """Vue cabinet (complète, avec lien entreprise)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    deal_type: DealTypeCode | None
    title: str
    sector: str
    zone: str | None
    revenue_band: str | None
    amount_band: str | None
    instrument: Instrument | None
    strengths: list[str]
    summary: str | None
    version: int
    status: TeaserStatus
    created_at: datetime


class TeaserPublicOut(BaseModel):
    """Vue investisseur — anonymisée (PAS de company_id, ni d'identité)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    deal_type: DealTypeCode | None
    title: str
    sector: str
    zone: str | None
    revenue_band: str | None
    amount_band: str | None
    instrument: Instrument | None
    strengths: list[str]
    summary: str | None


class TeaserUpdate(BaseModel):
    strengths: list[str] | None = None
    summary: str | None = None


class InterestCreate(BaseModel):
    note: str | None = Field(default=None, max_length=2000)


class InteractionStatusUpdate(BaseModel):
    status: InteractionStatus


class InteractionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    teaser_id: str
    company_id: str
    investor_id: str
    status: InteractionStatus
    note: str | None
    created_at: datetime
