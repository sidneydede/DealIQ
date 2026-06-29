"""Schémas Pydantic — ESG / impact (M19)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EsgIn(BaseModel):
    jobs_total: int | None = None
    jobs_female: int | None = None
    jobs_youth: int | None = None
    women_in_leadership: bool | None = None
    environmental_policy: bool | None = None
    climate_risk_assessed: bool | None = None
    governance_formalized: bool | None = None
    board_independent: bool | None = None
    evidence_note: str | None = Field(default=None, max_length=4000)
    notes: str | None = Field(default=None, max_length=4000)


class RequiredUpdate(BaseModel):
    esg_required: bool


class EsgOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    jobs_total: int | None
    jobs_female: int | None
    jobs_youth: int | None
    women_in_leadership: bool | None
    environmental_policy: bool | None
    climate_risk_assessed: bool | None
    governance_formalized: bool | None
    board_independent: bool | None
    esg_required: bool
    evidence_note: str | None
    notes: str | None
    completeness: float = 0.0
    incomplete_for_dfi: bool = False


class EsgExport(BaseModel):
    company_name: str | None
    indicators: dict
    completeness: float
    evidence_note: str | None
    disclaimer: str
