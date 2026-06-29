"""Routes data room (M13)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.domain.enums import DataRoomLogAction, Role
from app.models.dataroom import DataRoom, DataRoomAccess
from app.models.investor import Investor
from app.models.user import User
from app.schemas.dataroom import (
    AddDocumentIn,
    DataRoomAccessOut,
    DataRoomDocumentOut,
    DataRoomLogOut,
    DataRoomOut,
    DocumentViewOut,
    GrantAccessIn,
)
from app.services import dataroom as svc
from app.services import investors as inv_svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _room(room_id: str, db: Session) -> DataRoom:
    room = db.get(DataRoom, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data room introuvable")
    return room


def _investor_with_access(room: DataRoom, db: Session, user: User) -> Investor:
    if user.role != Role.investisseur:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    investor = inv_svc.my_investor(db, user)
    if investor is None or not svc.has_access(db, room, investor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès non accordé")
    return investor


# --- Cabinet ---
@router.post("/companies/{company_id}/dataroom", response_model=DataRoomOut)
def open_room(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> DataRoom:
    company = load_company(company_id, db, user)
    return svc.get_or_create(db, company, user)


@router.post("/dataroom/{room_id}/documents", response_model=DataRoomDocumentOut, status_code=201)
def add_document(
    room_id: str,
    payload: AddDocumentIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> dict:
    room = _room(room_id, db)
    try:
        svc.add_document(db, room, payload.document_id)
    except svc.GateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return next(d for d in svc.list_documents(db, room) if d["document_id"] == payload.document_id)


@router.post("/dataroom/{room_id}/access", response_model=DataRoomAccessOut, status_code=201)
def grant_access(
    room_id: str,
    payload: GrantAccessIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    room = _room(room_id, db)
    investor = db.get(Investor, payload.investor_id)
    if investor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    try:
        access = svc.grant_access(db, room, investor, user, payload.expires_at, ip=_ip(request))
    except svc.GateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return next(a for a in svc.list_access(db, room) if a["id"] == access.id)


@router.get("/dataroom/{room_id}/access", response_model=list[DataRoomAccessOut])
def list_access(
    room_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> list[dict]:
    return svc.list_access(db, _room(room_id, db))


@router.post("/dataroom/access/{access_id}/revoke")
def revoke_access(
    access_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    access = db.get(DataRoomAccess, access_id)
    if access is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accès introuvable")
    svc.revoke_access(db, access, user, ip=_ip(request))
    return {"revoked": True}


@router.get("/dataroom/{room_id}/logs", response_model=list[DataRoomLogOut])
def room_logs(
    room_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> list:
    return svc.logs(db, _room(room_id, db))


# --- Investisseur ---
@router.get("/dataroom/accessible", response_model=list[DataRoomOut])
def accessible_rooms(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[DataRoom]:
    if user.role != Role.investisseur:
        return []
    investor = inv_svc.my_investor(db, user)
    return svc.accessible_rooms(db, investor) if investor else []


@router.get("/dataroom/{room_id}/documents", response_model=list[DataRoomDocumentOut])
def room_documents(
    room_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[dict]:
    room = _room(room_id, db)
    if user.role in (Role.analyste, Role.senior, Role.admin, Role.conformite):
        return svc.list_documents(db, room)
    _investor_with_access(room, db, user)  # gate
    return svc.list_documents(db, room)


@router.post("/dataroom/{room_id}/documents/{document_id}/view", response_model=DocumentViewOut)
def view_document(
    room_id: str,
    document_id: str,
    download: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    room = _room(room_id, db)
    investor = _investor_with_access(room, db, user)
    action = DataRoomLogAction.telechargement if download else DataRoomLogAction.consultation
    try:
        return svc.view_document(db, room, document_id, investor, user, action=action)
    except svc.GateError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
