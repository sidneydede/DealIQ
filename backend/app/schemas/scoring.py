"""Schémas Pydantic — configuration & simulation du scoring (M5, calibrage)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ScoringConfigUpdate(BaseModel):
    version: str | None = None
    base_weights: dict | None = None
    caps: dict | None = None
    thresholds: dict | None = None
    confidence: dict | None = None


class ScoringConfigOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    version: str
    base_weights: dict
    caps: dict
    thresholds: dict
    confidence: dict
    active: bool
    # Pondérations effectives par type de deal (référentiel DealType)
    deal_type_weights: dict = {}


class SimulateIn(BaseModel):
    company_id: str | None = None
    deal_type: str | None = None
    signals: dict | None = None
    has_verified_financials: bool = False
    verified_fraction: float = 0.0
    need_complete: bool = False
    stage: str | None = None
    config_override: dict | None = None


class SimulateOut(BaseModel):
    total: float
    category: str | None
    confidence: float
    subscores: dict
    gaps: list[str]
    grid_version: str
