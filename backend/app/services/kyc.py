"""Service KYC/KYB/AML (M15)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import kyc as provider
from app.domain.enums import (
    AuditAction,
    KycCheckType,
    KycStatus,
    KycSubjectType,
    NotificationType,
    Role,
)
from app.models.company import Company
from app.models.investor import Investor
from app.models.kyc import KycCheck
from app.models.user import User
from app.services import audit
from app.services import notifications as notif


def _subject_label(db: Session, subject_type: KycSubjectType, subject_id: str) -> str | None:
    if subject_type == KycSubjectType.company:
        c = db.get(Company, subject_id)
        return c.name if c else None
    inv = db.get(Investor, subject_id)
    return inv.name if inv else None


def run_check(
    db: Session,
    subject_type: KycSubjectType,
    subject_id: str,
    check_type: KycCheckType,
    actor: User,
    ip: str | None = None,
) -> KycCheck:
    label = _subject_label(db, subject_type, subject_id)
    status, result = provider.run_mock(label or "", check_type)

    check = KycCheck(
        subject_type=subject_type,
        subject_id=subject_id,
        subject_label=label,
        check_type=check_type,
        status=status,
        provider=result.get("provider"),
        result=result,
    )
    db.add(check)
    db.commit()
    db.refresh(check)

    audit.record(
        db, AuditAction.kyc_check_created, actor=actor, object_type="KycCheck",
        object_id=check.id,
        meta={"subject": f"{subject_type.value}:{subject_id}", "type": check_type.value,
              "status": status.value},
        ip_address=ip, commit=False,
    )
    if status == KycStatus.hit:
        # Hit sanctions/PEP → alerte conformité (RG-M15-02, critère d'acceptation).
        audit.record(
            db, AuditAction.kyc_hit_alert, actor=actor, object_type="KycCheck",
            object_id=check.id, meta={"result": result}, ip_address=ip, commit=False,
        )
    db.commit()
    if status == KycStatus.hit:
        notif.notify_roles(
            db,
            (Role.conformite, Role.admin),
            type=NotificationType.kyc_hit,
            title="Alerte KYC/AML",
            body=f"Hit de filtrage sur « {label or subject_id} ». Revue conformité requise.",
            link="/kyc",
            object_type="KycCheck",
            object_id=check.id,
        )
    return check


def list_checks(
    db: Session,
    *,
    subject_type: KycSubjectType | None = None,
    subject_id: str | None = None,
    status: KycStatus | None = None,
) -> list[KycCheck]:
    q = db.query(KycCheck).order_by(KycCheck.created_at.desc())
    if subject_type:
        q = q.filter(KycCheck.subject_type == subject_type)
    if subject_id:
        q = q.filter(KycCheck.subject_id == subject_id)
    if status:
        q = q.filter(KycCheck.status == status)
    return q.all()


def update_status(
    db: Session, check: KycCheck, new_status: KycStatus, notes: str | None, actor: User,
    ip: str | None = None,
) -> KycCheck:
    old = check.status
    check.status = new_status
    if notes is not None:
        check.notes = notes
    check.checked_by = actor.id
    db.commit()
    db.refresh(check)
    audit.record(
        db, AuditAction.kyc_status_changed, actor=actor, object_type="KycCheck",
        object_id=check.id, meta={"old": old.value, "new": new_status.value}, ip_address=ip,
    )
    return check


def is_cleared(db: Session, subject_type: KycSubjectType, subject_id: str) -> bool:
    """Sujet « cleared » : au moins un contrôle validé et aucun hit/rejeté (gate data room)."""
    checks = list_checks(db, subject_type=subject_type, subject_id=subject_id)
    if any(c.status in (KycStatus.hit, KycStatus.rejete) for c in checks):
        return False
    return any(c.status == KycStatus.valide for c in checks)
