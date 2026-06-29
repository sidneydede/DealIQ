"""Schémas Pydantic — DD OHADA/SYSCOHADA (M18)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import DealTypeCode


class BalanceLine(BaseModel):
    account: str
    label: str | None = None
    amount: float = 0.0


class ImportIn(BaseModel):
    fiscal_year: str | None = None
    lines: list[BalanceLine]


class ImportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    fiscal_year: str | None
    version: int
    lines: list
    created_at: datetime


class DdAnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    deal_type: DealTypeCode | None
    class_totals: dict
    retraitements: dict
    focus: list
    synthesis: str | None
    grid_version: str | None
    created_at: datetime
