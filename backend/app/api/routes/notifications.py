"""Routes du centre de notifications (in-app)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationOut, UnreadCount
from app.services import notifications as svc

router = APIRouter()


@router.get("", response_model=list[NotificationOut])
def list_notifications(
    unread: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Notification]:
    return svc.list_for(db, user, unread_only=unread)


@router.get("/unread-count", response_model=UnreadCount)
def unread_count(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> UnreadCount:
    return UnreadCount(count=svc.unread_count(db, user))


@router.post("/{notif_id}/read", response_model=NotificationOut)
def mark_read(
    notif_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Notification:
    notif = db.get(Notification, notif_id)
    if notif is None or notif.recipient_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification introuvable"
        )
    return svc.mark_read(db, notif)


@router.post("/read-all", response_model=UnreadCount)
def mark_all_read(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> UnreadCount:
    svc.mark_all_read(db, user)
    return UnreadCount(count=0)
