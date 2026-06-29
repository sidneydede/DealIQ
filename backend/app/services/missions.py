"""Service espace mission / préparation (M8)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import mission as domain
from app.domain.enums import (
    AuditAction,
    CompanyStatus,
    DeliverableKind,
    MissionStatus,
    Role,
)
from app.models.company import Company
from app.models.mission import Deliverable, Mission, MissionReview, MissionTask
from app.models.user import User
from app.services import audit
from app.services import companies as company_svc


class GateError(Exception):
    """Conditions de promotion non remplies."""


def get_or_create(db: Session, company: Company, actor: User) -> Mission:
    mission = db.query(Mission).filter(Mission.company_id == company.id).first()
    if mission is None:
        mission = Mission(company_id=company.id, owner_id=actor.id)
        db.add(mission)
        db.flush()
        deal_type = (
            company.financing_need.deal_type_primary if company.financing_need else None
        )
        for pos, label in enumerate(domain.checklist_for(deal_type)):
            db.add(MissionTask(mission_id=mission.id, label=label, position=pos))
        db.commit()
        db.refresh(mission)
    return mission


def _tasks(db: Session, mission: Mission) -> list[MissionTask]:
    return (
        db.query(MissionTask)
        .filter(MissionTask.mission_id == mission.id)
        .order_by(MissionTask.position)
        .all()
    )


def _reviews(db: Session, mission: Mission) -> list[MissionReview]:
    return (
        db.query(MissionReview)
        .filter(MissionReview.mission_id == mission.id)
        .order_by(MissionReview.created_at)
        .all()
    )


def _gate(db: Session, mission: Mission, company: Company) -> list[str]:
    """Retourne la liste des blocages à la promotion (vide = promotion possible)."""
    blockers: list[str] = []
    tasks = _tasks(db, mission)
    if not tasks or any(not t.done for t in tasks):
        blockers.append("Checklist investor-ready incomplète")
    roles = {r.role for r in _reviews(db, mission)}
    if Role.analyste not in roles:
        blockers.append("Validation analyste manquante")
    if Role.senior not in roles:
        blockers.append("Validation senior manquante")
    if company.status == CompanyStatus.investor_ready:
        blockers.append("Dossier déjà investor-ready")
    return blockers


def detail(db: Session, mission: Mission, company: Company) -> dict:
    blockers = _gate(db, mission, company)
    return {
        "id": mission.id,
        "company_id": mission.company_id,
        "status": mission.status,
        "owner_id": mission.owner_id,
        "tasks": _tasks(db, mission),
        "deliverables": (
            db.query(Deliverable)
            .filter(Deliverable.mission_id == mission.id)
            .order_by(Deliverable.created_at)
            .all()
        ),
        "reviews": _reviews(db, mission),
        "can_promote": len(blockers) == 0,
        "blockers": blockers,
    }


def toggle_task(db: Session, task: MissionTask, done: bool) -> MissionTask:
    task.done = done
    db.commit()
    db.refresh(task)
    return task


def add_deliverable(
    db: Session, mission: Mission, kind: DeliverableKind, note: str | None
) -> Deliverable:
    version = (
        db.query(Deliverable)
        .filter(Deliverable.mission_id == mission.id, Deliverable.kind == kind)
        .count()
        + 1
    )
    deliverable = Deliverable(mission_id=mission.id, kind=kind, version=version, note=note)
    db.add(deliverable)
    db.commit()
    db.refresh(deliverable)
    return deliverable


def update_deliverable(db: Session, deliverable: Deliverable, data) -> Deliverable:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(deliverable, field, value)
    db.commit()
    db.refresh(deliverable)
    return deliverable


def add_review(
    db: Session, mission: Mission, actor: User, note: str | None = None
) -> MissionReview:
    """Enregistre une validation de revue (rôle = celui du valideur). Une par rôle."""
    if actor.role not in (Role.analyste, Role.senior):
        raise GateError("Seuls un analyste et un senior valident la revue.")
    review = (
        db.query(MissionReview)
        .filter(MissionReview.mission_id == mission.id, MissionReview.role == actor.role)
        .first()
    )
    if review is None:
        review = MissionReview(mission_id=mission.id, role=actor.role)
        db.add(review)
    review.reviewer_id = actor.id
    review.note = note
    db.commit()
    db.refresh(review)
    audit.record(
        db, AuditAction.mission_reviewed, actor=actor, object_type="Mission",
        object_id=mission.id, meta={"role": actor.role.value},
    )
    return review


def promote(db: Session, mission: Mission, company: Company, actor: User) -> Company:
    """Promotion en investor-ready : checklist complète + double validation (RG-M8-01/02)."""
    blockers = _gate(db, mission, company)
    if blockers:
        raise GateError("; ".join(blockers))
    mission.status = MissionStatus.livre
    db.commit()
    audit.record(
        db, AuditAction.mission_promoted, actor=actor, object_type="Mission",
        object_id=mission.id, meta={"company_id": company.id}, commit=False,
    )
    company_svc.change_status(db, company, CompanyStatus.investor_ready, actor)
    return company
