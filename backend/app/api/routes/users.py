"""Routes utilisateurs (M1, admin). Attribution de rôle tracée (M22)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.database import get_db
from app.domain.enums import AuditAction
from app.models.user import User
from app.schemas.auth import RoleUpdate, UserOut
from app.services import audit

router = APIRouter()


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).order_by(User.created_at).all()


@router.patch("/{user_id}/role", response_model=UserOut)
def change_role(
    user_id: str,
    payload: RoleUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    old_role = user.role
    user.role = payload.role
    db.commit()
    db.refresh(user)
    audit.record(
        db,
        AuditAction.role_changed,
        actor=admin,
        object_type="User",
        object_id=user.id,
        meta={"old": old_role.value, "new": payload.role.value},
        ip_address=request.client.host if request.client else None,
    )
    return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> User:
    return user
