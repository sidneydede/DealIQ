"""Logique d'onboarding / questionnaire (M3)."""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.questionnaire import evaluate_gating
from app.models.company import Company
from app.models.onboarding import OnboardingSession


def get_or_create(db: Session, company: Company) -> OnboardingSession:
    session = (
        db.query(OnboardingSession)
        .filter(OnboardingSession.company_id == company.id)
        .first()
    )
    if session is None:
        session = OnboardingSession(company_id=company.id, answers={})
        db.add(session)
        db.commit()
        db.refresh(session)
    return session


def save(db: Session, session: OnboardingSession, answers: dict, step: int) -> OnboardingSession:
    """Autosave : fusionne les réponses et mémorise l'étape (reprise possible)."""
    merged = {**session.answers, **answers}
    session.answers = merged
    session.current_step = step
    db.commit()
    db.refresh(session)
    return session


def give_consent(
    db: Session, session: OnboardingSession, text: str
) -> OnboardingSession:
    session.consent_given = True
    session.consent_at = datetime.now(UTC)
    session.consent_text = text
    db.commit()
    db.refresh(session)
    return session


def submit(db: Session, company: Company, session: OnboardingSession) -> dict:
    """Finalise le questionnaire et évalue le gating (route pipeline/nurturing/orientation)."""
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    result = evaluate_gating(deal_type, session.answers)
    session.completed = True
    session.gating_route = result["route"]
    db.commit()
    db.refresh(session)
    return result
