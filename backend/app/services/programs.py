"""Service programmes sponsorisés (M23) + reporting d'impact agrégé/anonymisé."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.enums import AuditAction, DealStage, Role
from app.models.company import Company
from app.models.deal import Deal
from app.models.esg import EsgProfile
from app.models.program import Program, ProgramMember
from app.models.score import Score
from app.models.user import User
from app.services import audit

CABINET_ROLES = {Role.analyste, Role.senior, Role.admin}


def create(db: Session, data, actor: User) -> Program:
    sponsor_user_id = None
    if data.sponsor_email:
        u = (
            db.query(User)
            .filter(User.email == data.sponsor_email, User.role == Role.sponsor)
            .first()
        )
        sponsor_user_id = u.id if u else None
    program = Program(
        name=data.name,
        sponsor_name=data.sponsor_name,
        sponsor_user_id=sponsor_user_id,
        scope=data.scope,
        deliverables=data.deliverables,
        created_by=actor.id,
    )
    db.add(program)
    db.commit()
    db.refresh(program)
    audit.record(
        db, AuditAction.program_created, actor=actor, object_type="Program", object_id=program.id,
        meta={"sponsor": data.sponsor_name},
    )
    return program


def can_access(user: User, program: Program) -> bool:
    if user.role in CABINET_ROLES:
        return True
    if user.role == Role.sponsor:
        return program.sponsor_user_id == user.id
    return False


def list_for_user(db: Session, user: User) -> list[Program]:
    q = db.query(Program).order_by(Program.created_at.desc())
    if user.role in CABINET_ROLES:
        return q.all()
    if user.role == Role.sponsor:
        return q.filter(Program.sponsor_user_id == user.id).all()
    return []


def add_member(db: Session, program: Program, company_id: str, actor: User) -> ProgramMember:
    existing = (
        db.query(ProgramMember)
        .filter(ProgramMember.program_id == program.id, ProgramMember.company_id == company_id)
        .first()
    )
    if existing:
        return existing
    member = ProgramMember(program_id=program.id, company_id=company_id)
    db.add(member)
    db.commit()
    db.refresh(member)
    audit.record(
        db, AuditAction.program_member_added, actor=actor, object_type="Program",
        object_id=program.id, meta={"company_id": company_id},
    )
    return member


def _member_company_ids(db: Session, program: Program) -> list[str]:
    return [
        row[0]
        for row in db.query(ProgramMember.company_id)
        .filter(ProgramMember.program_id == program.id)
        .all()
    ]


def members(db: Session, program: Program) -> list[dict]:
    out = []
    for cid in _member_company_ids(db, program):
        company = db.get(Company, cid)
        out.append({
            "id": cid, "company_id": cid,
            "company_name": company.name if company else None,
        })
    return out


def report(db: Session, program: Program) -> dict:
    """Agrège l'impact de la cohorte SANS exposer d'identité (RG-M23-02)."""
    ids = _member_company_ids(db, program)
    if not ids:
        return {
            "cohort_size": 0, "by_readiness_category": {}, "by_status": {},
            "esg": {}, "deals_total": 0, "closings": 0,
        }

    by_readiness: dict[str, int] = {}
    for s in db.query(Score).filter(Score.company_id.in_(ids)).all():
        if s.category:
            by_readiness[s.category.value] = by_readiness.get(s.category.value, 0) + 1

    by_status: dict[str, int] = {}
    for c in db.query(Company).filter(Company.id.in_(ids)).all():
        by_status[c.status.value] = by_status.get(c.status.value, 0) + 1

    esg_rows = db.query(EsgProfile).filter(EsgProfile.company_id.in_(ids)).all()
    jobs_total = sum(e.jobs_total or 0 for e in esg_rows)
    jobs_female = sum(e.jobs_female or 0 for e in esg_rows)
    esg = {
        "companies_with_esg": len(esg_rows),
        "jobs_total": jobs_total,
        "jobs_female": jobs_female,
        "female_ratio": round(jobs_female / jobs_total, 3) if jobs_total else 0.0,
        "women_in_leadership": sum(1 for e in esg_rows if e.women_in_leadership),
    }

    deals = db.query(Deal).filter(Deal.company_id.in_(ids)).all()
    closings = sum(1 for d in deals if d.stage == DealStage.closing)

    return {
        "cohort_size": len(ids),
        "by_readiness_category": by_readiness,
        "by_status": by_status,
        "esg": esg,
        "deals_total": len(deals),
        "closings": closings,
    }
