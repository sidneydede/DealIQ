"""Routes onboarding / questionnaire (M3)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company
from app.database import get_db
from app.domain.enums import DealTypeCode
from app.domain.questionnaire import questions_for
from app.models.user import User
from app.schemas.onboarding import (
    ConsentIn,
    GatingResult,
    OnboardingOut,
    OnboardingSave,
    QuestionOut,
)
from app.services import onboarding as svc

router = APIRouter()


@router.get("/meta/questionnaire/{deal_type}", response_model=list[QuestionOut], tags=["meta"])
def get_questionnaire(deal_type: DealTypeCode) -> list[dict]:
    return questions_for(deal_type)


@router.get("/companies/{company_id}/questionnaire", response_model=OnboardingOut)
def get_session(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    company = load_company(company_id, db, user)
    return svc.get_or_create(db, company)


@router.put("/companies/{company_id}/questionnaire", response_model=OnboardingOut)
def save_session(
    company_id: str,
    payload: OnboardingSave,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = load_company(company_id, db, user)
    session = svc.get_or_create(db, company)
    return svc.save(db, session, payload.answers, payload.current_step)


@router.post("/companies/{company_id}/questionnaire/consent", response_model=OnboardingOut)
def consent(
    company_id: str,
    payload: ConsentIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = load_company(company_id, db, user)
    session = svc.get_or_create(db, company)
    return svc.give_consent(db, session, payload.consent_text)


@router.post("/companies/{company_id}/questionnaire/submit", response_model=GatingResult)
def submit(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    company = load_company(company_id, db, user)
    session = svc.get_or_create(db, company)
    if not session.consent_given:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consentement requis avant la soumission",
        )
    return svc.submit(db, company, session)
