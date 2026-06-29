"""Routes documents & checklist (M4)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import ChecklistItem, DocumentOut, DocumentStatusUpdate
from app.services import documents as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post(
    "/companies/{company_id}/documents",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    company_id: str,
    request: Request,
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Document:
    company = load_company(company_id, db, user)
    data = await file.read()
    try:
        return svc.save_upload(
            db, company,
            filename=file.filename or "piece",
            content_type=file.content_type,
            data=data,
            doc_type=doc_type,
            actor=user,
            ip=_ip(request),
        )
    except svc.UploadError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e


@router.get("/companies/{company_id}/documents", response_model=list[DocumentOut])
def list_documents(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Document]:
    company = load_company(company_id, db, user)
    return svc.list_documents(db, company)


@router.get("/companies/{company_id}/documents/checklist", response_model=list[ChecklistItem])
def checklist(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[dict]:
    company = load_company(company_id, db, user)
    return svc.checklist(db, company)


@router.patch("/documents/{document_id}/status", response_model=DocumentOut)
def update_document_status(
    document_id: str,
    payload: DocumentStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Document:
    """Vérification d'une pièce — réservée au cabinet (RG-M4-03), tracée (M22)."""
    doc = db.get(Document, document_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pièce introuvable")
    # L'accès est garanti par require_cabinet (le cabinet voit toutes les fiches).
    return svc.update_status(db, doc, payload.status, user, ip=_ip(request))
