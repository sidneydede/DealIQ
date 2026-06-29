"""Schémas Pydantic — mandats & honoraires (M17)."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import (
    Currency,
    FeeStatus,
    FeeType,
    MandateStatus,
    MandateType,
    RepresentedParty,
)


class MandateCreate(BaseModel):
    represented_party: RepresentedParty
    mandate_type: MandateType
    exclusive: bool = False
    duration_months: int | None = None
    scope: str | None = Field(default=None, max_length=4000)
    deal_id: str | None = None


class MandateUpdate(BaseModel):
    status: MandateStatus | None = None
    signed: bool | None = None
    exclusive: bool | None = None
    scope: str | None = None


class MandateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    deal_id: str | None
    represented_party: RepresentedParty
    mandate_type: MandateType
    exclusive: bool
    duration_months: int | None
    scope: str | None
    status: MandateStatus
    signed: bool
    created_at: datetime


class FeeCreate(BaseModel):
    fee_type: FeeType
    amount: float | None = None
    currency: Currency = Currency.XOF
    due_date: date | None = None
    note: str | None = Field(default=None, max_length=2000)


class FeeUpdate(BaseModel):
    status: FeeStatus


class FeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mandate_id: str
    fee_type: FeeType
    amount: float | None
    currency: Currency
    due_date: date | None
    status: FeeStatus
    note: str | None


class ConflictItem(BaseModel):
    company_id: str
    company_name: str | None
    represented_parties: list[RepresentedParty]
    has_conflict: bool
    disclosure: str | None
