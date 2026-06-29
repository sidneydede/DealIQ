"""Service investisseurs & critères (M9)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.enums import Role
from app.models.investor import InvestmentCriteria, Investor
from app.models.user import User

CABINET_ROLES = {Role.analyste, Role.senior, Role.admin}


def create_investor(db: Session, data) -> Investor:
    user_id = None
    if data.user_email:
        u = (
            db.query(User)
            .filter(User.email == data.user_email, User.role == Role.investisseur)
            .first()
        )
        user_id = u.id if u else None
    investor = Investor(
        name=data.name,
        type=data.type,
        jurisdiction=data.jurisdiction,
        team=data.team,
        user_id=user_id,
    )
    db.add(investor)
    db.commit()
    db.refresh(investor)
    return investor


def can_access(user: User, investor: Investor) -> bool:
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return True
    return investor.user_id == user.id


def list_for_user(db: Session, user: User) -> list[Investor]:
    q = db.query(Investor).order_by(Investor.created_at.desc())
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return q.all()
    return q.filter(Investor.user_id == user.id).all()


def my_investor(db: Session, user: User) -> Investor | None:
    return db.query(Investor).filter(Investor.user_id == user.id).first()


def upsert_criteria(db: Session, investor: Investor, data) -> InvestmentCriteria:
    crit = investor.criteria or InvestmentCriteria(investor_id=investor.id)
    crit.countries = data.countries
    crit.sectors = data.sectors
    crit.instruments = data.instruments
    crit.deal_types = data.deal_types
    crit.stages = data.stages
    crit.exclusions = data.exclusions
    crit.ticket_min = data.ticket_min
    crit.ticket_max = data.ticket_max
    crit.ticket_currency = data.ticket_currency
    crit.esg_required = data.esg_required
    if crit.id is None:
        db.add(crit)
    db.commit()
    db.refresh(crit)
    return crit
