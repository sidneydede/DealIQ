"""Service notifications : centre in-app + e-mail (mock) déclenché par les événements métier."""
from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enums import NotificationType, Role
from app.models.notification import Notification
from app.models.user import User
from app.services import email as email_adapter


def notify(
    db: Session,
    *,
    recipient: User,
    type: NotificationType,
    title: str,
    body: str,
    link: str | None = None,
    object_type: str | None = None,
    object_id: str | None = None,
    send_email: bool = True,
    commit: bool = True,
) -> Notification:
    """Crée une notification in-app pour un destinataire et déclenche l'e-mail (mock)."""
    notif = Notification(
        recipient_id=recipient.id,
        type=type,
        title=title,
        body=body,
        link=link,
        object_type=object_type,
        object_id=object_id,
    )
    db.add(notif)
    if commit:
        db.commit()
        db.refresh(notif)
    if send_email and recipient.email:
        email_adapter.send_email(recipient.email, title, body)
    return notif


def notify_roles(
    db: Session,
    roles: Iterable[Role],
    *,
    exclude_user_id: str | None = None,
    **kwargs,
) -> list[Notification]:
    """Diffuse une notification à tous les comptes actifs des rôles donnés."""
    recipients = (
        db.query(User)
        .filter(User.role.in_(list(roles)), User.is_active.is_(True))
        .all()
    )
    out = []
    for r in recipients:
        if exclude_user_id and r.id == exclude_user_id:
            continue
        out.append(notify(db, recipient=r, **kwargs))
    return out


def list_for(
    db: Session, user: User, *, unread_only: bool = False, limit: int = 50
) -> list[Notification]:
    q = db.query(Notification).filter(Notification.recipient_id == user.id)
    if unread_only:
        q = q.filter(Notification.read_at.is_(None))
    return q.order_by(Notification.created_at.desc()).limit(limit).all()


def paginate(
    db: Session, user: User, *, unread_only: bool = False, limit: int, offset: int = 0
) -> tuple[list[Notification], int]:
    base = db.query(Notification).filter(Notification.recipient_id == user.id)
    if unread_only:
        base = base.filter(Notification.read_at.is_(None))
    total = base.count()
    items = (
        base.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
    )
    return items, total


def unread_count(db: Session, user: User) -> int:
    return (
        db.query(Notification)
        .filter(Notification.recipient_id == user.id, Notification.read_at.is_(None))
        .count()
    )


def mark_read(db: Session, notif: Notification) -> Notification:
    if notif.read_at is None:
        notif.read_at = datetime.now(UTC)
        db.commit()
        db.refresh(notif)
    return notif


def mark_all_read(db: Session, user: User) -> int:
    rows = (
        db.query(Notification)
        .filter(Notification.recipient_id == user.id, Notification.read_at.is_(None))
        .all()
    )
    now = datetime.now(UTC)
    for r in rows:
        r.read_at = now
    if rows:
        db.commit()
    return len(rows)
