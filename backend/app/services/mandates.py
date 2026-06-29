"""Service mandats & honoraires (M17) + registre des conflits d'intérêts."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.enums import AuditAction, RepresentedParty
from app.models.company import Company
from app.models.mandate import Fee, Mandate
from app.models.user import User
from app.services import audit

_DISCLOSURE = (
    "Double mandat : le Cabinet représente les deux parties. Muraille sur les honoraires "
    "et divulgation requise (RG-M17-01)."
)


def create_mandate(
    db: Session, company: Company, data, actor: User, ip: str | None = None
) -> Mandate:
    mandate = Mandate(
        company_id=company.id,
        deal_id=data.deal_id,
        represented_party=data.represented_party,
        mandate_type=data.mandate_type,
        exclusive=data.exclusive,
        duration_months=data.duration_months,
        scope=data.scope,
        created_by=actor.id,
    )
    db.add(mandate)
    db.commit()
    db.refresh(mandate)
    audit.record(
        db, AuditAction.mandate_created, actor=actor, object_type="Mandate", object_id=mandate.id,
        meta={"company_id": company.id, "represented": data.represented_party.value},
        ip_address=ip,
    )
    return mandate


def list_for_company(db: Session, company: Company) -> list[Mandate]:
    return (
        db.query(Mandate)
        .filter(Mandate.company_id == company.id)
        .order_by(Mandate.created_at.desc())
        .all()
    )


def update_mandate(
    db: Session, mandate: Mandate, data, actor: User, ip: str | None = None
) -> Mandate:
    old_status = mandate.status
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(mandate, field, value)
    db.commit()
    db.refresh(mandate)
    if data.status is not None and data.status != old_status:
        audit.record(
            db, AuditAction.mandate_status_changed, actor=actor, object_type="Mandate",
            object_id=mandate.id, meta={"old": old_status.value, "new": mandate.status.value},
            ip_address=ip,
        )
    return mandate


def add_fee(db: Session, mandate: Mandate, data, actor: User, ip: str | None = None) -> Fee:
    fee = Fee(
        mandate_id=mandate.id,
        fee_type=data.fee_type,
        amount=data.amount,
        currency=data.currency,
        due_date=data.due_date,
        note=data.note,
    )
    db.add(fee)
    db.commit()
    db.refresh(fee)
    audit.record(
        db, AuditAction.fee_added, actor=actor, object_type="Fee", object_id=fee.id,
        meta={"mandate_id": mandate.id, "type": data.fee_type.value}, ip_address=ip,
    )
    return fee


def list_fees(db: Session, mandate: Mandate) -> list[Fee]:
    return db.query(Fee).filter(Fee.mandate_id == mandate.id).order_by(Fee.created_at).all()


def update_fee(db: Session, fee: Fee, new_status) -> Fee:
    fee.status = new_status
    db.commit()
    db.refresh(fee)
    return fee


def conflicts(db: Session) -> list[dict]:
    """Registre des conflits : par entreprise, parties représentées + alerte double mandat."""
    by_company: dict[str, set[RepresentedParty]] = {}
    for m in db.query(Mandate).all():
        by_company.setdefault(m.company_id, set()).add(m.represented_party)

    out = []
    for company_id, parties in by_company.items():
        both = RepresentedParty.les_deux in parties or (
            RepresentedParty.entreprise in parties and RepresentedParty.investisseur in parties
        )
        company = db.get(Company, company_id)
        out.append({
            "company_id": company_id,
            "company_name": company.name if company else None,
            "represented_parties": sorted(parties, key=lambda p: p.value),
            "has_conflict": both,
            "disclosure": _DISCLOSURE if both else None,
        })
    return out
