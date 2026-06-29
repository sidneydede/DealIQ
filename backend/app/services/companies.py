"""Logique métier entreprise (M2) et type de deal (M24)."""
from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.domain.enums import (
    AuditAction,
    CompanyStatus,
    Country,
    Currency,
    DealTypeChangeSource,
    DealTypeCode,
    Role,
    currency_for_country,
)
from app.models.company import Company, FinancingNeed
from app.models.dealtype_history import DealTypeHistory
from app.models.user import User
from app.services import audit

CABINET_ROLES = {Role.analyste, Role.senior, Role.admin}


def normalize_name(name: str) -> str:
    """Normalise un nom pour la détection de doublon (RG-M2-01)."""
    return re.sub(r"\s+", " ", name.strip().lower())


def find_duplicates(db: Session, *, name: str, country: Country, rccm: str | None) -> list[dict]:
    """Doublons potentiels : même RCCM+pays, ou même nom normalisé+pays (RG-M2-01)."""
    matches: list[dict] = []
    seen: set[str] = set()

    if rccm:
        for c in db.query(Company).filter(Company.country == country, Company.rccm == rccm).all():
            if c.id not in seen:
                matches.append({"id": c.id, "name": c.name, "rccm": c.rccm, "reason": "rccm"})
                seen.add(c.id)

    norm = normalize_name(name)
    candidates = db.query(Company).filter(Company.country == country).all()
    for c in candidates:
        if c.id not in seen and normalize_name(c.name) == norm:
            matches.append({"id": c.id, "name": c.name, "rccm": c.rccm, "reason": "name"})
            seen.add(c.id)
    return matches


def create_company(db: Session, data, owner: User, ip: str | None = None) -> tuple[Company, list]:
    """Crée une fiche entreprise. Devise déduite du pays si absente. Doublons signalés."""
    duplicates = find_duplicates(
        db, name=data.name, country=data.country, rccm=data.rccm
    )
    currency: Currency = data.currency or currency_for_country(data.country)
    # L'entrepreneur est propriétaire ; un membre du cabinet crée une fiche non rattachée.
    owner_id = owner.id if owner.role == Role.entrepreneur else None
    company = Company(
        name=data.name,
        country=data.country,
        sector=data.sector,
        rccm=data.rccm,
        stage=data.stage,
        revenue_min=data.revenue_min,
        revenue_max=data.revenue_max,
        currency=currency,
        owner_id=owner_id,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    audit.record(
        db, AuditAction.company_created, actor=owner, object_type="Company",
        object_id=company.id, meta={"duplicates": len(duplicates)}, ip_address=ip,
    )
    return company, duplicates


def can_access(user: User, company: Company) -> bool:
    """Cabinet : accès à tout. Entrepreneur : uniquement sa fiche."""
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return True
    return company.owner_id == user.id


def list_for_user(db: Session, user: User) -> list[Company]:
    q = db.query(Company).order_by(Company.created_at.desc())
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return q.all()
    return q.filter(Company.owner_id == user.id).all()


def change_status(
    db: Session, company: Company, new_status: CompanyStatus, actor: User, ip: str | None = None
) -> Company:
    old = company.status
    company.status = new_status
    db.commit()
    db.refresh(company)
    audit.record(
        db, AuditAction.company_status_changed, actor=actor, object_type="Company",
        object_id=company.id, meta={"old": old.value, "new": new_status.value}, ip_address=ip,
    )
    return company


def _ensure_need(db: Session, company: Company) -> FinancingNeed:
    if company.financing_need is None:
        need = FinancingNeed(company_id=company.id, currency=company.currency)
        db.add(need)
        db.flush()
        company.financing_need = need
    return company.financing_need


def change_deal_type(
    db: Session,
    company: Company,
    *,
    primary: DealTypeCode,
    secondary: DealTypeCode | None,
    source: DealTypeChangeSource,
    actor: User,
    motif: str | None = None,
    amount: float | None = None,
    use_of_funds: str | None = None,
    horizon: str | None = None,
    ip: str | None = None,
) -> FinancingNeed:
    """Change le type de deal, historise (DealTypeHistory) et audite (M22).

    Jamais d'écrasement silencieux : l'ancien état est conservé dans l'historique.
    """
    need = _ensure_need(db, company)
    old_primary, old_secondary = need.deal_type_primary, need.deal_type_secondary

    need.deal_type_primary = primary
    need.deal_type_secondary = secondary
    if amount is not None:
        need.amount = amount
    if use_of_funds is not None:
        need.use_of_funds = use_of_funds
    if horizon is not None:
        need.horizon = horizon

    db.add(
        DealTypeHistory(
            company_id=company.id,
            old_primary=old_primary,
            new_primary=primary,
            old_secondary=old_secondary,
            new_secondary=secondary,
            source=source,
            actor_id=actor.id,
            motif=motif,
        )
    )
    db.commit()
    db.refresh(need)
    audit.record(
        db, AuditAction.deal_type_changed, actor=actor, object_type="Company",
        object_id=company.id,
        meta={
            "old": old_primary.value if old_primary else None,
            "new": primary.value,
            "source": source.value,
            "motif": motif,
        },
        ip_address=ip,
    )
    return need


def history(db: Session, company: Company) -> list[DealTypeHistory]:
    return (
        db.query(DealTypeHistory)
        .filter(DealTypeHistory.company_id == company.id)
        .order_by(DealTypeHistory.created_at.desc())
        .all()
    )
