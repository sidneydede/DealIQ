"""Service Q&A (M14) + contrôle d'accès aux mises en relation."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.enums import QAStatus, Role
from app.models.investor import Investor
from app.models.qa import QAItem
from app.models.teaser import Interaction
from app.models.user import User

CABINET_ROLES = {Role.analyste, Role.senior, Role.admin, Role.conformite}


def investor_ids_for(db: Session, user: User) -> set[str]:
    return {row[0] for row in db.query(Investor.id).filter(Investor.user_id == user.id).all()}


def can_access_interaction(db: Session, user: User, interaction: Interaction) -> bool:
    if user.role in CABINET_ROLES:
        return True
    if user.role == Role.investisseur:
        return interaction.investor_id in investor_ids_for(db, user)
    return False


def list_interactions(db: Session, user: User) -> list[Interaction]:
    q = db.query(Interaction).order_by(Interaction.created_at.desc())
    if user.role in CABINET_ROLES:
        return q.all()
    if user.role == Role.investisseur:
        ids = investor_ids_for(db, user)
        return q.filter(Interaction.investor_id.in_(ids)).all() if ids else []
    return []


def thread(db: Session, interaction: Interaction) -> list[QAItem]:
    return (
        db.query(QAItem)
        .filter(QAItem.interaction_id == interaction.id)
        .order_by(QAItem.created_at)
        .all()
    )


def ask(db: Session, interaction: Interaction, user: User, question: str) -> QAItem:
    item = QAItem(interaction_id=interaction.id, asked_by=user.id, question=question)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def answer(db: Session, item: QAItem, user: User, text: str) -> QAItem:
    item.answer = text
    item.answered_by = user.id
    item.status = QAStatus.repondue
    db.commit()
    db.refresh(item)
    return item


def set_status(db: Session, item: QAItem, new_status: QAStatus) -> QAItem:
    item.status = new_status
    db.commit()
    db.refresh(item)
    return item
