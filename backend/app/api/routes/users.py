"""Routes utilisateurs (M1, admin). Attribution de rôle et statut tracés (M22)."""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.core.security import hash_password
from app.database import get_db
from app.domain.enums import AuditAction, Role
from app.models.user import User
from app.schemas.auth import ActiveUpdate, RoleUpdate, UserCreate, UserCreatedOut, UserOut
from app.services import audit

router = APIRouter()


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).order_by(User.created_at).all()


@router.post("", response_model=UserCreatedOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> UserCreatedOut:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email déjà utilisé")
    generated: str | None = None
    secret = payload.password
    if not secret:
        # Mot de passe temporaire fort, à communiquer à l'utilisateur
        # (rotation au 1er accès prévue en V1).
        generated = secrets.token_urlsafe(9)
        secret = generated
    user = User(
        email=payload.email,
        hashed_password=hash_password(secret),
        full_name=payload.full_name,
        role=payload.role,
        email_verified=True,  # compte créé par un admin = pré-vérifié
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    audit.record(
        db,
        AuditAction.user_created,
        actor=admin,
        object_type="User",
        object_id=user.id,
        meta={"role": user.role.value, "by_admin": True},
        ip_address=_client_ip(request),
    )
    out = UserCreatedOut.model_validate(user)
    out.temporary_password = generated
    return out


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
    # Garde-fou : un admin ne peut pas se rétrograder lui-même (risque de verrouillage).
    if user.id == admin.id and payload.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas retirer votre propre rôle admin",
        )
    if user.role == payload.role:
        return user
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
        ip_address=_client_ip(request),
    )
    return user


@router.patch("/{user_id}/active", response_model=UserOut)
def set_active(
    user_id: str,
    payload: ActiveUpdate,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    # Garde-fou : un admin ne peut pas désactiver son propre compte.
    if user.id == admin.id and not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas désactiver votre propre compte",
        )
    if user.is_active == payload.is_active:
        return user
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    audit.record(
        db,
        AuditAction.account_status_changed,
        actor=admin,
        object_type="User",
        object_id=user.id,
        meta={"is_active": user.is_active},
        ip_address=_client_ip(request),
    )
    return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> User:
    return user
