"""Mini-rapport readiness (M6). Construit un rapport actionnable et conforme (§11)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import scoring
from app.domain.enums import DealTypeCode, Instrument, ReadinessCategory
from app.models.company import Company
from app.models.reference import DealType
from app.models.user import User
from app.services import scoring as scoring_svc

CATEGORY_LABELS = {
    ReadinessCategory.investor_ready: "Investor-ready",
    ReadinessCategory.a_preparer: "À préparer",
    ReadinessCategory.plutot_dette_banque: "Plutôt dette / banque",
    ReadinessCategory.trop_precoce: "Trop précoce",
}

INSTRUMENT_LABELS = {
    Instrument.equity: "Ouverture de capital (equity)",
    Instrument.dette: "Financement par dette",
    Instrument.quasi_equity: "Quasi-fonds propres",
    Instrument.subvention: "Subvention",
    Instrument.hybride: "Financement hybride",
    Instrument.variable: "Instrument à définir",
}

# Services recommandés (clés M7) selon la catégorie.
SERVICES_BY_CATEGORY = {
    ReadinessCategory.investor_ready: ["mandat"],
    ReadinessCategory.a_preparer: ["diagnostic_plus", "preparation"],
    ReadinessCategory.plutot_dette_banque: ["preparation_credit"],
    ReadinessCategory.trop_precoce: ["nurturing"],
}

DISCLAIMERS = [
    "Évaluation provisoire, sous réserve de vérification des pièces.",
    "Aucune garantie de financement. Pas d'offre au public.",
    "L'exactitude des données déclarées relève de l'entreprise.",
]


def _recommended_instrument(dt: DealType | None) -> str:
    if dt and dt.instruments:
        return INSTRUMENT_LABELS.get(Instrument(dt.instruments[0]), dt.instruments[0])
    return INSTRUMENT_LABELS[Instrument.variable]


def _alternative_suggestion(
    category: ReadinessCategory | None, deal_type: DealTypeCode | None
) -> str | None:
    """RG-M6-04 : suggère un type/instrument alternatif si le choix semble inadapté."""
    equity_types = (
        DealTypeCode.ouverture_capital,
        DealTypeCode.cession_parts,
        DealTypeCode.ma,
    )
    if category == ReadinessCategory.plutot_dette_banque and deal_type in equity_types:
        return (
            "D'après votre profil, un financement par dette bancaire semble plus adapté "
            "qu'une opération en capital. En discuter avec un expert ?"
        )
    return None


def build(db: Session, company: Company, actor: User) -> dict:
    """Calcule un score à jour et assemble le mini-rapport (M6)."""
    score = scoring_svc.compute(db, company, actor)
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    dt = (
        db.query(DealType).filter(DealType.code == deal_type).first()
        if deal_type is not None
        else None
    )
    gaps = scoring.derive_gaps(score.subscores or {})

    return {
        "company_name": company.name,
        "category": score.category,
        "category_label": CATEGORY_LABELS.get(score.category, "—"),
        "confidence": score.confidence,
        "deal_type": deal_type,
        "recommended_instrument": _recommended_instrument(dt),
        "blockers": gaps,
        "path_to_bankable": gaps[:3],
        "alternative_suggestion": _alternative_suggestion(score.category, deal_type),
        "recommended_services": SERVICES_BY_CATEGORY.get(score.category, ["preparation"]),
        "disclaimers": DISCLAIMERS,
    }
