"""Espace mission (M8) — checklist investor-ready, déclinée par type de deal (RG-M8-01)."""
from __future__ import annotations

from app.domain.enums import DealTypeCode

# Checklist de base avant tout passage en curation.
_BASE = [
    "Business plan validé",
    "Modèle financier",
    "Valorisation / pricing",
    "Teaser anonymisé",
    "Data room initiale",
    "Pièces clés vérifiées",
]

_EQUITY_EXTRA = ["Cap table à jour", "Pacte d'actionnaires préparé"]
_DEBT_EXTRA = ["Plan de trésorerie", "Sûretés / garanties documentées"]

_CHECKLIST_BY_TYPE: dict[DealTypeCode, list[str]] = {
    DealTypeCode.ouverture_capital: _EQUITY_EXTRA,
    DealTypeCode.cession_parts: _EQUITY_EXTRA,
    DealTypeCode.ma: ["Information memorandum", "Vendor due diligence"],
    DealTypeCode.dette_bancaire: _DEBT_EXTRA,
    DealTypeCode.dette_privee: _DEBT_EXTRA,
}


def checklist_for(deal_type: DealTypeCode | None) -> list[str]:
    """Liste ordonnée des tâches « investor-ready » pour un type de deal."""
    extra = _CHECKLIST_BY_TYPE.get(deal_type, []) if deal_type else []
    return [*_BASE, *extra]
