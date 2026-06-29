"""Routes teaser (M11) & mise en relation (M12)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.domain.enums import CompanyStatus, Role, TeaserStatus
from app.models.investor import Investor
from app.models.teaser import Interaction, Teaser
from app.models.user import User
from app.schemas.teaser import (
    InteractionOut,
    InteractionStatusUpdate,
    InterestCreate,
    TeaserOut,
    TeaserPublicOut,
)
from app.services import investors as inv_svc
from app.services import teasers as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


# --- M11 : teaser côté cabinet ---
@router.post("/companies/{company_id}/teaser", response_model=TeaserOut)
def generate_teaser(
    company_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Teaser:
    company = load_company(company_id, db, user)
    if company.status != CompanyStatus.investor_ready:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Le dossier doit être « investor-ready » pour générer un teaser.",
        )
    return svc.generate(db, company, user)


@router.get("/companies/{company_id}/teaser", response_model=TeaserOut)
def get_company_teaser(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Teaser:
    company = load_company(company_id, db, user)
    teaser = svc.get_by_company(db, company)
    if teaser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teaser non généré")
    return teaser


@router.post("/teasers/{teaser_id}/publish", response_model=TeaserOut)
def publish_teaser(
    teaser_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Teaser:
    teaser = db.get(Teaser, teaser_id)
    if teaser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teaser introuvable")
    return svc.publish(db, teaser, user, ip=_ip(request))


# --- M11 : catalogue investisseur (anonymisé) ---
@router.get("/teasers", response_model=list[TeaserPublicOut])
def list_teasers(
    instrument: str | None = None,
    deal_type: str | None = None,
    sector: str | None = None,
    zone: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Teaser]:
    return svc.list_published(
        db, instrument=instrument, deal_type=deal_type, sector=sector, zone=zone
    )


@router.get("/teasers/{teaser_id}", response_model=TeaserPublicOut)
def get_teaser(
    teaser_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> Teaser:
    teaser = db.get(Teaser, teaser_id)
    if teaser is None or teaser.status != TeaserStatus.publie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teaser introuvable")
    return teaser


# --- M12 : intérêt investisseur ---
@router.post("/teasers/{teaser_id}/interest", response_model=InteractionOut, status_code=201)
def express_interest(
    teaser_id: str,
    payload: InterestCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Interaction:
    if user.role != Role.investisseur:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Réservé aux investisseurs"
        )
    teaser = db.get(Teaser, teaser_id)
    if teaser is None or teaser.status != TeaserStatus.publie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teaser introuvable")
    investor: Investor | None = inv_svc.my_investor(db, user)
    if investor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune fiche investisseur rattachée à votre compte",
        )
    return svc.express_interest(db, teaser, investor, payload.note, user, ip=_ip(request))


# --- M12 : suivi des mises en relation (cabinet = toutes ; investisseur = les siennes) ---
@router.get("/interactions", response_model=list[InteractionOut])
def list_interactions(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Interaction]:
    from app.services import qa as qa_svc

    return qa_svc.list_interactions(db, user)


@router.patch("/interactions/{interaction_id}/status", response_model=InteractionOut)
def update_interaction(
    interaction_id: str,
    payload: InteractionStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Interaction:
    interaction = db.get(Interaction, interaction_id)
    if interaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interaction introuvable")
    return svc.update_interaction_status(db, interaction, payload.status, user, ip=_ip(request))
