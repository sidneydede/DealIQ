"""Service data room (M13). Connecteur mock + droits + watermark + logs."""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enums import (
    AuditAction,
    DataRoomLogAction,
    InteractionStatus,
    KycSubjectType,
    NotificationType,
)
from app.models.company import Company
from app.models.dataroom import DataRoom, DataRoomAccess, DataRoomDocument, DataRoomLog
from app.models.document import Document
from app.models.investor import Investor
from app.models.teaser import Interaction
from app.models.user import User
from app.services import audit
from app.services import kyc as kyc_svc
from app.services import notifications as notif


class GateError(Exception):
    """Conditions d'accès non remplies (KYC ou NDA)."""


def get_or_create(db: Session, company: Company, actor: User) -> DataRoom:
    room = db.query(DataRoom).filter(DataRoom.company_id == company.id).first()
    if room is None:
        room = DataRoom(company_id=company.id, provider_ref=f"mock-vdr-{company.id[:8]}",
                        created_by=actor.id)
        db.add(room)
        db.commit()
        db.refresh(room)
    return room


def add_document(db: Session, room: DataRoom, document_id: str) -> DataRoomDocument:
    doc = db.get(Document, document_id)
    if doc is None or doc.company_id != room.company_id:
        raise GateError("Document invalide pour ce deal (cloisonnement).")
    existing = (
        db.query(DataRoomDocument)
        .filter(
            DataRoomDocument.dataroom_id == room.id,
            DataRoomDocument.document_id == document_id,
        )
        .first()
    )
    if existing:
        return existing
    link = DataRoomDocument(dataroom_id=room.id, document_id=document_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def list_documents(db: Session, room: DataRoom) -> list[dict]:
    links = db.query(DataRoomDocument).filter(DataRoomDocument.dataroom_id == room.id).all()
    out = []
    for link in links:
        doc = db.get(Document, link.document_id)
        if doc:
            out.append({
                "id": link.id, "document_id": doc.id, "filename": doc.filename,
                "doc_type": doc.doc_type, "status": doc.status.value,
            })
    return out


def _nda_signed(db: Session, room: DataRoom, investor: Investor) -> bool:
    return (
        db.query(Interaction)
        .filter(
            Interaction.company_id == room.company_id,
            Interaction.investor_id == investor.id,
            Interaction.status == InteractionStatus.nda_signe,
        )
        .first()
        is not None
    )


def grant_access(
    db: Session, room: DataRoom, investor: Investor, actor: User,
    expires_at: datetime | None = None, ip: str | None = None,
) -> DataRoomAccess:
    """Octroi gaté (RG-M15-02 + M12) : KYC investisseur validé ET NDA signé."""
    if not kyc_svc.is_cleared(db, KycSubjectType.investor, investor.id):
        raise GateError("KYC investisseur non validé.")
    if not _nda_signed(db, room, investor):
        raise GateError("NDA non signé pour ce deal.")

    access = (
        db.query(DataRoomAccess)
        .filter(DataRoomAccess.dataroom_id == room.id, DataRoomAccess.investor_id == investor.id)
        .first()
    )
    if access is None:
        access = DataRoomAccess(dataroom_id=room.id, investor_id=investor.id)
        db.add(access)
    access.granted_by = actor.id
    access.expires_at = expires_at
    access.revoked = False
    db.commit()
    db.refresh(access)
    audit.record(
        db, AuditAction.dataroom_access_granted, actor=actor, object_type="DataRoomAccess",
        object_id=access.id, meta={"investor_id": investor.id, "company_id": room.company_id},
        ip_address=ip,
    )
    # Notifier l'investisseur que sa data room est ouverte (s'il a un compte).
    if investor.user_id:
        owner = db.get(User, investor.user_id)
        if owner:
            notif.notify(
                db,
                recipient=owner,
                type=NotificationType.dataroom_access_granted,
                title="Accès data room accordé",
                body="Vous avez désormais accès à une data room. Consultez vos data rooms.",
                link="/my-datarooms",
                object_type="DataRoom",
                object_id=room.id,
            )
    return access


def revoke_access(db: Session, access: DataRoomAccess, actor: User, ip: str | None = None) -> None:
    access.revoked = True
    db.commit()
    audit.record(
        db, AuditAction.dataroom_access_revoked, actor=actor, object_type="DataRoomAccess",
        object_id=access.id, ip_address=ip,
    )


def _active_access(db: Session, room: DataRoom, investor: Investor) -> DataRoomAccess | None:
    access = (
        db.query(DataRoomAccess)
        .filter(
            DataRoomAccess.dataroom_id == room.id,
            DataRoomAccess.investor_id == investor.id,
            DataRoomAccess.revoked.is_(False),
        )
        .first()
    )
    if access is None:
        return None
    if access.expires_at is not None:
        exp = access.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=UTC)
        if exp < datetime.now(UTC):
            return None
    return access


def has_access(db: Session, room: DataRoom, investor: Investor) -> bool:
    return _active_access(db, room, investor) is not None


def list_access(db: Session, room: DataRoom) -> list[dict]:
    rows = db.query(DataRoomAccess).filter(DataRoomAccess.dataroom_id == room.id).all()
    out = []
    for a in rows:
        inv = db.get(Investor, a.investor_id)
        out.append({
            "id": a.id, "investor_id": a.investor_id,
            "investor_name": inv.name if inv else None,
            "granted_by": a.granted_by, "expires_at": a.expires_at,
            "revoked": a.revoked, "created_at": a.created_at,
        })
    return out


def accessible_rooms(db: Session, investor: Investor) -> list[DataRoom]:
    rooms = db.query(DataRoom).all()
    return [r for r in rooms if has_access(db, r, investor)]


def view_document(
    db: Session, room: DataRoom, document_id: str, investor: Investor, user: User,
    action: DataRoomLogAction = DataRoomLogAction.consultation,
) -> dict:
    """Consultation d'un document : watermark dynamique + log (RG-M13-02/03)."""
    link = (
        db.query(DataRoomDocument)
        .filter(
            DataRoomDocument.dataroom_id == room.id,
            DataRoomDocument.document_id == document_id,
        )
        .first()
    )
    doc = db.get(Document, document_id)
    if link is None or doc is None:
        raise GateError("Document hors de cette data room.")

    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    watermark = f"CONFIDENTIEL — {investor.name} — {timestamp}"

    db.add(DataRoomLog(
        dataroom_id=room.id, document_id=document_id, investor_id=investor.id,
        actor_id=user.id, action=action,
    ))
    db.commit()
    audit.record(
        db, AuditAction.dataroom_document_viewed, actor=user, object_type="Document",
        object_id=document_id, meta={"dataroom_id": room.id, "action": action.value},
    )
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "watermark": watermark,
        "view_url": f"mock-vdr://{room.provider_ref}/{document_id}",
        "note": "Aperçu fourni par le connecteur VDR (mock). Export contrôlé par le prestataire.",
    }


def logs(db: Session, room: DataRoom) -> list[DataRoomLog]:
    return (
        db.query(DataRoomLog)
        .filter(DataRoomLog.dataroom_id == room.id)
        .order_by(DataRoomLog.created_at.desc())
        .all()
    )
