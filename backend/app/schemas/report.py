"""Schéma Pydantic — mini-rapport readiness (M6)."""
from __future__ import annotations

from pydantic import BaseModel

from app.domain.enums import DealTypeCode, ReadinessCategory


class ReportOut(BaseModel):
    company_name: str
    category: ReadinessCategory | None
    category_label: str
    confidence: float | None
    deal_type: DealTypeCode | None
    recommended_instrument: str
    blockers: list[str]
    path_to_bankable: list[str]
    alternative_suggestion: str | None
    recommended_services: list[str]
    disclaimers: list[str]
