"""Schémas Pydantic — readiness (M5). Vues différenciées par rôle (RG-M5-04)."""
from __future__ import annotations

from pydantic import BaseModel

from app.domain.enums import DealTypeCode, ReadinessCategory


class ScoreEntrepreneurOut(BaseModel):
    """Vue entrepreneur : catégorie + confiance + gaps. JAMAIS de score chiffré."""

    category: ReadinessCategory | None
    confidence: float | None
    gaps: list[str]
    provisional: bool = True  # « évaluation provisoire, sous réserve de vérification »


class ScoreFullOut(BaseModel):
    """Vue cabinet : score complet, sous-scores, confiance, historique de grille."""

    total: float | None
    category: ReadinessCategory | None
    confidence: float | None
    grid_version: str | None
    deal_type_applied: DealTypeCode | None
    subscores: dict
    gaps: list[str]
