"""Pipeline & jalons de closing (M16). Les jalons dépendent du type de deal (RG-M16-03)."""
from __future__ import annotations

from app.domain.enums import DealStage, DealTypeCode

# Ordre des étapes (hors terminal « abandonne »).
STAGE_ORDER: list[DealStage] = [
    DealStage.interesse,
    DealStage.nda,
    DealStage.data_room,
    DealStage.due_diligence,
    DealStage.term_sheet,
    DealStage.closing,
]

# Jalons / documents de closing par type de deal (RG-M16-03).
_EQUITY = [
    "Term sheet", "Due diligence", "Pacte d'actionnaires (SHA)",
    "Contrat de cession/souscription (SPA)", "Conditions suspensives (CPs)", "Closing",
]
_DEBT = [
    "Term sheet", "Due diligence crédit", "Convention de crédit",
    "Covenants", "Sûretés / garanties", "Conditions de tirage", "Closing",
]

MILESTONES_BY_DEAL_TYPE: dict[DealTypeCode, list[str]] = {
    DealTypeCode.ouverture_capital: _EQUITY,
    DealTypeCode.cession_parts: _EQUITY,
    DealTypeCode.ma: [
        "Information memorandum", "Due diligence", "SPA", "Conditions suspensives (CPs)",
        "Garanties d'actif et de passif", "Closing",
    ],
    DealTypeCode.dette_bancaire: _DEBT,
    DealTypeCode.dette_privee: _DEBT,
    DealTypeCode.hybride: [
        "Term sheet", "Due diligence", "Structure (equity + dette)",
        "Documentation equity (SHA/SPA)", "Documentation dette (convention)", "Closing",
    ],
    DealTypeCode.partenariat: [
        "Term sheet partenariat", "Accord de partenariat", "Gouvernance", "Signature",
    ],
}

_DEFAULT_MILESTONES = ["Term sheet", "Due diligence", "Documentation", "Closing"]


def milestones_for(deal_type: DealTypeCode | None) -> list[str]:
    if deal_type is None:
        return _DEFAULT_MILESTONES
    return MILESTONES_BY_DEAL_TYPE.get(deal_type, _DEFAULT_MILESTONES)


def next_stage(stage: DealStage) -> DealStage | None:
    if stage in STAGE_ORDER and stage != DealStage.closing:
        return STAGE_ORDER[STAGE_ORDER.index(stage) + 1]
    return None
