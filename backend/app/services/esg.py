"""Service ESG / impact (M19)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.esg import EsgProfile

# Indicateurs clés pris en compte dans la complétude.
_INDICATORS = [
    "jobs_total",
    "jobs_female",
    "women_in_leadership",
    "environmental_policy",
    "climate_risk_assessed",
    "governance_formalized",
    "board_independent",
]

_DISCLAIMER = (
    "Données ESG déclaratives, à justifier par pièces quand c'est possible "
    "(anti impact-washing, RG-M19-02)."
)


def get(db: Session, company: Company) -> EsgProfile | None:
    return db.query(EsgProfile).filter(EsgProfile.company_id == company.id).first()


def upsert(db: Session, company: Company, data) -> EsgProfile:
    profile = get(db, company) or EsgProfile(company_id=company.id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    if profile.id is None:
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def set_required(db: Session, profile: EsgProfile, required: bool) -> EsgProfile:
    profile.esg_required = required
    db.commit()
    db.refresh(profile)
    return profile


def completeness(profile: EsgProfile) -> float:
    filled = sum(1 for ind in _INDICATORS if getattr(profile, ind) is not None)
    return round(filled / len(_INDICATORS), 3)


def to_out(profile: EsgProfile) -> dict:
    c = completeness(profile)
    return {
        **{k: getattr(profile, k) for k in (
            "id", "company_id", "jobs_total", "jobs_female", "jobs_youth",
            "women_in_leadership", "environmental_policy", "climate_risk_assessed",
            "governance_formalized", "board_independent", "esg_required",
            "evidence_note", "notes",
        )},
        "completeness": c,
        "incomplete_for_dfi": profile.esg_required and c < 1.0,
    }


def export(db: Session, company: Company, profile: EsgProfile) -> dict:
    return {
        "company_name": company.name,
        "indicators": {ind: getattr(profile, ind) for ind in _INDICATORS}
        | {"jobs_youth": profile.jobs_youth},
        "completeness": completeness(profile),
        "evidence_note": profile.evidence_note,
        "disclaimer": _DISCLAIMER,
    }
