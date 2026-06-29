"""Service investisseurs & critères (M9)."""
from __future__ import annotations

import secrets

from sqlalchemy.orm import Session

from app.api.pagination import SortParams, apply_sql_sort
from app.core.security import hash_password
from app.domain import email_template
from app.domain.enums import (
    AuditAction,
    InvestorQualifStatus,
    InvestorType,
    NotificationType,
    Role,
)
from app.models.investor import InvestmentCriteria, Investor
from app.models.user import User
from app.services import audit
from app.services import email as email_adapter
from app.services import notifications as notif

CABINET_ROLES = {Role.analyste, Role.senior, Role.admin}


class InviteError(Exception):
    """Invitation impossible (e-mail manquant ou compte conflictuel)."""

    def __init__(self, detail: str, status_code: int = 400) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


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


def invite_investor(
    db: Session, investor: Investor, email: str | None, actor: User
) -> tuple[Investor, str | None]:
    """Invite (ou ré-invite) le compte investisseur rattaché à une fiche.

    Crée le compte (rôle investisseur) s'il n'existe pas, le lie à la fiche,
    envoie un e-mail d'invitation (mock) + une notification de bienvenue.
    Renvoie (fiche, mot de passe temporaire | None). Le mot de passe n'est
    généré (et renvoyé) que lorsqu'un compte est créé.
    """
    target_email = (email or "").strip().lower() or None
    if target_email is None and investor.user_id:
        linked = db.get(User, investor.user_id)
        target_email = linked.email if linked else None
    if not target_email:
        raise InviteError("Aucune adresse e-mail fournie pour l'invitation.")

    existing = db.query(User).filter(User.email == target_email).first()
    temp: str | None = None
    if existing is not None:
        if existing.role != Role.investisseur:
            raise InviteError(
                "Un compte non-investisseur utilise déjà cette adresse.", status_code=409
            )
        user = existing
    else:
        temp = secrets.token_urlsafe(9)
        user = User(
            email=target_email,
            hashed_password=hash_password(temp),
            role=Role.investisseur,
            full_name=investor.name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    investor.user_id = user.id
    db.commit()
    db.refresh(investor)

    if temp:
        body = (
            f"Bonjour, un espace investisseur DealIQ a été créé pour « {investor.name} ». "
            f"Identifiant : {target_email}. Mot de passe temporaire : {temp}. "
            "Merci de le modifier à la première connexion."
        )
    else:
        body = (
            f"Bonjour, votre accès à l'espace investisseur DealIQ pour « {investor.name} » "
            f"est confirmé. Identifiant : {target_email}."
        )
    email_adapter.send_email(
        target_email, "Invitation DealIQ", body,
        html=email_template.render("Invitation DealIQ", body),
    )

    notif.notify(
        db,
        recipient=user,
        type=NotificationType.account_invited,
        title="Bienvenue sur DealIQ",
        body=f"Votre espace investisseur « {investor.name} » est prêt.",
        link="/my-criteria",
        object_type="Investor",
        object_id=investor.id,
        send_email=False,  # l'e-mail d'invitation a déjà été envoyé ci-dessus
    )
    audit.record(
        db,
        AuditAction.investor_invited,
        actor=actor,
        object_type="Investor",
        object_id=investor.id,
        meta={"email": target_email, "new_account": temp is not None},
    )
    return investor, temp


def can_access(user: User, investor: Investor) -> bool:
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return True
    return investor.user_id == user.id


_SORT_COLUMNS = {
    "name": Investor.name,
    "type": Investor.type,
    "qualif_status": Investor.qualif_status,
    "created_at": Investor.created_at,
}


def _list_query(db: Session, user: User):
    q = db.query(Investor)
    if user.role in CABINET_ROLES or user.role == Role.conformite:
        return q
    return q.filter(Investor.user_id == user.id)


def list_for_user(db: Session, user: User) -> list[Investor]:
    return _list_query(db, user).order_by(Investor.created_at.desc()).all()


def paginate_for_user(
    db: Session,
    user: User,
    *,
    q: str | None = None,
    type_filter: InvestorType | None = None,
    qualif_status: InvestorQualifStatus | None = None,
    sort: SortParams | None = None,
    limit: int,
    offset: int = 0,
) -> tuple[list[Investor], int]:
    query = _list_query(db, user)
    if q:
        query = query.filter(Investor.name.ilike(f"%{q.strip()}%"))
    if type_filter:
        query = query.filter(Investor.type == type_filter)
    if qualif_status:
        query = query.filter(Investor.qualif_status == qualif_status)
    total = query.count()
    query = apply_sql_sort(
        query, sort or SortParams(None, False), _SORT_COLUMNS, default=Investor.created_at
    )
    items = query.offset(offset).limit(limit).all()
    return items, total


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
