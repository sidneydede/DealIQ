"""Routes Q&A (M14)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_cabinet
from app.database import get_db
from app.domain.enums import QAStatus
from app.models.qa import QAItem
from app.models.teaser import Interaction
from app.models.user import User
from app.schemas.qa import AnswerIn, QAItemOut, QuestionCreate
from app.services import qa as svc

router = APIRouter()


def _interaction(interaction_id: str, db: Session, user: User) -> Interaction:
    inter = db.get(Interaction, interaction_id)
    if inter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mise en relation introuvable"
        )
    if not svc.can_access_interaction(db, user, inter):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return inter


@router.get("/interactions/{interaction_id}/qa", response_model=list[QAItemOut])
def get_thread(
    interaction_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[QAItem]:
    inter = _interaction(interaction_id, db, user)
    return svc.thread(db, inter)


@router.post("/interactions/{interaction_id}/qa", response_model=QAItemOut, status_code=201)
def ask_question(
    interaction_id: str,
    payload: QuestionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> QAItem:
    inter = _interaction(interaction_id, db, user)
    return svc.ask(db, inter, user, payload.question)


@router.post("/qa/{item_id}/answer", response_model=QAItemOut)
def answer_question(
    item_id: str,
    payload: AnswerIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> QAItem:
    item = db.get(QAItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question introuvable")
    return svc.answer(db, item, user, payload.answer)


@router.patch("/qa/{item_id}/close", response_model=QAItemOut)
def close_question(
    item_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> QAItem:
    item = db.get(QAItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question introuvable")
    return svc.set_status(db, item, QAStatus.cloturee)
