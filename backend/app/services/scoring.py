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
from app.models.scoring_config import ScoringConfig
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


def active_config(db: Session) -> ScoringConfig | None:
    return db.query(ScoringConfig).filter(ScoringConfig.active.is_(True)).first()


def get_or_create_config(db: Session, actor: User | None = None) -> ScoringConfig:
    config = active_config(db)
    if config is None:
        config = ScoringConfig(
            version=scoring.GRID_VERSION,
            base_weights=dict(scoring.DEFAULT_WEIGHTS),
            caps=dict(scoring.CAPPED_DIMENSIONS),
            thresholds=dict(scoring.DEFAULT_THRESHOLDS),
            confidence=dict(scoring.DEFAULT_CONFIDENCE),
            active=True,
            updated_by=actor.id if actor else None,
        )
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


def update_config(db: Session, config: ScoringConfig, data, actor: User) -> ScoringConfig:
    for field in ("version", "base_weights", "caps", "thresholds", "confidence"):
        value = getattr(data, field, None)
        if value is not None:
            setattr(config, field, value)
    config.updated_by = actor.id
    db.commit()
    db.refresh(config)
    return config


def _config_dict(config: ScoringConfig | None) -> dict:
    """Config effective (défauts du domaine fusionnés avec la config active/override)."""
    return {
        "version": config.version if config else scoring.GRID_VERSION,
        "base_weights": (config.base_weights if config else None) or scoring.DEFAULT_WEIGHTS,
        "caps": (config.caps if config else None) or scoring.CAPPED_DIMENSIONS,
        "thresholds": (config.thresholds if config else None) or scoring.DEFAULT_THRESHOLDS,
        "confidence": (config.confidence if config else None) or scoring.DEFAULT_CONFIDENCE,
    }


def evaluate(
    *,
    signals: dict,
    deal_type,
    has_verified_financials: bool,
    verified_fraction: float,
    need_complete: bool,
    stage,
    dt_weights: dict | None,
    cfg: dict,
) -> dict:
    """Calcul pur d'un résultat de readiness à partir de signaux et d'une config (sans DB)."""
    base = dt_weights if dt_weights else cfg["base_weights"]
    weights = scoring.normalize_weights(base)
    capped = scoring.apply_caps(signals, cfg["caps"])
    total = scoring.weighted_total(capped, weights, risk_malus=0.0)
    category = scoring.map_category(
        total, stage=stage, deal_type=deal_type,
        has_verified_financials=has_verified_financials, thresholds=cfg["thresholds"],
    )
    confidence = scoring.confidence_index(verified_fraction, need_complete, cfg["confidence"])
    return {
        "subscores": capped,
        "total": total,
        "category": category,
        "confidence": confidence,
        "gaps": scoring.derive_gaps(capped),
        "grid_version": cfg["version"],
    }


def compute(db: Session, company: Company, actor: User, ip: str | None = None) -> Score:
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    dt = (
        db.query(DealType).filter(DealType.code == deal_type).first()
        if deal_type is not None
        else None
    )
    data = gather_signals(db, company)
    cfg = _config_dict(active_config(db))
    result = evaluate(
        signals=data["signals"], deal_type=deal_type,
        has_verified_financials=data["has_verified_financials"],
        verified_fraction=data["verified_fraction"], need_complete=data["need_complete"],
        stage=data["stage"], dt_weights=dt.scoring_weights if dt else None, cfg=cfg,
    )

    score = company.score or Score(company_id=company.id)
    score.subscores = result["subscores"]
    score.total = result["total"]
    score.category = result["category"]
    score.confidence = result["confidence"]
    score.grid_version = result["grid_version"]
    score.deal_type_applied = deal_type
    if score.id is None:
        db.add(score)
    db.commit()
    db.refresh(score)

    audit.record(
        db, AuditAction.score_computed, actor=actor, object_type="Company",
        object_id=company.id,
        meta={"total": result["total"], "category": result["category"].value,
              "grid": result["grid_version"]},
        ip_address=ip,
    )
    return score


def simulate(
    db: Session,
    *,
    company: Company | None = None,
    deal_type=None,
    signals: dict | None = None,
    has_verified_financials: bool = False,
    verified_fraction: float = 0.0,
    need_complete: bool = False,
    stage=None,
    config_override: dict | None = None,
) -> dict:
    """Calcule un résultat SANS persistance — harnais de calibrage.

    Si ``company`` est fourni, les signaux sont collectés depuis la base ; sinon on utilise
    les ``signals`` passés. ``config_override`` (dict partiel) est fusionné sur la config active.
    """
    cfg = _config_dict(active_config(db))
    if config_override:
        for key in ("base_weights", "caps", "thresholds", "confidence", "version"):
            if config_override.get(key) is not None:
                cfg[key] = config_override[key]

    dt_weights = None
    if company is not None:
        need = company.financing_need
        deal_type = need.deal_type_primary if need else None
        data = gather_signals(db, company)
        signals = data["signals"]
        has_verified_financials = data["has_verified_financials"]
        verified_fraction = data["verified_fraction"]
        need_complete = data["need_complete"]
        stage = data["stage"]
        if deal_type is not None:
            dt = db.query(DealType).filter(DealType.code == deal_type).first()
            dt_weights = dt.scoring_weights if dt else None

    result = evaluate(
        signals=signals or {}, deal_type=deal_type,
        has_verified_financials=has_verified_financials, verified_fraction=verified_fraction,
        need_complete=need_complete, stage=stage, dt_weights=dt_weights, cfg=cfg,
    )
    result["category"] = result["category"].value if result["category"] else None
    return result
