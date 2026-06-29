"""Schémas Pydantic — cockpit cabinet (M20)."""
from __future__ import annotations

from pydantic import BaseModel

from app.domain.enums import CompanyStatus, Country, DealTypeCode, ReadinessCategory


class CockpitItem(BaseModel):
    company_id: str
    name: str
    country: Country
    sector: str
    status: CompanyStatus
    deal_type_primary: DealTypeCode | None
    readiness_category: ReadinessCategory | None
    score_total: float | None
    quote_requests: int
    days_open: int
    sla_breach: bool


class QuoteStatusUpdate(BaseModel):
    status: str  # nouveau | traite
