"""Schémas Pydantic — investisseurs, critères (M9) et matching (M10)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import Currency, InvestorQualifStatus, InvestorType


class InvestorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: InvestorType
    jurisdiction: str | None = None
    team: str | None = None
    user_email: str | None = None  # lie la fiche à un compte investisseur existant


class InvestorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    type: InvestorType | None = None
    jurisdiction: str | None = None
    team: str | None = None
    qualif_status: InvestorQualifStatus | None = None


class CriteriaIn(BaseModel):
    countries: list[str] = []
    sectors: list[str] = []
    instruments: list[str] = []
    deal_types: list[str] = []
    stages: list[str] = []
    exclusions: list[str] = []
    ticket_min: float | None = None
    ticket_max: float | None = None
    ticket_currency: Currency = Currency.XOF
    esg_required: bool = False


class CriteriaOut(CriteriaIn):
    model_config = ConfigDict(from_attributes=True)


class InvestorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    type: InvestorType
    jurisdiction: str | None
    team: str | None
    qualif_status: InvestorQualifStatus
    user_id: str | None
    criteria: CriteriaOut | None = None


class MatchResult(BaseModel):
    investor_id: str
    investor_name: str
    investor_type: InvestorType
    passes_hard_filters: bool
    fit_score: float  # 0..1 (somme pondérée de critères vérifiables)
    reasons: list[str]  # raisons d'exclusion ou points de fit
