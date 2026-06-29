"""Reporting & dashboard (M21) : KPI MVP alignés sur O1–O6 (§2)."""
from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.company import Company, FinancingNeed
from app.models.onboarding import OnboardingSession
from app.models.quote import QuoteRequest
from app.models.score import Score
from app.models.user import User


def _ratio(num: int, den: int) -> float:
    return round(num / den, 3) if den else 0.0


def dashboard(db: Session) -> dict:
    users_total = db.query(func.count(User.id)).scalar() or 0
    companies_total = db.query(func.count(Company.id)).scalar() or 0

    started = db.query(func.count(OnboardingSession.id)).scalar() or 0
    completed = (
        db.query(func.count(OnboardingSession.id))
        .filter(OnboardingSession.completed.is_(True))
        .scalar()
        or 0
    )
    quotes = db.query(func.count(QuoteRequest.id)).scalar() or 0

    by_deal_type = {
        (code.value if code else "non_defini"): count
        for code, count in db.query(
            FinancingNeed.deal_type_primary, func.count(FinancingNeed.id)
        ).group_by(FinancingNeed.deal_type_primary)
    }
    by_readiness = {
        (cat.value if cat else "non_evalue"): count
        for cat, count in db.query(Score.category, func.count(Score.id)).group_by(Score.category)
    }
    by_status = {
        (st.value if hasattr(st, "value") else st): count
        for st, count in db.query(Company.status, func.count(Company.id)).group_by(Company.status)
    }

    return {
        # O1 — complétion du diagnostic
        "users_total": users_total,
        "companies_total": companies_total,
        "onboarding_started": started,
        "onboarding_completed": completed,
        "completion_rate": _ratio(completed, started),  # cible ≥ 0,40
        # O2 — conversion diagnostic → demande de devis
        "quote_requests_total": quotes,
        "conversion_rate": _ratio(quotes, completed),  # cible ≥ 0,15
        # Répartitions
        "by_deal_type": by_deal_type,
        "by_readiness_category": by_readiness,
        "companies_by_status": by_status,
    }
