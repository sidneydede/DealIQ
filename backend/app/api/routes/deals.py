from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.domain.enums import score_band
from app.models.deal import Deal, DealChangeLog, DealNote
from app.models.user import User
from app.schemas.deal import (
    ActivityBannerOut,
    ChangeLogOut,
    DealCreate,
    DealListItem,
    DealNoteCreate,
    DealNoteOut,
    DealOut,
    DealUpdate,
)
from app.services.completeness import DATA_ZERO_HINT, is_data_zero_mode
from app.services.deals import create_deal, update_deal
from app.services.enrichment.validation import activity_banner

router = APIRouter(prefix="/deals", tags=["deals"])


def _to_out(deal: Deal) -> DealOut:
    data_zero = is_data_zero_mode(deal)
    out = DealOut.model_validate(deal)
    out.score_band = score_band(deal.completeness_score)
    out.data_zero_mode = data_zero
    out.data_zero_hint = DATA_ZERO_HINT if data_zero else None
    banner = activity_banner(deal)
    out.activity = ActivityBannerOut(**banner) if banner else None
    return out


def _get_or_404(db: Session, deal_id: int) -> Deal:
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fiche introuvable.")
    return deal


@router.post("", response_model=DealOut, status_code=status.HTTP_201_CREATED)
def create(
    payload: DealCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DealOut:
    data = payload.model_dump()
    socials = data.pop("socials", [])
    deal = create_deal(db, fields=data, socials=socials)
    return _to_out(deal)


@router.get("", response_model=list[DealListItem])
def list_deals(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Deal]:
    return list(
        db.execute(select(Deal).order_by(Deal.updated_at.desc())).scalars().all()
    )


@router.get("/{deal_id}", response_model=DealOut)
def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DealOut:
    return _to_out(_get_or_404(db, deal_id))


@router.patch("/{deal_id}", response_model=DealOut)
def patch_deal(
    deal_id: int,
    payload: DealUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DealOut:
    deal = _get_or_404(db, deal_id)
    provided = payload.model_dump(exclude_unset=True)
    socials = provided.pop("socials", None)
    deal = update_deal(db, deal, fields=provided, socials=socials)
    return _to_out(deal)


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> None:
    deal = _get_or_404(db, deal_id)
    db.delete(deal)
    db.commit()


# ── Notes (journal de deal) ──────────────────────────────────────────────────
@router.post("/{deal_id}/notes", response_model=DealNoteOut, status_code=201)
def add_note(
    deal_id: int,
    payload: DealNoteCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DealNote:
    _get_or_404(db, deal_id)
    note = DealNote(deal_id=deal_id, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/{deal_id}/notes", response_model=list[DealNoteOut])
def list_notes(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[DealNote]:
    _get_or_404(db, deal_id)
    return list(
        db.execute(
            select(DealNote)
            .where(DealNote.deal_id == deal_id)
            .order_by(DealNote.created_at.desc())
        )
        .scalars()
        .all()
    )


# ── Historique des modifications ─────────────────────────────────────────────
@router.get("/{deal_id}/history", response_model=list[ChangeLogOut])
def deal_history(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[DealChangeLog]:
    _get_or_404(db, deal_id)
    return list(
        db.execute(
            select(DealChangeLog)
            .where(DealChangeLog.deal_id == deal_id)
            .order_by(DealChangeLog.changed_at.desc(), DealChangeLog.id.desc())
        )
        .scalars()
        .all()
    )
