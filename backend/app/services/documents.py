"""Logique documents & checklist (M4). Stockage via adaptateur (local ou S3)."""
from __future__ import annotations

import hashlib

from sqlalchemy.orm import Session

from app.config import settings
from app.domain.enums import AuditAction, DocumentStatus
from app.models.company import Company
from app.models.document import Document
from app.models.reference import DealType
from app.models.user import User
from app.services import audit, storage

# Types MIME autorisés (RG-M4-01) : PDF, images, tableurs.
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx
    "application/vnd.ms-excel",  # xls
}

# Signatures (magic bytes) attendues par type — défense contre le contenu falsifié.
_MAGIC = {
    "application/pdf": [b"%PDF"],
    "image/png": [b"\x89PNG\r\n\x1a\n"],
    "image/jpeg": [b"\xff\xd8\xff"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [b"PK\x03\x04"],
    "application/vnd.ms-excel": [b"PK\x03\x04", b"\xd0\xcf\x11\xe0"],
}


class UploadError(ValueError):
    """Erreur de validation d'upload (type, taille ou contenu)."""


def _content_matches(content_type: str | None, data: bytes) -> bool:
    """Vérifie que les premiers octets correspondent au type MIME déclaré."""
    signatures = _MAGIC.get(content_type or "")
    if not signatures:
        return False
    return any(data.startswith(sig) for sig in signatures)


def save_upload(
    db: Session,
    company: Company,
    *,
    filename: str,
    content_type: str | None,
    data: bytes,
    doc_type: str,
    actor: User,
    ip: str | None = None,
) -> Document:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise UploadError(f"Type de fichier non autorisé : {content_type}")
    if not _content_matches(content_type, data):
        raise UploadError("Le contenu du fichier ne correspond pas au type déclaré.")
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise UploadError(f"Fichier trop volumineux (max {settings.max_upload_mb} Mo)")

    # Versionnage : incrément par type de pièce sur la fiche.
    existing = (
        db.query(Document)
        .filter(Document.company_id == company.id, Document.doc_type == doc_type)
        .count()
    )
    doc = Document(
        company_id=company.id,
        doc_type=doc_type,
        filename=filename,
        content_type=content_type,
        size_bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
        version=existing + 1,
        status=DocumentStatus.recu,
        uploaded_by=actor.id,
    )
    db.add(doc)
    db.flush()  # obtient doc.id pour la clé de stockage

    doc.storage_key = storage.put(company.id, doc.id, filename, data, content_type)

    db.commit()
    db.refresh(doc)
    audit.record(
        db, AuditAction.document_uploaded, actor=actor, object_type="Document",
        object_id=doc.id, meta={"company_id": company.id, "doc_type": doc_type}, ip_address=ip,
    )
    return doc


def list_documents(db: Session, company: Company) -> list[Document]:
    return (
        db.query(Document)
        .filter(Document.company_id == company.id)
        .order_by(Document.created_at.desc())
        .all()
    )


def update_status(
    db: Session, doc: Document, new_status: DocumentStatus, actor: User, ip: str | None = None
) -> Document:
    old = doc.status
    doc.status = new_status
    db.commit()
    db.refresh(doc)
    audit.record(
        db, AuditAction.document_status_changed, actor=actor, object_type="Document",
        object_id=doc.id, meta={"old": old.value, "new": new_status.value}, ip_address=ip,
    )
    return doc


def checklist(db: Session, company: Company) -> list[dict]:
    """Checklist adaptée au type de deal (RG-M4-04) : pièces requises + reçues/vérifiées."""
    docs = list_documents(db, company)
    by_type: dict[str, list[Document]] = {}
    for d in docs:
        by_type.setdefault(d.doc_type, []).append(d)

    required_types: list[str] = []
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    if deal_type is not None:
        dt = db.query(DealType).filter(DealType.code == deal_type).first()
        if dt:
            required_types = list(dt.doc_checklist or [])

    items: list[dict] = []
    seen: set[str] = set()
    for dtype in required_types:
        group = by_type.get(dtype, [])
        items.append({
            "doc_type": dtype,
            "required": True,
            "received": len(group) > 0,
            "verified": any(d.status == DocumentStatus.verifie for d in group),
            "documents": group,
        })
        seen.add(dtype)

    # Pièces fournies hors checklist (non requises mais présentes)
    for dtype, group in by_type.items():
        if dtype not in seen:
            items.append({
                "doc_type": dtype,
                "required": False,
                "received": True,
                "verified": any(d.status == DocumentStatus.verifie for d in group),
                "documents": group,
            })
    return items
