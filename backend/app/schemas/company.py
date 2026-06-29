"""Schémas Pydantic — entreprise (M2), besoin de financement & type de deal (M24)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import (
    CompanyStage,
    CompanyStatus,
    Country,
    Currency,
    DataReliability,
    DealTypeChangeSource,
    DealTypeCode,
)


# --- M2 : entreprise ---
class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: Country
    sector: str = Field(min_length=1, max_length=120)
    rccm: str | None = None
    stage: CompanyStage | None = None
    revenue_min: float | None = None
    revenue_max: float | None = None
    currency: Currency | None = None  # défaut = devise de la zone du pays


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    sector: str | None = None
    rccm: str | None = None
    stage: CompanyStage | None = None
    revenue_min: float | None = None
    revenue_max: float | None = None
    currency: Currency | None = None


class CompanyStatusUpdate(BaseModel):
    status: CompanyStatus


class FinancingNeedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float | None
    currency: Currency
    use_of_funds: str | None
    horizon: str | None
    deal_type_primary: DealTypeCode | None
    deal_type_secondary: DealTypeCode | None


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    country: Country
    sector: str
    rccm: str | None
    stage: CompanyStage | None
    status: CompanyStatus
    revenue_min: float | None
    revenue_max: float | None
    currency: Currency
    financials_reliability: DataReliability
    owner_id: str | None
    financing_need: FinancingNeedOut | None = None


class DuplicateMatch(BaseModel):
    id: str
    name: str
    rccm: str | None
    reason: str  # "rccm" | "name"


class CompanyCreateResult(BaseModel):
    company: CompanyOut
    duplicate_warnings: list[DuplicateMatch] = []


# --- M24 : type de deal ---
class DealTypeSelect(BaseModel):
    """Sélection / changement du type de deal (entrepreneur ou cabinet)."""

    deal_type_primary: DealTypeCode
    deal_type_secondary: DealTypeCode | None = None
    # Champs de besoin optionnels (capturés à l'onboarding)
    amount: float | None = None
    use_of_funds: str | None = None
    horizon: str | None = None

    @model_validator(mode="after")
    def _coherence(self) -> DealTypeSelect:
        if self.deal_type_secondary and self.deal_type_secondary == self.deal_type_primary:
            raise ValueError("Le type secondaire doit différer du type principal")
        return self


class DealTypeRequalify(BaseModel):
    """Requalification réservée au cabinet — motif obligatoire (RG-M24-04)."""

    deal_type_primary: DealTypeCode
    deal_type_secondary: DealTypeCode | None = None
    motif: str = Field(min_length=3, max_length=1000)

    @model_validator(mode="after")
    def _coherence(self) -> DealTypeRequalify:
        if self.deal_type_secondary and self.deal_type_secondary == self.deal_type_primary:
            raise ValueError("Le type secondaire doit différer du type principal")
        return self


class DealTypeHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    old_primary: DealTypeCode | None
    new_primary: DealTypeCode | None
    old_secondary: DealTypeCode | None
    new_secondary: DealTypeCode | None
    source: DealTypeChangeSource
    actor_id: str | None
    motif: str | None
    created_at: datetime
