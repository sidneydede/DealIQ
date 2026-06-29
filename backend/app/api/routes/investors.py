"""Routes investisseurs & critères (M9)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_cabinet
from app.api.pagination import Page, Pagination, SortParams, pagination, sorting
from app.database import get_db
from app.domain.enums import InvestorQualifStatus, InvestorType
from app.models.investor import Investor
from app.models.user import User
from app.schemas.investor import (
    CriteriaIn,
    CriteriaOut,
    InvestorCreate,
    InvestorOut,
    InvestorUpdate,
    InviteIn,
    InviteResult,
)
from app.services import csv_export
from app.services import investors as svc

_INVESTOR_CSV_COLUMNS = [
    ("name", "Nom"),
    ("type", "Type"),
    ("jurisdiction", "Juridiction"),
    ("qualif_status", "Statut"),
    ("linked", "Compte rattaché"),
    ("has_criteria", "Critères définis"),
]

router = APIRouter()


def _load(investor_id: str, db: Session, user: User) -> Investor:
    inv = db.get(Investor, investor_id)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    if not svc.can_access(user, inv):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return inv


@router.post("", response_model=InvestorOut, status_code=status.HTTP_201_CREATED)
def create_investor(
    payload: InvestorCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Investor:
    return svc.create_investor(db, payload)


@router.get("", response_model=Page[InvestorOut])
def list_investors(
    q: str | None = None,
    type_filter: InvestorType | None = None,
    qualif_status: InvestorQualifStatus | None = None,
    sort: SortParams = Depends(sorting),
    page: Pagination = Depends(pagination),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Page[InvestorOut]:
    items, total = svc.paginate_for_user(
        db, user, q=q, type_filter=type_filter, qualif_status=qualif_status,
        sort=sort, limit=page.limit, offset=page.offset,
    )
    return Page.build(items, total, page)


@router.get("/export.csv")
def export_investors_csv(
    q: str | None = None,
    type_filter: InvestorType | None = None,
    qualif_status: InvestorQualifStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    items, _total = svc.paginate_for_user(
        db, user, q=q, type_filter=type_filter, qualif_status=qualif_status,
        limit=100000, offset=0,
    )
    rows = [
        {
            "name": inv.name,
            "type": inv.type,
            "jurisdiction": inv.jurisdiction,
            "qualif_status": inv.qualif_status,
            "linked": inv.user_id is not None,
            "has_criteria": inv.criteria is not None,
        }
        for inv in items
    ]
    content = csv_export.to_csv(rows, _INVESTOR_CSV_COLUMNS)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="investisseurs.csv"'},
    )


@router.get("/me", response_model=InvestorOut)
def my_investor(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Investor:
    inv = svc.my_investor(db, user)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucune fiche investisseur rattachée"
        )
    return inv


@router.get("/{investor_id}", response_model=InvestorOut)
def get_investor(
    investor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Investor:
    return _load(investor_id, db, user)


@router.patch("/{investor_id}", response_model=InvestorOut)
def update_investor(
    investor_id: str,
    payload: InvestorUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Investor:
    inv = db.get(Investor, investor_id)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(inv, field, value)
    db.commit()
    db.refresh(inv)
    return inv


@router.post("/{investor_id}/invite", response_model=InviteResult)
def invite_investor(
    investor_id: str,
    payload: InviteIn,
    db: Session = Depends(get_db),
    actor: User = Depends(require_cabinet),
) -> InviteResult:
    inv = db.get(Investor, investor_id)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    try:
        investor, temp = svc.invite_investor(db, inv, payload.email, actor)
    except svc.InviteError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return InviteResult(
        investor=InvestorOut.model_validate(investor),
        temporary_password=temp,
        new_account=temp is not None,
    )


@router.get("/{investor_id}/criteria", response_model=CriteriaOut)
def get_criteria(
    investor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> CriteriaOut:
    inv = _load(investor_id, db, user)
    if inv.criteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Critères non définis")
    return CriteriaOut.model_validate(inv.criteria)


@router.put("/{investor_id}/criteria", response_model=CriteriaOut)
def set_criteria(
    investor_id: str,
    payload: CriteriaIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CriteriaOut:
    inv = _load(investor_id, db, user)  # cabinet ou investisseur propriétaire (US-M9-03)
    crit = svc.upsert_criteria(db, inv, payload)
    return CriteriaOut.model_validate(crit)
