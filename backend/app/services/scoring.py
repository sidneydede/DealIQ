"""Service de readiness (M5) : collecte des signaux, calcul, persistance du Score."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import scoring
from app.domain.enums import AuditAction, CompanyStage, DocumentStatus
from app.models.company import Company
from app.models.document import Document
from app.models.onboarding import OnboardingSession
from app.models.reference import DealType
from app.models.score import Score
from app.models.user import User
from app.services import audit

# Pièces considérées comme « financières » pour le gating (RG-M5-01).
FINANCIAL_DOC_TYPES = {
    "etats_financiers", "comptes", "releves_bancaires", "plan_tresorerie",
}

_REVENUE_SIGNAL = {
    "< 50 M FCFA": 0.3,
    "50 – 200 M FCFA": 0.5,
    "200 M – 1 Md FCFA": 0.7,
    "> 1 Md FCFA": 0.9,
}

_STAGE_FROM_LABEL = {
    "Idée": CompanyStage.idee,
    "Amorçage": CompanyStage.amorcage,
    "Early": CompanyStage.early,
    "Croissance": CompanyStage.croissance,
    "Mature": CompanyStage.mature,
}


def _stage(company: Company, answers: dict) -> CompanyStage | None:
    if company.stage:
        return company.stage
    return _STAGE_FROM_LABEL.get(answers.get("stage"))


def _doc_metrics(db: Session, company: Company) -> tuple[float, float, bool]:
    """Renvoie (complétude requise, fraction vérifiée, pièces financières vérifiées)."""
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    required: list[str] = []
    if deal_type is not None:
        dt = db.query(DealType).filter(DealType.code == deal_type).first()
        required = list(dt.doc_checklist or []) if dt else []

    docs = db.query(Document).filter(Document.company_id == company.id).all()
    received_types = {d.doc_type for d in docs}
    verified_types = {d.doc_type for d in docs if d.status == DocumentStatus.verifie}

    if required:
        completeness = len([r for r in required if r in received_types]) / len(required)
        verified_fraction = len([r for r in required if r in verified_types]) / len(required)
    else:
        completeness = 1.0 if received_types else 0.0
        verified_fraction = 1.0 if verified_types else 0.0

    has_verified_financials = any(
        d.doc_type in FINANCIAL_DOC_TYPES and d.status == DocumentStatus.verifie for d in docs
    )
    return completeness, verified_fraction, has_verified_financials


def gather_signals(db: Session, company: Company) -> dict:
    need = company.financing_need
    session = (
        db.query(OnboardingSession)
        .filter(OnboardingSession.company_id == company.id)
        .first()
    )
    answers = session.answers if session else {}

    completeness, verified_fraction, has_verified_financials = _doc_metrics(db, company)

    need_fields = [
        need and need.amount,
        need and need.use_of_funds,
        need and need.horizon,
        need and need.deal_type_primary,
    ]
    clarte = sum(1 for f in need_fields if f) / len(need_fields)

    governance = 0.0
    if company.rccm:
        governance += 0.5
    if answers.get("cap_table_ready") == "Oui":
        governance += 0.3
    governance = min(governance, 1.0)

    signals = {
        "traction": _REVENUE_SIGNAL.get(answers.get("revenue_band"), 0.4),
        "profitabilite_cashflow": 0.6 if answers.get("bank_history") == "Oui" else 0.4,
        "qualite_info_financiere": verified_fraction,
        "clarte_besoin": clarte,
        "gouvernance": governance,
        "qualite_documentaire": completeness,
        "scalabilite_marche": 0.4,
        "esg": 0.2,
    }
    return {
        "signals": signals,
        "verified_fraction": verified_fraction,
        "has_verified_financials": has_verified_financials,
        "need_complete": clarte >= 1.0,
        "stage": _stage(company, answers),
    }


def compute(db: Session, company: Company, actor: User, ip: str | None = None) -> Score:
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    dt = (
        db.query(DealType).filter(DealType.code == deal_type).first()
        if deal_type is not None
        else None
    )
    weights = scoring.normalize_weights(dt.scoring_weights if dt else None)

    data = gather_signals(db, company)
    signals = scoring.apply_caps(data["signals"])
    total = scoring.weighted_total(signals, weights, risk_malus=0.0)
    category = scoring.map_category(
        total,
        stage=data["stage"],
        deal_type=deal_type,
        has_verified_financials=data["has_verified_financials"],
    )
    confidence = scoring.confidence_index(data["verified_fraction"], data["need_complete"])

    score = company.score or Score(company_id=company.id)
    score.subscores = signals
    score.total = total
    score.category = category
    score.confidence = confidence
    score.grid_version = scoring.GRID_VERSION
    score.deal_type_applied = deal_type
    if score.id is None:
        db.add(score)
    db.commit()
    db.refresh(score)

    audit.record(
        db, AuditAction.score_computed, actor=actor, object_type="Company",
        object_id=company.id,
        meta={"total": total, "category": category.value, "grid": scoring.GRID_VERSION},
        ip_address=ip,
    )
    return score
